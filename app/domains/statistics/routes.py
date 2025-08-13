# 统计领域路由配置
# 定义统计相关的URL路由映射

from typing import List, Tuple
from tornado.web import URLSpec

from .handlers import (
    SalesReportHandler,
    OrderProfitHandler,
    ProductPerformanceHandler,
    ProfitStatisticsHandler,
    ShipmentRemovalHandler
)


def get_statistics_routes() -> List[URLSpec]:
    """获取统计模块的路由配置
    
    Returns:
        路由配置列表
    """
    return [
        # 销量报表路由
        URLSpec(
            r"/api/statistics/sales-report",
            SalesReportHandler,
            name="sales_report"
        ),
        
        # 订单利润路由
        URLSpec(
            r"/api/statistics/order-profit",
            OrderProfitHandler,
            name="order_profit"
        ),
        
        # 产品表现路由
        URLSpec(
            r"/api/statistics/product-performance",
            ProductPerformanceHandler,
            name="product_performance"
        ),
        
        # 利润统计路由
        URLSpec(
            r"/api/statistics/profit-statistics",
            ProfitStatisticsHandler,
            name="profit_statistics"
        ),
        
        # 移除货件报表路由
        URLSpec(
            r"/api/statistics/shipment-removal",
            ShipmentRemovalHandler,
            name="shipment_removal"
        ),
    ]


def get_statistics_route_patterns() -> List[Tuple[str, str]]:
    """获取统计模块的路由模式
    
    Returns:
        路由模式列表，格式为 (pattern, name)
    """
    return [
        (r"/api/statistics/sales-report", "sales_report"),
        (r"/api/statistics/order-profit", "order_profit"),
        (r"/api/statistics/product-performance", "product_performance"),
        (r"/api/statistics/profit-statistics", "profit_statistics"),
        (r"/api/statistics/shipment-removal", "shipment_removal"),
    ]


def get_statistics_api_info() -> dict:
    """获取统计模块的API信息
    
    Returns:
        API信息字典
    """
    return {
        "module": "statistics",
        "version": "1.0.0",
        "description": "统计数据相关API",
        "endpoints": [
            {
                "path": "/api/statistics/sales-report",
                "method": ["GET", "POST"],
                "description": "获取销量报表数据",
                "parameters": {
                    "sid": "店铺ID（必填）",
                    "asin_type": "ASIN类型（必填）",
                    "asin": "ASIN或MSKU（可选）",
                    "event_date": "事件日期（必填）",
                    "marketplace": "市场（可选）",
                    "page": "页码（可选，默认1）",
                    "page_size": "每页大小（可选，默认20）"
                }
            },
            {
                "path": "/api/statistics/order-profit",
                "method": ["GET", "POST"],
                "description": "获取订单利润数据",
                "parameters": {
                    "sid": "店铺ID（必填）",
                    "msku": "MSKU（可选）",
                    "order_id": "订单ID（可选）",
                    "marketplace": "市场（可选）",
                    "start_date": "开始日期（可选）",
                    "end_date": "结束日期（可选）",
                    "page": "页码（可选，默认1）",
                    "page_size": "每页大小（可选，默认20）"
                }
            },
            {
                "path": "/api/statistics/product-performance",
                "method": ["GET", "POST"],
                "description": "获取产品表现数据",
                "parameters": {
                    "sid": "店铺ID（必填）",
                    "asin": "ASIN（可选）",
                    "marketplace": "市场（可选）",
                    "report_type": "报表类型（可选，默认销量）",
                    "start_date": "开始日期（可选）",
                    "end_date": "结束日期（可选）",
                    "page": "页码（可选，默认1）",
                    "page_size": "每页大小（可选，默认20）"
                }
            },
            {
                "path": "/api/statistics/profit-statistics",
                "method": ["GET", "POST"],
                "description": "获取利润统计数据",
                "parameters": {
                    "sid": "店铺ID（必填）",
                    "marketplace": "市场（可选）",
                    "start_date": "开始日期（可选）",
                    "end_date": "结束日期（可选）",
                    "group_by": "分组方式（可选，默认day）"
                }
            },
            {
                "path": "/api/statistics/shipment-removal",
                "method": ["GET", "POST"],
                "description": "获取移除货件报表",
                "parameters": {
                    "sid": "店铺ID（必填）",
                    "removal_order_id": "移除订单ID（可选）",
                    "disposition": "处置方式（可选）",
                    "start_date": "开始日期（可选）",
                    "end_date": "结束日期（可选）",
                    "page": "页码（可选，默认1）",
                    "page_size": "每页大小（可选，默认20）"
                }
            }
        ]
    }


# 路由组配置
STATISTICS_ROUTE_GROUP = {
    "prefix": "/api/statistics",
    "handlers": [
        (r"/sales-report", SalesReportHandler),
        (r"/order-profit", OrderProfitHandler),
        (r"/product-performance", ProductPerformanceHandler),
        (r"/profit-statistics", ProfitStatisticsHandler),
        (r"/shipment-removal", ShipmentRemovalHandler),
    ],
    "middleware": [],  # 可以添加中间件
    "description": "统计数据相关API路由组"
}