#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化模块
实现自动建表功能（触发式，非脚本式）

功能：
1. 检查数据库连接
2. 自动创建表结构（如果不存在）
3. 验证表结构完整性
4. 提供数据库状态检查

作者：AI Assistant
创建时间：2025-08-13
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import logging
from typing import Optional, Dict, Any, List

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入项目模块
try:
    from templates.manage_data import (
        DatabaseManager, 
        Shop, 
        Sale, 
        ExchangeRate, 
        Base,
        get_db_engine,
        test_db_connection
    )
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('db_init.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class DatabaseInitializer:
    """
    数据库初始化器
    负责自动创建和维护数据库表结构
    """
    
    def __init__(self):
        """初始化数据库初始化器"""
        self.db_manager = None
        self.engine = None
        
    def check_database_connection(self) -> bool:
        """
        检查数据库连接
        
        Returns:
            bool: 连接是否成功
        """
        logger.info("🔍 检查数据库连接...")
        try:
            if test_db_connection():
                logger.info("✅ 数据库连接成功")
                return True
            else:
                logger.error("❌ 数据库连接失败")
                return False
        except Exception as e:
            logger.error(f"❌ 数据库连接检查出错: {str(e)}")
            return False
    
    def initialize_database_manager(self) -> bool:
        """
        初始化数据库管理器
        
        Returns:
            bool: 初始化是否成功
        """
        try:
            logger.info("🔧 初始化数据库管理器...")
            self.db_manager = DatabaseManager()
            self.engine = get_db_engine()
            logger.info("✅ 数据库管理器初始化成功")
            return True
        except Exception as e:
            logger.error(f"❌ 数据库管理器初始化失败: {str(e)}")
            return False
    
    def check_table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在
        
        Args:
            table_name: 表名
            
        Returns:
            bool: 表是否存在
        """
        try:
            from sqlalchemy import inspect
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            exists = table_name in tables
            logger.info(f"📋 表 '{table_name}' {'存在' if exists else '不存在'}")
            return exists
        except Exception as e:
            logger.error(f"❌ 检查表 '{table_name}' 时出错: {str(e)}")
            return False
    
    def get_table_status(self) -> Dict[str, bool]:
        """
        获取所有表的状态
        
        Returns:
            Dict[str, bool]: 表名和存在状态的映射
        """
        tables = {
            'shops': False,
            'sales': False,
            'exchange_rate': False
        }
        
        for table_name in tables.keys():
            tables[table_name] = self.check_table_exists(table_name)
        
        return tables
    
    def create_tables_if_not_exists(self) -> bool:
        """
        如果表不存在则创建表
        
        Returns:
            bool: 创建是否成功
        """
        logger.info("🏗️ 开始检查并创建数据库表...")
        
        try:
            # 获取当前表状态
            table_status = self.get_table_status()
            missing_tables = [name for name, exists in table_status.items() if not exists]
            
            if not missing_tables:
                logger.info("✅ 所有表都已存在，无需创建")
                return True
            
            logger.info(f"📝 需要创建的表: {missing_tables}")
            
            # 使用DatabaseManager的init_db方法创建表
            success = self.db_manager.init_db()
            
            if success:
                logger.info("✅ 数据库表创建成功")
                
                # 验证表是否创建成功
                new_table_status = self.get_table_status()
                all_created = all(new_table_status.values())
                
                if all_created:
                    logger.info("🎉 所有表创建并验证成功")
                    return True
                else:
                    missing_after_create = [name for name, exists in new_table_status.items() if not exists]
                    logger.error(f"❌ 以下表创建失败: {missing_after_create}")
                    return False
            else:
                logger.error("❌ 数据库表创建失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ 创建数据库表时出错: {str(e)}")
            return False
    
    def validate_table_structure(self) -> bool:
        """
        验证表结构完整性
        
        Returns:
            bool: 验证是否通过
        """
        logger.info("🔍 验证表结构完整性...")
        
        try:
            from sqlalchemy import inspect
            inspector = inspect(self.engine)
            
            # 定义期望的表结构
            expected_tables = {
                'shops': ['shop_id', 'platform_id', 'shop_name', 'platform', 'created_at', 'updated_at'],
                'sales': ['id', 'shop_id', 'sale_date', 'cny_amount', 'usd_amount', 'entry_time'],
                'exchange_rate': ['id', 'currency_code', 'rate', 'date', 'created_at']
            }
            
            validation_results = {}
            
            for table_name, expected_columns in expected_tables.items():
                try:
                    # 获取实际列名
                    actual_columns = [col['name'] for col in inspector.get_columns(table_name)]
                    
                    # 检查必要列是否存在
                    missing_columns = [col for col in expected_columns if col not in actual_columns]
                    
                    if missing_columns:
                        logger.warning(f"⚠️ 表 '{table_name}' 缺少列: {missing_columns}")
                        validation_results[table_name] = False
                    else:
                        logger.info(f"✅ 表 '{table_name}' 结构验证通过")
                        validation_results[table_name] = True
                        
                except Exception as e:
                    logger.error(f"❌ 验证表 '{table_name}' 结构时出错: {str(e)}")
                    validation_results[table_name] = False
            
            # 检查整体验证结果
            all_valid = all(validation_results.values())
            
            if all_valid:
                logger.info("🎉 所有表结构验证通过")
            else:
                failed_tables = [name for name, valid in validation_results.items() if not valid]
                logger.error(f"❌ 以下表结构验证失败: {failed_tables}")
            
            return all_valid
            
        except Exception as e:
            logger.error(f"❌ 验证表结构时出错: {str(e)}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        获取数据库信息
        
        Returns:
            Dict[str, Any]: 数据库信息
        """
        info = {
            'connection_status': False,
            'tables': {},
            'total_records': {},
            'last_check_time': datetime.now().isoformat()
        }
        
        try:
            # 检查连接状态
            info['connection_status'] = self.check_database_connection()
            
            if info['connection_status']:
                # 获取表状态
                info['tables'] = self.get_table_status()
                
                # 获取记录数量
                if self.db_manager:
                    session = self.db_manager.Session()
                    try:
                        info['total_records'] = {
                            'shops': session.query(Shop).count() if info['tables'].get('shops') else 0,
                            'sales': session.query(Sale).count() if info['tables'].get('sales') else 0,
                            'exchange_rate': session.query(ExchangeRate).count() if info['tables'].get('exchange_rate') else 0
                        }
                    finally:
                        session.close()
                        
        except Exception as e:
            logger.error(f"❌ 获取数据库信息时出错: {str(e)}")
        
        return info
    
    def auto_initialize(self) -> bool:
        """
        自动初始化数据库（触发式）
        
        Returns:
            bool: 初始化是否成功
        """
        logger.info("🚀 开始自动数据库初始化流程...")
        
        try:
            # 步骤1: 检查数据库连接
            if not self.check_database_connection():
                logger.error("❌ 数据库连接失败，无法继续初始化")
                return False
            
            # 步骤2: 初始化数据库管理器
            if not self.initialize_database_manager():
                logger.error("❌ 数据库管理器初始化失败")
                return False
            
            # 步骤3: 检查并创建表
            if not self.create_tables_if_not_exists():
                logger.error("❌ 数据库表创建失败")
                return False
            
            # 步骤4: 验证表结构
            if not self.validate_table_structure():
                logger.warning("⚠️ 表结构验证未完全通过，但可以继续使用")
            
            # 步骤5: 输出数据库信息
            db_info = self.get_database_info()
            logger.info(f"📊 数据库状态: {db_info}")
            
            logger.info("🎉 数据库自动初始化完成")
            return True
            
        except Exception as e:
            logger.error(f"❌ 自动初始化过程中出错: {str(e)}")
            return False

def ensure_database_ready() -> bool:
    """
    确保数据库准备就绪（触发式函数）
    
    这是一个触发式函数，可以在应用启动时调用，
    自动检查并初始化数据库结构。
    
    Returns:
        bool: 数据库是否准备就绪
    """
    initializer = DatabaseInitializer()
    return initializer.auto_initialize()

def main():
    """
    主函数 - 用于直接运行此脚本进行数据库初始化
    """
    print("=" * 60)
    print("🗄️  电商数据看板 - 数据库初始化工具")
    print("=" * 60)
    
    # 执行自动初始化
    success = ensure_database_ready()
    
    if success:
        print("\n✅ 数据库初始化成功！")
        print("📋 数据库已准备就绪，可以开始使用电商数据看板功能。")
    else:
        print("\n❌ 数据库初始化失败！")
        print("🔧 请检查数据库连接配置和权限设置。")
        sys.exit(1)

if __name__ == "__main__":
    main()