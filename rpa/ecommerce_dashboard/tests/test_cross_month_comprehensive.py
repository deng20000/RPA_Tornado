#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面的跨月份数据同步测试脚本
测试各种时间范围场景的数据同步功能
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
        logging.FileHandler('test_comprehensive.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def test_month_range_scenarios():
    """测试各种月份范围场景"""
    logger.info("=" * 80)
    logger.info("🧪 测试各种月份范围场景")
    logger.info("=" * 80)
    
    test_cases = [
        # (开始日期, 结束日期, 预期月份, 描述)
        (date(2025, 8, 1), date(2025, 8, 31), ['2025-08'], "单月测试"),
        (date(2025, 6, 15), date(2025, 8, 15), ['2025-06', '2025-07', '2025-08'], "跨3个月测试"),
        (date(2024, 12, 15), date(2025, 2, 15), ['2024-12', '2025-01', '2025-02'], "跨年测试"),
        (date(2025, 7, 31), date(2025, 8, 1), ['2025-07', '2025-08'], "跨月边界测试"),
        (date(2025, 8, 5), date(2025, 8, 5), ['2025-08'], "单日测试"),
    ]
    
    for i, (start_date, end_date, expected_months, description) in enumerate(test_cases, 1):
        try:
            logger.info(f"\n📋 测试用例 {i}: {description}")
            logger.info(f"   时间范围: {start_date} 到 {end_date}")
            
            result_months = GetData.get_required_months(start_date, end_date)
            
            if result_months == expected_months:
                logger.info(f"   ✅ 通过 - 结果: {result_months}")
            else:
                logger.error(f"   ❌ 失败 - 预期: {expected_months}, 实际: {result_months}")
                
        except Exception as e:
            logger.error(f"   ❌ 异常 - {str(e)}")

def test_exchange_rate_checking():
    """测试汇率数据检查功能"""
    logger.info("\n" + "=" * 80)
    logger.info("💱 测试汇率数据检查功能")
    logger.info("=" * 80)
    
    db_manager = DatabaseManager()
    
    test_months = [
        ['2025-08'],  # 应该存在
        ['2025-06'],  # 可能不存在
        ['2024-12', '2025-01'],  # 混合情况
    ]
    
    for i, months in enumerate(test_months, 1):
        try:
            logger.info(f"\n📊 测试 {i}: 检查月份 {months}")
            
            missing_months = GetData.check_missing_exchange_rates(db_manager, months)
            
            if missing_months:
                logger.warning(f"   ⚠️ 缺失的月份: {missing_months}")
            else:
                logger.info(f"   ✅ 所有月份的汇率数据都存在")
                
        except Exception as e:
            logger.error(f"   ❌ 检查汇率数据时出错: {str(e)}")

def test_sync_scenarios():
    """测试不同的同步场景"""
    logger.info("\n" + "=" * 80)
    logger.info("🚀 测试不同的同步场景")
    logger.info("=" * 80)
    
    db_manager = DatabaseManager()
    
    scenarios = [
        # (开始日期, 结束日期, 描述)
        (None, None, "默认同步（昨天数据）"),
        (date(2025, 8, 1), date(2025, 8, 3), "单月短期同步"),
        (date(2025, 8, 1), date(2025, 8, 5), "单月中期同步"),
    ]
    
    for i, (start_date, end_date, description) in enumerate(scenarios, 1):
        try:
            logger.info(f"\n🎯 场景 {i}: {description}")
            if start_date and end_date:
                logger.info(f"   时间范围: {start_date} 到 {end_date}")
            else:
                logger.info(f"   时间范围: 默认（昨天）")
            
            # 执行同步
            success = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
            
            if success:
                logger.info(f"   ✅ {description} 同步成功")
            else:
                logger.error(f"   ❌ {description} 同步失败")
                
        except Exception as e:
            logger.error(f"   ❌ {description} 同步异常: {str(e)}")

def test_edge_cases():
    """测试边界情况"""
    logger.info("\n" + "=" * 80)
    logger.info("🔍 测试边界情况")
    logger.info("=" * 80)
    
    db_manager = DatabaseManager()
    
    edge_cases = [
        # (开始日期, 结束日期, 描述, 预期结果)
        (date(2025, 8, 5), date(2025, 8, 1), "开始日期大于结束日期", False),
        (date(2025, 8, 1), date(2025, 8, 1), "开始日期等于结束日期", True),
    ]
    
    for i, (start_date, end_date, description, expected) in enumerate(edge_cases, 1):
        try:
            logger.info(f"\n🧪 边界测试 {i}: {description}")
            logger.info(f"   时间范围: {start_date} 到 {end_date}")
            
            success = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
            
            if success == expected:
                logger.info(f"   ✅ 结果符合预期: {success}")
            else:
                logger.error(f"   ❌ 结果不符合预期: 预期={expected}, 实际={success}")
                
        except Exception as e:
            logger.error(f"   ❌ 边界测试异常: {str(e)}")

def main():
    """主测试函数"""
    try:
        logger.info("🎬 开始全面的跨月份数据同步测试")
        
        # 测试月份范围检测
        test_month_range_scenarios()
        
        # 测试汇率数据检查
        test_exchange_rate_checking()
        
        # 测试同步场景
        test_sync_scenarios()
        
        # 测试边界情况
        test_edge_cases()
        
        logger.info("\n" + "=" * 80)
        logger.info("🎉 全面测试完成")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"测试过程中出现严重错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()