# -*- coding: utf-8 -*-
"""
数据库连接管理模块
提供数据库会话管理和连接池功能
"""

import logging
import os
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

# 配置日志记录器
logger = logging.getLogger(__name__)

# 数据库引擎和会话工厂
engine = None
SessionLocal = None


def init_database(database_url: str = None):
    """
    初始化数据库连接
    
    Args:
        database_url: 数据库连接URL，如果为None则从环境变量读取
    """
    if database_url is None:
        # 从环境变量读取数据库配置
        database_url = os.getenv('DATABASE_URL', 'sqlite:///./data/dashboard.db')
    global engine, SessionLocal
    
    try:
        # 创建数据库引擎
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            echo=False  # 设置为True可以看到SQL语句
        )
        
        # 创建会话工厂
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        
        logger.info(f"数据库连接初始化成功: {database_url}")
        
    except Exception as e:
        logger.error(f"数据库连接初始化失败: {str(e)}")
        raise


def create_tables():
    """
    创建数据库表
    """
    try:
        from ..models.dashboard_models import Base
        
        if engine is None:
            raise RuntimeError("数据库引擎未初始化，请先调用 init_database()")
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        
    except Exception as e:
        logger.error(f"数据库表创建失败: {str(e)}")
        raise


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    获取数据库会话的上下文管理器
    
    Yields:
        Session: SQLAlchemy会话对象
    """
    if SessionLocal is None:
        raise RuntimeError("数据库会话工厂未初始化，请先调用 init_database()")
    
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"数据库操作失败: {str(e)}")
        raise
    finally:
        session.close()


def get_db() -> Session:
    """
    获取数据库会话（用于依赖注入）
    
    Returns:
        Session: SQLAlchemy会话对象
    """
    if SessionLocal is None:
        raise RuntimeError("数据库会话工厂未初始化，请先调用 init_database()")
    
    return SessionLocal()


def close_database():
    """
    关闭数据库连接
    """
    global engine
    
    if engine:
        engine.dispose()
        logger.info("数据库连接已关闭")


# 数据库健康检查
def check_database_health() -> bool:
    """
    检查数据库连接健康状态
    
    Returns:
        bool: 数据库是否健康
    """
    try:
        if engine is None:
            return False
        
        # 尝试执行简单查询
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return True
        
    except Exception as e:
        logger.error(f"数据库健康检查失败: {str(e)}")
        return False