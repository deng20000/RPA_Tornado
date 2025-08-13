# -*- coding: utf-8 -*-
"""
电商数据看板领域模块

该模块提供电商数据看板相关的业务逻辑处理，包括：
- 店铺数据管理
- 销售数据统计
- 汇率数据管理
- 数据同步和转换
"""

__version__ = "1.0.0"
__author__ = "RPA_Tornado Team"

# 导出主要组件
from .services import EcommerceDashboardService
from .handlers import EcommerceDashboardHandler
from .routes import dashboard_routes

__all__ = [
    'EcommerceDashboardService',
    'EcommerceDashboardHandler', 
    'dashboard_routes'
]