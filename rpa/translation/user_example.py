#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户提供的列表格式销量数据使用示例
"""

import os
import data_pro

def main():
    """使用用户提供的列表格式销量数据"""
    
    # 用户提供的销量数据（列表格式）
    sales_data = [
        {'SKU': 'GL-X2000', '平台': '美亚', '数量': '29'}, 
        {'SKU': 'GL-BE3600', '平台': '美亚', '数量': '581'}, 
        {'SKU': 'GL-RM1', '平台': '美亚', '数量': '502'}, 
        {'SKU': 'GL-X2000', '平台': '欧亚', '数量': '14'}, 
        {'SKU': 'GL-BE3600', '平台': '欧亚', '数量': '150'}, 
        {'SKU': 'GL-RM1', '平台': '欧亚', '数量': '133'}, 
        {'SKU': 'GL-X2000', '平台': 'Shopee', '数量': '0'}, 
        {'SKU': 'GL-BE3600', '平台': 'Shopee', '数量': '13'}, 
        {'SKU': 'GL-X2000', '平台': 'Walmart', '数量': '0'}, 
        {'SKU': 'GL-BE3600', '平台': 'Walmart', '数量': '0'}
    ]
    
    # Excel文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "2025年06月16日退货订单(2).xlsx")
    
    print("=== 使用用户提供的列表格式销量数据 ===")
    print(f"文件路径: {file_path}")
    print("销量数据格式: 列表")
    print(f"销量数据条目数: {len(sales_data)}")
    
    # 显示销量数据样例
    print("\n销量数据样例:")
    for i, item in enumerate(sales_data[:3]):
        print(f"  {i+1}. {item}")
    if len(sales_data) > 3:
        print(f"  ... 还有 {len(sales_data) - 3} 条数据")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"\n❌ 错误：文件不存在 {file_path}")
        print("请确保Excel文件存在于当前目录")
        return
    
    try:
        # 处理数据
        print(f"\n开始处理数据...")
        data_pro.main(file_path, sales_data)
        
        print(f"\n✅ 处理完成！")
        print("输出文件包含以下工作表:")
        print("  - 周度销量数据: 包含销量、退货数量等信息")
        print("  - 客户问题分析: 包含问题总结和分析")
        
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        print("请检查文件格式和数据是否正确")

if __name__ == "__main__":
    main()