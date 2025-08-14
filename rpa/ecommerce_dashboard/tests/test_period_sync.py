#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试指定时间区间的销售数据同步
获取6月1号到8月5号的销售数据
"""

import logging
from datetime import date, datetime, timedelta
from manage_data import DatabaseManager, GetData

# 配置日志
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),  # 控制台输出
        logging.FileHandler('sales_sync.log', encoding='utf-8')  # 文件输出
    ]
)
logger = logging.getLogger(__name__)

def test_period_sync():
    """测试指定时间区间的销售数据同步"""
    try:
        # 初始化数据库管理器
        logger.info("初始化数据库管理器...")
        db_manager = DatabaseManager()
        
        # 确保数据库表存在
        db_manager.init_db()
        
        # 测试指定时间区间同步（6月1号到8月5号）
        start_date = date(2024, 6, 1)
        end_date = date(2024, 8, 5)
        
        logger.info("="*60)
        logger.info(f"🚀 开始同步销售数据")
        logger.info(f"📅 时间区间: {start_date} 到 {end_date}")
        logger.info(f"📊 总天数: {(end_date - start_date).days + 1} 天")
        logger.info("="*60)
        
        # 执行销售数据同步
        logger.info("🔄 开始执行销售数据同步...")
        success = GetData.sync_sales_data_with_period(db_manager, start_date, end_date)
        logger.info(f"🔍 同步结果: {success}")
        
        if success:
            logger.info("✅ 销售数据同步成功完成！")
            
            # 查询同步结果统计
            session = db_manager.Session()
            try:
                # 统计指定时间区间内的销售记录数量
                from manage_data import Sale
                total_records = session.query(Sale).filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                ).count()
                
                # 统计涉及的店铺数量
                distinct_shops = session.query(Sale.shop_id).filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                ).distinct().count()
                
                # 统计涉及的日期数量
                distinct_dates = session.query(Sale.sale_date).filter(
                    Sale.sale_date >= start_date,
                    Sale.sale_date <= end_date
                ).distinct().count()
                
                logger.info("="*60)
                logger.info("📈 同步结果统计:")
                logger.info(f"   📝 总销售记录数: {total_records}")
                logger.info(f"   🏪 涉及店铺数: {distinct_shops}")
                logger.info(f"   📅 涉及日期数: {distinct_dates}")
                logger.info("="*60)
                
            finally:
                session.close()
                
        else:
            logger.error("❌ 销售数据同步失败！")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试过程中发生错误: {str(e)}")
        return False

def test_yesterday_sync():
    """测试默认获取昨天数据的功能"""
    try:
        logger.info("="*60)
        logger.info("🔄 测试默认获取昨天数据功能")
        logger.info("="*60)
        
        # 初始化数据库管理器
        db_manager = DatabaseManager()
        
        # 获取昨天的日期
        yesterday = datetime.now().date() - timedelta(days=1)
        logger.info(f"📅 昨天日期: {yesterday}")
        
        # 执行默认同步（不传参数，默认获取昨天数据）
        success = GetData.sync_sales_data_with_period(db_manager)
        
        if success:
            logger.info("✅ 昨天数据同步成功！")
            
            # 查询昨天的销售记录
            session = db_manager.Session()
            try:
                from manage_data import Sale
                yesterday_records = session.query(Sale).filter(
                    Sale.sale_date == yesterday
                ).count()
                
                logger.info(f"📊 昨天({yesterday})的销售记录数: {yesterday_records}")
                
            finally:
                session.close()
        else:
            logger.error("❌ 昨天数据同步失败！")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ 昨天数据同步测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    logger.info("🎯 开始销售数据同步测试")
    
    # 测试1：获取6月1号到8月5号的数据
    logger.info("\n" + "="*80)
    logger.info("📋 任务1: 获取6月1号到8月5号的销售数据")
    logger.info("="*80)
    
    period_success = test_period_sync()
    
    # 测试2：测试默认获取昨天数据
    logger.info("\n" + "="*80)
    logger.info("📋 任务2: 测试默认获取昨天数据（更新/添加逻辑）")
    logger.info("="*80)
    
    yesterday_success = test_yesterday_sync()
    
    # 总结
    logger.info("\n" + "="*80)
    logger.info("📊 测试结果总结")
    logger.info("="*80)
    logger.info(f"📅 时间区间同步 (6月1号-8月5号): {'✅ 成功' if period_success else '❌ 失败'}")
    logger.info(f"🔄 昨天数据同步: {'✅ 成功' if yesterday_success else '❌ 失败'}")
    
    if period_success and yesterday_success:
        logger.info("🎉 所有测试均成功完成！")
    else:
        logger.error("⚠️  部分测试失败，请检查日志")

if __name__ == "__main__":
    main()