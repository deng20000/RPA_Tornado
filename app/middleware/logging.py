#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志记录中间件
记录请求和响应信息，用于调试和监控
"""

import time
import json
import logging
import tornado.web
from typing import Dict, Any, Optional
from datetime import datetime


class LoggingMixin:
    """日志记录混入类"""
    
    def prepare(self):
        """请求开始时调用"""
        self.start_time = time.time()
        self.request_id = self.generate_request_id()
        
        # 记录请求开始
        self.log_request_start()
    
    def on_finish(self):
        """请求结束时调用"""
        # 记录请求结束
        self.log_request_end()
    
    def generate_request_id(self) -> str:
        """生成请求ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def log_request_start(self):
        """记录请求开始"""
        logger = logging.getLogger('request')
        
        # 获取客户端信息
        client_ip = self.get_client_ip()
        user_agent = self.request.headers.get('User-Agent', 'Unknown')
        
        # 构建日志信息
        log_data = {
            'request_id': self.request_id,
            'method': self.request.method,
            'uri': self.request.uri,
            'client_ip': client_ip,
            'user_agent': user_agent,
            'timestamp': datetime.now().isoformat(),
            'event': 'request_start'
        }
        
        # 记录请求体（仅对POST/PUT/PATCH请求）
        if self.request.method in ['POST', 'PUT', 'PATCH'] and self.request.body:
            try:
                # 尝试解析JSON
                body_data = json.loads(self.request.body.decode('utf-8'))
                # 过滤敏感信息
                filtered_body = self.filter_sensitive_data(body_data)
                log_data['request_body'] = filtered_body
            except (json.JSONDecodeError, UnicodeDecodeError):
                log_data['request_body'] = '<binary_or_invalid_data>'
        
        logger.info(f"Request started: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_request_end(self):
        """记录请求结束"""
        logger = logging.getLogger('request')
        
        # 计算请求耗时
        duration = time.time() - self.start_time
        
        # 构建日志信息
        log_data = {
            'request_id': self.request_id,
            'method': self.request.method,
            'uri': self.request.uri,
            'status_code': self.get_status(),
            'duration_ms': round(duration * 1000, 2),
            'timestamp': datetime.now().isoformat(),
            'event': 'request_end'
        }
        
        # 根据状态码选择日志级别
        if self.get_status() >= 500:
            logger.error(f"Request completed with error: {json.dumps(log_data, ensure_ascii=False)}")
        elif self.get_status() >= 400:
            logger.warning(f"Request completed with client error: {json.dumps(log_data, ensure_ascii=False)}")
        else:
            logger.info(f"Request completed: {json.dumps(log_data, ensure_ascii=False)}")
    
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
    
    def filter_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """过滤敏感数据"""
        if not isinstance(data, dict):
            return data
        
        sensitive_fields = {
            'password', 'passwd', 'pwd', 'secret', 'token', 'key',
            'api_key', 'access_token', 'refresh_token', 'auth_token',
            'credit_card', 'card_number', 'cvv', 'ssn', 'social_security'
        }
        
        filtered = {}
        for key, value in data.items():
            if key.lower() in sensitive_fields:
                filtered[key] = '***FILTERED***'
            elif isinstance(value, dict):
                filtered[key] = self.filter_sensitive_data(value)
            elif isinstance(value, list):
                filtered[key] = [
                    self.filter_sensitive_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                filtered[key] = value
        
        return filtered


class LoggingMiddleware:
    """日志记录中间件"""
    
    def __init__(self, 
                 log_requests: bool = True,
                 log_responses: bool = True,
                 log_errors: bool = True,
                 sensitive_fields: Optional[set] = None):
        """
        初始化日志中间件
        
        Args:
            log_requests: 是否记录请求信息
            log_responses: 是否记录响应信息
            log_errors: 是否记录错误信息
            sensitive_fields: 敏感字段集合
        """
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_errors = log_errors
        self.sensitive_fields = sensitive_fields or {
            'password', 'passwd', 'pwd', 'secret', 'token', 'key',
            'api_key', 'access_token', 'refresh_token', 'auth_token'
        }
        
        # 配置日志记录器
        self.setup_loggers()
    
    def setup_loggers(self):
        """设置日志记录器"""
        # 请求日志记录器
        request_logger = logging.getLogger('request')
        request_logger.setLevel(logging.INFO)
        
        # 错误日志记录器
        error_logger = logging.getLogger('error')
        error_logger.setLevel(logging.ERROR)
        
        # 性能日志记录器
        performance_logger = logging.getLogger('performance')
        performance_logger.setLevel(logging.INFO)
    
    def log_slow_request(self, handler, duration: float, threshold: float = 1.0):
        """记录慢请求"""
        if duration > threshold:
            logger = logging.getLogger('performance')
            
            log_data = {
                'request_id': getattr(handler, 'request_id', 'unknown'),
                'method': handler.request.method,
                'uri': handler.request.uri,
                'duration_ms': round(duration * 1000, 2),
                'threshold_ms': round(threshold * 1000, 2),
                'event': 'slow_request'
            }
            
            logger.warning(f"Slow request detected: {json.dumps(log_data, ensure_ascii=False)}")
    
    def log_error(self, handler, error: Exception):
        """记录错误信息"""
        if not self.log_errors:
            return
        
        logger = logging.getLogger('error')
        
        log_data = {
            'request_id': getattr(handler, 'request_id', 'unknown'),
            'method': handler.request.method,
            'uri': handler.request.uri,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'event': 'error'
        }
        
        logger.error(f"Request error: {json.dumps(log_data, ensure_ascii=False)}", exc_info=True)


class LoggingHandler(tornado.web.RequestHandler, LoggingMixin):
    """带日志记录的基础Handler"""
    pass


def enable_logging(handler_class):
    """装饰器：为Handler类启用日志记录"""
    class LoggingEnabledHandler(handler_class, LoggingMixin):
        pass
    
    LoggingEnabledHandler.__name__ = handler_class.__name__
    LoggingEnabledHandler.__module__ = handler_class.__module__
    
    return LoggingEnabledHandler


# 全局日志中间件实例
logging_middleware = LoggingMiddleware()