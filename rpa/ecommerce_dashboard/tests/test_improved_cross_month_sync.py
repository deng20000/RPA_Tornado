#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试改进的跨月份数据同步逻辑
验证月份范围检测、汇率数据自动更新和按月份处理销售数据功能
"""

import logging
from datetime import date, timedelta
from manage_data import DatabaseManager, GetData, Sale, ExchangeRate
from sqlalchemy import func

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_improved_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_improved_cross_month_sync():
    """测试改进的跨月份数据同步逻辑"""
    try:
        # 初始化数据库管理器
        db_manager = DatabaseManager()
        db_manager.init_db()
        
        print("=" * 80)
        print("🧪 测试改进的跨月份数据同步逻辑")
        print("=" * 80)
        
        # 测试1: 默认处理昨天数据
        print("\n📋 测试1: 默认处理昨天数据")
        print("-" * 50)
        
        # 获取同步前的统计信息
        session = db_manager.Session()
        try:
            before_count = session.query(Sale).count()
            yesterday = date.today() - timedelta(days=1)
            yesterday_count_before = session.query(Sale).filter(Sale.sale_date == yesterday).count()
        finally:
            session.close()
        
        # 执行默认同步（昨天数据）
        result1 = GetData.sync_sales_data_with_improved_logic(db_manager)
        
        # 获取同步后的统计信息
        session = db_manager.Session()
        try:
            after_count = session.query(Sale).count()
            yesterday_count_after = session.query(Sale).filter(Sale.sale_date == yesterday).count()
        finally:
            session.close()
        
        print(f"   同步前总记录数: {before_count}")
        print(f"   同步后总记录数: {after_count}")
        print(f"   昨天记录数变化: {yesterday_count_before} -> {yesterday_count_after}")
        print(f"   结果: {'✅ 成功' if result1 else '❌ 失败'}")
        
        # 测试2: 跨月份数据同步（2025年6月到8月）
        print("\n📋 测试2: 跨月份数据同步（2025年6月到8月）")
        print("-" * 50)
        
        start_date = date(2025, 6, 1)
        end_date = date(2025, 8, 5)
        
        # 获取同步前的统计信息
        session = db_manager.Session()
        try:
            before_period_count = session.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).count()
        finally:
            session.close()
        
        # 执行跨月份同步
        result2 = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
        
        # 获取同步后的统计信息
        session = db_manager.Session()
        try:
            after_period_count = session.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).count()
            
            # 按月份统计
            monthly_stats = session.query(
                func.date_trunc('month', Sale.sale_date).label('month'),
                func.count(Sale.sale_id).label('count'),
                func.count(func.distinct(Sale.shop_id)).label('shops')
            ).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).group_by(func.date_trunc('month', Sale.sale_date)).order_by('month').all()
        finally:
            session.close()
        
        print(f"   时间范围: {start_date} 到 {end_date}")
        print(f"   同步前记录数: {before_period_count}")
        print(f"   同步后记录数: {after_period_count}")
        print(f"   新增记录数: {after_period_count - before_period_count}")
        
        if monthly_stats:
            print("   📊 按月份统计:")
            for month, count, shops in monthly_stats:
                print(f"      {month.strftime('%Y-%m')}: {count} 条记录, {shops} 个店铺")
        
        print(f"   结果: {'✅ 成功' if result2 else '❌ 失败'}")
        
        # 测试3: 单月数据同步（2025年8月）
        print("\n📋 测试3: 单月数据同步（2025年8月）")
        print("-" * 50)
        
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 31)
        
        # 获取同步前的统计信息
        session = db_manager.Session()
        try:
            before_month_count = session.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).count()
        finally:
            session.close()
        
        # 执行单月同步
        result3 = GetData.sync_sales_data_with_improved_logic(db_manager, start_date, end_date)
        
        # 获取同步后的统计信息
        session = db_manager.Session()
        try:
            after_month_count = session.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).count()
            
            # 获取该月份的详细统计
            month_details = session.query(
                func.count(Sale.sale_id).label('total_records'),
                func.count(func.distinct(Sale.shop_id)).label('unique_shops'),
                func.count(func.distinct(Sale.sale_date)).label('unique_dates'),
                func.sum(Sale.cny_amount).label('total_cny'),
                func.sum(Sale.usd_amount).label('total_usd')
            ).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).first()
        finally:
            session.close()
        
        print(f"   时间范围: {start_date} 到 {end_date}")
        print(f"   同步前记录数: {before_month_count}")
        print(f"   同步后记录数: {after_month_count}")
        print(f"   新增记录数: {after_month_count - before_month_count}")
        
        if month_details:
            print(f"   📊 8月份详细统计:")
            print(f"      总记录数: {month_details.total_records}")
            print(f"      涉及店铺: {month_details.unique_shops}")
            print(f"      涉及日期: {month_details.unique_dates}")
            print(f"      总CNY金额: {month_details.total_cny}")
            print(f"      总USD金额: {month_details.total_usd}")
        
        print(f"   结果: {'✅ 成功' if result3 else '❌ 失败'}")
        
        # 测试4: 检查汇率数据完整性
        print("\n📋 测试4: 检查汇率数据完整性")
        print("-" * 50)
        
        session = db_manager.Session()
        try:
            # 检查汇率数据
            rate_stats = session.query(
                func.date_trunc('month', ExchangeRate.date).label('month'),
                func.count(ExchangeRate.id).label('count'),
                func.count(func.distinct(ExchangeRate.currency_code)).label('currencies')
            ).group_by(func.date_trunc('month', ExchangeRate.date)).order_by('month').all()
            
            print("   💱 汇率数据按月份统计:")
            for month, count, currencies in rate_stats:
                print(f"      {month.strftime('%Y-%m')}: {count} 条记录, {currencies} 种货币")
        finally:
            session.close()
        
        # 总结
        print("\n" + "=" * 80)
        print(f"🎯 测试总结:")
        print(f"   默认昨天数据同步: {'✅' if result1 else '❌'}")
        print(f"   跨月份数据同步: {'✅' if result2 else '❌'}")
        print(f"   单月数据同步: {'✅' if result3 else '❌'}")
        
        overall_success = result1 and result2 and result3
        print(f"   整体测试结果: {'🎉 全部成功' if overall_success else '⚠️ 部分失败'}")
        print("=" * 80)
        
        return overall_success
        
    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")
        return False

def test_month_range_detection():
    """测试月份范围检测功能"""
    print("\n🔍 测试月份范围检测功能")
    print("-" * 40)
    
    test_cases = [
        (date(2025, 6, 1), date(2025, 8, 5), ["2025-6", "2025-7", "2025-8"]),
        (date(2025, 12, 15), date(2026, 2, 10), ["2025-12", "2026-1", "2026-2"]),
        (date(2025, 8, 1), date(2025, 8, 31), ["2025-8"]),
        (date(2025, 7, 20), date(2025, 7, 25), ["2025-7"])
    ]
    
    for i, (start, end, expected) in enumerate(test_cases, 1):
        result = GetData.get_required_months(start, end)
        success = result == expected
        print(f"   测试{i}: {start} 到 {end}")
        print(f"   期望: {expected}")
        print(f"   实际: {result}")
        print(f"   结果: {'✅' if success else '❌'}")
        print()

if __name__ == "__main__":
    # 先测试月份范围检测
    test_month_range_detection()
    
    # 再测试完整的同步逻辑
    test_improved_cross_month_sync()