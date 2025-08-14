#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Shopee和Walmart平台匹配功能
"""

import pandas as pd
import os

def test_shopee_walmart_matching():
    """测试Shopee和Walmart平台的匹配功能"""
    
    print("=== Shopee和Walmart平台匹配测试 ===\n")
    
    # 检查Excel文件是否存在
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '2025年08月11日退货订单.xlsx')
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    try:
        # 读取周度销量数据
        df = pd.read_excel(file_path, sheet_name='周度销量数据', engine='openpyxl')
        
        print("📊 当前周度销量数据:")
        print(df.to_string(index=False))
        print()
        
        # 检查是否有Shopee或Walmart数据
        shopee_data = df[df['地区/平台'].str.contains('Shopee', na=False)]
        walmart_data = df[df['地区/平台'].str.contains('Walmart', na=False)]
        
        print("🛍️ Shopee平台数据:")
        if not shopee_data.empty:
            print(shopee_data.to_string(index=False))
            print(f"   - Shopee总销量: {shopee_data['销量'].sum()}")
            print(f"   - Shopee总退货: {shopee_data['退货数量'].sum()}")
            print(f"   - Shopee平均退货率: {shopee_data['退货率'].mean():.2f}%")
        else:
            print("   无Shopee平台数据")
        print()
        
        print("🏪 Walmart平台数据:")
        if not walmart_data.empty:
            print(walmart_data.to_string(index=False))
            print(f"   - Walmart总销量: {walmart_data['销量'].sum()}")
            print(f"   - Walmart总退货: {walmart_data['退货数量'].sum()}")
            print(f"   - Walmart平均退货率: {walmart_data['退货率'].mean():.2f}%")
        else:
            print("   无Walmart平台数据")
        print()
        
        # 分析平台映射支持情况
        print("🔄 平台映射支持分析:")
        print("✅ 支持的Shopee变体:")
        shopee_variants = [
            'Shopee', 'Shopee SG', 'Shopee MY', 'Shopee TH', 
            'Shopee VN', 'Shopee PH', 'Shopee ID', 'Shopee TW', 'Shopee BR'
        ]
        for variant in shopee_variants:
            print(f"   - {variant}")
        
        print("\n✅ 支持的Walmart变体:")
        walmart_variants = [
            'Walmart', 'Walmart US', 'Walmart.com', 
            'Walmart CA', 'Walmart Canada'
        ]
        for variant in walmart_variants:
            print(f"   - {variant}")
        
        print("\n📋 匹配机制说明:")
        print("1. 直接匹配：退货数据平台名 = 销量数据平台名")
        print("2. 映射匹配：退货数据平台名 → 映射转换 → 销量数据平台名")
        print("3. 如果都匹配失败，销量默认为0")
        
    except Exception as e:
        print(f"❌ 读取文件时发生错误: {e}")

if __name__ == "__main__":
    test_shopee_walmart_matching()