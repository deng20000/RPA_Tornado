# -*- coding: utf-8 -*-
"""
电商数据看板数据模式
定义电商数据看板相关的请求和响应数据结构
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, validator
import re


class SyncShopDataRequest(BaseModel):
    """同步店铺数据请求模式"""
    access_token: str = Field(..., description="访问令牌")
    
    @validator('access_token')
    def validate_access_token(cls, v):
        if not v or not v.strip():
            raise ValueError('访问令牌不能为空')
        return v.strip()


class SyncExchangeRateRequest(BaseModel):
    """同步汇率数据请求模式"""
    access_token: str = Field(..., description="访问令牌")
    target_date: Optional[str] = Field(None, description="目标日期，格式为 YYYY-MM")
    
    @validator('access_token')
    def validate_access_token(cls, v):
        if not v or not v.strip():
            raise ValueError('访问令牌不能为空')
        return v.strip()
    
    @validator('target_date')
    def validate_target_date(cls, v):
        if v is not None:
            if not re.match(r'^\d{4}-\d{2}$', v):
                raise ValueError('目标日期格式必须为 YYYY-MM')
        return v


class SyncSalesDataRequest(BaseModel):
    """同步销售数据请求模式"""
    access_token: str = Field(..., description="访问令牌")
    start_date: Optional[str] = Field(None, description="开始日期，格式为 YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="结束日期，格式为 YYYY-MM-DD")
    
    @validator('access_token')
    def validate_access_token(cls, v):
        if not v or not v.strip():
            raise ValueError('访问令牌不能为空')
        return v.strip()
    
    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        if v is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
                raise ValueError('日期格式必须为 YYYY-MM-DD')
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('无效的日期')
        return v


class ShopInfo(BaseModel):
    """店铺信息模式"""
    id: int = Field(..., description="主键ID")
    shop_id: str = Field(..., description="店铺ID")
    shop_name: str = Field(..., description="店铺名称")
    platform_id: str = Field(..., description="平台ID")
    platform: str = Field(..., description="平台名称")
    status: str = Field(..., description="店铺状态")
    currency: str = Field(..., description="店铺主要货币")
    timezone: str = Field(..., description="店铺时区")
    description: Optional[str] = Field(None, description="店铺描述")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class SaleInfo(BaseModel):
    """销售信息模式"""
    id: int = Field(..., description="主键ID")
    shop_id: int = Field(..., description="店铺ID")
    sale_date: str = Field(..., description="销售日期")
    order_id: Optional[str] = Field(None, description="订单ID")
    product_id: Optional[str] = Field(None, description="产品ID")
    product_name: Optional[str] = Field(None, description="产品名称")
    original_amount: str = Field(..., description="原始金额")
    original_currency: str = Field(..., description="原始货币")
    cny_amount: str = Field(..., description="人民币金额")
    usd_amount: Optional[str] = Field(None, description="美元金额")
    quantity: int = Field(..., description="销售数量")
    unit_price: Optional[str] = Field(None, description="单价")
    commission: Optional[str] = Field(None, description="佣金")
    shipping_fee: Optional[str] = Field(None, description="运费")
    tax: Optional[str] = Field(None, description="税费")
    exchange_rate: Optional[str] = Field(None, description="使用的汇率")
    exchange_rate_date: Optional[str] = Field(None, description="汇率日期")
    category: Optional[str] = Field(None, description="产品类别")
    region: Optional[str] = Field(None, description="销售地区")
    notes: Optional[str] = Field(None, description="备注信息")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class ExchangeRateInfo(BaseModel):
    """汇率信息模式"""
    id: int = Field(..., description="主键ID")
    currency_code: str = Field(..., description="货币代码")
    currency_name: Optional[str] = Field(None, description="货币名称")
    base_currency: str = Field(..., description="基准货币")
    rate: str = Field(..., description="汇率值")
    user_rate: Optional[str] = Field(None, description="用户自定义汇率")
    rate_date: str = Field(..., description="汇率日期")
    effective_date: Optional[str] = Field(None, description="生效日期")
    expiry_date: Optional[str] = Field(None, description="失效日期")
    source: str = Field(..., description="汇率来源")
    status: str = Field(..., description="状态")
    previous_rate: Optional[str] = Field(None, description="前一次汇率")
    change_rate: Optional[str] = Field(None, description="变化率")
    change_amount: Optional[str] = Field(None, description="变化金额")
    description: Optional[str] = Field(None, description="汇率描述")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")


class SyncResponse(BaseModel):
    """同步操作响应模式"""
    success: bool = Field(..., description="操作是否成功")
    synced_count: int = Field(..., description="新增记录数")
    updated_count: Optional[int] = Field(None, description="更新记录数")
    total_count: int = Field(..., description="总记录数")
    target_date: Optional[str] = Field(None, description="目标日期")
    start_date: Optional[str] = Field(None, description="开始日期")
    end_date: Optional[str] = Field(None, description="结束日期")
    message: Optional[str] = Field(None, description="操作消息")


class SalesAmount(BaseModel):
    """销售金额模式"""
    cny: str = Field(..., description="人民币金额")
    usd: str = Field(..., description="美元金额")
    order_count: int = Field(..., description="订单数量")


class DashboardSummaryResponse(BaseModel):
    """数据看板摘要响应模式"""
    total_shops: int = Field(..., description="店铺总数")
    total_sales_today: SalesAmount = Field(..., description="今日销售总额")
    total_sales_yesterday: SalesAmount = Field(..., description="昨日销售总额")
    exchange_rate_updated: Optional[str] = Field(None, description="汇率更新时间")
    last_sync_time: str = Field(..., description="最后同步时间")


class ShopListRequest(BaseModel):
    """店铺列表请求模式"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    platform: Optional[str] = Field(None, description="平台筛选")


