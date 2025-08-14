#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证销量数据是否正确填充到Excel文件中
"""

import pandas as pd
import os

def verify_sales_data():
    """验证销量数据和退货率统计是否正确"""
    
    # 文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '2025年08月11日退货订单.xlsx')
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    try:
        # 读取"周度销量数据"工作表
        df = pd.read_excel(file_path, sheet_name='周度销量数据', engine='openpyxl')
        
        print("=== 周度销量数据验证 ===")
        print(f"总行数: {len(df)}")
        print(f"列名: {df.columns.tolist()}")
        
        # 显示完整数据
        print(f"\n完整数据:")
        print(df.to_string(index=False))
        
        # 检查销量列
        if '销量' in df.columns:
            print(f"\n销量统计:")
            print(f"- 销量为0的行数: {len(df[df['销量'] == 0])}")
            print(f"- 销量大于0的行数: {len(df[df['销量'] > 0])}")
            print(f"- 销量总和: {df['销量'].sum()}")
            
            # 按平台统计销量
            print(f"\n按平台统计销量:")
            platform_sales = df.groupby('地区/平台')['销量'].sum()
            for platform, total_sales in platform_sales.items():
                print(f"- {platform}: {total_sales}")
                
        # 检查退货数量列
        if '退货数量' in df.columns:
            print(f"\n退货数量统计:")
            print(f"- 退货数量总和: {df['退货数量'].sum()}")
            
            # 按平台统计退货数量
            print(f"\n按平台统计退货数量:")
            platform_returns = df.groupby('地区/平台')['退货数量'].sum()
            for platform, total_returns in platform_returns.items():
                print(f"- {platform}: {total_returns}")
        
        # 退货率已删除，不再进行相关统计和验证
        print(f"\n退货率统计: 已删除退货率列")
            
    except Exception as e:
        print(f"❌ 读取文件时发生错误: {e}")

if __name__ == "__main__":
    verify_sales_data()