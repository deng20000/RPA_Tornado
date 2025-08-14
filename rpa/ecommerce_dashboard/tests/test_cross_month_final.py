#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨月份数据同步最终测试脚本
测试改进的跨月份数据同步逻辑
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
        logging.FileHandler('test_cross_month_final.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def test_month_range_detection():
    """测试月份范围检测功能"""
    logger.info("=" * 60)
    logger.info("🧪 测试月份范围检测功能")
    logger.info("=" * 60)
    
    try:
        # 测试用例1: 单月
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 31)
        months = GetData.get_required_months(start_date, end_date)
        logger.info(f"单月测试 ({start_date} 到 {end_date}): {months}")
        
        # 测试用例2: 跨月
        start_date = date(2025, 6, 15)
        end_date = date(2025, 8, 15)
        months = GetData.get_required_months(start_date, end_date)
        logger.info(f"跨月测试 ({start_date} 到 {end_date}): {months}")
        
        # 测试用例3: 跨年
        start_date = date(2024, 12, 15)
        end_date = date(2025, 2, 15)
        months = GetData.get_required_months(start_date, end_date)
        logger.info(f"跨年测试 ({start_date} 到 {end_date}): {months}")
        
        logger.info("✅ 月份范围检测功能测试完成")
        
    except Exception as e:
        logger.error(f"❌ 月份范围检测功能测试失败: {str(e)}")

def test_improved_sync():
    """测试改进的数据同步功能"""
    logger.info("=" * 60)
    logger.info("🚀 开始测试改进的数据同步功能")
    logger.info("=" * 60)
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    
    # 测试1: 默认处理昨天数据
    logger.info("\n📅 测试1: 默认处理昨天数据")
    logger.info("-" * 40)
    try:
        success = GetData.sync_sales_data_with_improved_logic(db_manager)
        if success:
            logger.info("✅ 默认昨天数据同步成功")
        else:
            logger.error("❌ 默认昨天数据同步失败")
    except Exception as e:
        logger.error(f"❌ 默认昨天数据同步出错: {str(e)}")
    
    # 测试2: 指定时间范围同步（使用有汇率数据的时间）
    logger.info("\n📊 测试2: 指定时间范围同步（2025年8月1日到8月3日）")
    logger.info("-" * 40)
    try:
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 3)
        
        logger.info(f"同步时间范围: {start_date} 到 {end_date}")
        
        # 检查汇率数据完整性
        required_months = GetData.get_required_months(start_date, end_date)
        logger.info(f"需要的月份: {required_months}")
        
        missing_months = GetData.check_missing_exchange_rates(db_manager, required_months)
        if missing_months:
            logger.info(f"缺失的汇率月份: {missing_months}")
        else:
            logger.info("所有需要的汇率数据都已存在")
        
        success = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
        if success:
            logger.info("✅ 指定时间范围数据同步成功")
        else:
            logger.error("❌ 指定时间范围数据同步失败")
    except Exception as e:
        logger.error(f"❌ 指定时间范围数据同步出错: {str(e)}")

if __name__ == "__main__":
    try:
        # 测试月份范围检测
        test_month_range_detection()
        
        # 测试改进的数据同步
        test_improved_sync()
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 所有测试完成")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"测试过程中出现错误: {str(e)}")
        sys.exit(1)