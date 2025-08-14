#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库表结构修复脚本
用于检查和修复 sales 表的主键设置问题
"""

import logging
from sqlalchemy import create_engine, text, inspect
from manage_data import DatabaseManager, Sale, Base

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)

def check_table_structure():
    """检查当前表结构"""
    try:
        db_manager = DatabaseManager()
        inspector = inspect(db_manager.engine)
        
        # 检查 sales 表结构
        if 'sales' in inspector.get_table_names():
            columns = inspector.get_columns('sales')
            pk_constraint = inspector.get_pk_constraint('sales')
            
            logger.info("当前 sales 表结构:")
            for col in columns:
                logger.info(f"  {col['name']}: {col['type']} (nullable: {col['nullable']})")
            
            logger.info(f"主键约束: {pk_constraint}")
            
            # 检查是否有问题
            pk_columns = pk_constraint.get('constrained_columns', [])
            if 'sale_date' in pk_columns:
                logger.error("发现问题: sale_date 被设置为主键，需要修复")
                return False
            else:
                logger.info("表结构正常")
                return True
        else:
            logger.info("sales 表不存在")
            return False
            
    except Exception as e:
        logger.error(f"检查表结构失败: {str(e)}")
        return False

def fix_table_structure():
    """修复表结构"""
    try:
        db_manager = DatabaseManager()
        
        with db_manager.engine.connect() as conn:
            # 开始事务
            trans = conn.begin()
            try:
                logger.info("开始修复 sales 表结构...")
                
                # 1. 删除现有的主键约束
                logger.info("删除现有主键约束...")
                conn.execute(text("ALTER TABLE sales DROP CONSTRAINT IF EXISTS sales_pkey"))
                
                # 2. 创建序列（如果不存在）
                logger.info("创建序列...")
                conn.execute(text("CREATE SEQUENCE IF NOT EXISTS sales_sale_id_seq OWNED BY sales.sale_id"))
                
                # 3. 设置序列的当前值
                logger.info("设置序列当前值...")
                result = conn.execute(text("SELECT COALESCE(MAX(sale_id), 0) + 1 FROM sales"))
                next_val = result.scalar()
                conn.execute(text(f"SELECT setval('sales_sale_id_seq', {next_val})"))
                
                # 4. 修改 sale_id 列为自增主键
                logger.info("修改 sale_id 列...")
                conn.execute(text("ALTER TABLE sales ALTER COLUMN sale_id SET DEFAULT nextval('sales_sale_id_seq')"))
                
                # 5. 添加新的主键约束
                logger.info("添加新的主键约束...")
                conn.execute(text("ALTER TABLE sales ADD PRIMARY KEY (sale_id)"))
                
                # 6. 确保 sale_date 不为空但不是主键
                logger.info("修改 sale_date 列...")
                conn.execute(text("ALTER TABLE sales ALTER COLUMN sale_date SET NOT NULL"))
                
                # 提交事务
                trans.commit()
                logger.info("表结构修复完成")
                return True
                
            except Exception as e:
                trans.rollback()
                logger.error(f"修复表结构失败: {str(e)}")
                return False
                
    except Exception as e:
        logger.error(f"连接数据库失败: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("开始检查数据库表结构...")
    
    # 检查表结构
    if check_table_structure():
        logger.info("表结构正常，无需修复")
        return
    
    # 修复表结构
    logger.info("开始修复表结构...")
    if fix_table_structure():
        logger.info("表结构修复成功")
        
        # 再次检查
        logger.info("验证修复结果...")
        if check_table_structure():
            logger.info("表结构修复验证成功")
        else:
            logger.error("表结构修复验证失败")
    else:
        logger.error("表结构修复失败")

if __name__ == "__main__":
    main()