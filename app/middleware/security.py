#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全中间件
提供安全头设置、CSRF防护、XSS防护等安全功能
"""

import tornado.web
import hashlib
import secrets
import time
from typing import Dict, Any, Optional, List
from functools import wraps

from app.core.exceptions import BaseAPIException
from app.shared import ResponseFormatter


class SecurityError(BaseAPIException):
    """安全异常"""
    
    def __init__(self, message: str = "安全验证失败", status_code: int = 403):
        super().__init__(message, status_code)


class CSRFError(SecurityError):
    """CSRF异常"""
    
    def __init__(self, message: str = "CSRF验证失败"):
        super().__init__(message, 403)


class SecurityMixin:
    """安全混入类"""
    
    def prepare(self):
        """请求预处理，应用安全策略"""
        # 调用父类的prepare方法
        if hasattr(super(), 'prepare'):
            super().prepare()
        
        # 应用安全策略
        self.apply_security_policies()
    
    def set_default_headers(self):
        """设置默认安全头"""
        # 调用父类的方法
        if hasattr(super(), 'set_default_headers'):
            super().set_default_headers()
        
        # 设置安全头
        self.set_security_headers()
    
    def apply_security_policies(self):
        """应用安全策略"""
        # 检查HTTPS（生产环境）
        self.check_https_requirement()
        
        # 验证请求头
        self.validate_request_headers()
        
        # CSRF保护
        if self.requires_csrf_protection():
            self.check_csrf_token()
        
        # 检查请求大小
        self.check_request_size()
    
    def set_security_headers(self):
        """设置安全响应头"""
        # 获取安全配置
        security_config = self.get_security_config()
        
        # X-Content-Type-Options
        if security_config.get('x_content_type_options', True):
            self.set_header('X-Content-Type-Options', 'nosniff')
        
        # X-Frame-Options
        frame_options = security_config.get('x_frame_options', 'DENY')
        if frame_options:
            self.set_header('X-Frame-Options', frame_options)
        
        # X-XSS-Protection
        if security_config.get('x_xss_protection', True):
            self.set_header('X-XSS-Protection', '1; mode=block')
        
        # Strict-Transport-Security (HSTS)
        hsts_config = security_config.get('hsts')
        if hsts_config and self.request.protocol == 'https':
            max_age = hsts_config.get('max_age', 31536000)  # 1年
            include_subdomains = hsts_config.get('include_subdomains', True)
            preload = hsts_config.get('preload', False)
            
            hsts_value = f'max-age={max_age}'
            if include_subdomains:
                hsts_value += '; includeSubDomains'
            if preload:
                hsts_value += '; preload'
            
            self.set_header('Strict-Transport-Security', hsts_value)
        
        # Content-Security-Policy
        csp_config = security_config.get('csp')
        if csp_config:
            csp_value = self.build_csp_header(csp_config)
            if csp_value:
                self.set_header('Content-Security-Policy', csp_value)
        
        # Referrer-Policy
        referrer_policy = security_config.get('referrer_policy', 'strict-origin-when-cross-origin')
        if referrer_policy:
            self.set_header('Referrer-Policy', referrer_policy)
        
        # Permissions-Policy
        permissions_policy = security_config.get('permissions_policy')
        if permissions_policy:
            policy_value = self.build_permissions_policy(permissions_policy)
            if policy_value:
                self.set_header('Permissions-Policy', policy_value)
        
        # 移除服务器信息
        if security_config.get('hide_server_header', True):
            self.clear_header('Server')
    
    def get_security_config(self) -> Dict[str, Any]:
        """获取安全配置"""
        # 检查Handler是否有安全配置
        if hasattr(self, 'security_config'):
            return self.security_config
        
        # 检查类级别的安全配置
        if hasattr(self.__class__, 'security_config'):
            return self.__class__.security_config
        
        # 从配置文件获取默认安全配置
        try:
            from app.config import settings
            return getattr(settings, 'SECURITY_CONFIG', self.get_default_security_config())
        except:
            return self.get_default_security_config()
    
    def get_default_security_config(self) -> Dict[str, Any]:
        """获取默认安全配置"""
        return {
            'x_content_type_options': True,
            'x_frame_options': 'DENY',
            'x_xss_protection': True,
            'hsts': {
                'max_age': 31536000,
                'include_subdomains': True,
                'preload': False
            },
            'csp': {
                'default-src': ["'self'"],
                'script-src': ["'self'", "'unsafe-inline'"],
                'style-src': ["'self'", "'unsafe-inline'"],
                'img-src': ["'self'", 'data:', 'https:'],
                'font-src': ["'self'"],
                'connect-src': ["'self'"],
                'frame-ancestors': ["'none'"]
            },
            'referrer_policy': 'strict-origin-when-cross-origin',
            'permissions_policy': {
                'camera': [],
                'microphone': [],
                'geolocation': [],
                'payment': []
            },
            'hide_server_header': True,
            'max_request_size': 10 * 1024 * 1024,  # 10MB
            'require_https': False,  # 生产环境应设为True
            'csrf_protection': True
        }
    
    def build_csp_header(self, csp_config: Dict[str, List[str]]) -> str:
        """构建CSP头"""
        csp_parts = []
        for directive, sources in csp_config.items():
            if sources:
                sources_str = ' '.join(sources)
                csp_parts.append(f"{directive} {sources_str}")
        
        return '; '.join(csp_parts)
    
    def build_permissions_policy(self, permissions_config: Dict[str, List[str]]) -> str:
        """构建Permissions-Policy头"""
        policy_parts = []
        for feature, allowlist in permissions_config.items():
            if allowlist:
                allowlist_str = ' '.join(f'"{origin}"' for origin in allowlist)
                policy_parts.append(f"{feature}=({allowlist_str})")
            else:
                policy_parts.append(f"{feature}=()")
        
        return ', '.join(policy_parts)
    
    def check_https_requirement(self):
        """检查HTTPS要求"""
        security_config = self.get_security_config()
        
        if security_config.get('require_https', False):
            if self.request.protocol != 'https':
                raise SecurityError("此操作需要HTTPS连接")
    
    def validate_request_headers(self):
        """验证请求头"""
        # 检查Host头
        host = self.request.headers.get('Host')
        if not host:
            raise SecurityError("缺少Host头")
        
        # 检查User-Agent头（可选）
        user_agent = self.request.headers.get('User-Agent')
        if not user_agent:
            # 记录可疑请求
            self.log_security_event('missing_user_agent', {
                'ip': self.request.remote_ip,
                'path': self.request.path
            })
    
    def requires_csrf_protection(self) -> bool:
        """检查是否需要CSRF保护"""
        # 只对修改数据的请求进行CSRF保护
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            security_config = self.get_security_config()
            return security_config.get('csrf_protection', True)
        
        return False
    
    def check_csrf_token(self):
        """检查CSRF令牌"""
        # 获取CSRF令牌
        csrf_token = self.get_csrf_token_from_request()
        
        if not csrf_token:
            raise CSRFError("缺少CSRF令牌")
        
        # 验证CSRF令牌
        if not self.validate_csrf_token(csrf_token):
            raise CSRFError("无效的CSRF令牌")
    
    def get_csrf_token_from_request(self) -> Optional[str]:
        """从请求中获取CSRF令牌"""
        # 从头部获取
        csrf_token = self.request.headers.get('X-CSRFToken')
        if csrf_token:
            return csrf_token
        
        # 从表单数据获取
        if hasattr(self, 'get_argument'):
            try:
                return self.get_argument('csrf_token', None)
            except:
                pass
        
        return None
    
    def validate_csrf_token(self, token: str) -> bool:
        """验证CSRF令牌"""
        # 简单的令牌验证（实际应用中应该更复杂）
        try:
            # 从session或cookie中获取预期的令牌
            expected_token = self.get_secure_cookie('csrf_token')
            if expected_token:
                expected_token = expected_token.decode('utf-8')
                return secrets.compare_digest(token, expected_token)
        except:
            pass
        
        return False
    
    def generate_csrf_token(self) -> str:
        """生成CSRF令牌"""
        token = secrets.token_urlsafe(32)
        # 将令牌存储到安全cookie中
        self.set_secure_cookie('csrf_token', token, expires_days=1)
        return token
    
    def check_request_size(self):
        """检查请求大小"""
        security_config = self.get_security_config()
        max_size = security_config.get('max_request_size', 10 * 1024 * 1024)  # 10MB
        
        content_length = self.request.headers.get('Content-Length')
        if content_length:
            try:
                size = int(content_length)
                if size > max_size:
                    raise SecurityError(f"请求体过大，最大允许{max_size}字节")
            except ValueError:
                raise SecurityError("无效的Content-Length头")
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """记录安全事件"""
        try:
            import logging
            security_logger = logging.getLogger('security')
            security_logger.warning(f"Security event: {event_type}", extra={
                'event_type': event_type,
                'details': details,
                'timestamp': time.time(),
                'request_id': getattr(self, 'request_id', None)
            })
        except:
            pass


class SecurityMiddleware:
    """安全中间件"""
    
    def __init__(self, security_config: Optional[Dict[str, Any]] = None):
        """
        初始化安全中间件
        
        Args:
            security_config: 安全配置
        """
        self.security_config = security_config or {}
    
    def apply_security_headers(self, handler):
        """应用安全头"""
        # 这里可以实现中间件级别的安全头设置
        pass
    
    def validate_request(self, handler) -> bool:
        """验证请求安全性"""
        try:
            # 检查请求大小
            max_size = self.security_config.get('max_request_size', 10 * 1024 * 1024)
            content_length = handler.request.headers.get('Content-Length')
            if content_length and int(content_length) > max_size:
                return False
            
            # 检查Host头
            host = handler.request.headers.get('Host')
            if not host:
                return False
            
            return True
        except:
            return False


def secure(csrf_protection: bool = True, 
          require_https: bool = False,
          custom_headers: Optional[Dict[str, str]] = None):
    """安全装饰器"""
    def decorator(handler_class):
        # 为Handler类添加安全配置
        security_config = {
            'csrf_protection': csrf_protection,
            'require_https': require_https
        }
        
        if custom_headers:
            security_config['custom_headers'] = custom_headers
        
        handler_class.security_config = security_config
        
        # 创建带安全功能的Handler类
        class SecureHandler(handler_class, SecurityMixin):
            def set_default_headers(self):
                super().set_default_headers()
                # 设置自定义头
                if custom_headers:
                    for name, value in custom_headers.items():
                        self.set_header(name, value)
        
        SecureHandler.__name__ = handler_class.__name__
        SecureHandler.__module__ = handler_class.__module__
        
        return SecureHandler
    
    return decorator


def csrf_exempt(handler_class):
    """CSRF豁免装饰器"""
    class CSRFExemptHandler(handler_class):
        def requires_csrf_protection(self):
            return False
    
    CSRFExemptHandler.__name__ = handler_class.__name__
    CSRFExemptHandler.__module__ = handler_class.__module__
    
    return CSRFExemptHandler


class SecurityHandler(tornado.web.RequestHandler, SecurityMixin):
    """带安全功能的基础Handler"""
    pass


def enable_security(handler_class, **security_options):
    """为Handler类启用安全功能"""
    class SecurityEnabledHandler(handler_class, SecurityMixin):
        security_config = security_options
    
    SecurityEnabledHandler.__name__ = handler_class.__name__
    SecurityEnabledHandler.__module__ = handler_class.__module__
    
    return SecurityEnabledHandler


# 全局安全中间件实例
security_middleware = SecurityMiddleware()