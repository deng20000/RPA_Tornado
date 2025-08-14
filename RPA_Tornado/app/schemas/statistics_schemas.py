# 统计模块数据传输对象模式
# 定义统计相关的请求和响应数据结构

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .base_schemas import BaseRequest, BaseResponse, PaginationRequest, DateRangeRequest
from ..shared.enums.business_enums import AsinType, ReportType


@dataclass
class SalesReportRequest(PaginationRequest, DateRangeRequest):
    """销量报表请求模式"""
    sid: Optional[str] = None  # 店铺ID
    asin_type: int = AsinType.ASIN  # ASIN类型
    asin: Optional[str] = None  # ASIN或MSKU
    event_date: Optional[str] = None  # 事件日期
    marketplace: Optional[str] = None  # 市场
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        # 验证必填字段
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
        
        if not self.event_date:
            errors.append("事件日期(event_date)不能为空")
        
        # 验证日期格式
        if self.event_date:
            try:
                datetime.strptime(self.event_date, '%Y-%m-%d')
            except ValueError:
                errors.append("事件日期格式不正确，应为YYYY-MM-DD")
        
        # 验证ASIN类型
        if self.asin_type not in [AsinType.ASIN, AsinType.MSKU]:
            errors.append("ASIN类型无效")
            
        return errors


@dataclass
class SalesReportItem:
    """销量报表项"""
    asin: str
    title: str
    sales_amount: float  # 销售额
    sales_quantity: int  # 销量
    order_count: int     # 订单数
    marketplace: str
    event_date: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'asin': self.asin,
            'title': self.title,
            'sales_amount': self.sales_amount,
            'sales_quantity': self.sales_quantity,
            'order_count': self.order_count,
            'marketplace': self.marketplace,
            'event_date': self.event_date
        }


@dataclass
class SalesReportResponse(BaseResponse):
    """销量报表响应模式"""
    data: List[SalesReportItem] = field(default_factory=list)
    total: int = 0
    summary: Optional[Dict[str, Any]] = None  # 汇总信息


@dataclass
class OrderProfitRequest(PaginationRequest, DateRangeRequest):
    """订单利润请求模式"""
    sid: Optional[str] = None  # 店铺ID
    msku: Optional[str] = None  # MSKU
    order_id: Optional[str] = None  # 订单ID
    marketplace: Optional[str] = None  # 市场
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        return errors


@dataclass
class OrderProfitItem:
    """订单利润项"""
    order_id: str
    msku: str
    asin: str
    title: str
    quantity: int
    unit_price: float
    total_amount: float
    cost: float
    profit: float
    profit_margin: float  # 利润率
    marketplace: str
    order_date: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'order_id': self.order_id,
            'msku': self.msku,
            'asin': self.asin,
            'title': self.title,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'total_amount': self.total_amount,
            'cost': self.cost,
            'profit': self.profit,
            'profit_margin': self.profit_margin,
            'marketplace': self.marketplace,
            'order_date': self.order_date
        }


@dataclass
class OrderProfitResponse(BaseResponse):
    """订单利润响应模式"""
    data: List[OrderProfitItem] = field(default_factory=list)
    total: int = 0
    summary: Optional[Dict[str, Any]] = None


@dataclass
class ProductPerformanceRequest(PaginationRequest, DateRangeRequest):
    """产品表现请求模式"""
    sid: Optional[str] = None  # 店铺ID
    asin: Optional[str] = None  # ASIN
    marketplace: Optional[str] = None  # 市场
    report_type: int = ReportType.SALES  # 报表类型
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
        
        if self.report_type not in [ReportType.SALES, ReportType.QUANTITY, ReportType.ORDERS]:
            errors.append("报表类型无效")
            
        return errors


@dataclass
class ProductPerformanceItem:
    """产品表现项"""
    asin: str
    title: str
    marketplace: str
    sales_rank: Optional[int]  # 销售排名
    category_rank: Optional[int]  # 分类排名
    review_count: int
    review_rating: float
    price: float
    sales_amount: float
    sales_quantity: int
    conversion_rate: float  # 转化率
    click_through_rate: float  # 点击率
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'asin': self.asin,
            'title': self.title,
            'marketplace': self.marketplace,
            'sales_rank': self.sales_rank,
            'category_rank': self.category_rank,
            'review_count': self.review_count,
            'review_rating': self.review_rating,
            'price': self.price,
            'sales_amount': self.sales_amount,
            'sales_quantity': self.sales_quantity,
            'conversion_rate': self.conversion_rate,
            'click_through_rate': self.click_through_rate
        }


@dataclass
class ProductPerformanceResponse(BaseResponse):
    """产品表现响应模式"""
    data: List[ProductPerformanceItem] = field(default_factory=list)
    total: int = 0
    summary: Optional[Dict[str, Any]] = None


@dataclass
class ProfitStatisticsRequest(DateRangeRequest):
    """利润统计请求模式"""
    sid: Optional[str] = None  # 店铺ID
    marketplace: Optional[str] = None  # 市场
    group_by: str = 'day'  # 分组方式: day, week, month
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
        
        if self.group_by not in ['day', 'week', 'month']:
            errors.append("分组方式只能是 day, week, month")
            
        return errors


@dataclass
class ProfitStatisticsItem:
    """利润统计项"""
    period: str  # 时间周期
    total_sales: float  # 总销售额
    total_cost: float   # 总成本
    total_profit: float # 总利润
    profit_margin: float # 利润率
    order_count: int    # 订单数
    product_count: int  # 产品数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'period': self.period,
            'total_sales': self.total_sales,
            'total_cost': self.total_cost,
            'total_profit': self.total_profit,
            'profit_margin': self.profit_margin,
            'order_count': self.order_count,
            'product_count': self.product_count
        }


@dataclass
class ProfitStatisticsResponse(BaseResponse):
    """利润统计响应模式"""
    data: List[ProfitStatisticsItem] = field(default_factory=list)
    summary: Optional[Dict[str, Any]] = None


@dataclass
class ShipmentRemovalRequest(PaginationRequest, DateRangeRequest):
    """移除货件报表请求模式"""
    sid: Optional[str] = None  # 店铺ID
    removal_order_id: Optional[str] = None  # 移除订单ID
    disposition: Optional[str] = None  # 处置方式
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        return errors


@dataclass
class ShipmentRemovalItem:
    """移除货件项"""
    removal_order_id: str
    request_date: str
    order_status: str
    order_type: str
    sku: str
    fnsku: str
    disposition: str
    requested_quantity: int
    cancelled_quantity: int
    disposed_quantity: int
    shipped_quantity: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'removal_order_id': self.removal_order_id,
            'request_date': self.request_date,
            'order_status': self.order_status,
            'order_type': self.order_type,
            'sku': self.sku,
            'fnsku': self.fnsku,
            'disposition': self.disposition,
            'requested_quantity': self.requested_quantity,
            'cancelled_quantity': self.cancelled_quantity,
            'disposed_quantity': self.disposed_quantity,
            'shipped_quantity': self.shipped_quantity
        }


@dataclass
class ShipmentRemovalResponse(BaseResponse):
    """移除货件报表响应模式"""
    data: List[ShipmentRemovalItem] = field(default_factory=list)
    total: int = 0