class ShopListResponse(BaseModel):
    """店铺列表响应模式"""
    shops: List[ShopInfo] = Field(..., description="店铺列表")
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")


class SalesStatisticsRequest(BaseModel):
    """销售统计请求模式"""
    start_date: Optional[str] = Field(None, description="开始日期，格式为 YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="结束日期，格式为 YYYY-MM-DD")
    shop_id: Optional[str] = Field(None, description="店铺ID")
    currency: str = Field('CNY', description="货币类型")
    
    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        if v is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
                raise ValueError('日期格式必须为 YYYY-MM-DD')
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('无效的日期')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        if v not in ['CNY', 'USD']:
            raise ValueError('货币类型必须是 CNY 或 USD')
        return v


class ShopBreakdown(BaseModel):
    """店铺销售分解模式"""
    shop_name: str = Field(..., description="店铺名称")
    platform: str = Field(..., description="平台名称")
    sales: str = Field(..., description="销售金额")
    orders: int = Field(..., description="订单数量")


class SalesStatisticsResponse(BaseModel):
    """销售统计响应模式"""
    total_sales: str = Field(..., description="总销售额")
    total_orders: int = Field(..., description="总订单数")
    average_order_value: str = Field(..., description="平均订单价值")
    currency: str = Field(..., description="货币类型")
    period: Dict[str, Optional[str]] = Field(..., description="统计周期")
    shop_breakdown: List[ShopBreakdown] = Field(..., description="店铺销售分解")


class CurrencyConversionRequest(BaseModel):
    """货币转换请求模式"""
    amount: str = Field(..., description="金额")
    from_currency: str = Field(..., description="源货币代码")
    to_currency: str = Field(..., description="目标货币代码")
    conversion_date: Optional[str] = Field(None, description="转换日期，格式为 YYYY-MM-DD")
    
    @validator('amount')
    def validate_amount(cls, v):
        try:
            amount_decimal = Decimal(v)
            if amount_decimal < 0:
                raise ValueError('金额不能为负数')
        except (ValueError, TypeError):
            raise ValueError('无效的金额格式')
        return v
    
    @validator('from_currency', 'to_currency')
    def validate_currency_code(cls, v):
        if not re.match(r'^[A-Z]{3}$', v):
            raise ValueError('货币代码必须是3位大写字母')
        return v
    
    @validator('conversion_date')
    def validate_conversion_date(cls, v):
        if v is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
                raise ValueError('转换日期格式必须为 YYYY-MM-DD')
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('无效的转换日期')
        return v


class CurrencyConversionResponse(BaseModel):
    """货币转换响应模式"""
    original_amount: str = Field(..., description="原始金额")
    original_currency: str = Field(..., description="原始货币")
    converted_amount: str = Field(..., description="转换后金额")
    target_currency: str = Field(..., description="目标货币")
    exchange_rate: str = Field(..., description="使用的汇率")
    conversion_date: str = Field(..., description="转换日期")
    rate_source: str = Field(..., description="汇率来源")


class ErrorResponse(BaseModel):
    """错误响应模式"""
    code: int = Field(..., description="错误代码")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
    timestamp: str = Field(..., description="错误时间戳")


class SuccessResponse(BaseModel):
    """成功响应模式"""
    code: int = Field(200, description="响应代码")
    message: str = Field(..., description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
    timestamp: str = Field(..., description="响应时间戳")


class PaginationInfo(BaseModel):
    """分页信息模式"""
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total: int = Field(..., description="总记录数")
    total_pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")


class DateRangeRequest(BaseModel):
    """日期范围请求模式"""
    start_date: str = Field(..., description="开始日期，格式为 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期，格式为 YYYY-MM-DD")
    
    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('日期格式必须为 YYYY-MM-DD')
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('无效的日期')
        return v
    
    @validator('end_date')
    def validate_date_range(cls, v, values):
        if 'start_date' in values:
            start_date = datetime.strptime(values['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(v, '%Y-%m-%d').date()
            if start_date > end_date:
                raise ValueError('开始日期不能大于结束日期')
        return v


class BatchOperationRequest(BaseModel):
    """批量操作请求模式"""
    operation: str = Field(..., description="操作类型")
    items: List[Dict[str, Any]] = Field(..., description="操作项目列表")
    options: Optional[Dict[str, Any]] = Field(None, description="操作选项")
    
    @validator('operation')
    def validate_operation(cls, v):
        allowed_operations = ['sync', 'update', 'delete', 'export']
        if v not in allowed_operations:
            raise ValueError(f'操作类型必须是以下之一: {", ".join(allowed_operations)}')
        return v
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('操作项目列表不能为空')
        if len(v) > 1000:
            raise ValueError('单次批量操作不能超过1000个项目')
        return v


class BatchOperationResponse(BaseModel):
    """批量操作响应模式"""
    operation: str = Field(..., description="操作类型")
    total_items: int = Field(..., description="总项目数")
    success_count: int = Field(..., description="成功数量")
    failed_count: int = Field(..., description="失败数量")
    errors: List[Dict[str, Any]] = Field(..., description="错误列表")
    execution_time: float = Field(..., description="执行时间（秒）")
    result_summary: Dict[str, Any] = Field(..., description="结果摘要")


# 导出所有模式
__all__ = [
    'SyncShopDataRequest',
    'SyncExchangeRateRequest', 
    'SyncSalesDataRequest',
    'ShopInfo',
    'SaleInfo',
    'ExchangeRateInfo',
    'SyncResponse',
    'SalesAmount',
    'DashboardSummaryResponse',
    'ShopListRequest',
    'ShopListResponse',
    'SalesStatisticsRequest',
    'ShopBreakdown',
    'SalesStatisticsResponse',
    'CurrencyConversionRequest',
    'CurrencyConversionResponse',
    'ErrorResponse',
    'SuccessResponse',
    'PaginationInfo',
    'DateRangeRequest',
    'BatchOperationRequest',
    'BatchOperationResponse'
]