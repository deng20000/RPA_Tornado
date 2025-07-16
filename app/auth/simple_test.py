#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Lingxing API 演示模块
# 作用 : 查看订单 - 订单管理模块内容

该模块演示如何使用 Lingxing OpenAPI 进行以下操作：
1. 获取访问令牌
2. 查询订单列表
3. 处理API响应数据

示例用法：
    python demo.py
"""

import asyncio
from typing import Dict, Any
import sys,os

# # 获取当前文件所在目录
# current_dir = os.path.dirname(os.path.abspath(__file__))

# # 获取父目录（项目根目录）
# project_root = os.path.dirname(current_dir)
# sys.path.append(os.path.join(project_root, 'Lingxing_Auth'))

# 获取时间戳
from time import time
from datetime import datetime,timedelta
# from openapi import OpenApiBase
from openapi import OpenApiBase

async def main() -> None:
    """Lingxing API 主演示函数
    
    功能：
    1. 初始化API客户端
    2. 获取访问令牌
    3. 查询订单数据
    4. 处理并保存响应数据
    
    异常：
    - ValueError: 当缺少必要凭证时抛出
    - Exception: 处理API请求时的各种错误
    """
    # 从环境变量获取凭证(更安全)
    import os
    # HOST = os.getenv('API_HOST', "https://api.example.com")  # 默认值可替换
    # APP_ID = os.getenv('APP_ID')            # 必须设置
    # APP_SECRET = os.getenv('APP_SECRET')    # 必须设置
    HOST = "https://openapi.lingxing.com"
    APP_ID ="ak_LmR8frklEqfe2"
    APP_SECRET = "gS/Qn/dLNtD9qKwYaBLkZA=="
    if not all([APP_ID, APP_SECRET]):
        raise ValueError("请设置APP_ID和APP_SECRET环境变量")
    
    # 初始化客户端
    api = OpenApiBase(HOST, APP_ID, APP_SECRET)
    print(f"[demo.py] HOST: {HOST}")
    print(f"[demo.py] APP_ID: {APP_ID}")
    print(f"[demo.py] APP_SECRET: {APP_SECRET}")
    try:
        # 1. 获取访问令牌
        token = await api.generate_access_token()
        print(f"[demo.py] Access Token: {token.access_token}")
        print(f"[demo.py] Expires in: {token.expires_in}秒")
        
        
        end_time = int(time())
        # 获取昨天时间
        yesterday = datetime.now() - timedelta(days=10)

        # 获取时间戳（单位：秒）
        start_time = int(yesterday.timestamp())

        print("昨天的开始时间戳（秒）:", start_time)
        print("昨天的结束时间戳（秒）:", end_time)
        # print("昨天的时间戳为（秒）:", timestamp)
        # print("昨天的时间戳为：", timestamp) 
        query_data = {
            "offset": 0,
            "length": 20,
            # 为订购时间
            "date_type": "global_purchase_time",
            "start_time": start_time,
            "end_time": end_time,
            "platform_code": [i for i in range(10001,10039)],
            "order_status": 5
        }
        print("[demo.py] 请求参数:", query_data)
        response = await api.request(
            access_token=token.access_token,
            route_name="/pb/mp/order/v2/list",
            # route_name="/erp/sc/routing/order/Order/getOrderDetail",
            method="POST",
            req_body=query_data
        )
        
        # 3. 打印完整响应数据并保存到文件
        from pprint import pprint
        import json
        print("订单详情响应数据:")
        response_data = response.model_dump()
        pprint(response_data)
        # 查看数据长度
        print(f"响应数据长度: {len(response_data['data'])}条订单")
        
        # 保存数据到test.json
        with open('test.json', 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        print("数据已保存到test.json")
        
        # 保存比对信息
        import json as _json
        compare_info = {
            "access_token": token.access_token,
            "query_data": query_data,
            "sign_raw": sign_str if 'sign_str' in locals() else None,
            "sign": sign if 'sign' in locals() else None,
            "response": response.model_dump() if hasattr(response, 'model_dump') else str(response)
        }
        with open('compare_demo.json', 'w', encoding='utf-8') as f:
            _json.dump(compare_info, f, ensure_ascii=False, indent=2)

    except ValueError as ve:
        print("\n[配置错误] 缺少必要凭证:")
        print(f"- {str(ve)}")
        print("解决方案: 请设置正确的APP_ID和APP_SECRET环境变量")
    except asyncio.TimeoutError:
        print("\n[网络错误] 请求超时")
        print("解决方案: 检查网络连接或增加超时时间")
    except Exception as e:
        import traceback
        print("\n=== 错误详情 ===")
        print(f"[{type(e).__name__}] {str(e)}")
        print("\n=== 完整堆栈 ===")
        traceback.print_exc()
        print("\n=== 调试建议 ===")
        print("1. 检查API端点URL是否正确")
        print("2. 验证访问令牌是否有效")
        print("3. 检查请求参数格式")
        print("4. 联系Lingxing技术支持")

if __name__ == '__main__':
    asyncio.run(main())