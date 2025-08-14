# 领域模块
# 定义各个业务领域的模块结构

from .statistics import StatisticsDomain
from .base_data import BaseDataDomain
from .multi_platform import MultiPlatformDomain
from .product import ProductDomain


class DomainRegistry:
    """领域注册表"""
    
    @staticmethod
    def get_all_domains():
        """获取所有领域"""
        return {
            'statistics': StatisticsDomain,
            'base_data': BaseDataDomain,
            'multi_platform': MultiPlatformDomain,
            'product': ProductDomain
        }
    
    @staticmethod
    def get_all_routes():
        """获取所有路由"""
        routes = []
        domains = DomainRegistry.get_all_domains()
        
        for domain_name, domain_class in domains.items():
            domain_routes = domain_class.get_routes()
            routes.extend(domain_routes)
        
        return routes
    
    @staticmethod
    def get_all_handlers():
        """获取所有处理器"""
        handlers = {}
        domains = DomainRegistry.get_all_domains()
        
        for domain_name, domain_class in domains.items():
            domain_handlers = domain_class.get_handlers()
            handlers[domain_name] = domain_handlers
        
        return handlers
    
    @staticmethod
    def get_all_services():
        """获取所有服务"""
        services = {}
        domains = DomainRegistry.get_all_domains()
        
        for domain_name, domain_class in domains.items():
            domain_services = domain_class.get_services()
            services[domain_name] = domain_services
        
        return services


# 导出所有领域
__all__ = [
    'StatisticsDomain',
    'BaseDataDomain', 
    'MultiPlatformDomain',
    'ProductDomain',
    'DomainRegistry'
]