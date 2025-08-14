# 产品领域模块
# 定义产品相关的处理器、服务和路由

from .handlers import (
    ProductListHandler,
    ProductDetailHandler,
    CreateProductHandler,
    UpdateProductHandler,
    DeleteProductHandler,
    ProductInventoryHandler,
    BatchProductHandler
)
from .services import ProductService
from .routes import get_product_routes


class ProductDomain:
    """产品领域类"""
    
    @staticmethod
    def get_handlers():
        """获取所有处理器"""
        return {
            'ProductListHandler': ProductListHandler,
            'ProductDetailHandler': ProductDetailHandler,
            'CreateProductHandler': CreateProductHandler,
            'UpdateProductHandler': UpdateProductHandler,
            'DeleteProductHandler': DeleteProductHandler,
            'ProductInventoryHandler': ProductInventoryHandler,
            'BatchProductHandler': BatchProductHandler
        }
    
    @staticmethod
    def get_routes():
        """获取路由配置"""
        return get_product_routes()
    
    @staticmethod
    def get_services():
        """获取服务实例"""
        return {
            'ProductService': ProductService()
        }


# 导出主要组件
__all__ = [
    # 处理器
    'ProductListHandler',
    'ProductDetailHandler', 
    'CreateProductHandler',
    'UpdateProductHandler',
    'DeleteProductHandler',
    'ProductInventoryHandler',
    'BatchProductHandler',
    
    # 服务
    'ProductService',
    
    # 路由
    'get_product_routes',
    
    # 领域类
    'ProductDomain'
]