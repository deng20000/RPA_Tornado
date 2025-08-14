#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
改进的跨月份数据同步逻辑
实现月份范围检测、汇率数据自动更新和按月份处理销售数据
"""

import logging
from datetime import date, datetime, timedelta
from typing import List, Optional, Set, Tuple
from dateutil.relativedelta import relativedelta
from manage_data import DatabaseManager, DataSyncManager, ExchangeRate

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('improved_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImprovedDataSyncManager:
    """改进的数据同步管理器
    
    支持跨月份数据同步，包含智能汇率数据检查和更新
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """初始化改进的数据同步管理器
        
        Args:
            db_manager: 数据库管理器实例
        """
        self.db_manager = db_manager
        self.data_sync_manager = DataSyncManager()
    
    def get_required_months(self, start_date: date, end_date: date) -> List[str]:
        """获取指定日期范围内需要的月份列表
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            List[str]: 月份列表，格式为 YYYY-MM
        """
        months = []
        current_date = start_date.replace(day=1)  # 从月初开始
        end_month = end_date.replace(day=1)
        
        while current_date <= end_month:
            months.append(current_date.strftime('%Y-%m'))
            current_date += relativedelta(months=1)
        
        logger.info(f"📅 需要的月份范围: {months}")
        return months
    
    def check_missing_exchange_rates(self, required_months: List[str]) -> List[str]:
        """检查缺失的汇率数据月份
        
        Args:
            required_months: 需要的月份列表
            
        Returns:
            List[str]: 缺失汇率数据的月份列表
        """
        session = self.db_manager.Session()
        missing_months = []
        
        try:
            for month_str in required_months:
                year, month = map(int, month_str.split('-'))
                # 检查该月份是否有汇率数据
                month_start = date(year, month, 1)
                if month == 12:
                    month_end = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    month_end = date(year, month + 1, 1) - timedelta(days=1)
                
                # 查询该月份是否有汇率记录
                existing_rate = session.query(ExchangeRate).filter(
                    ExchangeRate.date >= month_start,
                    ExchangeRate.date <= month_end
                ).first()
                
                if not existing_rate:
                    missing_months.append(month_str)
                    logger.warning(f"❌ 缺少 {month_str} 月份的汇率数据")
                else:
                    logger.info(f"✅ {month_str} 月份汇率数据存在")
        
        except Exception as e:
            logger.error(f"检查汇率数据时出错: {str(e)}")
        finally:
            session.close()
        
        return missing_months
    
    def update_missing_exchange_rates(self, missing_months: List[str]) -> bool:
        """更新缺失的汇率数据
        
        Args:
            missing_months: 缺失汇率数据的月份列表
            
        Returns:
            bool: 更新是否成功
        """
        if not missing_months:
            logger.info("✅ 所有月份的汇率数据都已存在，无需更新")
            return True
        
        logger.info(f"🔄 开始更新缺失的汇率数据: {missing_months}")
        
        success_count = 0
        for month_str in missing_months:
            try:
                # 获取该月份的汇率数据
                logger.info(f"📡 正在获取 {month_str} 月份的汇率数据...")
                currency_data = self.data_sync_manager.get_currency_rates(month_str)
                
                if not currency_data:
                    logger.error(f"❌ 无法获取 {month_str} 月份的汇率数据")
                    continue
                
                # 使用该月份第一天作为汇率日期
                year, month = map(int, month_str.split('-'))
                target_date = date(year, month, 1)
                
                # 同步汇率数据到数据库
                if self.data_sync_manager.sync_currency_data(self.db_manager, currency_data, target_date):
                    logger.info(f"✅ {month_str} 月份汇率数据更新成功")
                    success_count += 1
                else:
                    logger.error(f"❌ {month_str} 月份汇率数据更新失败")
                    
            except Exception as e:
                logger.error(f"更新 {month_str} 月份汇率数据时出错: {str(e)}")
        
        if success_count == len(missing_months):
            logger.info(f"🎉 所有缺失的汇率数据更新完成 ({success_count}/{len(missing_months)})")
            return True
        else:
            logger.warning(f"⚠️ 部分汇率数据更新失败 ({success_count}/{len(missing_months)})")
            return False
    
    def sync_sales_data_by_month(self, start_date: date, end_date: date) -> bool:
        """按月份同步销售数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 同步是否成功
        """
        logger.info(f"🔄 开始按月份同步销售数据: {start_date} 到 {end_date}")
        
        # 获取需要的月份
        required_months = self.get_required_months(start_date, end_date)
        
        success_count = 0
        total_records = 0
        
        for month_str in required_months:
            try:
                year, month = map(int, month_str.split('-'))
                
                # 计算该月份的开始和结束日期
                month_start = date(year, month, 1)
                if month == 12:
                    month_end = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    month_end = date(year, month + 1, 1) - timedelta(days=1)
                
                # 确保不超出用户指定的范围
                actual_start = max(month_start, start_date)
                actual_end = min(month_end, end_date)
                
                logger.info(f"📊 正在处理 {month_str} 月份数据: {actual_start} 到 {actual_end}")
                
                # 获取该月份的销售数据
                sales_data = self.data_sync_manager.get_sales_stats(
                    start_date=actual_start.strftime('%Y-%m-%d'),
                    end_date=actual_end.strftime('%Y-%m-%d')
                )
                
                if sales_data:
                    # 处理销售数据
                    processed_count = self.data_sync_manager.process_sales_data(
                        self.db_manager, sales_data
                    )
                    
                    if processed_count > 0:
                        logger.info(f"✅ {month_str} 月份销售数据处理成功: {processed_count} 条记录")
                        success_count += 1
                        total_records += processed_count
                    else:
                        logger.warning(f"⚠️ {month_str} 月份没有销售数据")
                else:
                    logger.warning(f"⚠️ 无法获取 {month_str} 月份的销售数据")
                    
            except Exception as e:
                logger.error(f"处理 {month_str} 月份销售数据时出错: {str(e)}")
        
        logger.info(f"🎯 按月份销售数据同步完成: 成功处理 {success_count}/{len(required_months)} 个月份，共 {total_records} 条记录")
        return success_count == len(required_months)
    
    def sync_data_with_improved_logic(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> bool:
        """使用改进逻辑同步数据
        
        Args:
            start_date: 开始日期，如果为None则默认为昨天
            end_date: 结束日期，如果为None则默认为昨天
            
        Returns:
            bool: 同步是否成功
        """
        try:
            # 处理默认日期参数
            if start_date is None and end_date is None:
                # 默认处理昨天的数据
                yesterday = date.today() - timedelta(days=1)
                start_date = end_date = yesterday
                logger.info(f"📅 使用默认日期范围（昨天）: {yesterday}")
            elif start_date is None:
                start_date = end_date
            elif end_date is None:
                end_date = start_date
            
            # 验证日期范围
            if start_date > end_date:
                logger.error("❌ 开始日期不能大于结束日期")
                return False
            
            logger.info(f"🚀 开始改进的数据同步流程: {start_date} 到 {end_date}")
            
            # 步骤1: 获取需要的月份
            required_months = self.get_required_months(start_date, end_date)
            
            # 步骤2: 检查缺失的汇率数据
            missing_months = self.check_missing_exchange_rates(required_months)
            
            # 步骤3: 更新缺失的汇率数据
            if missing_months:
                if not self.update_missing_exchange_rates(missing_months):
                    logger.error("❌ 汇率数据更新失败，无法继续同步销售数据")
                    return False
            
            # 步骤4: 按月份同步销售数据
            if self.sync_sales_data_by_month(start_date, end_date):
                logger.info("🎉 改进的数据同步流程完成成功")
                return True
            else:
                logger.error("❌ 销售数据同步失败")
                return False
                
        except Exception as e:
            logger.error(f"改进的数据同步流程出错: {str(e)}")
            return False

def test_improved_sync():
    """测试改进的同步逻辑"""
    try:
        # 初始化数据库管理器
        db_manager = DatabaseManager()
        db_manager.init_db()
        
        # 创建改进的同步管理器
        improved_sync = ImprovedDataSyncManager(db_manager)
        
        print("=" * 60)
        print("🧪 测试改进的跨月份数据同步逻辑")
        print("=" * 60)
        
        # 测试1: 默认处理昨天数据
        print("\n📋 测试1: 默认处理昨天数据")
        print("-" * 40)
        result1 = improved_sync.sync_data_with_improved_logic()
        print(f"结果: {'✅ 成功' if result1 else '❌ 失败'}")
        
        # 测试2: 跨月份数据同步（2025年6月到8月）
        print("\n📋 测试2: 跨月份数据同步（2025年6月到8月）")
        print("-" * 40)
        start_date = date(2025, 6, 1)
        end_date = date(2025, 8, 5)
        result2 = improved_sync.sync_data_with_improved_logic(start_date, end_date)
        print(f"结果: {'✅ 成功' if result2 else '❌ 失败'}")
        
        # 测试3: 单月数据同步
        print("\n📋 测试3: 单月数据同步（2025年8月）")
        print("-" * 40)
        start_date = date(2025, 8, 1)
        end_date = date(2025, 8, 31)
        result3 = improved_sync.sync_data_with_improved_logic(start_date, end_date)
        print(f"结果: {'✅ 成功' if result3 else '❌ 失败'}")
        
        print("\n" + "=" * 60)
        print(f"🎯 测试总结:")
        print(f"   默认昨天数据: {'✅' if result1 else '❌'}")
        print(f"   跨月份同步: {'✅' if result2 else '❌'}")
        print(f"   单月同步: {'✅' if result3 else '❌'}")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"测试过程中出错: {str(e)}")

if __name__ == "__main__":
    test_improved_sync()