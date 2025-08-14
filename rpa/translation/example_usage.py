#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例：演示如何正确使用data_pro.py中的功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_pro

def example_basic_usage():
    """示例1: 基本使用方法（不带销量数据）"""
    print("=== 示例1: 基本使用方法 ===")
    
    # 构建完整的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "2025年06月16日退货订单(2).xlsx")
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        try:
            result = data_pro.main(file_path)
            print(f"处理结果: {result}")
        except Exception as e:
            print(f"处理失败: {e}")
    else:
        print(f"文件不存在: {file_path}")

def example_with_custom_file():
    """示例2: 使用自定义文件路径"""
    print("\n=== 示例2: 使用自定义文件路径 ===")
    
    # 构建完整的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "2025年06月16日退货订单(2).xlsx")
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        try:
            result = data_pro.main(file_path)
            print(f"处理结果: {result}")
        except Exception as e:
            print(f"处理失败: {e}")
    else:
        print(f"文件不存在: {file_path}")

def example_with_sales_data():
    """示例3: 使用销量数据（字典格式）"""
    print("\n=== 示例3: 使用销量数据（字典格式） ===")
    
    # 销量数据示例（字典格式）
    sales_data = {
        "GL-BE3600": {
            "EU Amazon": 1000,
            "US Amazon": 800
        },
        "GL-X2000": {
            "EU Amazon": 1200,
            "US Amazon": 900
        }
    }
    
    # 构建完整的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "2025年06月16日退货订单(2).xlsx")
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        try:
            # 使用销量数据处理
            data_pro.main(file_path, sales_data)
            print(f"✅ 文件 {file_path} 处理完成（带销量数据）")
        except Exception as e:
            print(f"❌ 处理失败: {e}")
    else:
        print(f"❌ 文件不存在: {file_path}")
        print("请确保文件存在后重试")

def example_with_list_sales_data():
    """示例4: 使用销量数据（列表格式）"""
    print("\n=== 示例4: 使用销量数据（列表格式） ===")
    
    # 销量数据示例（列表格式）- 用户提供的格式
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
    
    # 构建完整的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "2025年06月16日退货订单(2).xlsx")
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        try:
            # 使用销量数据处理
            data_pro.main(file_path, sales_data)
            print(f"✅ 文件 {file_path} 处理完成（带列表格式销量数据）")
        except Exception as e:
            print(f"❌ 处理失败: {e}")
    else:
        print(f"❌ 文件不存在: {file_path}")
        print("请确保文件存在后重试")

def example_direct_function_call():
    """示例5: 直接调用process_fba_returns函数"""
    print("\n=== 示例5: 直接调用process_fba_returns函数 ===")
    
    # 构建文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "2025年06月16日退货订单(2).xlsx")
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        try:
            # 不带销量数据
            data_pro.process_fba_returns(file_path)
            print("✅ 直接调用成功")
        except Exception as e:
            print(f"❌ 直接调用失败: {e}")
    else:
        print(f"❌ 文件不存在: {file_path}")

def example_error_handling():
    """示例6: 错误处理演示"""
    print("\n=== 示例6: 错误处理演示 ===")
    
    # 演示错误的参数类型
    print("演示错误的参数类型:")
    try:
        # 这会引发TypeError
        data_pro.process_fba_returns({"file": "test.xlsx"})
    except TypeError as e:
        print(f"✅ 正确捕获参数类型错误: {e}")
    
    try:
        # 这也会引发TypeError
        data_pro.process_fba_returns("test.xlsx", "not_a_dict")
    except TypeError as e:
        print(f"✅ 正确捕获sales_data类型错误: {e}")

if __name__ == "__main__":
    print("=== data_pro.py 使用示例 ===")
    
    # 运行所有示例
    example_basic_usage()
    example_with_custom_file()
    example_with_sales_data()
    example_with_list_sales_data()
    example_direct_function_call()
    example_error_handling()
    
    print("\n=== 所有示例完成 ===")
    print("\n使用说明:")
    print("1. 基本使用: data_pro.main()")
    print("2. 自定义文件: data_pro.main('your_file.xlsx')")
    print("3. 带销量数据: data_pro.main('your_file.xlsx', sales_dict)")
    print("4. 直接调用: data_pro.process_fba_returns(file_path, sales_data)")
    print("5. 确保file_path是字符串，sales_data是字典或None")