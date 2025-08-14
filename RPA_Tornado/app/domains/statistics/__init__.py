# 统计领域模块
# 包含销量报表、利润分析、产品表现等统计相关功能

from .handlers import (
    SalesReportHandler,
    OrderProfitHandler,
    ProductPerformanceHandler,
    ProfitStatisticsHandler,
    ShipmentRemovalHandler
)
from .services import StatisticsService
from .routes import get_statistics_routes


class StatisticsDomain:
    """统计领域"""
    
    @staticmethod
    def get_handlers():
        """获取处理器列表"""
        return [
            SalesReportHandler,
            OrderProfitHandler,
            ProductPerformanceHandler,
            ProfitStatisticsHandler,
            ShipmentRemovalHandler
        ]
    
    @staticmethod
    def get_routes():
        """获取路由列表"""
        return get_statistics_routes()
    
    @staticmethod
    def get_service():
        """获取服务实例"""
        return StatisticsService()


__all__ = [
    'StatisticsDomain',
    'SalesReportHandler',
    'OrderProfitHandler',
    'ProductPerformanceHandler',
    'ProfitStatisticsHandler',
    'ShipmentRemovalHandler',
    'StatisticsService',
    'get_statistics_routes'
]