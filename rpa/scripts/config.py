"""
RPA项目配置文件
管理不同环境的设置和配置
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 环境类型
ENVIRONMENT = os.getenv('RPA_ENV', 'development')

class Config:
    """基础配置类"""
    
    # 项目基本信息
    PROJECT_NAME = "RPA自动化项目"
    VERSION = "1.0.0"
    
    # 目录配置
    DATA_DIR = PROJECT_ROOT / "data"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    LOGS_DIR = PROJECT_ROOT / "logs"
    TEMP_DIR = PROJECT_ROOT / "temp"
    
    # 文件配置
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    SUPPORTED_FORMATS = ['.xlsx', '.xls', '.csv', '.json']
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = LOGS_DIR / "rpa.log"
    
    # 数据处理配置
    CHUNK_SIZE = 1000
    MAX_WORKERS = 4
    
    # 超时配置
    REQUEST_TIMEOUT = 30
    PROCESS_TIMEOUT = 300
    
    # 重试配置
    MAX_RETRIES = 3
    RETRY_DELAY = 1

class DevelopmentConfig(Config):
    """开发环境配置"""
    
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    
    # 开发环境特定配置
    TEST_MODE = True
    MOCK_DATA = True
    
    # 数据库配置（开发环境）
    DATABASE_URL = "sqlite:///dev.db"
    
    # API配置（开发环境）
    API_BASE_URL = "http://localhost:8000"
    API_TIMEOUT = 10

class ProductionConfig(Config):
    """生产环境配置"""
    
    DEBUG = False
    LOG_LEVEL = "WARNING"
    
    # 生产环境特定配置
    TEST_MODE = False
    MOCK_DATA = False
    
    # 数据库配置（生产环境）
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    
    # API配置（生产环境）
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.company.com')
    API_TIMEOUT = 30

class TestingConfig(Config):
    """测试环境配置"""
    
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    
    # 测试环境特定配置
    TEST_MODE = True
    MOCK_DATA = True
    
    # 测试数据库
    DATABASE_URL = "sqlite:///test.db"
    
    # 测试API
    API_BASE_URL = "http://test-api.company.com"
    API_TIMEOUT = 5

# 配置映射
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}

def get_config() -> Config:
    """获取当前环境配置"""
    config_class = config_map.get(ENVIRONMENT, DevelopmentConfig)
    return config_class()

def create_directories():
    """创建必要的目录"""
    config = get_config()
    
    directories = [
        config.DATA_DIR,
        config.OUTPUT_DIR,
        config.LOGS_DIR,
        config.TEMP_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"📁 创建目录: {directory}")

def get_file_path(file_type: str, filename: str) -> Path:
    """获取文件路径"""
    config = get_config()
    
    path_map = {
        'data': config.DATA_DIR,
        'output': config.OUTPUT_DIR,
        'logs': config.LOGS_DIR,
        'temp': config.TEMP_DIR,
    }
    
    base_path = path_map.get(file_type, config.DATA_DIR)
    return base_path / filename

def validate_config():
    """验证配置"""
    config = get_config()
    
    # 检查必要目录
    required_dirs = [
        config.DATA_DIR,
        config.OUTPUT_DIR,
        config.LOGS_DIR,
        config.TEMP_DIR,
    ]
    
    for directory in required_dirs:
        if not directory.exists():
            print(f"⚠️  目录不存在: {directory}")
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ 已创建目录: {directory}")
    
    print(f"✅ 配置验证完成 - 环境: {ENVIRONMENT}")

# 全局配置实例
config = get_config()

if __name__ == "__main__":
    # 测试配置
    print(f"当前环境: {ENVIRONMENT}")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"数据目录: {config.DATA_DIR}")
    print(f"输出目录: {config.OUTPUT_DIR}")
    print(f"日志目录: {config.LOGS_DIR}")
    print(f"临时目录: {config.TEMP_DIR}")
    
    # 创建目录
    create_directories()
    
    # 验证配置
    validate_config() 