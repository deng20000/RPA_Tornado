#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试销量报表ASIN日列表查询接口
"""

import requests
import json
from datetime import datetime

# API配置
BASE_URL = "http://localhost:8888"
API_ENDPOINT = "/api/multi-platform/sales-report-asin-daily-lists"

def test_sales_report_api():
    """测试销量报表API"""
    
    print("=" * 60)
    print("测试销量报表ASIN日列表查询接口")
    print("=" * 60)
    
    # 测试用例1: 基本查询（按ASIN查询销售额）
    print("\n1. 测试基本查询（按ASIN查询销售额）")
    test_case_1 = {
        "sid": 109,
        "event_date": "2024-08-05"
    }
    print(f"请求参数: {json.dumps(test_case_1, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_1, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例2: 按MSKU查询销量
    print("\n2. 测试按MSKU查询销量")
    test_case_2 = {
        "sid": 109,
        "event_date": "2024-08-05",
        "asin_type": 2,
        "type": 2
    }
    print(f"请求参数: {json.dumps(test_case_2, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_2, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例3: 按ASIN查询订单量，带分页
    print("\n3. 测试按ASIN查询订单量，带分页")
    test_case_3 = {
        "sid": 109,
        "event_date": "2024-08-05",
        "asin_type": 1,
        "type": 3,
        "offset": 10,
        "length": 50
    }
    print(f"请求参数: {json.dumps(test_case_3, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_3, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例4: 参数验证测试 - 缺少必填参数
    print("\n4. 测试参数验证 - 缺少必填参数")
    test_case_4 = {
        "event_date": "2024-08-05"
        # 缺少sid
    }
    print(f"请求参数: {json.dumps(test_case_4, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_4, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例5: 参数验证测试 - 日期格式错误
    print("\n5. 测试参数验证 - 日期格式错误")
    test_case_5 = {
        "sid": 109,
        "event_date": "2024/08/05"  # 错误格式
    }
    print(f"请求参数: {json.dumps(test_case_5, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_5, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例6: 参数验证测试 - 无效的asin_type
    print("\n6. 测试参数验证 - 无效的asin_type")
    test_case_6 = {
        "sid": 109,
        "event_date": "2024-08-05",
        "asin_type": 3  # 无效值
    }
    print(f"请求参数: {json.dumps(test_case_6, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_6, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例7: 参数验证测试 - 无效的type
    print("\n7. 测试参数验证 - 无效的type")
    test_case_7 = {
        "sid": 109,
        "event_date": "2024-08-05",
        "type": 4  # 无效值
    }
    print(f"请求参数: {json.dumps(test_case_7, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               json=test_case_7, 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"请求失败: {e}")
    
    # 测试用例8: 空请求体测试
    print("\n8. 测试空请求体")
    try:
        response = requests.post(f"{BASE_URL}{API_ENDPOINT}", 
                               data="", 
                               headers={'Content-Type': 'application/json'})
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_sales_report_api() 