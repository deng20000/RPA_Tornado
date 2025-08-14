#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨月份数据同步功能使用示例
展示如何使用改进的数据同步逻辑
"""

import sys
import os
from datetime import date, timedelta
from manage_data import DatabaseManager, GetData
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('cross_month_usage.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def example_default_sync():
    """示例1: 默认同步（昨天数据）"""
    logger.info("=" * 60)
    logger.info("📅 示例1: 默认同步（昨天数据）")
    logger.info("=" * 60)
    
    db_manager = DatabaseManager()
    
    try:
        # 不传入任何参数，默认同步昨天的数据
        success = GetData.sync_sales_data_with_improved_logic(db_manager)
        
        if success:
            logger.info("✅ 默认同步成功 - 昨天的数据已更新")
        else:
            logger.error("❌ 默认同步失败")
            
    except Exception as e:
        logger.error(f"默认同步异常: {str(e)}")

def example_single_month_sync():
    """示例2: 单月数据同步"""
    logger.info("\n" + "=" * 60)
    logger.info("📊 示例2: 单月数据同步（2025年8月）")
    logger.info("=" * 60)
    
    db_manager = DatabaseManager()
    
    try:
        # 同步2025年8月的数据
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 31)
        
        logger.info(f"同步时间范围: {start_date} 到 {end_date}")
        
        success = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
        
        if success:
            logger.info("✅ 单月同步成功 - 2025年8月数据已更新")
        else:
            logger.error("❌ 单月同步失败")
            
    except Exception as e:
        logger.error(f"单月同步异常: {str(e)}")

def example_cross_month_sync():
    """示例3: 跨月份数据同步"""
    logger.info("\n" + "=" * 60)
    logger.info("🌐 示例3: 跨月份数据同步（2025年6月-8月）")
    logger.info("=" * 60)
    
    db_manager = DatabaseManager()
    
    try:
        # 同步2025年6月到8月的数据
        start_date = date(2025, 6, 1)
        end_date = date(2025, 8, 5)
        
        logger.info(f"同步时间范围: {start_date} 到 {end_date}")
        
        # 先检查需要哪些月份的数据
        required_months = GetData.get_required_months(start_date, end_date)
        logger.info(f"需要的月份: {required_months}")
        
        # 检查缺失的汇率数据
        missing_months = GetData.check_missing_exchange_rates(db_manager, required_months)
        if missing_months:
            logger.info(f"缺失的汇率月份: {missing_months}")
            logger.info("系统将自动获取并更新缺失的汇率数据")
        else:
            logger.info("所有需要的汇率数据都已存在")
        
        success = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
        
        if success:
            logger.info("✅ 跨月份同步成功 - 2025年6-8月数据已更新")
        else:
            logger.error("❌ 跨月份同步失败")
            
    except Exception as e:
        logger.error(f"跨月份同步异常: {str(e)}")

def example_recent_days_sync():
    """示例4: 最近几天数据同步"""
    logger.info("\n" + "=" * 60)
    logger.info("📈 示例4: 最近几天数据同步")
    logger.info("=" * 60)
    
    db_manager = DatabaseManager()
    
    try:
        # 同步最近7天的数据
        end_date = date.today() - timedelta(days=1)  # 昨天
        start_date = end_date - timedelta(days=6)    # 7天前
        
        logger.info(f"同步时间范围: {start_date} 到 {end_date}")
        
        success = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
        
        if success:
            logger.info("✅ 最近几天同步成功")
        else:
            logger.error("❌ 最近几天同步失败")
            
    except Exception as e:
        logger.error(f"最近几天同步异常: {str(e)}")

def example_specific_date_sync():
    """示例5: 特定日期数据同步"""
    logger.info("\n" + "=" * 60)
    logger.info("🎯 示例5: 特定日期数据同步")
    logger.info("=" * 60)
    
    db_manager = DatabaseManager()
    
    try:
        # 同步特定日期的数据
        target_date = date(2025, 8, 5)
        
        logger.info(f"同步特定日期: {target_date}")
        
        success = GetData.sync_sales_data_with_improved_logic(db_manager, target_date, target_date)
        
        if success:
            logger.info(f"✅ 特定日期同步成功 - {target_date} 数据已更新")
        else:
            logger.error(f"❌ 特定日期同步失败")
            
    except Exception as e:
        logger.error(f"特定日期同步异常: {str(e)}")

def show_usage_summary():
    """显示使用总结"""
    logger.info("\n" + "=" * 80)
    logger.info("📚 跨月份数据同步功能使用总结")
    logger.info("=" * 80)
    
    usage_info = """
🔧 核心方法: GetData.sync_sales_data_with_improved_logic()

📋 参数说明:
   - db_manager: DatabaseManager实例（必需）
   - start_date: 开始日期（可选，默认为昨天）
   - end_date: 结束日期（可选，默认为昨天）

💡 使用场景:
   1. 默认同步: sync_sales_data_with_improved_logic(db_manager)
   2. 单日同步: sync_sales_data_with_improved_logic(db_manager, date, date)
   3. 时间范围: sync_sales_data_with_improved_logic(db_manager, start_date, end_date)

🚀 功能特点:
   ✅ 自动检测需要的月份
   ✅ 自动检查和更新缺失的汇率数据
   ✅ 支持跨月份数据同步
   ✅ 支持单日、多日、跨月等各种时间范围
   ✅ 智能处理默认参数（昨天数据）
   ✅ 完整的错误处理和日志记录

⚠️ 注意事项:
   - 确保数据库连接正常
   - 汇率数据会自动获取和更新
   - 销售数据会根据现有记录进行更新或创建
   - 建议在非高峰时段进行大范围数据同步
    """
    
    logger.info(usage_info)

def main():
    """主函数 - 运行所有示例"""
    try:
        logger.info("🎬 开始跨月份数据同步功能使用示例")
        
        # 示例1: 默认同步
        # example_default_sync()
        
        # 示例2: 单月同步
        # example_single_month_sync()
        
        # 示例3: 跨月份同步（注释掉，因为可能需要很长时间）
        example_cross_month_sync()
        
        # 示例4: 最近几天同步
        # example_recent_days_sync()
        
        # 示例5: 特定日期同步
        # example_specific_date_sync()
        
        # 显示使用总结
        show_usage_summary()
        
        logger.info("\n" + "=" * 80)
        logger.info("🎉 所有使用示例演示完成")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"示例演示过程中出现错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()