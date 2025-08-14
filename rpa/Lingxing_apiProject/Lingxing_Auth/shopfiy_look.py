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
import json
# 获取时间戳
from time import time
from datetime import datetime,timedelta
# from openapi import OpenApiBase
from openapi import OpenApiBase

async def main() -> None:
    
        
    # 1. 查询订单数据总量
    # 1.1获取仓库请求route和请求体
    warehouse_query_route_name,warehouse_query_data = get_warehouse_request_body()
    # 1.2 获取店铺请求route和请求体
    glinet_route_name, glinet_query_data = get_glinet_accounts()
    # 1.3 调用API请求
    return_warehouse_query_data = await api_request(warehouse_query_route_name, warehouse_query_data)
    return_glinet_query_data = await api_request(glinet_route_name, glinet_query_data)
    print(f"店铺订单总数: {return_warehouse_query_data['total']}，店铺订单总数: {return_glinet_query_data['total']}")
    # 2.1 查看总数 total
    if return_warehouse_query_data['total'] != -1 and return_glinet_query_data['total'] != -1:
        print(f"仓库订单总数: {return_warehouse_query_data['total']}，店铺订单总数: {return_glinet_query_data['total']}")
        # 2.2 实际获取到数据量
        len_warehouse_data = len(return_warehouse_query_data['data'])
        len_glinet_data = len(return_glinet_query_data['data'])
        print(f"仓库实际订单数据量: {len_warehouse_data}，GL.iNet店铺实际订单数据量: {len_glinet_data}")
        # warehouse_data 最大800条,glinet_data 最大200条
        # 2.3 如果实际数据量与总数不一致，可能需要翻页获取
        max_warehouse_length = 800
        max_glinet_length = 200
        
        warehouse_need_page = return_warehouse_query_data["total"] // max_warehouse_length + 1
        glinet_need_page = return_glinet_query_data["total"] // max_glinet_length + 1
        print(f"仓库订单需要翻页获取: {warehouse_need_page}页，GL.iNet店铺订单需要翻页获取: {glinet_need_page}页")
        warehouse_data = []
        # 2.4 仓库开始页数
        for _ in range(1, warehouse_need_page + 1):
            # 设置偏移量
            start_offset = (_ - 1) * max_warehouse_length
            print(f"正在获取第{_}页仓库订单数据...")
            warehouse_query_route_name,warehouse_query_data = get_warehouse_request_body(offset=start_offset, length=max_warehouse_length)
            return_warehouse_query_data = await api_request(warehouse_query_route_name, warehouse_query_data)
            warehouse_data+= return_warehouse_query_data['data']
        with open('warehouse_order_list.json', 'w', encoding='utf-8') as f:
            json.dump(warehouse_data, f, ensure_ascii=False, indent=4)
        print("仓库订单数据已保存到 warehouse_order_list.json")
        
        glinet_data = []
        # 2.5 GL.iNet店铺开始页数
        for _ in range(1, glinet_need_page + 1):
            # 设置偏移量
            start_page = (_ - 1) * max_glinet_length
            print(f"正在获取第{_}页GL.iNet店铺订单数据...")
            glinet_route_name, glinet_query_data = get_glinet_accounts(page=start_page, length=max_glinet_length)
            return_glinet_query_data = await api_request(glinet_route_name, glinet_query_data)
            glinet_data+= return_glinet_query_data['data']
        # 进行覆盖写入
        # 2.6 保存GL.iNet店铺订单数据
        with open('glinet_order_list.json', 'w', encoding='utf-8') as f:
            json.dump(glinet_data, f, ensure_ascii=False, indent=4)
        print("仓库订单数据已保存到 warehouse_order_list.json")
        
        # 2.7 打印订单总数
        print(f"仓库订单总数: {len(warehouse_data)}，GL.iNet店铺订单总数: {len(glinet_data)}")
        print("所有订单数据已成功获取并保存到JSON文件中")
        # 清洗数据
        # 3.1 清洗数据
        
        
    else:
        print("店铺订单总数查询失败")
        
        

