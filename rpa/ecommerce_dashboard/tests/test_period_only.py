#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
专门测试时间区间销售数据同步功能
"""

import logging
from datetime import date
from manage_data import DatabaseManager, GetData

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s:%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('period_sync_test.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

def test_period_sync():
    """测试指定时间区间的销售数据同步"""
    try:
        # 初始化数据库管理器
        logger.info("🔧 初始化数据库管理器...")
        db_manager = DatabaseManager()
        db_manager.init_db()
        
        # 定义时间区间：2025年8月1日到2025年8月5日（使用现有汇率数据的时间范围）
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 5)
        
        logger.info("="*60)
        logger.info(f"🔄 开始测试时间区间同步: {start_date} 到 {end_date}")
        logger.info("="*60)
        
        # 执行销售数据同步
        logger.info("🔄 开始执行销售数据同步...")
        try:
            success = GetData.sync_sales_data_with_period(db_manager, start_date, end_date)
            logger.info(f"🔍 同步结果: {success}")
            
            if success:
                logger.info("✅ 时间区间同步成功！")
                
                # 查询同步结果统计
                session = db_manager.Session()
                try:
                    # 统计该时间区间内的销售记录数
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
                    
                    logger.info(f"📊 同步统计:")
                    logger.info(f"   总记录数: {total_records}")
                    logger.info(f"   涉及店铺数: {distinct_shops}")
                    logger.info(f"   涉及日期数: {distinct_dates}")
                    
                finally:
                    session.close()
                    
            else:
                logger.error("❌ 时间区间同步失败！")
                return False
                
        except Exception as e:
            logger.error(f"❌ 同步过程中发生异常: {str(e)}")
            logger.exception("详细错误信息:")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {str(e)}")
        logger.exception("详细错误信息:")
        return False

if __name__ == "__main__":
    logger.info("🚀 开始时间区间同步测试...")
    
    success = test_period_sync()
    
    logger.info("="*60)
    logger.info("📊 测试结果总结")
    logger.info("="*60)
    
    if success:
        logger.info("✅ 时间区间同步测试成功")
    else:
        logger.error("❌ 时间区间同步测试失败")
        
    logger.info("🏁 测试完成")