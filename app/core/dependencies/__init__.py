# 依赖注入模块
# 管理应用程序的依赖关系，提供统一的依赖注入机制

from .auth_dependencies import get_access_token, verify_token
from .service_dependencies import get_statistics_service, get_base_data_service

__all__ = [
    'get_access_token',
    'verify_token',
    'get_statistics_service',
    'get_base_data_service'
]