#!/usr/bin/env python3
"""
退货跟踪处理
业务人员每天需要登录领星及钉钉获取各店铺退货信息，并反馈给相关负责人
"""

import pandas as pd
import os
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import sys

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import get_config
from utils.logger import LoggerMixin, log_execution_time

class ReturnTrackingProcessor(LoggerMixin):
    """退货跟踪处理器"""
    
    def __init__(self):
        self.config = get_config()
        self.output_dir = self.config.OUTPUT_DIR / "finance"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 区域配置
        self.regions = {
            'US': {
                'region': 'US',
                'shopify_channel': 'Shopify',
                'amazon_channel': 'Amazon',
                'shopify_site': 'US',
                'amazon_site': 'Amazon US',
                'shopify_store_name': 'shopfiy-US买家退货',
                'amazon_store_name': '亚马逊-买家退货-US',
                'shopify_sheet_name': 'shopify-US买家退货',
                'amazon_sheet_name': '亚马逊-买家退货-US',
                'amazon_remove_sheet_name': '亚马逊移除-US',
                'removal_store_name': 'Heison NA-US',
            },
            'UK': {
                'region': 'UK',
                'shopify_channel': 'Shopify',
                'amazon_channel': 'Amazon',
                'shopify_site': 'UK',
                'amazon_site': 'Amazon UK',
                'shopify_store_name': 'shopfiy-UK买家退货',
                'amazon_store_name': '亚马逊-买家退货-UK',
                'shopify_sheet_name': 'shopify-UK买家退货',
                'amazon_sheet_name': '亚马逊-买家退货-UK',
                'amazon_remove_sheet_name': '亚马逊移除-UK',
                'removal_store_name': 'Heison NA-UK',
            },
            'EU': {
                'region': 'EU',
                'shopify_channel': 'Shopify',
                'amazon_channel': 'Amazon',
                'shopify_site': 'EU',
                'amazon_site': 'Amazon EU',
                'amazon_sites': ['Amazon IT', 'Amazon DE', 'Amazon FR', 'Amazon ES',
                                'Amazon NL', 'Amazon SE', 'Amazon TR', 'Amazon PL',
                                'Amazon BE', 'Amazon IE'],
                'shopify_store_name': 'shopfiy-EU买家退货',
                'amazon_store_name': '亚马逊-买家退货-EU',
                'shopify_sheet_name': 'shopify-EU买家退货',
                'amazon_sheet_name': '亚马逊-买家退货-EU',
                'amazon_remove_sheet_name': '亚马逊移除-EU',
                'removal_store_name': 'Heison NA-EU',
            }
        }
    
    def close_wps_process(self):
        """关闭所有WPS进程"""
        for proc in psutil.process_iter():
            try:
                if "wps" in proc.name().lower():
                    proc.kill()
                    self.logger.info("已关闭WPS进程")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    
    @log_execution_time
    def process_returns_data(self, excel_path: str, region: str) -> Dict:
        """
        处理退货数据
        
        Args:
            excel_path: Excel文件路径
            region: 区域代码 (US, UK, EU)
            
        Returns:
            处理结果字典
        """
        self.logger.info(f"开始处理 {region} 区域退货数据")
        
        # 关闭WPS进程
        self.close_wps_process()
        
        if region not in self.regions:
            raise ValueError(f"不支持的区域: {region}")
        
        region_config = self.regions[region]
        
        try:
            # 读取Excel文件
            df = pd.read_excel(excel_path, sheet_name='退货统计表')
            self.logger.info(f"成功读取数据，共 {len(df)} 条记录")
        except Exception as e:
            self.logger.error(f"读取Excel文件失败: {e}")
            raise
        
        # 处理数据
        results = self._process_region_data(df, region_config)
        
        # 生成输出文件
        output_file = self._generate_output(results, region)
        
        self.logger.info(f"退货数据处理完成，输出文件: {output_file}")
        return results
    
    def _process_region_data(self, df: pd.DataFrame, region_config: Dict) -> Dict:
        """处理区域数据"""
        results = {}
        
        # 处理Shopify数据
        shopify_df = df[
            (df['购买渠道'] == region_config['shopify_channel']) &
            (df['shopify站点'] == region_config['shopify_site'])
        ].copy()
        
        if not shopify_df.empty:
            shopify_df.insert(0, '表中来源数据', '退货统计表')
            shopify_df.insert(1, '店铺', region_config['shopify_store_name'])
            results['shopify'] = shopify_df
            self.logger.info(f"Shopify数据: {len(shopify_df)} 条")
        
        # 处理Amazon数据
        amazon_sites = region_config.get('amazon_sites', [region_config.get('amazon_site')])
        amazon_sites = [site for site in amazon_sites if site]
        
        if amazon_sites:
            amazon_df = df[
                (df['购买渠道'] == region_config['amazon_channel']) &
                (df['shopify站点'].isin(amazon_sites))
            ].copy()
            
            if not amazon_df.empty:
                amazon_df.insert(0, '表中来源数据', '退货统计表')
                amazon_df.insert(1, '店铺', region_config['amazon_store_name'])
                results['amazon'] = amazon_df
                self.logger.info(f"Amazon数据: {len(amazon_df)} 条")
        
        # 创建Amazon移除数据
        amazon_remove_columns = [
            '表中来源数据', '店铺', 'Amazon系統建移出單日期', 'Amazon移出單號',
            '移出日期', '型號', 'Amazon FUSKU', '產品狀態', '數量', 
            '物流公司', '跟蹤號', '移除命令類型'
        ]
        
        amazon_remove_df = pd.DataFrame(columns=amazon_remove_columns)
        amazon_remove_df.loc[0] = {
            '表中来源数据': '退货统计表',
            '店铺': region_config['amazon_store_name'],
            'Amazon系統建移出單日期': None,
            'Amazon移出單號': None,
            '移出日期': None,
            '型號': None,
            'Amazon FUSKU': None,
            '產品狀態': None,
            '數量': None,
            '物流公司': None,
            '跟蹤號': None,
            '移除命令类型': None
        }
        
        results['amazon_remove'] = amazon_remove_df
        self.logger.info("创建Amazon移除数据表")
        
        return results
    
    def _generate_output(self, results: Dict, region: str) -> str:
        """生成输出文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"退货跟踪_{region}_{timestamp}.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            for sheet_name, data in results.items():
                if not data.empty:
                    data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return str(output_file)
    
    def process_all_regions(self, excel_path: str) -> Dict:
        """处理所有区域数据"""
        all_results = {}
        
        for region in self.regions.keys():
            try:
                results = self.process_returns_data(excel_path, region)
                all_results[region] = results
            except Exception as e:
                self.logger.error(f"处理 {region} 区域数据失败: {e}")
                all_results[region] = {'error': str(e)}
        
        return all_results

def main():
    """主函数"""
    processor = ReturnTrackingProcessor()
    
    # 示例用法
    excel_path = input("请输入退货数据Excel文件路径: ").strip()
    region = input("请输入区域代码 (US/UK/EU，回车处理所有区域): ").strip().upper()
    
    try:
        if region and region in processor.regions:
            results = processor.process_returns_data(excel_path, region)
            print(f"✅ {region} 区域处理完成！")
        elif not region:
            results = processor.process_all_regions(excel_path)
            print("✅ 所有区域处理完成！")
        else:
            print(f"❌ 不支持的区域: {region}")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 