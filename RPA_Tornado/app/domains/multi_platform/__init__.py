# 多平台领域模块
# 处理多平台数据同步、跨平台分析和平台配置管理

from .handlers import (
    PlatformSyncHandler,
    SyncStatusHandler,
    PlatformDataHandler,
    CrossPlatformAnalysisHandler,
    PlatformConfigHandler
)
from .services import MultiPlatformService
from .routes import get_multi_platform_routes


class MultiPlatformDomain:
    """多平台领域"""
    
    @staticmethod
    def get_handlers():
        """获取处理器"""
        return {
            'platform_sync': PlatformSyncHandler,
            'sync_status': SyncStatusHandler,
            'platform_data': PlatformDataHandler,
            'cross_platform_analysis': CrossPlatformAnalysisHandler,
            'platform_config': PlatformConfigHandler
        }
    
    @staticmethod
    def get_routes():
        """获取路由"""
        return get_multi_platform_routes()
    
    @staticmethod
    def get_service():
        """获取服务"""
        return MultiPlatformService()


__all__ = [
    'MultiPlatformDomain',
    'PlatformSyncHandler',
    'SyncStatusHandler',
    'PlatformDataHandler',
    'CrossPlatformAnalysisHandler',
    'PlatformConfigHandler',
    'MultiPlatformService',
    'get_multi_platform_routes'
]