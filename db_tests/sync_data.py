#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据同步脚本
用于同步指定时间区间的电商数据

功能：
1. 同步店铺数据
2. 同步汇率数据
3. 同步销售数据
4. 支持指定时间区间同步
5. 提供详细的同步进度和结果报告

作者：AI Assistant
创建时间：2025-08-13
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date, timedelta
import logging
from typing import Optional, Dict, Any, List, Tuple
import argparse

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入项目模块
try:
    from templates.manage_data import (
        DatabaseManager, 
        GetData,
        Shop, 
        Sale, 
        ExchangeRate
    )
    from db_tests.db_init import ensure_database_ready
except ImportError as e:
    print(f"导入模块失败: {e}")
    sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('sync_data.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

class DataSynchronizer:
    """
    数据同步器
    负责同步电商数据看板的各类数据
    """
    
    def __init__(self):
        """初始化数据同步器"""
        self.db_manager = None
        self.sync_stats = {
            'shops': {'success': 0, 'failed': 0},
            'exchange_rates': {'success': 0, 'failed': 0},
            'sales': {'success': 0, 'failed': 0}
        }
        
    def initialize(self) -> bool:
        """
        初始化同步器
        
        Returns:
            bool: 初始化是否成功
        """
        logger.info("🔧 初始化数据同步器...")
        
        try:
            # 确保数据库准备就绪
            if not ensure_database_ready():
                logger.error("❌ 数据库初始化失败")
                return False
            
            # 初始化数据库管理器
            self.db_manager = DatabaseManager()
            logger.info("✅ 数据同步器初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据同步器初始化失败: {str(e)}")
            return False
    
    def sync_shop_data(self) -> bool:
        """
        同步店铺数据
        
        Returns:
            bool: 同步是否成功
        """
        logger.info("🏪 开始同步店铺数据...")
        
        try:
            # 从API获取店铺列表数据
            logger.info("📡 正在从API获取店铺列表...")
            api_data = GetData.get_seller_list()
            
            if not api_data:
                logger.error("❌ 无法获取店铺数据")
                self.sync_stats['shops']['failed'] += 1
                return False
            
            # 解析店铺数据
            stores_info = GetData.extract_store_info_as_dict(api_data)
            logger.info(f"📋 提取到 {len(stores_info)} 条店铺信息")
            
            # 同步店铺数据到数据库
            success = GetData.sync_store_data(self.db_manager, api_data)
            
            if success:
                logger.info("✅ 店铺数据同步成功")
                self.sync_stats['shops']['success'] += len(stores_info)
                return True
            else:
                logger.error("❌ 店铺数据同步失败")
                self.sync_stats['shops']['failed'] += len(stores_info)
                return False
                
        except Exception as e:
            logger.error(f"❌ 同步店铺数据时出错: {str(e)}")
            self.sync_stats['shops']['failed'] += 1
            return False
    
    def sync_exchange_rates_for_period(self, start_date: date, end_date: date) -> bool:
        """
        同步指定时间区间的汇率数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 同步是否成功
        """
        logger.info(f"💱 开始同步汇率数据: {start_date} 到 {end_date}")
        
        try:
            # 获取需要的月份
            required_months = GetData.get_required_months(start_date, end_date)
            logger.info(f"📅 需要同步的月份: {required_months}")
            
            # 检查缺失的汇率数据
            missing_months = GetData.check_missing_exchange_rates(self.db_manager, required_months)
            
            if not missing_months:
                logger.info("✅ 所有月份的汇率数据都已存在")
                return True
            
            # 更新缺失的汇率数据
            success = GetData.update_missing_exchange_rates(self.db_manager, missing_months)
            
            if success:
                logger.info("✅ 汇率数据同步成功")
                self.sync_stats['exchange_rates']['success'] += len(missing_months)
                return True
            else:
                logger.error("❌ 汇率数据同步失败")
                self.sync_stats['exchange_rates']['failed'] += len(missing_months)
                return False
                
        except Exception as e:
            logger.error(f"❌ 同步汇率数据时出错: {str(e)}")
            self.sync_stats['exchange_rates']['failed'] += 1
            return False
    
    def sync_sales_data_for_period(self, start_date: date, end_date: date) -> bool:
        """
        同步指定时间区间的销售数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 同步是否成功
        """
        logger.info(f"📊 开始同步销售数据: {start_date} 到 {end_date}")
        
        try:
            # 使用改进的销售数据同步方法
            success = GetData.sync_sales_data_with_improved_logic(
                self.db_manager, start_date, end_date
            )
            
            if success:
                logger.info("✅ 销售数据同步成功")
                self.sync_stats['sales']['success'] += 1
                return True
            else:
                logger.error("❌ 销售数据同步失败")
                self.sync_stats['sales']['failed'] += 1
                return False
                
        except Exception as e:
            logger.error(f"❌ 同步销售数据时出错: {str(e)}")
            self.sync_stats['sales']['failed'] += 1
            return False
    
    def sync_data_for_period(self, start_date: date, end_date: date, 
                           sync_shops: bool = True, 
                           sync_rates: bool = True, 
                           sync_sales: bool = True) -> bool:
        """
        同步指定时间区间的所有数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            sync_shops: 是否同步店铺数据
            sync_rates: 是否同步汇率数据
            sync_sales: 是否同步销售数据
            
        Returns:
            bool: 同步是否成功
        """
        logger.info(f"🚀 开始完整数据同步: {start_date} 到 {end_date}")
        
        success_count = 0
        total_tasks = sum([sync_shops, sync_rates, sync_sales])
        
        try:
            # 步骤1: 同步店铺数据（如果需要）
            if sync_shops:
                logger.info("📋 步骤 1/3: 同步店铺数据")
                if self.sync_shop_data():
                    success_count += 1
                    logger.info("✅ 店铺数据同步完成")
                else:
                    logger.error("❌ 店铺数据同步失败")
            
            # 步骤2: 同步汇率数据（如果需要）
            if sync_rates:
                logger.info("📋 步骤 2/3: 同步汇率数据")
                if self.sync_exchange_rates_for_period(start_date, end_date):
                    success_count += 1
                    logger.info("✅ 汇率数据同步完成")
                else:
                    logger.error("❌ 汇率数据同步失败")
            
            # 步骤3: 同步销售数据（如果需要）
            if sync_sales:
                logger.info("📋 步骤 3/3: 同步销售数据")
                if self.sync_sales_data_for_period(start_date, end_date):
                    success_count += 1
                    logger.info("✅ 销售数据同步完成")
                else:
                    logger.error("❌ 销售数据同步失败")
            
            # 检查整体同步结果
            if success_count == total_tasks:
                logger.info("🎉 所有数据同步成功")
                return True
            else:
                logger.warning(f"⚠️ 部分数据同步失败: {success_count}/{total_tasks}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 数据同步过程中出错: {str(e)}")
            return False
    
    def get_sync_report(self) -> Dict[str, Any]:
        """
        获取同步报告
        
        Returns:
            Dict[str, Any]: 同步统计报告
        """
        total_success = sum(stats['success'] for stats in self.sync_stats.values())
        total_failed = sum(stats['failed'] for stats in self.sync_stats.values())
        
        return {
            'sync_time': datetime.now().isoformat(),
            'total_success': total_success,
            'total_failed': total_failed,
            'success_rate': f"{(total_success / (total_success + total_failed) * 100):.1f}%" if (total_success + total_failed) > 0 else "0%",
            'details': self.sync_stats
        }
    
    def print_sync_report(self):
        """
        打印同步报告
        """
        report = self.get_sync_report()
        
        print("\n" + "="*60)
        print("📊 数据同步报告")
        print("="*60)
        print(f"同步时间: {report['sync_time']}")
        print(f"总成功数: {report['total_success']}")
        print(f"总失败数: {report['total_failed']}")
        print(f"成功率: {report['success_rate']}")
        print("\n详细统计:")
        
        for data_type, stats in report['details'].items():
            print(f"  {data_type}: 成功 {stats['success']}, 失败 {stats['failed']}")
        
        print("="*60)

def parse_date(date_str: str) -> date:
    """
    解析日期字符串
    
    Args:
        date_str: 日期字符串 (YYYY-MM-DD)
        
    Returns:
        date: 解析后的日期对象
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"日期格式错误: {date_str}，请使用 YYYY-MM-DD 格式")

def sync_target_period() -> bool:
    """
    同步目标时间区间的数据 (2025-06-01 到 2025-08-12)
    
    Returns:
        bool: 同步是否成功
    """
    # 目标时间区间
    start_date = date(2025, 6, 1)
    end_date = date(2025, 8, 12)
    
    logger.info(f"🎯 开始同步目标时间区间: {start_date} 到 {end_date}")
    
    # 创建同步器
    synchronizer = DataSynchronizer()
    
    # 初始化
    if not synchronizer.initialize():
        logger.error("❌ 同步器初始化失败")
        return False
    
    # 执行同步
    success = synchronizer.sync_data_for_period(start_date, end_date)
    
    # 打印报告
    synchronizer.print_sync_report()
    
    return success

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='电商数据看板数据同步工具')
    parser.add_argument('--start-date', type=str, help='开始日期 (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='结束日期 (YYYY-MM-DD)')
    parser.add_argument('--target', action='store_true', help='同步目标时间区间 (2025-06-01 到 2025-08-12)')
    parser.add_argument('--no-shops', action='store_true', help='跳过店铺数据同步')
    parser.add_argument('--no-rates', action='store_true', help='跳过汇率数据同步')
    parser.add_argument('--no-sales', action='store_true', help='跳过销售数据同步')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📊 电商数据看板 - 数据同步工具")
    print("=" * 60)
    
    try:
        if args.target:
            # 同步目标时间区间
            success = sync_target_period()
        elif args.start_date and args.end_date:
            # 同步指定时间区间
            start_date = parse_date(args.start_date)
            end_date = parse_date(args.end_date)
            
            synchronizer = DataSynchronizer()
            if not synchronizer.initialize():
                print("❌ 同步器初始化失败")
                sys.exit(1)
            
            success = synchronizer.sync_data_for_period(
                start_date, end_date,
                sync_shops=not args.no_shops,
                sync_rates=not args.no_rates,
                sync_sales=not args.no_sales
            )
            
            synchronizer.print_sync_report()
        else:
            # 默认同步目标时间区间
            print("未指定时间区间，将同步目标时间区间 (2025-06-01 到 2025-08-12)")
            success = sync_target_period()
        
        if success:
            print("\n✅ 数据同步成功！")
        else:
            print("\n❌ 数据同步失败！")
            sys.exit(1)
            
    except ValueError as e:
        print(f"❌ 参数错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 同步过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()