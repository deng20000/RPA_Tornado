#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试错误处理脚本：验证参数类型检查是否正常工作
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_pro

def test_parameter_type_checking():
    """测试参数类型检查功能"""
    print("=== 测试参数类型检查 ===")
    
    # 测试1: 传递字典作为file_path（这应该会引发错误）
    print("\n测试1: 传递字典作为file_path")
    try:
        data_pro.process_fba_returns({"file": "test.xlsx"})
        print("❌ 应该引发TypeError，但没有")
    except TypeError as e:
        print(f"✅ 正确捕获TypeError: {e}")
    except Exception as e:
        print(f"❌ 捕获了意外的错误: {e}")
    
    # 测试2: 传递正确的文件路径和错误的sales_data类型
    print("\n测试2: 传递错误的sales_data类型")
    try:
        data_pro.process_fba_returns("test.xlsx", "not_a_dict")
        print("❌ 应该引发TypeError，但没有")
    except TypeError as e:
        print(f"✅ 正确捕获TypeError: {e}")
    except Exception as e:
        print(f"❌ 捕获了意外的错误: {e}")
    
    # 测试3: 传递正确的参数类型
    print("\n测试3: 传递正确的参数类型")
    try:
        # 这会因为文件不存在而失败，但不会因为参数类型而失败
        data_pro.process_fba_returns("nonexistent.xlsx", {"product1": 100})
        print("❌ 应该因为文件不存在而失败")
    except FileNotFoundError:
        print("✅ 正确处理文件不存在的情况")
    except TypeError as e:
        print(f"❌ 意外的TypeError: {e}")
    except Exception as e:
        print(f"✅ 其他预期的错误: {e}")

def test_main_function():
    """测试main函数的参数处理"""
    print("\n=== 测试main函数参数处理 ===")
    
    # 测试正确的参数类型
    print("\n测试main函数与sales_data参数")
    try:
        result = data_pro.main("nonexistent.xlsx", {"product1": 100})
        print(f"main函数返回: {result}")
    except Exception as e:
        print(f"main函数错误: {e}")

if __name__ == "__main__":
    test_parameter_type_checking()
    test_main_function()
    print("\n=== 测试完成 ===")