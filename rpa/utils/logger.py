"""
日志工具模块
提供统一的日志记录功能
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from config import get_config

def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[Path] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
        format_string: 日志格式字符串
    
    Returns:
        配置好的日志记录器
    """
    config = get_config()
    
    # 获取配置
    level = level or config.LOG_LEVEL
    log_file = log_file or config.LOG_FILE
    format_string = format_string or config.LOG_FORMAT
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(format_string)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        # 确保日志目录存在
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        日志记录器实例
    """
    return logging.getLogger(name)

class LoggerMixin:
    """日志记录器混入类"""
    
    @property
    def logger(self) -> logging.Logger:
        """获取日志记录器"""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger

def log_function_call(func):
    """函数调用日志装饰器"""
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        logger.debug(f"调用函数: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"函数 {func.__name__} 执行成功")
            return result
        except Exception as e:
            logger.error(f"函数 {func.__name__} 执行失败: {e}")
            raise
    return wrapper

def log_execution_time(func):
    """执行时间日志装饰器"""
    import time
    
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()
        logger.debug(f"开始执行: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"函数 {func.__name__} 执行完成，耗时: {execution_time:.2f}秒")
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            logger.error(f"函数 {func.__name__} 执行失败，耗时: {execution_time:.2f}秒，错误: {e}")
            raise
    
    return wrapper

# 默认日志记录器
default_logger = setup_logger('rpa')

if __name__ == "__main__":
    # 测试日志功能
    logger = setup_logger('test')
    
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    
    # 测试装饰器
    @log_function_call
    @log_execution_time
    def test_function():
        import time
        time.sleep(1)
        return "测试完成"
    
    result = test_function()
    print(f"结果: {result}") 