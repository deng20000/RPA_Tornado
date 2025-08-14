# 多平台领域路由
# 定义多平台模块的URL路由映射

from tornado.web import URLSpec
from typing import List, Dict, Any

from .handlers import (
    PlatformSyncHandler,
    SyncStatusHandler,
    PlatformDataHandler,
    CrossPlatformAnalysisHandler,
    PlatformConfigHandler
)


def get_multi_platform_routes() -> List[URLSpec]:
    """获取多平台模块的路由列表
    
    Returns:
        URLSpec列表
    """
    return [
        # 平台同步相关
        URLSpec(r"/api/multi-platform/sync", PlatformSyncHandler, name="platform_sync"),
        URLSpec(r"/api/multi-platform/sync/status", SyncStatusHandler, name="sync_status"),
        
        # 平台数据相关
        URLSpec(r"/api/multi-platform/data", PlatformDataHandler, name="platform_data"),
        
        # 跨平台分析相关
        URLSpec(r"/api/multi-platform/analysis", CrossPlatformAnalysisHandler, name="cross_platform_analysis"),
        
        # 平台配置相关
        URLSpec(r"/api/multi-platform/config", PlatformConfigHandler, name="platform_config"),
    ]


def get_multi_platform_route_patterns() -> List[str]:
    """获取多平台模块的路由模式列表
    
    Returns:
        路由模式字符串列表
    """
    return [
        r"/api/multi-platform/sync",
        r"/api/multi-platform/sync/status",
        r"/api/multi-platform/data",
        r"/api/multi-platform/analysis",
        r"/api/multi-platform/config",
    ]


def get_multi_platform_api_info() -> Dict[str, Any]:
    """获取多平台模块的API信息
    
    Returns:
        API信息字典
    """
    return {
        "module": "multi_platform",
        "description": "多平台数据管理模块",
        "version": "1.0.0",
        "endpoints": [
            {
                "path": "/api/multi-platform/sync",
                "methods": ["POST"],
                "description": "启动平台数据同步",
                "handler": "PlatformSyncHandler"
            },
            {
                "path": "/api/multi-platform/sync/status",
                "methods": ["GET"],
                "description": "获取同步状态",
                "handler": "SyncStatusHandler"
            },
            {
                "path": "/api/multi-platform/data",
                "methods": ["GET"],
                "description": "获取平台数据",
                "handler": "PlatformDataHandler"
            },
            {
                "path": "/api/multi-platform/analysis",
                "methods": ["GET"],
                "description": "获取跨平台分析数据",
                "handler": "CrossPlatformAnalysisHandler"
            },
            {
                "path": "/api/multi-platform/config",
                "methods": ["GET", "PUT"],
                "description": "平台配置管理",
                "handler": "PlatformConfigHandler"
            }
        ]
    }


# 路由组配置
MULTI_PLATFORM_ROUTE_GROUP = {
    "name": "multi_platform",
    "prefix": "/api/multi-platform",
    "description": "多平台数据管理路由组",
    "routes": get_multi_platform_routes(),
    "middleware": [],  # 可以添加特定的中间件
    "rate_limit": {
        "requests_per_minute": 100,
        "burst_size": 20
    },
    "auth_required": True,
    "permissions": [
        "multi_platform.view",
        "multi_platform.sync",
        "multi_platform.config"
    ]
}


# 导出路由相关信息
__all__ = [
    'get_multi_platform_routes',
    'get_multi_platform_route_patterns',
    'get_multi_platform_api_info',
    'MULTI_PLATFORM_ROUTE_GROUP'
]