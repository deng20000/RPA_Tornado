# 基础数据模块数据传输对象模式
# 定义基础数据相关的请求和响应数据结构

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .base_schemas import BaseRequest, BaseResponse, PaginationRequest
from ..shared.enums.business_enums import SellerStatus, Platform, Market


@dataclass
class BaseDataRequest(BaseRequest):
    """基础数据请求模式"""
    sid: Optional[str] = None  # 店铺ID
    marketplace: Optional[str] = None  # 市场
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        return errors


@dataclass
class BaseDataResponse(BaseResponse):
    """基础数据响应模式"""
    data: Any = None


@dataclass
class SellerInfoRequest(BaseDataRequest):
    """店铺信息请求模式"""
    include_metrics: bool = False  # 是否包含指标数据
    include_settings: bool = False  # 是否包含设置信息


@dataclass
class SellerInfo:
    """店铺信息"""
    sid: str
    seller_name: str
    marketplace: str
    country: str
    currency: str
    status: int
    registration_date: str
    last_sync_time: Optional[str] = None
    
    # 可选的指标数据
    total_sales: Optional[float] = None
    total_orders: Optional[int] = None
    active_products: Optional[int] = None
    
    # 可选的设置信息
    timezone: Optional[str] = None
    language: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'sid': self.sid,
            'seller_name': self.seller_name,
            'marketplace': self.marketplace,
            'country': self.country,
            'currency': self.currency,
            'status': self.status,
            'status_name': SellerStatus.get_description(self.status),
            'registration_date': self.registration_date,
            'last_sync_time': self.last_sync_time
        }
        
        # 添加可选字段
        if self.total_sales is not None:
            result['total_sales'] = self.total_sales
        if self.total_orders is not None:
            result['total_orders'] = self.total_orders
        if self.active_products is not None:
            result['active_products'] = self.active_products
        if self.timezone is not None:
            result['timezone'] = self.timezone
        if self.language is not None:
            result['language'] = self.language
            
        return result


@dataclass
class SellerInfoResponse(BaseDataResponse):
    """店铺信息响应模式"""
    data: Optional[SellerInfo] = None


@dataclass
class MarketplaceListRequest(BaseRequest):
    """市场列表请求模式"""
    platform: Optional[str] = None  # 平台筛选
    active_only: bool = True  # 只返回活跃市场


@dataclass
class MarketplaceInfo:
    """市场信息"""
    marketplace_id: str
    marketplace_name: str
    country_code: str
    country_name: str
    currency: str
    platform: str
    is_active: bool
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'marketplace_id': self.marketplace_id,
            'marketplace_name': self.marketplace_name,
            'country_code': self.country_code,
            'country_name': self.country_name,
            'currency': self.currency,
            'platform': self.platform,
            'platform_name': Platform.get_description(self.platform),
            'is_active': self.is_active
        }


@dataclass
class MarketplaceListResponse(BaseDataResponse):
    """市场列表响应模式"""
    data: List[MarketplaceInfo] = field(default_factory=list)


@dataclass
class CategoryListRequest(BaseDataRequest):
    """分类列表请求模式"""
    parent_id: Optional[str] = None  # 父分类ID
    level: Optional[int] = None  # 分类级别
    include_children: bool = False  # 是否包含子分类


@dataclass
class CategoryInfo:
    """分类信息"""
    category_id: str
    category_name: str
    parent_id: Optional[str]
    level: int
    path: str  # 分类路径
    is_leaf: bool  # 是否叶子节点
    product_count: Optional[int] = None  # 产品数量
    children: List['CategoryInfo'] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'parent_id': self.parent_id,
            'level': self.level,
            'path': self.path,
            'is_leaf': self.is_leaf
        }
        
        if self.product_count is not None:
            result['product_count'] = self.product_count
            
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]
            
        return result


@dataclass
class CategoryListResponse(BaseDataResponse):
    """分类列表响应模式"""
    data: List[CategoryInfo] = field(default_factory=list)


@dataclass
class CurrencyRateRequest(BaseRequest):
    """汇率请求模式"""
    base_currency: str = 'USD'  # 基础货币
    target_currencies: List[str] = field(default_factory=list)  # 目标货币列表
    date: Optional[str] = None  # 指定日期，默认为当前日期
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.base_currency:
            errors.append("基础货币不能为空")
            
        if not self.target_currencies:
            errors.append("目标货币列表不能为空")
            
        if self.date:
            try:
                datetime.strptime(self.date, '%Y-%m-%d')
            except ValueError:
                errors.append("日期格式不正确，应为YYYY-MM-DD")
                
        return errors


@dataclass
class CurrencyRate:
    """汇率信息"""
    base_currency: str
    target_currency: str
    rate: float
    date: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'base_currency': self.base_currency,
            'target_currency': self.target_currency,
            'rate': self.rate,
            'date': self.date
        }


@dataclass
class CurrencyRateResponse(BaseDataResponse):
    """汇率响应模式"""
    data: List[CurrencyRate] = field(default_factory=list)
    base_currency: str = 'USD'
    date: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))


@dataclass
class SettingsRequest(BaseDataRequest):
    """设置请求模式"""
    setting_type: Optional[str] = None  # 设置类型
    setting_key: Optional[str] = None   # 设置键


@dataclass
class SettingItem:
    """设置项"""
    setting_key: str
    setting_value: Any
    setting_type: str
    description: Optional[str] = None
    is_encrypted: bool = False
    last_updated: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'setting_key': self.setting_key,
            'setting_value': self.setting_value if not self.is_encrypted else '***',
            'setting_type': self.setting_type,
            'description': self.description,
            'is_encrypted': self.is_encrypted,
            'last_updated': self.last_updated
        }


@dataclass
class SettingsResponse(BaseDataResponse):
    """设置响应模式"""
    data: List[SettingItem] = field(default_factory=list)


@dataclass
class UpdateSettingRequest(BaseRequest):
    """更新设置请求模式"""
    sid: str
    setting_key: str
    setting_value: Any
    setting_type: str = 'string'
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.setting_key:
            errors.append("设置键(setting_key)不能为空")
            
        if self.setting_value is None:
            errors.append("设置值(setting_value)不能为空")
            
        return errors


@dataclass
class UpdateSettingResponse(BaseDataResponse):
    """更新设置响应模式"""
    message: str = "设置更新成功"