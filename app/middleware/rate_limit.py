#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
限流中间件
基于令牌桶算法实现API请求限流
"""

import tornado.web
from typing import Dict, Any, Optional, Callable
from functools import wraps

from app.core.security.rate_limiter import rate_limiter
from app.core.exceptions import BaseAPIException
from app.shared import ResponseFormatter


class RateLimitExceeded(BaseAPIException):
    """限流异常"""
    
    def __init__(self, message: str = "请求过于频繁，请稍后再试", retry_after: Optional[int] = None):
        super().__init__(message, 429)
        self.retry_after = retry_after


class RateLimitMixin:
    """限流混入类"""
    
    def prepare(self):
        """请求预处理，检查限流"""
        # 调用父类的prepare方法
        if hasattr(super(), 'prepare'):
            super().prepare()
        
        # 检查限流
        self.check_rate_limit()
    
    def check_rate_limit(self):
        """检查请求限流"""
        # 获取限流配置
        rate_limit_config = self.get_rate_limit_config()
        
        if not rate_limit_config:
            return  # 未配置限流，跳过检查
        
        # 生成限流键
        rate_limit_key = self.generate_rate_limit_key()
        
        # 检查是否允许请求
        allowed = rate_limiter.is_allowed(
            key=rate_limit_key,
            capacity=rate_limit_config.get('capacity', 10),
            refill_rate=rate_limit_config.get('refill_rate', 1.0),
            tokens=rate_limit_config.get('tokens', 1)
        )
        
        if not allowed:
            # 获取桶状态用于计算重试时间
            bucket_status = rate_limiter.get_bucket_status(rate_limit_key)
            retry_after = self.calculate_retry_after(bucket_status, rate_limit_config)
            
            # 设置响应头
            if retry_after:
                self.set_header('Retry-After', str(retry_after))
            
            # 抛出限流异常
            raise RateLimitExceeded(retry_after=retry_after)
        
        # 设置限流相关的响应头
        self.set_rate_limit_headers(rate_limit_key, rate_limit_config)
    
    def get_rate_limit_config(self) -> Optional[Dict[str, Any]]:
        """获取限流配置"""
        # 检查Handler是否有限流配置
        if hasattr(self, 'rate_limit_config'):
            return self.rate_limit_config
        
        # 检查类级别的限流配置
        if hasattr(self.__class__, 'rate_limit_config'):
            return self.__class__.rate_limit_config
        
        # 从配置文件获取默认限流配置
        try:
            from app.config import settings
            return {
                'capacity': getattr(settings, 'RATE_LIMIT_CAPACITY', 10),
                'refill_rate': getattr(settings, 'RATE_LIMIT_REFILL_RATE', 1.0),
                'tokens': 1
            }
        except:
            return None
    
    def generate_rate_limit_key(self) -> str:
        """生成限流键"""
        # 获取客户端IP
        client_ip = self.get_client_ip()
        
        # 获取用户标识（如果有认证）
        user_id = self.get_user_id()
        
        # 获取端点标识
        endpoint = f"{self.request.method}:{self.request.path}"
        
        # 构建限流键
        if user_id:
            return f"rate_limit:user:{user_id}:{endpoint}"
        else:
            return f"rate_limit:ip:{client_ip}:{endpoint}"
    
    def get_client_ip(self) -> str:
        """获取客户端IP地址"""
        # 检查代理头
        forwarded_for = self.request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        real_ip = self.request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
        
        return self.request.remote_ip or 'unknown'
    
    def get_user_id(self) -> Optional[str]:
        """获取用户ID（需要在认证中间件中设置）"""
        return getattr(self, 'current_user_id', None)
    
    def calculate_retry_after(self, bucket_status: Optional[Dict[str, float]], 
                            config: Dict[str, Any]) -> Optional[int]:
        """计算重试时间"""
        if not bucket_status:
            return 60  # 默认60秒
        
        # 计算需要等待多长时间才能获得足够的令牌
        tokens_needed = config.get('tokens', 1)
        current_tokens = bucket_status.get('tokens', 0)
        refill_rate = config.get('refill_rate', 1.0)
        
        if current_tokens >= tokens_needed:
            return 0
        
        tokens_to_wait = tokens_needed - current_tokens
        wait_time = tokens_to_wait / refill_rate
        
        return max(1, int(wait_time))
    
    def set_rate_limit_headers(self, rate_limit_key: str, config: Dict[str, Any]):
        """设置限流相关的响应头"""
        bucket_status = rate_limiter.get_bucket_status(rate_limit_key)
        
        if bucket_status:
            # 设置剩余请求数
            remaining = int(bucket_status.get('tokens', 0))
            self.set_header('X-RateLimit-Remaining', str(remaining))
            
            # 设置限流容量
            capacity = config.get('capacity', 10)
            self.set_header('X-RateLimit-Limit', str(capacity))
            
            # 设置重置时间（下次令牌补充时间）
            refill_rate = config.get('refill_rate', 1.0)
            reset_time = int(1 / refill_rate) if refill_rate > 0 else 60
            self.set_header('X-RateLimit-Reset', str(reset_time))


class RateLimitMiddleware:
    """限流中间件"""
    
    def __init__(self, 
                 default_capacity: int = 10,
                 default_refill_rate: float = 1.0,
                 key_generator: Optional[Callable] = None):
        """
        初始化限流中间件
        
        Args:
            default_capacity: 默认令牌桶容量
            default_refill_rate: 默认令牌补充速率
            key_generator: 自定义键生成器
        """
        self.default_capacity = default_capacity
        self.default_refill_rate = default_refill_rate
        self.key_generator = key_generator
    
    def check_rate_limit(self, handler, 
                        capacity: Optional[int] = None,
                        refill_rate: Optional[float] = None,
                        tokens: int = 1) -> bool:
        """检查限流"""
        # 使用默认值
        capacity = capacity or self.default_capacity
        refill_rate = refill_rate or self.default_refill_rate
        
        # 生成限流键
        if self.key_generator:
            key = self.key_generator(handler)
        else:
            key = self.generate_default_key(handler)
        
        # 检查限流
        return rate_limiter.is_allowed(key, capacity, refill_rate, tokens)
    
    def generate_default_key(self, handler) -> str:
        """生成默认限流键"""
        client_ip = handler.request.remote_ip or 'unknown'
        endpoint = f"{handler.request.method}:{handler.request.path}"
        return f"rate_limit:ip:{client_ip}:{endpoint}"


def rate_limit(capacity: int = 10, refill_rate: float = 1.0, tokens: int = 1):
    """限流装饰器"""
    def decorator(handler_class):
        # 为Handler类添加限流配置
        handler_class.rate_limit_config = {
            'capacity': capacity,
            'refill_rate': refill_rate,
            'tokens': tokens
        }
        
        # 创建带限流功能的Handler类
        class RateLimitedHandler(handler_class, RateLimitMixin):
            pass
        
        RateLimitedHandler.__name__ = handler_class.__name__
        RateLimitedHandler.__module__ = handler_class.__module__
        
        return RateLimitedHandler
    
    return decorator


def rate_limit_method(capacity: int = 10, refill_rate: float = 1.0, tokens: int = 1):
    """方法级限流装饰器"""
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            # 生成限流键
            client_ip = self.request.remote_ip or 'unknown'
            method_name = method.__name__
            endpoint = f"{self.request.method}:{self.request.path}:{method_name}"
            key = f"rate_limit:ip:{client_ip}:{endpoint}"
            
            # 检查限流
            allowed = rate_limiter.is_allowed(key, capacity, refill_rate, tokens)
            
            if not allowed:
                # 计算重试时间
                bucket_status = rate_limiter.get_bucket_status(key)
                retry_after = None
                if bucket_status:
                    tokens_needed = tokens
                    current_tokens = bucket_status.get('tokens', 0)
                    if current_tokens < tokens_needed:
                        tokens_to_wait = tokens_needed - current_tokens
                        retry_after = max(1, int(tokens_to_wait / refill_rate))
                
                # 设置响应头
                if retry_after:
                    self.set_header('Retry-After', str(retry_after))
                
                raise RateLimitExceeded(retry_after=retry_after)
            
            # 设置限流响应头
            bucket_status = rate_limiter.get_bucket_status(key)
            if bucket_status:
                remaining = int(bucket_status.get('tokens', 0))
                self.set_header('X-RateLimit-Remaining', str(remaining))
                self.set_header('X-RateLimit-Limit', str(capacity))
            
            return method(self, *args, **kwargs)
        
        return wrapper
    return decorator


class RateLimitHandler(tornado.web.RequestHandler, RateLimitMixin):
    """带限流功能的基础Handler"""
    pass


def enable_rate_limit(handler_class, capacity: int = 10, refill_rate: float = 1.0):
    """为Handler类启用限流功能"""
    class RateLimitEnabledHandler(handler_class, RateLimitMixin):
        rate_limit_config = {
            'capacity': capacity,
            'refill_rate': refill_rate,
            'tokens': 1
        }
    
    RateLimitEnabledHandler.__name__ = handler_class.__name__
    RateLimitEnabledHandler.__module__ = handler_class.__module__
    
    return RateLimitEnabledHandler


# 全局限流中间件实例
rate_limit_middleware = RateLimitMiddleware()