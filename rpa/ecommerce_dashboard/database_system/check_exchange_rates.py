#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
检查数据库中现有的汇率数据
"""

import logging
from manage_data import DatabaseManager, ExchangeRate
from sqlalchemy import func

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s:%(message)s'
)

logger = logging.getLogger(__name__)

def check_exchange_rates():
    """检查数据库中的汇率数据"""
    try:
        # 初始化数据库管理器
        db_manager = DatabaseManager()
        db_manager.init_db()
        
        session = db_manager.Session()
        try:
            # 查询所有汇率记录
            all_rates = session.query(ExchangeRate).all()
            logger.info(f"📊 数据库中共有 {len(all_rates)} 条汇率记录")
            
            if all_rates:
                # 按月份分组统计
                monthly_stats = session.query(
                    func.date_trunc('month', ExchangeRate.date).label('month'),
                    func.count(ExchangeRate.id).label('count')
                ).group_by(func.date_trunc('month', ExchangeRate.date)).order_by('month').all()
                
                logger.info("📅 按月份统计的汇率记录:")
                for month, count in monthly_stats:
                    logger.info(f"   {month.strftime('%Y-%m')}: {count} 条记录")
                
                # 查询最早和最晚的汇率日期
                earliest = session.query(func.min(ExchangeRate.date)).scalar()
                latest = session.query(func.max(ExchangeRate.date)).scalar()
                logger.info(f"📅 汇率数据时间范围: {earliest} 到 {latest}")
                
                # 查询不同货币的汇率记录
                currency_stats = session.query(
                    ExchangeRate.currency_code,
                    func.count(ExchangeRate.id).label('count')
                ).group_by(ExchangeRate.currency_code).order_by('count').all()
                
                logger.info("💱 按货币统计的汇率记录:")
                for currency, count in currency_stats:
                    logger.info(f"   {currency}: {count} 条记录")
                    
                # 显示最近的几条汇率记录
                recent_rates = session.query(ExchangeRate).order_by(ExchangeRate.date.desc()).limit(10).all()
                logger.info("🔍 最近的汇率记录:")
                for rate in recent_rates:
                    logger.info(f"   {rate.date} {rate.currency_code}: {rate.user_rate}")
                    
            else:
                logger.warning("⚠️  数据库中没有汇率记录")
                
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"❌ 检查汇率数据时发生错误: {str(e)}")
        logger.exception("详细错误信息:")

if __name__ == "__main__":
    logger.info("🔍 开始检查汇率数据...")
    check_exchange_rates()
    logger.info("🏁 检查完成")