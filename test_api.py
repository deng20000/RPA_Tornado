import requests
import json

def test_order_profit_api():
    url = "http://127.0.0.1:8888/api/basicOpen/finance/mreport/OrderProfit"
    
    # 测试数据1：最小参数
    data1 = {
        "startDate": "2024-07-17",
        "endDate": "2025-07-17"
    }
    
    # 测试数据2：完整参数
    data2 = {
        "offset": 0,
        "length": 100,
        "sids": [511633],
        "startDate": "2025-07-17",
        "endDate": "2025-07-17",
        "searchField": "seller_sku",
        "searchValue": ["GL-BE3600"]
    }
    
    headers = {"Content-Type": "application/json"}
    
    print("=== 测试1：最小参数 ===")
    try:
        response1 = requests.post(url, json=data1, headers=headers)
        print(f"状态码: {response1.status_code}")
        print(f"响应: {response1.json()}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n=== 测试2：完整参数 ===")
    try:
        response2 = requests.post(url, json=data2, headers=headers)
        print(f"状态码: {response2.status_code}")
        print(f"响应: {response2.json()}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_order_profit_api() 