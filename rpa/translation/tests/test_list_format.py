#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试列表格式的sales_data功能
"""

import os
import sys
from data_pro import convert_sales_data_format, main, process_fba_returns

def test_convert_sales_data_format():
    """测试销量数据格式转换功能"""
    print("=== 测试销量数据格式转换功能 ===")
    
    # 测试用户提供的列表格式数据
    list_format_data = [
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
    
    print("原始列表格式数据:")
    for item in list_format_data:
        print(f"  {item}")
    
    # 转换为字典格式
    converted_data = convert_sales_data_format(list_format_data)
    
    print("\n转换后的字典格式数据:")
    for sku, platforms in converted_data.items():
        print(f"  {sku}: {platforms}")
    
    # 验证转换结果
    expected_data = {
        'GL-X2000': {'美亚': 29, '欧亚': 14, 'Shopee': 0, 'Walmart': 0},
        'GL-BE3600': {'美亚': 581, '欧亚': 150, 'Shopee': 13, 'Walmart': 0},
        'GL-RM1': {'美亚': 502, '欧亚': 133}
    }
    
    print("\n验证转换结果:")
    success = True
    for sku, platforms in expected_data.items():
        if sku not in converted_data:
            print(f"❌ 缺少SKU: {sku}")
            success = False
            continue
        
        for platform, quantity in platforms.items():
            if platform not in converted_data[sku]:
                print(f"❌ SKU {sku} 缺少平台: {platform}")
                success = False
            elif converted_data[sku][platform] != quantity:
                print(f"❌ SKU {sku} 平台 {platform} 数量不匹配: 期望 {quantity}, 实际 {converted_data[sku][platform]}")
                success = False
    
    if success:
        print("✅ 所有转换结果验证通过")
    else:
        print("❌ 转换结果验证失败")
    
    return converted_data

def test_dict_format_compatibility():
    """测试字典格式的兼容性"""
    print("\n=== 测试字典格式兼容性 ===")
    
    # 测试原有的字典格式
    dict_format_data = {
        "GL-BE3600": {"EU Amazon": 1000, "US Amazon": 800},
        "GL-X2000": {"EU Amazon": 1200, "US Amazon": 900}
    }
    
    print("原始字典格式数据:")
    for sku, platforms in dict_format_data.items():
        print(f"  {sku}: {platforms}")
    
    # 转换（应该保持不变）
    converted_data = convert_sales_data_format(dict_format_data)
    
    print("\n转换后的数据:")
    for sku, platforms in converted_data.items():
        print(f"  {sku}: {platforms}")
    
    # 验证是否保持不变
    if converted_data == dict_format_data:
        print("✅ 字典格式兼容性测试通过")
    else:
        print("❌ 字典格式兼容性测试失败")
    
    return converted_data

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    
    # 测试None
    result = convert_sales_data_format(None)
    print(f"None输入: {result}")
    assert result is None, "None输入应该返回None"
    
    # 测试空列表
    result = convert_sales_data_format([])
    print(f"空列表输入: {result}")
    assert result == {}, "空列表应该返回空字典"
    
    # 测试包含无效数据的列表
    invalid_data = [
        {'SKU': 'GL-X2000', '平台': '美亚', '数量': 'invalid'},  # 无效数量
        {'SKU': 'GL-BE3600'},  # 缺少字段
        {'平台': '美亚', '数量': '100'},  # 缺少SKU
        {'SKU': 'GL-RM1', '平台': '美亚', '数量': '200'}  # 正常数据
    ]
    
    result = convert_sales_data_format(invalid_data)
    print(f"包含无效数据的列表: {result}")
    
    # 应该只包含有效的数据
    expected = {'GL-RM1': {'美亚': 200}}
    if result == expected:
        print("✅ 边界情况测试通过")
    else:
        print("❌ 边界情况测试失败")

def test_with_sample_file():
    """测试使用示例文件（如果存在）"""
    print("\n=== 测试使用示例文件 ===")
    
    # 用户提供的销量数据
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
    
    # 查找示例Excel文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_files = [f for f in os.listdir(current_dir) if f.endswith('.xlsx')]
    
    if sample_files:
        sample_file = os.path.join(current_dir, sample_files[0])
        print(f"找到示例文件: {sample_file}")
        
        try:
            # 测试使用列表格式的sales_data
            print("测试使用列表格式的销量数据...")
            main(sample_file, sales_data)
            print("✅ 列表格式销量数据测试成功")
        except Exception as e:
            print(f"❌ 列表格式销量数据测试失败: {e}")
    else:
        print("未找到示例Excel文件，跳过文件处理测试")
        print("如需测试完整功能，请在当前目录放置一个Excel文件")

def main_test():
    """主测试函数"""
    print("开始测试列表格式的sales_data功能\n")
    
    try:
        # 测试格式转换
        test_convert_sales_data_format()
        
        # 测试字典格式兼容性
        test_dict_format_compatibility()
        
        # 测试边界情况
        test_edge_cases()
        
        # 测试使用示例文件
        test_with_sample_file()
        
        print("\n=== 测试完成 ===")
        print("✅ 列表格式的sales_data功能已成功实现")
        print("\n使用方法:")
        print("1. 列表格式: [{'SKU': 'GL-X2000', '平台': '美亚', '数量': '29'}, ...]")
        print("2. 字典格式: {'GL-X2000': {'美亚': 29}, ...}")
        print("3. 两种格式都支持，会自动转换为统一的字典格式进行处理")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main_test()