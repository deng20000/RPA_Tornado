# 基础数据领域模块
# 处理店铺信息、市场列表、分类列表、汇率和设置等基础数据

from .handlers import (
    SellerInfoHandler,
    MarketplaceListHandler,
    CategoryListHandler,
    CurrencyRateHandler,
    SettingsHandler
)
from .services import BaseDataService
from .routes import get_base_data_routes


class BaseDataDomain:
    """基础数据领域"""
    
    @staticmethod
    def get_handlers():
        """获取处理器"""
        return {
            'seller_info': SellerInfoHandler,
            'marketplace_list': MarketplaceListHandler,
            'category_list': CategoryListHandler,
            'currency_rate': CurrencyRateHandler,
            'settings': SettingsHandler
        }
    
    @staticmethod
    def get_routes():
        """获取路由"""
        return get_base_data_routes()
    
    @staticmethod
    def get_service():
        """获取服务"""
        return BaseDataService()


__all__ = [
    'BaseDataDomain',
    'SellerInfoHandler',
    'MarketplaceListHandler',
    'CategoryListHandler',
    'CurrencyRateHandler',
    'SettingsHandler',
    'BaseDataService',
    'get_base_data_routes'
]