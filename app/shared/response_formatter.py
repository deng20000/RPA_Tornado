# 响应格式化工具
# 统一API响应格式

import json
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from ..core.exceptions.base_exceptions import BaseAPIException
from .constants.error_codes import ErrorCode, get_error_message
from .enums.api_enums import ResponseStatus


class ResponseFormatter:
    """API响应格式化器"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "操作成功",
        code: int = ErrorCode.SUCCESS,
        meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """格式化成功响应
        
        Args:
            data: 响应数据
            message: 响应消息
            code: 响应码
            meta: 元数据（如分页信息）
            
        Returns:
            格式化的响应字典
        """
        response = {
            "success": True,
            "code": code,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        if meta:
            response["meta"] = meta
            
        return response
    
    @staticmethod
    def error(
        message: str = "操作失败",
        code: int = ErrorCode.INTERNAL_ERROR,
        details: Optional[Dict] = None,
        data: Any = None
    ) -> Dict[str, Any]:
        """格式化错误响应
        
        Args:
            message: 错误消息
            code: 错误码
            details: 错误详情
            data: 附加数据
            
        Returns:
            格式化的错误响应字典
        """
        response = {
            "success": False,
            "code": code,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            response["details"] = details
            
        return response
    
    @staticmethod
    def from_exception(exception: Exception) -> Dict[str, Any]:
        """从异常对象格式化错误响应
        
        Args:
            exception: 异常对象
            
        Returns:
            格式化的错误响应字典
        """
        if isinstance(exception, BaseAPIException):
            return ResponseFormatter.error(
                message=exception.message,
                code=exception.code,
                details=exception.details
            )
        else:
            # 处理未知异常
            return ResponseFormatter.error(
                message="系统内部错误",
                code=ErrorCode.INTERNAL_ERROR,
                details={
                    "exception_type": type(exception).__name__,
                    "exception_message": str(exception),
                    "traceback": traceback.format_exc()
                }
            )
    
    @staticmethod
    def paginated(
        data: List[Any],
        total: int,
        page: int = 1,
        page_size: int = 20,
        message: str = "查询成功"
    ) -> Dict[str, Any]:
        """格式化分页响应
        
        Args:
            data: 数据列表
            total: 总记录数
            page: 当前页码
            page_size: 每页大小
            message: 响应消息
            
        Returns:
            格式化的分页响应字典
        """
        total_pages = (total + page_size - 1) // page_size
        
        meta = {
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
        return ResponseFormatter.success(
            data=data,
            message=message,
            meta=meta
        )
    
    @staticmethod
    def validation_error(
        errors: Union[Dict, List],
        message: str = "数据验证失败"
    ) -> Dict[str, Any]:
        """格式化验证错误响应
        
        Args:
            errors: 验证错误信息
            message: 错误消息
            
        Returns:
            格式化的验证错误响应字典
        """
        return ResponseFormatter.error(
            message=message,
            code=ErrorCode.VALIDATION_ERROR,
            details={"validation_errors": errors}
        )
    
    @staticmethod
    def not_found(
        resource: str = "资源",
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """格式化资源未找到响应
        
        Args:
            resource: 资源名称
            message: 自定义消息
            
        Returns:
            格式化的未找到响应字典
        """
        if not message:
            message = f"{resource}不存在"
            
        return ResponseFormatter.error(
            message=message,
            code=ErrorCode.NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(
        message: str = "未授权访问"
    ) -> Dict[str, Any]:
        """格式化未授权响应
        
        Args:
            message: 错误消息
            
        Returns:
            格式化的未授权响应字典
        """
        return ResponseFormatter.error(
            message=message,
            code=ErrorCode.UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden(
        message: str = "禁止访问"
    ) -> Dict[str, Any]:
        """格式化禁止访问响应
        
        Args:
            message: 错误消息
            
        Returns:
            格式化的禁止访问响应字典
        """
        return ResponseFormatter.error(
            message=message,
            code=ErrorCode.FORBIDDEN
        )
    
    @staticmethod
    def rate_limit_exceeded(
        message: str = "请求频率超限",
        retry_after: Optional[int] = None
    ) -> Dict[str, Any]:
        """格式化限流响应
        
        Args:
            message: 错误消息
            retry_after: 重试等待时间（秒）
            
        Returns:
            格式化的限流响应字典
        """
        details = {}
        if retry_after:
            details["retry_after"] = retry_after
            
        return ResponseFormatter.error(
            message=message,
            code=ErrorCode.TOO_MANY_REQUESTS,
            details=details if details else None
        )
    
    @staticmethod
    def to_json(response: Dict[str, Any], ensure_ascii: bool = False) -> str:
        """将响应字典转换为JSON字符串
        
        Args:
            response: 响应字典
            ensure_ascii: 是否确保ASCII编码
            
        Returns:
            JSON字符串
        """
        return json.dumps(
            response,
            ensure_ascii=ensure_ascii,
            separators=(',', ':'),
            default=str
        )
    
    @staticmethod
    def get_http_status(code: int) -> int:
        """根据业务错误码获取HTTP状态码
        
        Args:
            code: 业务错误码
            
        Returns:
            HTTP状态码
        """
        # 成功状态
        if code == ErrorCode.SUCCESS:
            return ResponseStatus.SUCCESS
        
        # 客户端错误
        if code in [ErrorCode.VALIDATION_ERROR, ErrorCode.INVALID_PARAMETER]:
            return ResponseStatus.BAD_REQUEST
        elif code == ErrorCode.UNAUTHORIZED:
            return ResponseStatus.UNAUTHORIZED
        elif code == ErrorCode.FORBIDDEN:
            return ResponseStatus.FORBIDDEN
        elif code == ErrorCode.NOT_FOUND:
            return ResponseStatus.NOT_FOUND
        elif code == ErrorCode.TOO_MANY_REQUESTS:
            return ResponseStatus.TOO_MANY_REQUESTS
        
        # 服务器错误
        elif code in [
            ErrorCode.INTERNAL_ERROR,
            ErrorCode.DATABASE_ERROR,
            ErrorCode.EXTERNAL_API_ERROR,
            ErrorCode.BUSINESS_LOGIC_ERROR
        ]:
            return ResponseStatus.INTERNAL_ERROR
        
        # 默认返回500
        return ResponseStatus.INTERNAL_SERVER_ERROR