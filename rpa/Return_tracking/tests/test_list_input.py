#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证数据列表输入功能

该脚本用于测试 process_orders 函数是否能正确处理直接传入的数据列表，
而不仅仅是JSON文件路径。

作者: 系统自动生成
创建时间: 2024年
"""

from Return_tracking_processing import process_orders, export_to_excel


def test_list_input():
    """
    测试直接传入数据列表的功能
    """
    print("=== 测试数据列表输入功能 ===")
    
    # 准备测试数据列表
    test_data = [
        {
            "id": "test_001",
            "fields": {
                "shopify站点": [{"name": "Amazon US"}],
                "订单号": "TEST-US-001",
                "产品型号": [{"name": "测试产品A"}],
                "数量": 1,
                "购买渠道": {"name": "Amazon US"},
                "退货时间": "1640995200000",  # 2022-01-01
                "购买时间": "1640908800000",  # 2021-12-31
                "退货点": "美国测试仓库",
                "客户是否寄回(寄回单号）": "已寄回-TEST001"
            }
        },
        {
            "id": "test_002",
            "fields": {
                "shopify站点": [{"name": "Amazon UK"}],
                "订单号": "TEST-UK-002",
                "产品型号": [{"name": "测试产品B"}],
                "数量": 2,
                "购买渠道": {"name": "Amazon UK"},
                "退货时间": "1641081600000",  # 2022-01-02
                "购买时间": "1640995200000",  # 2022-01-01
                "退货点": "英国测试仓库",
                "客户是否寄回(寄回单号）": "未寄回"
            }
        },
        {
            "id": "test_003",
            "fields": {
                "shopify站点": [{"name": "Amazon DE"}],
                "订单号": "TEST-DE-003",
                "产品型号": [{"name": "测试产品C"}],
                "数量": 3,
                "购买渠道": {"name": "Amazon DE"},
                "退货时间": "1641168000000",  # 2022-01-03
                "购买时间": "1641081600000",  # 2022-01-02
                "退货点": "德国测试仓库",
                "客户是否寄回(寄回单号）": "已寄回-TEST003"
            }
        },
        {
            "id": "test_004",
            "fields": {
                "shopify站点": [{"name": "Shopify US"}],
                "订单号": "TEST-SHOP-US-004",
                "产品型号": [{"name": "测试产品D"}],
                "数量": 1,
                "购买渠道": {"name": "Shopify US"},
                "退货时间": "1641254400000",  # 2022-01-04
                "购买时间": "1641168000000",  # 2022-01-03
                "退货点": "美国Shopify测试仓库",
                "客户是否寄回(寄回单号）": "已寄回-SHOP004"
            }
        },
        {
            "id": "test_005",
            "fields": {
                "shopify站点": [{"name": "Shopify UK"}],
                "订单号": "TEST-SHOP-UK-005",
                "产品型号": [{"name": "测试产品E"}],
                "数量": 2,
                "购买渠道": {"name": "Shopify UK"},
                "退货时间": "1641340800000",  # 2022-01-05
                "购买时间": "1641254400000",  # 2022-01-04
                "退货点": "英国Shopify测试仓库",
                "客户是否寄回(寄回单号）": "未寄回"
            }
        }
    ]
    
    print(f"准备测试数据：{len(test_data)} 条订单")
    
    try:
        # 测试处理数据列表
        print("\n1. 处理数据列表...")
        results = process_orders(test_data)
        
        # 验证结果
        print("\n2. 验证处理结果...")
        total_orders = sum(len(orders) for orders in results.values())
        print(f"总订单数量: {total_orders}")
        
        # 详细统计
        print("\n3. 详细统计结果:")
        print(f"   亚马逊美国订单: {len(results['US_orders'])} 条")
        print(f"   亚马逊欧洲订单: {len(results['EU_orders'])} 条")
        print(f"   亚马逊英国订单: {len(results['UK_orders'])} 条")
        print(f"   Shopify美国订单: {len(results['shopfiy_US'])} 条")
        print(f"   Shopify欧洲订单: {len(results['shopfiy_EU'])} 条")
        print(f"   Shopify英国订单: {len(results['shopfiy_UK'])} 条")
        
        # 验证预期结果
        expected_counts = {
            'US_orders': 1,      # Amazon US
            'EU_orders': 1,      # Amazon DE
            'UK_orders': 1,      # Amazon UK
            'shopfiy_US': 1,     # Shopify US
            'shopfiy_EU': 0,     # Shopify EU (无数据)
            'shopfiy_UK': 1      # Shopify UK
        }
        
        print("\n4. 验证预期结果:")
        all_correct = True
        for key, expected in expected_counts.items():
            actual = len(results[key])
            status = "✅" if actual == expected else "❌"
            print(f"   {key}: 预期 {expected}, 实际 {actual} {status}")
            if actual != expected:
                all_correct = False
        
        if all_correct:
            print("\n✅ 所有测试通过！数据列表输入功能正常工作。")
        else:
            print("\n❌ 部分测试失败，请检查数据处理逻辑。")
        
        # 测试导出Excel功能
        print("\n5. 测试Excel导出...")
        export_to_excel(results)
        print("✅ Excel导出测试完成")
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


def test_error_handling():
    """
    测试错误处理功能
    """
    print("\n=== 测试错误处理功能 ===")
    
    # 测试1：传入空列表
    print("\n1. 测试空列表...")
    try:
        results = process_orders([])
        total = sum(len(orders) for orders in results.values())
        print(f"✅ 空列表处理成功，总订单数: {total}")
    except Exception as e:
        print(f"❌ 空列表处理失败: {e}")
    
    # 测试2：传入错误的数据类型
    print("\n2. 测试错误数据类型...")
    try:
        results = process_orders(123)  # 传入数字
        print("❌ 应该抛出异常但没有")
    except (TypeError, ValueError) as e:
        print(f"✅ 正确捕获类型错误: {e}")
    except Exception as e:
        print(f"⚠️ 捕获了其他异常: {e}")
    
    # 测试3：传入格式错误的列表
    print("\n3. 测试格式错误的列表...")
    try:
        invalid_data = [{"invalid": "data"}]
        results = process_orders(invalid_data)
        print("✅ 格式错误的数据处理完成（可能跳过无效订单）")
    except Exception as e:
        print(f"⚠️ 格式错误数据处理异常: {e}")


if __name__ == "__main__":
    """
    运行所有测试
    """
    print("🧪 开始测试数据列表输入功能")
    print("=" * 60)
    
    # 运行主要功能测试
    test_list_input()
    
    # 运行错误处理测试
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试完成！")
    print("请检查生成的Excel文件以验证导出功能。")