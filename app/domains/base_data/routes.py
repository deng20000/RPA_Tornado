# 基础数据领域路由配置
# 定义基础数据相关的URL路由映射

from typing import List, Tuple
from tornado.web import URLSpec

from .handlers import (
    SellerInfoHandler,
    MarketplaceListHandler,
    CategoryListHandler,
    CurrencyRateHandler,
    SettingsHandler
)


def get_base_data_routes() -> List[URLSpec]:
    """获取基础数据模块的路由配置
    
    Returns:
        路由配置列表
    """
    return [
        # 店铺信息路由
        URLSpec(
            r"/api/base-data/seller-info",
            SellerInfoHandler,
            name="seller_info"
        ),
        
        # 市场列表路由
        URLSpec(
            r"/api/base-data/marketplace-list",
            MarketplaceListHandler,
            name="marketplace_list"
        ),
        
        # 分类列表路由
        URLSpec(
            r"/api/base-data/category-list",
            CategoryListHandler,
            name="category_list"
        ),
        
        # 汇率路由
        URLSpec(
            r"/api/base-data/currency-rate",
            CurrencyRateHandler,
            name="currency_rate"
        ),
        
        # 设置路由
        URLSpec(
            r"/api/base-data/settings",
            SettingsHandler,
            name="settings"
        ),
    ]


def get_base_data_route_patterns() -> List[Tuple[str, str]]:
    """获取基础数据模块的路由模式
    
    Returns:
        路由模式列表，格式为 (pattern, name)
    """
    return [
        (r"/api/base-data/seller-info", "seller_info"),
        (r"/api/base-data/marketplace-list", "marketplace_list"),
        (r"/api/base-data/category-list", "category_list"),
        (r"/api/base-data/currency-rate", "currency_rate"),
        (r"/api/base-data/settings", "settings"),
    ]


def get_base_data_api_info() -> dict:
    """获取基础数据模块的API信息
    
    Returns:
        API信息字典
    """
    return {
        "module": "base_data",
        "version": "1.0.0",
        "description": "基础数据相关API",
        "endpoints": [
            {
                "path": "/api/base-data/seller-info",
                "method": ["GET", "POST"],
                "description": "获取店铺信息",
                "parameters": {
                    "sid": "店铺ID（必填）",
                    "include_details": "是否包含详细信息（可选，默认false）"
                }
            },
            {
                "path": "/api/base-data/marketplace-list",
                "method": ["GET", "POST"],
                "description": "获取市场列表",
                "parameters": {
                    "country_code": "国家代码（可选）",
                    "active_only": "是否只返回活跃市场（可选，默认true）"
                }
            },
            {
                "path": "/api/base-data/category-list",
                "method": ["GET", "POST"],
                "description": "获取分类列表",
                "parameters": {
                    "marketplace": "市场（可选）",
                    "parent_category": "父分类（可选）",
                    "level": "分类级别（可选，1-5）"
                }
            },
            {
                "path": "/api/base-data/currency-rate",
                "method": ["GET", "POST"],
                "description": "获取汇率信息",
                "parameters": {
                    "from_currency": "源货币（可选）",
                    "to_currency": "目标货币（可选）",
                    "date": "日期（可选，格式YYYY-MM-DD）"
                }
            },
            {
                "path": "/api/base-data/settings",
                "method": ["GET", "POST", "PUT"],
                "description": "获取或更新系统设置",
                "parameters": {
                    "category": "设置分类（可选）",
                    "key": "设置键（可选）",
                    "value": "设置值（PUT时必填）",
                    "description": "设置描述（PUT时可选）"
                }
            }
        ]
    }


# 路由组配置
BASE_DATA_ROUTE_GROUP = {
    "prefix": "/api/base-data",
    "handlers": [
        (r"/seller-info", SellerInfoHandler),
        (r"/marketplace-list", MarketplaceListHandler),
        (r"/category-list", CategoryListHandler),
        (r"/currency-rate", CurrencyRateHandler),
        (r"/settings", SettingsHandler),
    ],
    "middleware": [],  # 可以添加中间件
    "description": "基础数据相关API路由组"
}