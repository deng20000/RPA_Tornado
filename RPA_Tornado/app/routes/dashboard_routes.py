# -*- coding: utf-8 -*-
"""
电商数据看板路由配置
定义电商数据看板相关的API路由
"""

from tornado.web import URLSpec
from app.handlers.dashboard_handler import (
    SyncShopDataHandler,
    SyncExchangeRateHandler,
    SyncSalesDataHandler,
    DashboardSummaryHandler,
    ShopListHandler,
    SalesStatisticsHandler,
    CurrencyConversionHandler,
    HealthCheckHandler
)

# 电商数据看板路由配置
dashboard_routes = [
    # 数据同步相关路由
    URLSpec(
        r"/api/dashboard/sync/shops",
        SyncShopDataHandler,
        name="sync_shop_data"
    ),
    URLSpec(
        r"/api/dashboard/sync/exchange-rates",
        SyncExchangeRateHandler,
        name="sync_exchange_rate_data"
    ),
    URLSpec(
        r"/api/dashboard/sync/sales",
        SyncSalesDataHandler,
        name="sync_sales_data"
    ),
    
    # 数据查询相关路由
    URLSpec(
        r"/api/dashboard/summary",
        DashboardSummaryHandler,
        name="dashboard_summary"
    ),
    URLSpec(
        r"/api/dashboard/shops",
        ShopListHandler,
        name="shop_list"
    ),
    URLSpec(
        r"/api/dashboard/statistics/sales",
        SalesStatisticsHandler,
        name="sales_statistics"
    ),
    
    # 工具类路由
    URLSpec(
        r"/api/dashboard/currency/convert",
        CurrencyConversionHandler,
        name="currency_conversion"
    ),
    
    # 健康检查路由
    URLSpec(
        r"/api/dashboard/health",
        HealthCheckHandler,
        name="dashboard_health_check"
    ),
]

# 路由组信息
route_group_info = {
    "name": "电商数据看板",
    "description": "电商数据看板相关API路由",
    "version": "1.0.0",
    "prefix": "/api/dashboard",
    "routes": [
        {
            "path": "/sync/shops",
            "method": "POST",
            "handler": "SyncShopDataHandler",
            "description": "同步店铺数据",
            "parameters": {
                "access_token": "访问令牌"
            },
            "response": "同步结果信息"
        },
        {
            "path": "/sync/exchange-rates",
            "method": "POST",
            "handler": "SyncExchangeRateHandler",
            "description": "同步汇率数据",
            "parameters": {
                "access_token": "访问令牌",
                "target_date": "目标日期（可选）"
            },
            "response": "同步结果信息"
        },
        {
            "path": "/sync/sales",
            "method": "POST",
            "handler": "SyncSalesDataHandler",
            "description": "同步销售数据",
            "parameters": {
                "access_token": "访问令牌",
                "start_date": "开始日期（可选）",
                "end_date": "结束日期（可选）"
            },
            "response": "同步结果信息"
        },
        {
            "path": "/summary",
            "method": "GET",
            "handler": "DashboardSummaryHandler",
            "description": "获取数据看板摘要信息",
            "parameters": {},
            "response": "看板摘要数据"
        },
        {
            "path": "/shops",
            "method": "GET",
            "handler": "ShopListHandler",
            "description": "获取店铺列表",
            "parameters": {
                "page": "页码（可选，默认1）",
                "page_size": "每页数量（可选，默认20）",
                "platform": "平台筛选（可选）"
            },
            "response": "店铺列表数据"
        },
        {
            "path": "/statistics/sales",
            "method": "GET",
            "handler": "SalesStatisticsHandler",
            "description": "获取销售统计数据",
            "parameters": {
                "start_date": "开始日期（可选）",
                "end_date": "结束日期（可选）",
                "shop_id": "店铺ID（可选）",
                "currency": "货币类型（可选，默认CNY）"
            },
            "response": "销售统计数据"
        },
        {
            "path": "/currency/convert",
            "method": "POST",
            "handler": "CurrencyConversionHandler",
            "description": "货币转换",
            "parameters": {
                "amount": "金额",
                "from_currency": "源货币代码",
                "to_currency": "目标货币代码",
                "conversion_date": "转换日期（可选）"
            },
            "response": "货币转换结果"
        },
        {
            "path": "/health",
            "method": "GET",
            "handler": "HealthCheckHandler",
            "description": "健康检查",
            "parameters": {},
            "response": "服务健康状态"
        }
    ]
}

# API文档信息
api_documentation = {
    "title": "电商数据看板API",
    "description": "电商数据看板系统提供的RESTful API接口",
    "version": "1.0.0",
    "base_url": "/api/dashboard",
    "authentication": {
        "type": "Bearer Token",
        "description": "部分接口需要提供访问令牌进行身份验证"
    },
    "response_format": {
        "success": {
            "code": "响应状态码",
            "message": "响应消息",
            "data": "响应数据",
            "timestamp": "响应时间戳"
        },
        "error": {
            "code": "错误状态码",
            "message": "错误消息",
            "details": "错误详情（可选）",
            "timestamp": "错误时间戳"
        }
    },
    "status_codes": {
        "200": "请求成功",
        "400": "请求参数错误",
        "401": "未授权访问",
        "403": "禁止访问",
        "404": "资源不存在",
        "422": "业务逻辑错误",
        "500": "服务器内部错误",
        "503": "服务不可用"
    },
    "examples": {
        "sync_shop_data": {
            "request": {
                "method": "POST",
                "url": "/api/dashboard/sync/shops",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "access_token": "your_access_token_here"
                }
            },
            "response": {
                "code": 200,
                "message": "店铺数据同步成功",
                "data": {
                    "success": True,
                    "synced_count": 5,
                    "total_count": 5,
                    "message": "同步完成"
                },
                "timestamp": "2024-01-15T10:30:00"
            }
        },
        "dashboard_summary": {
            "request": {
                "method": "GET",
                "url": "/api/dashboard/summary"
            },
            "response": {
                "code": 200,
                "message": "获取数据看板摘要成功",
                "data": {
                    "total_shops": 10,
                    "total_sales_today": {
                        "cny": "15000.00",
                        "usd": "2100.00",
                        "order_count": 25
                    },
                    "total_sales_yesterday": {
                        "cny": "12000.00",
                        "usd": "1680.00",
                        "order_count": 20
                    },
                    "exchange_rate_updated": "2024-01-15T08:00:00",
                    "last_sync_time": "2024-01-15T10:00:00"
                },
                "timestamp": "2024-01-15T10:30:00"
            }
        },
        "currency_conversion": {
            "request": {
                "method": "POST",
                "url": "/api/dashboard/currency/convert",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": {
                    "amount": "100.00",
                    "from_currency": "USD",
                    "to_currency": "CNY",
                    "conversion_date": "2024-01-15"
                }
            },
            "response": {
                "code": 200,
                "message": "货币转换成功",
                "data": {
                    "original_amount": "100.00",
                    "original_currency": "USD",
                    "converted_amount": "715.20",
                    "target_currency": "CNY",
                    "exchange_rate": "7.152",
                    "conversion_date": "2024-01-15",
                    "rate_source": "API"
                },
                "timestamp": "2024-01-15T10:30:00"
            }
        }
    }
}

# 导出路由和相关信息
__all__ = [
    'dashboard_routes',
    'route_group_info',
    'api_documentation'
]