# -*- coding: utf-8 -*-
"""
配置管理模块
支持环境变量、多环境配置和配置验证
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class BaseConfig:
    """基础配置类"""
    
    def __init__(self):
        # 加载环境变量
        if load_dotenv:
            env_file = Path(__file__).parent.parent / '.env'
            if env_file.exists():
                load_dotenv(env_file)
        
        # 应用基础配置
        self.APP_NAME = os.getenv('APP_NAME', 'RPA_Tornado')
        self.APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
        self.APP_DEBUG = os.getenv('APP_DEBUG', 'false').lower() == 'true'
        self.APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
        self.APP_PORT = int(os.getenv('APP_PORT', '8888'))
        
        # 领星API配置
        self.LLX_API_HOST = os.getenv('LLX_API_HOST', 'https://openapi.lingxing.com')
        self.LLX_APP_ID = os.getenv('LLX_APP_ID', 'ak_LmR8frklEqfe2')
        self.LLX_APP_SECRET = os.getenv('LLX_APP_SECRET', 'gS/Qn/dLNtD9qKwYaBLkZA==')
        
        # 数据库配置
        self.DATABASE_URL = os.getenv('DATABASE_URL')
        self.REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        
        # 日志配置
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
        self.LOG_MAX_SIZE = os.getenv('LOG_MAX_SIZE', '10MB')
        self.LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
        
        # 安全配置
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
        self.JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
        self.JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES', '30'))
        
        # API限流配置
        self.RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
        self.RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
        
        # 监控配置
        self.MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'true').lower() == 'true'
        self.METRICS_PORT = int(os.getenv('METRICS_PORT', '9090'))
        self.HEALTH_CHECK_ENDPOINT = os.getenv('HEALTH_CHECK_ENDPOINT', '/health')
        
        # 外部服务配置
        self.EXTERNAL_API_TIMEOUT = int(os.getenv('EXTERNAL_API_TIMEOUT', '30'))
        self.EXTERNAL_API_RETRY_COUNT = int(os.getenv('EXTERNAL_API_RETRY_COUNT', '3'))
        self.EXTERNAL_API_RETRY_DELAY = int(os.getenv('EXTERNAL_API_RETRY_DELAY', '1'))
        
        # 文件存储配置
        self.UPLOAD_DIR = os.getenv('UPLOAD_DIR', 'uploads')
        self.MAX_FILE_SIZE = os.getenv('MAX_FILE_SIZE', '10MB')
        self.ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'json,csv,xlsx,txt')
        
        # 缓存配置
        self.CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))
        self.CACHE_MAX_SIZE = int(os.getenv('CACHE_MAX_SIZE', '1000'))
        
        # 开发环境配置
        self.DEV_RELOAD = os.getenv('DEV_RELOAD', 'true').lower() == 'true'
        self.DEV_CORS_ENABLED = os.getenv('DEV_CORS_ENABLED', 'true').lower() == 'true'
        self.DEV_CORS_ORIGINS = os.getenv('DEV_CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000')
    
    @property
    def allowed_extensions_list(self) -> list:
        """获取允许的文件扩展名列表"""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(',')]
    
    @property
    def cors_origins_list(self) -> list:
        """获取CORS允许的源列表"""
        return [origin.strip() for origin in self.DEV_CORS_ORIGINS.split(',')]
    
    def get_database_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        if not self.DATABASE_URL:
            return {}
        
        # 解析数据库URL
        # 格式: postgresql://user:password@host:port/database
        import urllib.parse as urlparse
        parsed = urlparse.urlparse(self.DATABASE_URL)
        
        return {
            'host': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path[1:],  # 移除开头的 '/'
            'username': parsed.username,
            'password': parsed.password,
            'driver': parsed.scheme
        }
    
    def validate_config(self) -> bool:
        """验证配置的有效性"""
        errors = []
        
        # 验证必需的配置
        if not self.LLX_APP_ID:
            errors.append("LLX_APP_ID is required")
        
        if not self.LLX_APP_SECRET:
            errors.append("LLX_APP_SECRET is required")
        
        if not self.SECRET_KEY or self.SECRET_KEY == 'your-secret-key-here':
            errors.append("SECRET_KEY must be set to a secure value")
        
        # 验证端口范围
        if not (1 <= self.APP_PORT <= 65535):
            errors.append(f"APP_PORT must be between 1 and 65535, got {self.APP_PORT}")
        
        if errors:
            print("Configuration validation errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    APP_DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    APP_DEBUG = False
    LOG_LEVEL = 'WARNING'
    DEV_RELOAD = False
    DEV_CORS_ENABLED = False


class TestingConfig(BaseConfig):
    """测试环境配置"""
    APP_DEBUG = True
    LOG_LEVEL = 'DEBUG'
    DATABASE_URL = 'sqlite:///:memory:'


# 配置工厂
def get_config(env: str = None) -> BaseConfig:
    """根据环境获取配置"""
    if env is None:
        env = os.getenv('ENVIRONMENT', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    config = config_class()
    
    # 验证配置
    if not config.validate_config():
        raise ValueError(f"Invalid configuration for environment: {env}")
    
    return config


# 全局配置实例
settings = get_config()

# 向后兼容的Settings类
class Settings:
    """向后兼容的配置类"""
    LLX_API_HOST = settings.LLX_API_HOST
    LLX_APP_ID = settings.LLX_APP_ID
    LLX_APP_SECRET = settings.LLX_APP_SECRET


# 导出
__all__ = [
    'BaseConfig',
    'DevelopmentConfig', 
    'ProductionConfig',
    'TestingConfig',
    'get_config',
    'settings',
    'Settings'  # 向后兼容
]