#!/usr/bin/env python3
"""
各店铺发货数据汇总 - 数据处理
财务每个月初汇总上个月各店铺的发货订单数据，快速获取产品名、料号、金额、数据、仓位
"""

import pandas as pd
import numpy as np
import openpyxl
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import sys

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import get_config
from utils.logger import LoggerMixin, log_execution_time

class ShippingDataProcessor(LoggerMixin):
    """发货数据处理器"""
    
    def __init__(self):
        self.config = get_config()
        self.output_dir = self.config.OUTPUT_DIR / "finance"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    @log_execution_time
    def process_shipping_data(self, input_file: str, month: Optional[str] = None) -> str:
        """
        处理发货数据
        
        Args:
            input_file: 输入文件路径
            month: 处理月份，格式：YYYY-MM，如果为None则处理当前月份
            
        Returns:
            输出文件路径
        """
        self.logger.info(f"开始处理发货数据: {input_file}")
        
        if not month:
            month = datetime.now().strftime("%Y-%m")
        
        # 读取Excel文件
        try:
            df = pd.read_excel(input_file, dtype=str)
            self.logger.info(f"成功读取数据，共 {len(df)} 条记录")
        except Exception as e:
            self.logger.error(f"读取文件失败: {e}")
            raise
        
        # 数据清洗和预处理
        df = self._clean_data(df)
        
        # 数据汇总
        summary = self._summarize_data(df)
        
        # 生成输出文件
        output_file = self._generate_output(summary, month)
        
        self.logger.info(f"数据处理完成，输出文件: {output_file}")
        return output_file
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """数据清洗"""
        self.logger.info("开始数据清洗...")
        
        # 移除空行
        df = df.dropna(how='all')
        
        # 处理合并单元格
        df = self._handle_merged_cells(df)
        
        # 标准化列名
        df.columns = df.columns.str.strip()
        
        # 处理日期格式
        if '发货时间' in df.columns:
            df['发货日期'] = pd.to_datetime(df['发货时间']).dt.strftime('%Y-%m-%d')
        
        # 处理金额格式
        if '商品金额' in df.columns:
            df['商品金额'] = pd.to_numeric(df['商品金额'], errors='coerce').fillna(0)
        
        self.logger.info(f"数据清洗完成，剩余 {len(df)} 条记录")
        return df
    
    def _handle_merged_cells(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理合并单元格"""
        # 向前填充空值
        df = df.fillna(method='ffill')
        return df
    
    def _summarize_data(self, df: pd.DataFrame) -> Dict:
        """数据汇总"""
        self.logger.info("开始数据汇总...")
        
        summary = {
            'total_orders': len(df),
            'total_amount': df['商品金额'].sum() if '商品金额' in df.columns else 0,
            'total_quantity': df['数量'].sum() if '数量' in df.columns else 0,
            'stores': df['发货仓库'].nunique() if '发货仓库' in df.columns else 0,
            'products': df['品名'].nunique() if '品名' in df.columns else 0,
        }
        
        # 按店铺汇总
        if '发货仓库' in df.columns:
            store_summary = df.groupby('发货仓库').agg({
                '商品金额': 'sum',
                '数量': 'sum',
                '平台单号': 'count'
            }).rename(columns={'平台单号': '订单数量'})
            summary['store_breakdown'] = store_summary
        
        # 按产品汇总
        if '品名' in df.columns:
            product_summary = df.groupby('品名').agg({
                '商品金额': 'sum',
                '数量': 'sum',
                '平台单号': 'count'
            }).rename(columns={'平台单号': '订单数量'})
            summary['product_breakdown'] = product_summary
        
        self.logger.info("数据汇总完成")
        return summary
    
    def _generate_output(self, summary: Dict, month: str) -> str:
        """生成输出文件"""
        output_file = self.output_dir / f"发货数据汇总_{month}.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 汇总信息
            summary_df = pd.DataFrame([summary])
            summary_df.to_excel(writer, sheet_name='汇总信息', index=False)
            
            # 店铺明细
            if 'store_breakdown' in summary:
                summary['store_breakdown'].to_excel(writer, sheet_name='店铺明细')
            
            # 产品明细
            if 'product_breakdown' in summary:
                summary['product_breakdown'].to_excel(writer, sheet_name='产品明细')
        
        return str(output_file)

def main():
    """主函数"""
    processor = ShippingDataProcessor()
    
    # 示例用法
    input_file = input("请输入数据文件路径: ").strip()
    month = input("请输入处理月份 (YYYY-MM，回车使用当前月份): ").strip() or None
    
    try:
        output_file = processor.process_shipping_data(input_file, month)
        print(f"✅ 处理完成！输出文件: {output_file}")
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 