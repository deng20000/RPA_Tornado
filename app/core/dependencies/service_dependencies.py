# 服务层依赖注入
# 提供各种服务类的依赖注入函数

from typing import Optional
from app.services.statistics_service import StatisticsService
from app.services.base_data_service import BaseDataService
from app.services.multi_platform_service import MultiPlatformService
from app.services.product_service import ProductService
from app.services.amazon_table_service import AmazonTableService


# 服务实例缓存
_service_cache = {}


def get_statistics_service() -> StatisticsService:
    """获取统计服务实例
    
    Returns:
        StatisticsService: 统计服务实例
    """
    if 'statistics' not in _service_cache:
        _service_cache['statistics'] = StatisticsService()
    return _service_cache['statistics']


def get_base_data_service() -> BaseDataService:
    """获取基础数据服务实例
    
    Returns:
        BaseDataService: 基础数据服务实例
    """
    if 'base_data' not in _service_cache:
        _service_cache['base_data'] = BaseDataService()
    return _service_cache['base_data']


def get_multi_platform_service() -> MultiPlatformService:
    """获取多平台服务实例
    
    Returns:
        MultiPlatformService: 多平台服务实例
    """
    if 'multi_platform' not in _service_cache:
        _service_cache['multi_platform'] = MultiPlatformService()
    return _service_cache['multi_platform']


def get_product_service() -> ProductService:
    """获取产品服务实例
    
    Returns:
        ProductService: 产品服务实例
    """
    if 'product' not in _service_cache:
        _service_cache['product'] = ProductService()
    return _service_cache['product']


def get_amazon_table_service() -> AmazonTableService:
    """获取亚马逊表格服务实例
    
    Returns:
        AmazonTableService: 亚马逊表格服务实例
    """
    if 'amazon_table' not in _service_cache:
        _service_cache['amazon_table'] = AmazonTableService()
    return _service_cache['amazon_table']


def clear_service_cache():
    """清空服务缓存
    
    主要用于测试环境
    """
    global _service_cache
    _service_cache.clear()