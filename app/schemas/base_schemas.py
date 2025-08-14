# 基础数据传输对象模式
# 定义通用的请求和响应数据结构

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, field
import json


@dataclass
class BaseRequest:
    """基础请求模式"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                elif hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                elif isinstance(value, list):
                    result[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
                else:
                    result[key] = value
        return result
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """从字典创建实例"""
        # 过滤掉不存在的字段
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid_fields)
    
    def validate(self) -> List[str]:
        """验证数据，返回错误列表"""
        errors = []
        # 子类可以重写此方法添加具体验证逻辑
        return errors


@dataclass
class BaseResponse:
    """基础响应模式"""
    success: bool = True
    message: str = "操作成功"
    code: int = 200
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                elif hasattr(value, 'to_dict'):
                    result[key] = value.to_dict()
                elif isinstance(value, list):
                    result[key] = [item.to_dict() if hasattr(item, 'to_dict') else item for item in value]
                else:
                    result[key] = value
        return result
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)


@dataclass
class PaginationRequest(BaseRequest):
    """分页请求模式"""
    page: int = 1
    page_size: int = 20
    
    def validate(self) -> List[str]:
        """验证分页参数"""
        errors = super().validate()
        
        if self.page < 1:
            errors.append("页码必须大于0")
        
        if self.page_size < 1:
            errors.append("每页大小必须大于0")
        elif self.page_size > 1000:
            errors.append("每页大小不能超过1000")
            
        return errors
    
    @property
    def offset(self) -> int:
        """计算偏移量"""
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        """获取限制数量"""
        return self.page_size


@dataclass
class PaginationInfo:
    """分页信息"""
    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool
    
    @classmethod
    def create(cls, page: int, page_size: int, total: int) -> 'PaginationInfo':
        """创建分页信息"""
        total_pages = (total + page_size - 1) // page_size
        return cls(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )


@dataclass
class PaginationResponse(BaseResponse):
    """分页响应模式"""
    data: List[Any] = field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
    
    @classmethod
    def create(
        cls,
        data: List[Any],
        page: int,
        page_size: int,
        total: int,
        message: str = "查询成功"
    ) -> 'PaginationResponse':
        """创建分页响应"""
        pagination = PaginationInfo.create(page, page_size, total)
        return cls(
            data=data,
            pagination=pagination,
            message=message
        )


@dataclass
class DateRangeRequest(BaseRequest):
    """日期范围请求模式"""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    def validate(self) -> List[str]:
        """验证日期范围"""
        errors = super().validate()
        
        if self.start_date:
            try:
                start = datetime.fromisoformat(self.start_date.replace('Z', '+00:00'))
            except ValueError:
                errors.append("开始日期格式不正确")
                return errors
        
        if self.end_date:
            try:
                end = datetime.fromisoformat(self.end_date.replace('Z', '+00:00'))
            except ValueError:
                errors.append("结束日期格式不正确")
                return errors
        
        if self.start_date and self.end_date:
            try:
                start = datetime.fromisoformat(self.start_date.replace('Z', '+00:00'))
                end = datetime.fromisoformat(self.end_date.replace('Z', '+00:00'))
                if start > end:
                    errors.append("开始日期不能晚于结束日期")
            except ValueError:
                pass  # 日期格式错误已在上面检查
                
        return errors


@dataclass
class SortRequest(BaseRequest):
    """排序请求模式"""
    sort_by: Optional[str] = None
    sort_order: str = 'asc'  # asc 或 desc
    
    def validate(self) -> List[str]:
        """验证排序参数"""
        errors = super().validate()
        
        if self.sort_order not in ['asc', 'desc']:
            errors.append("排序方向只能是 'asc' 或 'desc'")
            
        return errors


@dataclass
class FilterRequest(BaseRequest):
    """过滤请求模式"""
    filters: Dict[str, Any] = field(default_factory=dict)
    
    def add_filter(self, key: str, value: Any) -> None:
        """添加过滤条件"""
        self.filters[key] = value
    
    def get_filter(self, key: str, default: Any = None) -> Any:
        """获取过滤条件"""
        return self.filters.get(key, default)
    
    def has_filter(self, key: str) -> bool:
        """检查是否有指定过滤条件"""
        return key in self.filters


@dataclass
class ErrorDetail:
    """错误详情"""
    field: str
    message: str
    code: Optional[str] = None


@dataclass
class ErrorResponse(BaseResponse):
    """错误响应模式"""
    success: bool = False
    errors: List[ErrorDetail] = field(default_factory=list)
    
    def add_error(self, field: str, message: str, code: Optional[str] = None) -> None:
        """添加错误"""
        self.errors.append(ErrorDetail(field=field, message=message, code=code))
    
    @classmethod
    def from_validation_errors(cls, errors: List[str], message: str = "数据验证失败") -> 'ErrorResponse':
        """从验证错误创建响应"""
        response = cls(message=message, code=400)
        for error in errors:
            response.add_error("validation", error)
        return response