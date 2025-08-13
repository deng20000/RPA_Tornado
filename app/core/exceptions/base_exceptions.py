# 基础异常类定义
# 定义项目中所有自定义异常的基类和常用异常类型

from typing import Optional, Dict, Any


class BaseAPIException(Exception):
    """API异常基类"""
    
    def __init__(
        self, 
        message: str = "API错误", 
        code: int = 500, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'code': self.code,
            'message': self.message,
            'details': self.details
        }


class ValidationError(BaseAPIException):
    """参数验证异常"""
    
    def __init__(self, message: str = "参数验证失败", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, details)


class AuthenticationError(BaseAPIException):
    """认证异常"""
    
    def __init__(self, message: str = "认证失败", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 401, details)


class AuthorizationError(BaseAPIException):
    """授权异常"""
    
    def __init__(self, message: str = "权限不足", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 403, details)


class NotFoundError(BaseAPIException):
    """资源未找到异常"""
    
    def __init__(self, message: str = "资源未找到", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 404, details)


class ExternalAPIError(BaseAPIException):
    """外部API调用异常"""
    
    def __init__(self, message: str = "外部API调用失败", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 502, details)


class BusinessLogicError(BaseAPIException):
    """业务逻辑异常"""
    
    def __init__(self, message: str = "业务逻辑错误", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422, details)


class ValidationException(BaseAPIException):
    """验证异常"""
    
    def __init__(self, message: str = "验证失败", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 400, details)


class BusinessException(BaseAPIException):
    """业务异常"""
    
    def __init__(self, message: str = "业务处理异常", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 422, details)


class DatabaseException(BaseAPIException):
    """数据库异常"""
    
    def __init__(self, message: str = "数据库操作异常", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, 500, details)