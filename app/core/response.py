# 响应处理模块
# 定义统一的API响应格式和处理函数

from typing import Any, Dict, Optional, Union
import json
from datetime import datetime


class APIResponse:
    """API响应类"""
    
    def __init__(
        self,
        success: bool = True,
        code: int = 200,
        message: str = "操作成功",
        data: Any = None,
        timestamp: Optional[str] = None
    ):
        self.success = success
        self.code = code
        self.message = message
        self.data = data
        self.timestamp = timestamp or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'success': self.success,
            'code': self.code,
            'message': self.message,
            'data': self.data,
            'timestamp': self.timestamp
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = 200
) -> APIResponse:
    """成功响应"""
    return APIResponse(
        success=True,
        code=code,
        message=message,
        data=data
    )


def error_response(
    message: str = "操作失败",
    code: int = 500,
    data: Any = None
) -> APIResponse:
    """错误响应"""
    return APIResponse(
        success=False,
        code=code,
        message=message,
        data=data
    )


def validation_error_response(
    message: str = "参数验证失败",
    errors: Optional[Dict[str, Any]] = None
) -> APIResponse:
    """参数验证错误响应"""
    return APIResponse(
        success=False,
        code=400,
        message=message,
        data={'errors': errors} if errors else None
    )


def not_found_response(
    message: str = "资源未找到"
) -> APIResponse:
    """资源未找到响应"""
    return APIResponse(
        success=False,
        code=404,
        message=message
    )


def unauthorized_response(
    message: str = "未授权访问"
) -> APIResponse:
    """未授权响应"""
    return APIResponse(
        success=False,
        code=401,
        message=message
    )


def forbidden_response(
    message: str = "权限不足"
) -> APIResponse:
    """权限不足响应"""
    return APIResponse(
        success=False,
        code=403,
        message=message
    )


def paginated_response(
    data: list,
    total: int,
    page: int = 1,
    page_size: int = 20,
    message: str = "查询成功"
) -> APIResponse:
    """分页响应"""
    return APIResponse(
        success=True,
        code=200,
        message=message,
        data={
            'items': data,
            'pagination': {
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': (total + page_size - 1) // page_size
            }
        }
    )


class ResponseHandler:
    """响应处理器"""
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功", code: int = 200) -> Dict[str, Any]:
        """成功响应"""
        return success_response(data, message, code).to_dict()
    
    @staticmethod
    def error(message: str = "操作失败", code: int = 500, data: Any = None) -> Dict[str, Any]:
        """错误响应"""
        return error_response(message, code, data).to_dict()
    
    @staticmethod
    def validation_error(message: str = "参数验证失败", errors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """参数验证错误响应"""
        return validation_error_response(message, errors).to_dict()
    
    @staticmethod
    def not_found(message: str = "资源未找到") -> Dict[str, Any]:
        """资源未找到响应"""
        return not_found_response(message).to_dict()
    
    @staticmethod
    def unauthorized(message: str = "未授权访问") -> Dict[str, Any]:
        """未授权响应"""
        return unauthorized_response(message).to_dict()
    
    @staticmethod
    def forbidden(message: str = "权限不足") -> Dict[str, Any]:
        """权限不足响应"""
        return forbidden_response(message).to_dict()
    
    @staticmethod
    def paginated(data: list, total: int, page: int = 1, page_size: int = 20, message: str = "查询成功") -> Dict[str, Any]:
        """分页响应"""
        return paginated_response(data, total, page, page_size, message).to_dict()