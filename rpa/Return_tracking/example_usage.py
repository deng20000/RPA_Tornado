"""
退货追踪数据处理模块使用示例

本文件展示了如何使用 Return_tracking_processing.py 模块
来处理退货订单数据并生成Excel报告。
"""

from Return_tracking_processing import process_orders, export_to_excel
import json
from datetime import datetime


def create_sample_data():
    """
    创建示例数据文件
    
    生成一个包含不同地区和平台订单的示例JSON文件，
    用于测试和演示模块功能。
    """
    sample_data = [
        {
            "id": "order_001",
            "fields": {
                "shopify站点": [{"name": "Amazon US"}],
                "订单号": "US-12345",
                "产品型号": [{"name": "iPhone-Case-001"}],
                "数量": "2",
                "购买渠道": {"name": "Amazon官网"},
                "退货时间": str(int(datetime(2024, 1, 15).timestamp() * 1000)),
                "购买时间": str(int(datetime(2024, 1, 10).timestamp() * 1000)),
                "退货点": "美国仓库",
                "客户是否寄回(寄回单号）": "已寄回-TR123456"
            }
        },
        {
            "id": "order_002", 
            "fields": {
                "Shopify站点": [{"name": "Amazon UK"}],
                "订单号": "UK-67890",
                "产品型号": [{"name": "Phone-Holder-002"}],
                "数量": "1",
                "购买渠道": {"name": "Amazon英国"},
                "退货时间": str(int(datetime(2024, 1, 20).timestamp() * 1000)),
                "购买时间": str(int(datetime(2024, 1, 12).timestamp() * 1000)),
                "退货点": "英国仓库",
                "客户是否寄回(寄回单号）": "未寄回"
            }
        },
        {
            "id": "order_003",
            "fields": {
                "shopify_site": [{"name": "Amazon DE"}],
                "订单号": "DE-11111",
                "产品型号": [{"name": "Wireless-Charger-003"}],
                "数量": "3",
                "购买渠道": {"name": "Amazon德国"},
                "退货时间": str(int(datetime(2024, 1, 25).timestamp() * 1000)),
                "购买时间": str(int(datetime(2024, 1, 18).timestamp() * 1000)),
                "退货点": "德国仓库",
                "客户是否寄回(寄回单号）": "已寄回-TR789012"
            }
        },
        {
            "id": "order_004",
            "fields": {
                "shopify站点": [{"name": "Shopify US Store"}],
                "订单号": "SP-US-001",
                "产品型号": [{"name": "Bluetooth-Speaker-004"}],
                "数量": "1",
                "购买渠道": {"name": "Shopify官网"},
                "退货时间": str(int(datetime(2024, 1, 28).timestamp() * 1000)),
                "购买时间": str(int(datetime(2024, 1, 22).timestamp() * 1000)),
                "退货点": "美国Shopify仓库",
                "客户是否寄回(寄回单号）": "处理中"
            }
        },
        {
            "id": "order_005",
            "fields": {
                "Shopify站点": [{"name": "Shopify UK Store"}],
                "订单号": "SP-UK-001",
                "产品型号": [{"name": "Smart-Watch-005"}],
                "数量": "2",
                "购买渠道": {"name": "Shopify英国"},
                "退货时间": str(int(datetime(2024, 2, 1).timestamp() * 1000)),
                "购买时间": str(int(datetime(2024, 1, 25).timestamp() * 1000)),
                "退货点": "英国Shopify仓库",
                "客户是否寄回(寄回单号）": "已寄回-TR345678"
            }
        }
    ]
    
    # 保存示例数据到文件
    with open('sample_data.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    print("示例数据文件 'sample_data.json' 已创建")
    return sample_data


def basic_usage_example():
    """
    基本使用示例：处理JSON文件并生成Excel报告
    """
    print("=== 基本使用示例（从文件） ===")
    
    # 1. 处理订单数据
    results = process_orders('test.json')
    
    # 2. 查看统计结果
    print(f"亚马逊美国订单数量: {len(results['US_orders'])}")
    print(f"亚马逊欧洲订单数量: {len(results['EU_orders'])}")
    print(f"亚马逊英国订单数量: {len(results['UK_orders'])}")
    print(f"Shopify美国订单数量: {len(results['shopfiy_US'])}")
    print(f"Shopify欧洲订单数量: {len(results['shopfiy_EU'])}")
    print(f"Shopify英国订单数量: {len(results['shopfiy_UK'])}")
    
    # 3. 导出到Excel
    export_to_excel(results)
    print("Excel文件已生成完成！")


def list_usage_example():
    """
    列表使用示例：直接传入数据列表并生成Excel报告
    """
    print("=== 列表使用示例（从数据列表） ===")
    
    # 1. 准备示例数据列表（格式与test.json相同）
    sample_data = [
        {
            "订单号": "US-12345",
            "产品型号": [{"name": "产品A"}],
            "数量": 2,
            "购买渠道": {"name": "Amazon US"},
            "退货时间": "1640995200000",  # 2022-01-01
            "购买时间": "1640908800000",  # 2021-12-31
            "退货点": "美国仓库",
            "客户是否寄回(寄回单号）": "已寄回-US123"
        },
        {
            "订单号": "UK-67890",
            "产品型号": [{"name": "产品B"}],
            "数量": 1,
            "购买渠道": {"name": "Amazon UK"},
            "退货时间": "1641081600000",  # 2022-01-02
            "购买时间": "1640995200000",  # 2022-01-01
            "退货点": "英国仓库",
            "客户是否寄回(寄回单号）": "未寄回"
        },
        {
            "订单号": "EU-11111",
            "产品型号": [{"name": "产品C"}],
            "数量": 3,
            "购买渠道": {"name": "Amazon DE"},
            "退货时间": "1641168000000",  # 2022-01-03
            "购买时间": "1641081600000",  # 2022-01-02
            "退货点": "德国仓库",
            "客户是否寄回(寄回单号）": "已寄回-DE456"
        },
        {
            "订单号": "SHOP-US-22222",
            "产品型号": [{"name": "产品D"}],
            "数量": 1,
            "购买渠道": {"name": "Shopify US"},
            "退货时间": "1641254400000",  # 2022-01-04
            "购买时间": "1641168000000",  # 2022-01-03
            "退货点": "美国Shopify仓库",
            "客户是否寄回(寄回单号）": "已寄回-SHOP789"
        }
    ]
    
    # 2. 处理数据列表
    results = process_orders(sample_data)
    
    # 3. 查看统计结果
    print(f"亚马逊美国订单数量: {len(results['US_orders'])}")
    print(f"亚马逊欧洲订单数量: {len(results['EU_orders'])}")
    print(f"亚马逊英国订单数量: {len(results['UK_orders'])}")
    print(f"Shopify美国订单数量: {len(results['shopfiy_US'])}")
    print(f"Shopify欧洲订单数量: {len(results['shopfiy_EU'])}")
    print(f"Shopify英国订单数量: {len(results['shopfiy_UK'])}")
    
    # 4. 导出到Excel
    export_to_excel(results)
    print("从数据列表生成的Excel文件已完成！")


def advanced_usage_example():
    """
    高级使用示例
    
    演示如何进行更复杂的数据处理：
    1. 自定义数据验证
    2. 批量处理多个文件
    3. 生成详细报告
    """
    print("\n=== 高级使用示例 ===")
    
    # 创建示例数据
    sample_data = create_sample_data()
    
    # 处理数据
    results = process_orders('sample_data.json')
    
    # 生成详细报告
    print("\n详细分析报告:")
    print("-" * 50)
    
    total_orders = sum(len(orders) for orders in results.values())
    print(f"总订单数量: {total_orders}")
    
    # 按平台统计
    amazon_total = len(results['US_orders']) + len(results['EU_orders']) + len(results['UK_orders'])
    shopify_total = len(results['shopfiy_US']) + len(results['shopfiy_EU']) + len(results['shopfiy_UK'])
    
    print(f"亚马逊平台订单: {amazon_total} 条 ({amazon_total/total_orders*100:.1f}%)")
    print(f"Shopify平台订单: {shopify_total} 条 ({shopify_total/total_orders*100:.1f}%)")
    
    # 按地区统计
    us_total = len(results['US_orders']) + len(results['shopfiy_US'])
    eu_total = len(results['EU_orders']) + len(results['shopfiy_EU'])
    uk_total = len(results['UK_orders']) + len(results['shopfiy_UK'])
    
    print(f"\n地区分布:")
    print(f"美国地区: {us_total} 条 ({us_total/total_orders*100:.1f}%)")
    print(f"欧洲地区: {eu_total} 条 ({eu_total/total_orders*100:.1f}%)")
    print(f"英国地区: {uk_total} 条 ({uk_total/total_orders*100:.1f}%)")
    
    # 导出Excel
    export_to_excel(results)
    
    print("\n✅ 高级使用示例完成！")


def error_handling_example():
    """
    错误处理示例
    
    演示如何处理各种可能的错误情况：
    1. 文件不存在
    2. JSON格式错误
    3. 数据字段缺失
    """
    print("\n=== 错误处理示例 ===")
    
    # 1. 处理文件不存在的情况
    print("\n1. 测试文件不存在的情况:")
    try:
        results = process_orders('nonexistent_file.json')
    except Exception as e:
        print(f"   捕获到预期错误: {type(e).__name__}")
    
    # 2. 创建格式错误的JSON文件
    print("\n2. 测试JSON格式错误的情况:")
    with open('invalid.json', 'w', encoding='utf-8') as f:
        f.write('{"invalid": json format}')  # 故意写错误的JSON
    
    try:
        results = process_orders('invalid.json')
    except Exception as e:
        print(f"   捕获到预期错误: {type(e).__name__}")
    
    # 3. 创建空文件
    print("\n3. 测试空文件的情况:")
    with open('empty.json', 'w', encoding='utf-8') as f:
        f.write('')
    
    try:
        results = process_orders('empty.json')
    except Exception as e:
        print(f"   捕获到预期错误: {type(e).__name__}")
    
    # 清理测试文件
    import os
    for file in ['invalid.json', 'empty.json']:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n✅ 错误处理示例完成！")


if __name__ == "__main__":
    """
    运行所有示例
    """
    print("🚀 退货追踪数据处理模块使用示例")
    print("=" * 50)
    
    try:
        # 运行基本使用示例（从文件）
        basic_usage_example()
        
        print("\n" + "=" * 50)
        
        # 运行列表使用示例（从数据列表）
        list_usage_example()
        
        print("\n" + "=" * 50)
        
        # 运行高级使用示例
        advanced_usage_example()
        
        print("\n" + "=" * 50)
        
        # 运行错误处理示例
        error_handling_example()
        
    except Exception as e:
        print(f"❌ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 所有示例运行完成！")