async def api_request(route_name: str, query_data: Dict[str, Any]) -> Dict[Any,Any]:
    """Lingxing API 主演示函数
    
    功能：
    1. 初始化API客户端
    2. 获取访问令牌
    3. 查询订单数据
    4. 处理并保存响应数据 到JSON文件
    
    异常：
    - ValueError: 当缺少必要凭证时抛出
    - Exception: 处理API请求时的各种错误
    
    正常返回请求体，异常返回 {"total":-1}
    """
    HOST = "https://openapi.lingxing.com"
    APP_ID ="ak_LmR8frklEqfe2"
    APP_SECRET = "gS/Qn/dLNtD9qKwYaBLkZA=="
    if not all([APP_ID, APP_SECRET]):
        raise ValueError("请设置APP_ID和APP_SECRET环境变量")
    
    # 初始化客户端
    api = OpenApiBase(HOST, APP_ID, APP_SECRET)    
    try:
        # 1. 获取访问令牌
        token = await api.generate_access_token()
        print(f"Access Token: {token.access_token}")
        print(f"Expires in: {token.expires_in}秒")
    # 这里可以添加实际的API请求逻辑
    # 例如使用requests库发送POST请求
        response = await api.request(
            access_token=token.access_token,
            route_name=route_name,
            method="POST",
            req_body=query_data
        )
        response_data = response.model_dump()
        print(f"数据总数为:", response_data.get('total', '未知'))
        return response_data
    except ValueError as ve:
        print("\n[配置错误] 缺少必要凭证:")
        print(f"- {str(ve)}")
        return {"total":-1}
    except asyncio.TimeoutError:
        print("\n[网络错误] 请求超时")
        print("解决方案: 检查网络连接或增加超时时间")
        return {"total":-2}
    except Exception as e:
        import traceback
        print(f"[{type(e).__name__}] {str(e)}")
        print("\n=== 完整堆栈 ===")
        traceback.print_exc()
        return {"total":-3}
    # finally:
    #     return {"total":-1}

def get_date_range():
    # 获取昨天的日期
    yesterday = datetime.now() - timedelta(days=1)
    
    # 获取昨天所在月份的1号
    start_date = yesterday.replace(day=1)
    
    # 格式化成 "Y-m-d"
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = yesterday.strftime("%Y-%m-%d")
    
    return start_str, end_str

def get_warehouse_request_body(offset: int = 0, length: int = 20):
    route_name = "/erp/sc/routing/data/local_inventory/inventoryDetails	"
    warehouses = {
        "电商仓库": 507895,
        "4PX-英国路腾仓": 517681,
        "4PX-加拿大温哥华仓": 517680,
        "4PX-美国洛杉矶1仓": 508971,
        "4PX-德国法兰克福仓": 508964
        }
    
    query_data = {
            "wid":list(warehouses.values()),  # 使用仓库ID列表
            "offset": offset,  # 偏移量
            "length":length # default max 800
    }
    return route_name,query_data

def get_glinet_accounts(page: int = 1,length: int = 20):
    """
    返回GL.iNet相关店铺和查询数据字典
        :param page: 页码,默认从第1页开始
        :param length: 每页数量，默认20条
        :return: 返回路由名称和查询数据字典
    """
    
    """获取GL.iNet相关"""
    # SKU维度统计销量 /basicOpen/platformStatisticsV2/saleStat/pageList
    route_name = "/basicOpen/platformStatisticsV2/saleStat/pageList"
    glinet_accounts = {
            "gl-inet": 110281641666737664,
            "GL.iNet UK": 110425257270190592,
            "GL.iNet CA": 110425257626878464,
            "GL.iNet US": 110289025814384640,
            "GL.iNet EU": 110291088764368384
    }
    start_date, end_date = get_date_range()
    #  销量、SKU、、按日、
    query_data = {
        "start_date": start_date,  # 开始日期
        "end_date": end_date,      # 结束日期
        "result_type": "1",  # 销量
        "date_unit": "4",  # 按日统计
        "page":1, # 页码
        "length": length,
        # "length": 1000, # 每页数量 ,后续可以考虑翻页处理,默认可能最大为200
        "data_type":'4', #统计数据维度,SKU = 4
        "sids": list(glinet_accounts.values()),  # 使用账户ID列表
        
    }
    return route_name, query_data

def clean_data(warehouse_file, glinet_data_file):
    """
    清洗数据
    :param warehouse_data: 仓库订单数据
    :param glinet_data: GL.iNet店铺订单数据
    :return: 清洗后的数据
    """
    with open(warehouse_file, 'r', encoding='utf-8') as f:
        warehouse_data = json.load(f)

    # 获取 sku,product_valid_num(可用量),third_inventory>>qty_sellable(可用量)	
    result_warehouse_data = {item['sku']: item['product_valid_num'] for item in warehouse_data}
    print(result_warehouse_data)
    with open('cleaned_warehouse_data.json', 'w', encoding='utf-8') as f:
        json.dump(warehouse_data, f, ensure_ascii=False, indent=4)
    
    with open(glinet_data_file, 'r', encoding='utf-8') as f:
        glinet_data = json.load(f)
    # 获取店铺名称(store_name),sku,quantitySold(销量=总使用量)、spu_name()   
    result_glinet_data = {item['sku'][0]: [item['store_name'], item['volumeTotal'],item['skuAndProductName'][0],item['date_collect']] for item in glinet_data}
    print(result_glinet_data)
    # 进行匹配关系

if __name__ == '__main__':
    # asyncio.run(main())
    clean_data('warehouse_order_list.json', 'glinet_order_list.json')
    