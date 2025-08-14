#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORS中间件
处理跨域资源共享(CORS)请求
"""

import tornado.web
from typing import List, Optional


class CORSMixin:
    """CORS混入类，为Handler添加CORS支持"""
    
    def set_default_headers(self):
        """设置默认的CORS头"""
        # 从配置获取CORS设置
        from app.config import settings
        
        # 允许的源
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', ['*'])
        origin = self.request.headers.get('Origin')
        
        if '*' in allowed_origins or (origin and origin in allowed_origins):
            self.set_header('Access-Control-Allow-Origin', origin or '*')
        
        # 允许的方法
        allowed_methods = getattr(settings, 'CORS_ALLOWED_METHODS', 
                                ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
        self.set_header('Access-Control-Allow-Methods', ', '.join(allowed_methods))
        
        # 允许的头
        allowed_headers = getattr(settings, 'CORS_ALLOWED_HEADERS', [
            'Content-Type', 'Authorization', 'X-Requested-With', 'Accept',
            'Origin', 'Cache-Control', 'X-File-Name'
        ])
        self.set_header('Access-Control-Allow-Headers', ', '.join(allowed_headers))
        
        # 暴露的头
        exposed_headers = getattr(settings, 'CORS_EXPOSED_HEADERS', [])
        if exposed_headers:
            self.set_header('Access-Control-Expose-Headers', ', '.join(exposed_headers))
        
        # 是否允许凭证
        allow_credentials = getattr(settings, 'CORS_ALLOW_CREDENTIALS', False)
        if allow_credentials:
            self.set_header('Access-Control-Allow-Credentials', 'true')
        
        # 预检请求缓存时间
        max_age = getattr(settings, 'CORS_MAX_AGE', 86400)  # 24小时
        self.set_header('Access-Control-Max-Age', str(max_age))
    
    def options(self, *args, **kwargs):
        """处理OPTIONS预检请求"""
        # 设置CORS头
        self.set_default_headers()
        
        # 返回204状态码
        self.set_status(204)
        self.finish()


class CORSMiddleware:
    """CORS中间件类"""
    
    def __init__(self, 
                 allowed_origins: Optional[List[str]] = None,
                 allowed_methods: Optional[List[str]] = None,
                 allowed_headers: Optional[List[str]] = None,
                 exposed_headers: Optional[List[str]] = None,
                 allow_credentials: bool = False,
                 max_age: int = 86400):
        """
        初始化CORS中间件
        
        Args:
            allowed_origins: 允许的源列表
            allowed_methods: 允许的HTTP方法列表
            allowed_headers: 允许的请求头列表
            exposed_headers: 暴露给客户端的响应头列表
            allow_credentials: 是否允许发送凭证
            max_age: 预检请求缓存时间（秒）
        """
        self.allowed_origins = allowed_origins or ['*']
        self.allowed_methods = allowed_methods or [
            'GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'
        ]
        self.allowed_headers = allowed_headers or [
            'Content-Type', 'Authorization', 'X-Requested-With', 'Accept',
            'Origin', 'Cache-Control', 'X-File-Name'
        ]
        self.exposed_headers = exposed_headers or []
        self.allow_credentials = allow_credentials
        self.max_age = max_age
    
    def is_cors_request(self, request):
        """检查是否为CORS请求"""
        return 'Origin' in request.headers
    
    def is_preflight_request(self, request):
        """检查是否为预检请求"""
        return (request.method == 'OPTIONS' and 
                'Origin' in request.headers and
                'Access-Control-Request-Method' in request.headers)
    
    def is_origin_allowed(self, origin: str) -> bool:
        """检查源是否被允许"""
        if '*' in self.allowed_origins:
            return True
        return origin in self.allowed_origins
    
    def add_cors_headers(self, handler, origin: str):
        """添加CORS响应头"""
        if self.is_origin_allowed(origin):
            handler.set_header('Access-Control-Allow-Origin', origin)
        
        handler.set_header('Access-Control-Allow-Methods', 
                          ', '.join(self.allowed_methods))
        
        handler.set_header('Access-Control-Allow-Headers', 
                          ', '.join(self.allowed_headers))
        
        if self.exposed_headers:
            handler.set_header('Access-Control-Expose-Headers', 
                              ', '.join(self.exposed_headers))
        
        if self.allow_credentials:
            handler.set_header('Access-Control-Allow-Credentials', 'true')
        
        handler.set_header('Access-Control-Max-Age', str(self.max_age))


class CORSHandler(tornado.web.RequestHandler, CORSMixin):
    """带CORS支持的基础Handler"""
    pass


def enable_cors(handler_class):
    """装饰器：为Handler类启用CORS支持"""
    class CORSEnabledHandler(handler_class, CORSMixin):
        pass
    
    CORSEnabledHandler.__name__ = handler_class.__name__
    CORSEnabledHandler.__module__ = handler_class.__module__
    
    return CORSEnabledHandler


# 全局CORS中间件实例
cors_middleware = CORSMiddleware()