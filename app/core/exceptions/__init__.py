# 自定义异常模块
# 定义项目中使用的各种自定义异常类

from .base_exceptions import (
    BaseAPIException,
    ValidationError,
    ValidationException,
    BusinessException,
    DatabaseException,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ExternalAPIError,
    BusinessLogicError
)

__all__ = [
    'BaseAPIException',
    'ValidationError',
    'ValidationException',
    'BusinessException',
    'DatabaseException',
    'AuthenticationError',
    'AuthorizationError',
    'NotFoundError',
    'ExternalAPIError',
    'BusinessLogicError'
]