#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理中间件
统一处理应用异常，提供友好的错误响应
"""

import json
import logging
import traceback
import tornado.web
from typing import Dict, Any, Optional
from datetime import datetime

from app.core.exceptions import BaseAPIException
from app.shared import ResponseFormatter


class ErrorHandlerMixin:
    """错误处理混入类"""
    
    def write_error(self, status_code: int, **kwargs):
        """重写错误处理方法"""
        # 获取异常信息
        exc_info = kwargs.get('exc_info')
        error = None
        
        if exc_info:
            error = exc_info[1]
        
        # 处理不同类型的异常
        if isinstance(error, BaseAPIException):
            self.handle_api_exception(error)
        elif isinstance(error, tornado.web.HTTPError):
            self.handle_http_error(error)
        else:
            self.handle_generic_error(status_code, error)
    
    def handle_api_exception(self, error: BaseAPIException):
        """处理API异常"""
        self.set_status(error.code)
        
        response = ResponseFormatter.error(
            message=error.message,
            code=error.code,
            details=error.details
        )
        
        self.write_json_response(response)
        
        # 记录错误日志
        self.log_error(error, error.code)
    
    def handle_http_error(self, error: tornado.web.HTTPError):
        """处理HTTP错误"""
        self.set_status(error.status_code)
        
        # 获取错误消息
        error_messages = {
            400: "请求参数错误",
            401: "未授权访问",
            403: "禁止访问",
            404: "资源未找到",
            405: "方法不允许",
            408: "请求超时",
            413: "请求实体过大",
            429: "请求过于频繁",
            500: "服务器内部错误",
            502: "网关错误",
            503: "服务不可用",
            504: "网关超时"
        }
        
        message = error_messages.get(error.status_code, "未知错误")
        if error.reason:
            message = error.reason
        
        response = ResponseFormatter.error(
            message=message,
            code=error.status_code
        )
        
        self.write_json_response(response)
        
        # 记录错误日志
        self.log_error(error, error.status_code)
    
    def handle_generic_error(self, status_code: int, error: Optional[Exception]):
        """处理通用错误"""
        self.set_status(status_code)
        
        # 根据状态码确定错误消息
        if status_code >= 500:
            message = "服务器内部错误"
            # 服务器错误不暴露详细信息
            if hasattr(self, 'settings') and self.settings.get('debug', False):
                message = str(error) if error else message
        else:
            message = str(error) if error else "请求处理失败"
        
        response = ResponseFormatter.error(
            message=message,
            code=status_code
        )
        
        self.write_json_response(response)
        
        # 记录错误日志
        self.log_error(error, status_code)
    
    def write_json_response(self, response: Dict[str, Any]):
        """写入JSON响应"""
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(json.dumps(response, ensure_ascii=False, indent=2))
    
    def log_error(self, error: Optional[Exception], status_code: int):
        """记录错误日志"""
        logger = logging.getLogger('error')
        
        # 构建错误信息
        error_data = {
            'request_id': getattr(self, 'request_id', 'unknown'),
            'method': self.request.method,
            'uri': self.request.uri,
            'status_code': status_code,
            'client_ip': self.get_client_ip(),
            'user_agent': self.request.headers.get('User-Agent', 'Unknown'),
            'timestamp': datetime.now().isoformat()
        }
        
        if error:
            error_data.update({
                'error_type': type(error).__name__,
                'error_message': str(error)
            })
        
        # 根据错误级别选择日志级别
        if status_code >= 500:
            logger.error(
                f"Server error: {json.dumps(error_data, ensure_ascii=False)}",
                exc_info=error
            )
        elif status_code >= 400:
            logger.warning(
                f"Client error: {json.dumps(error_data, ensure_ascii=False)}"
            )
        else:
            logger.info(
                f"Request info: {json.dumps(error_data, ensure_ascii=False)}"
            )
    
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


class ErrorHandlerMiddleware:
    """错误处理中间件"""
    
    def __init__(self, 
                 debug: bool = False,
                 log_errors: bool = True,
                 include_traceback: bool = False):
        """
        初始化错误处理中间件
        
        Args:
            debug: 调试模式，是否显示详细错误信息
            log_errors: 是否记录错误日志
            include_traceback: 是否在响应中包含堆栈跟踪（仅调试模式）
        """
        self.debug = debug
        self.log_errors = log_errors
        self.include_traceback = include_traceback and debug
        
        # 设置错误日志记录器
        if log_errors:
            self.setup_error_logger()
    
    def setup_error_logger(self):
        """设置错误日志记录器"""
        logger = logging.getLogger('error')
        logger.setLevel(logging.ERROR)
        
        # 如果没有处理器，添加一个
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
    
    def handle_exception(self, handler, error: Exception) -> Dict[str, Any]:
        """处理异常并返回响应数据"""
        if isinstance(error, BaseAPIException):
            return self.handle_api_exception(error)
        elif isinstance(error, tornado.web.HTTPError):
            return self.handle_http_error(error)
        else:
            return self.handle_generic_exception(error)
    
    def handle_api_exception(self, error: BaseAPIException) -> Dict[str, Any]:
        """处理API异常"""
        response = {
            'success': False,
            'code': error.code,
            'message': error.message,
            'data': None
        }
        
        if error.details:
            response['details'] = error.details
        
        if self.include_traceback:
            response['traceback'] = traceback.format_exc()
        
        return response
    
    def handle_http_error(self, error: tornado.web.HTTPError) -> Dict[str, Any]:
        """处理HTTP错误"""
        # 错误消息映射
        error_messages = {
            400: "请求参数错误",
            401: "未授权访问", 
            403: "禁止访问",
            404: "资源未找到",
            405: "方法不允许",
            408: "请求超时",
            413: "请求实体过大",
            429: "请求过于频繁",
            500: "服务器内部错误",
            502: "网关错误",
            503: "服务不可用",
            504: "网关超时"
        }
        
        message = error.reason or error_messages.get(error.status_code, "未知错误")
        
        response = {
            'success': False,
            'code': error.status_code,
            'message': message,
            'data': None
        }
        
        if self.include_traceback:
            response['traceback'] = traceback.format_exc()
        
        return response
    
    def handle_generic_exception(self, error: Exception) -> Dict[str, Any]:
        """处理通用异常"""
        if self.debug:
            message = f"{type(error).__name__}: {str(error)}"
        else:
            message = "服务器内部错误"
        
        response = {
            'success': False,
            'code': 500,
            'message': message,
            'data': None
        }
        
        if self.include_traceback:
            response['traceback'] = traceback.format_exc()
        
        return response
    
    def log_exception(self, handler, error: Exception):
        """记录异常日志"""
        if not self.log_errors:
            return
        
        logger = logging.getLogger('error')
        
        error_info = {
            'request_id': getattr(handler, 'request_id', 'unknown'),
            'method': handler.request.method,
            'uri': handler.request.uri,
            'error_type': type(error).__name__,
            'error_message': str(error),
            'client_ip': handler.request.remote_ip,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.error(
            f"Unhandled exception: {json.dumps(error_info, ensure_ascii=False)}",
            exc_info=error
        )


class ErrorHandlerHandler(tornado.web.RequestHandler, ErrorHandlerMixin):
    """带错误处理的基础Handler"""
    pass


def enable_error_handling(handler_class):
    """装饰器：为Handler类启用错误处理"""
    class ErrorHandlingEnabledHandler(handler_class, ErrorHandlerMixin):
        pass
    
    ErrorHandlingEnabledHandler.__name__ = handler_class.__name__
    ErrorHandlingEnabledHandler.__module__ = handler_class.__module__
    
    return ErrorHandlingEnabledHandler


# 全局错误处理中间件实例
error_handler_middleware = ErrorHandlerMiddleware()