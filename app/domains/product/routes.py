# 产品领域路由
# 定义产品模块的URL路由映射

from tornado.web import URLSpec
from typing import List, Dict, Any

from .handlers import (
    ProductListHandler,
    ProductDetailHandler,
    CreateProductHandler,
    UpdateProductHandler,
    DeleteProductHandler,
    ProductInventoryHandler,
    BatchProductHandler
)


def get_product_routes() -> List[URLSpec]:
    """获取产品模块的路由列表
    
    Returns:
        URLSpec列表
    """
    return [
        # 产品列表
        URLSpec(r"/api/products", ProductListHandler, name="product_list"),
        
        # 产品详情
        URLSpec(r"/api/products/detail", ProductDetailHandler, name="product_detail"),
        
        # 创建产品
        URLSpec(r"/api/products/create", CreateProductHandler, name="create_product"),
        
        # 更新产品
        URLSpec(r"/api/products/update", UpdateProductHandler, name="update_product"),
        
        # 删除产品
        URLSpec(r"/api/products/delete", DeleteProductHandler, name="delete_product"),
        
        # 产品库存
        URLSpec(r"/api/products/inventory", ProductInventoryHandler, name="product_inventory"),
        
        # 批量产品操作
        URLSpec(r"/api/products/batch", BatchProductHandler, name="batch_product"),
    ]


def get_product_route_patterns() -> List[str]:
    """获取产品模块的路由模式列表
    
    Returns:
        路由模式字符串列表
    """
    return [
        r"/api/products",
        r"/api/products/detail",
        r"/api/products/create",
        r"/api/products/update",
        r"/api/products/delete",
        r"/api/products/inventory",
        r"/api/products/batch",
    ]


def get_product_api_info() -> Dict[str, Any]:
    """获取产品模块的API信息
    
    Returns:
        API信息字典
    """
    return {
        "module": "product",
        "description": "产品管理模块",
        "version": "1.0.0",
        "endpoints": [
            {
                "path": "/api/products",
                "methods": ["GET"],
                "description": "获取产品列表",
                "handler": "ProductListHandler"
            },
            {
                "path": "/api/products/detail",
                "methods": ["GET"],
                "description": "获取产品详情",
                "handler": "ProductDetailHandler"
            },
            {
                "path": "/api/products/create",
                "methods": ["POST"],
                "description": "创建产品",
                "handler": "CreateProductHandler"
            },
            {
                "path": "/api/products/update",
                "methods": ["PUT"],
                "description": "更新产品",
                "handler": "UpdateProductHandler"
            },
            {
                "path": "/api/products/delete",
                "methods": ["DELETE"],
                "description": "删除产品",
                "handler": "DeleteProductHandler"
            },
            {
                "path": "/api/products/inventory",
                "methods": ["GET"],
                "description": "获取产品库存",
                "handler": "ProductInventoryHandler"
            },
            {
                "path": "/api/products/batch",
                "methods": ["POST"],
                "description": "批量产品操作",
                "handler": "BatchProductHandler"
            }
        ]
    }


# 路由组配置
PRODUCT_ROUTE_GROUP = {
    "name": "product",
    "prefix": "/api/products",
    "description": "产品管理路由组",
    "routes": get_product_routes(),
    "middleware": [],  # 可以添加特定的中间件
    "rate_limit": {
        "requests_per_minute": 200,
        "burst_size": 50
    },
    "auth_required": True,
    "permissions": [
        "product.view",
        "product.create",
        "product.update",
        "product.delete",
        "product.inventory"
    ]
}


# 导出路由相关信息
__all__ = [
    'get_product_routes',
    'get_product_route_patterns',
    'get_product_api_info',
    'PRODUCT_ROUTE_GROUP'
]