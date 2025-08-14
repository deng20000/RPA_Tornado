# -*- coding: utf-8 -*-
"""
电商数据看板领域路由配置
定义电商数据看板相关的API路由
"""

from tornado.web import URLSpec
from .handlers import EcommerceDashboardHandler

# 电商数据看板路由配置
dashboard_routes = [
    # 数据同步相关接口
    URLSpec(
        r"/api/dashboard/sync/shops",
        EcommerceDashboardHandler,
        dict(action="sync_shop_data"),
        name="dashboard_sync_shops"
    ),
    URLSpec(
        r"/api/dashboard/sync/exchange-rates",
        EcommerceDashboardHandler,
        dict(action="sync_exchange_rate_data"),
        name="dashboard_sync_exchange_rates"
    ),
    URLSpec(
        r"/api/dashboard/sync/sales",
        EcommerceDashboardHandler,
        dict(action="sync_sales_data"),
        name="dashboard_sync_sales"
    ),
    
    # 数据查询相关接口
    URLSpec(
        r"/api/dashboard/summary",
        EcommerceDashboardHandler,
        dict(action="get_dashboard_summary"),
        name="dashboard_summary"
    ),
    URLSpec(
        r"/api/dashboard/shops",
        EcommerceDashboardHandler,
        dict(action="get_shop_list"),
        name="dashboard_shops"
    ),
    URLSpec(
        r"/api/dashboard/sales/statistics",
        EcommerceDashboardHandler,
        dict(action="get_sales_statistics"),
        name="dashboard_sales_statistics"
    ),
]

# 导出路由列表
__all__ = ['dashboard_routes']