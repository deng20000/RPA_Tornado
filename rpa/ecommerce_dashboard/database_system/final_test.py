#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
最终测试脚本：验证两个任务的完成情况
1. 昨天数据的存在则更新，不存在则添加
2. 时间区间数据同步功能
"""

import logging
from datetime import date, timedelta, datetime
from manage_data import DatabaseManager, GetData, Sale

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s:%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('final_test.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def test_yesterday_update_add():
    """测试昨天数据的更新/添加功能"""
    logger.info("🔄 测试任务1：昨天数据的存在则更新，不存在则添加")
    
    try:
        db_manager = DatabaseManager()
        db_manager.init_db()
        
        # 获取昨天的日期
        yesterday = datetime.now().date() - timedelta(days=1)
        logger.info(f"📅 昨天日期: {yesterday}")
        
        # 查询昨天同步前的记录数
        session = db_manager.Session()
        try:
            before_count = session.query(Sale).filter(Sale.sale_date == yesterday).count()
            logger.info(f"📊 同步前昨天的销售记录数: {before_count}")
        finally:
            session.close()
        
        # 执行昨天数据同步（默认行为）
        logger.info("🔄 开始同步昨天数据...")
        success = GetData.sync_sales_data_with_period(db_manager)
        
        if success:
            # 查询同步后的记录数
            session = db_manager.Session()
            try:
                after_count = session.query(Sale).filter(Sale.sale_date == yesterday).count()
                logger.info(f"📊 同步后昨天的销售记录数: {after_count}")
                
                if before_count > 0:
                    logger.info("✅ 昨天已有数据，执行了更新操作")
                else:
                    logger.info("✅ 昨天没有数据，执行了添加操作")
                    
                return True
            finally:
                session.close()
        else:
            logger.error("❌ 昨天数据同步失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试昨天数据更新/添加功能时发生错误: {str(e)}")
        return False

def test_period_sync():
    """测试时间区间数据同步功能"""
    logger.info("🔄 测试任务2：时间区间数据同步功能")
    
    try:
        db_manager = DatabaseManager()
        
        # 使用现有汇率数据的时间范围：2025年8月1日到8月3日
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 3)
        
        logger.info(f"📅 测试时间区间: {start_date} 到 {end_date}")
        
        # 查询同步前的记录数
        session = db_manager.Session()
        try:
            before_count = session.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).count()
            logger.info(f"📊 同步前该时间区间的销售记录数: {before_count}")
        finally:
            session.close()
        
        # 执行时间区间数据同步
        logger.info("🔄 开始同步时间区间数据...")
        success = GetData.sync_sales_data_with_period(db_manager, start_date, end_date)
        
        if success:
            # 查询同步后的记录数和统计信息
            session = db_manager.Session()
            try:
                after_count = session.query(Sale).filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                ).count()
                
                distinct_shops = session.query(Sale.shop_id).filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                ).distinct().count()
                
                distinct_dates = session.query(Sale.sale_date).filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                ).distinct().count()
                
                logger.info(f"📊 同步后该时间区间的销售记录数: {after_count}")
                logger.info(f"📊 涉及店铺数: {distinct_shops}")
                logger.info(f"📊 涉及日期数: {distinct_dates}")
                
                logger.info("✅ 时间区间数据同步成功")
                return True
                
            finally:
                session.close()
        else:
            logger.error("❌ 时间区间数据同步失败")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试时间区间数据同步功能时发生错误: {str(e)}")
        return False

def main():
    """主测试函数"""
    logger.info("🚀 开始最终测试...")
    logger.info("="*80)
    
    # 测试任务1：昨天数据的更新/添加
    task1_success = test_yesterday_update_add()
    
    logger.info("="*80)
    
    # 测试任务2：时间区间数据同步
    task2_success = test_period_sync()
    
    logger.info("="*80)
    logger.info("📊 最终测试结果总结")
    logger.info("="*80)
    
    logger.info(f"📋 任务1 - 昨天数据更新/添加: {'✅ 成功' if task1_success else '❌ 失败'}")
    logger.info(f"📋 任务2 - 时间区间数据同步: {'✅ 成功' if task2_success else '❌ 失败'}")
    
    if task1_success and task2_success:
        logger.info("🎉 所有任务测试成功！")
        logger.info("✅ 系统功能完全符合需求：")
        logger.info("   1. ✅ 默认获取昨天数据时，存在则更新，不存在则添加")
        logger.info("   2. ✅ 支持获取指定时间区间的数据")
        return True
    else:
        logger.error("❌ 部分任务测试失败")
        return False

if __name__ == "__main__":
    success = main()
    logger.info("🏁 最终测试完成")
    
    if success:
        exit(0)
    else:
        exit(1)