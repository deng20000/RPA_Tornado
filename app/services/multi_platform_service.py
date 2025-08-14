# multi_platform_service.py
# 用于多平台相关的业务逻辑
from app.auth.openapi import OpenApiBase
from app.config import settings
from typing import Optional, Dict, Any, List
from datetime import datetime
import json as _json
import os

class MultiPlatformService:
    def __init__(self):
        self.api = OpenApiBase(settings.LLX_API_HOST, settings.LLX_APP_ID, settings.LLX_APP_SECRET)

    async def get_seller_list(
        self,
        access_token: str,
        offset: Optional[int] = None,
        length: Optional[int] = None,
        platform_code: Optional[List[int]] = None,
        is_sync: Optional[int] = None,
        status: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        查询多平台店铺信息 - 支持查询多平台店铺基础信息，其中store_id为多平台店铺唯一
        Args:
            offset: 分页偏移量
            length: 分页长度，上限200
            platform_code: 平台code数组
            is_sync: 店铺同步状态 1-启用 0-停用
            status: 店铺授权状态 1-正常授权 0-授权失败
        Returns:
            dict: 多平台店铺信息数据响应
        """
        # 构建请求参数
        query_data = {}
        if offset is not None:
            query_data["offset"] = offset
        if length is not None:
            query_data["length"] = length
        if platform_code is not None:
            query_data["platform_code"] = platform_code
        if is_sync is not None:
            query_data["is_sync"] = is_sync
        if status is not None:
            query_data["status"] = status

        print(f"[RPA_Tornado] 查询多平台店铺信息 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/pb/mp/shop/v2/getSellerList",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            return resp_data
        except Exception as e:
            raise e

    async def get_sale_statistics_v2(
        self,
        access_token: str,
        start_date: str,
        end_date: str,
        result_type: str,
        date_unit: str,
        data_type: str,
        page: Optional[int] = None,
        length: Optional[int] = None,
        sids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        查询销量统计列表v2 - 支持多平台销量统计查询
        Args:
            start_date: 开始日期【下单时间】，格式：Y-m-d，时间间隔最长不超过90天
            end_date: 结束日期【下单时间】，格式：Y-m-d，时间间隔最长不超过90天
            result_type: 汇总类型 1-销量 2-订单量 3-销售额
            date_unit: 统计时间指标 1-年 2-月 3-周 4-日
            data_type: 统计数据维度 1-ASIN 2-父体 3-MSKU 4-SKU 5-SPU 6-店铺
            page: 分页页码，默认1
            length: 分页大小，默认20
            sids: 店铺id数组，多个使用英文逗号分隔
        Returns:
            dict: 销量统计数据响应
        """
        # 构建请求参数
        query_data = {
            "start_date": start_date,
            "end_date": end_date,
            "result_type": result_type,
            "date_unit": date_unit,
            "data_type": data_type
        }
        
        if page is not None:
            query_data["page"] = page
        if length is not None:
            query_data["length"] = length
        if sids is not None:
            query_data["sids"] = sids

        print(f"[RPA_Tornado] 查询销量统计列表v2 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/platformStatisticsV2/saleStat/pageList",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            return resp_data
        except Exception as e:
            raise e

    async def get_profit_report_seller(self, access_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["offset", "length", "startDate", "endDate"]
        for field in required_fields:
            if field not in params or not params[field]:
                return {'code': 400, 'message': f'缺少必填参数: {field}', 'data': None}
        query_data = {
            "offset": params["offset"],
            "length": params["length"],
            "startDate": params["startDate"],
            "endDate": params["endDate"]
        }
        for k in ["platformCodeS", "mids", "sids", "currencyCode"]:
            if k in params:
                query_data[k] = params[k]
        print(f"[RPA_Tornado] 查询结算利润报表 - 请求参数: {query_data}")
        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/multiplatform/profit/report/seller",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            return resp_data
        except Exception as e:
            raise e

    async def get_profit_report_msku(self, access_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["offset", "length", "startDate", "endDate"]
        # for field in required_fields:
        #     if field not in params or not params[field]:
        #         return {'code': 400, 'message': f'缺少必填参数: {field}', 'data': None}
        query_data = {
            "offset": params["offset"],
            "length": params["length"],
            "startDate": params["startDate"],
            "endDate": params["endDate"]
        }
        for k in ["platformCodeS", "mids", "sids", "currencyCode", "searchField", "searchValue", "developers", "cids", "bids"]:
            if k in params:
                query_data[k] = params[k]
        print(f"[RPA_Tornado] 查询多平台利润报表-msku - 请求参数: {query_data}")
        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/multiplatform/profit/report/msku",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            return resp_data
        except Exception as e:
            raise e

    async def get_profit_report_sku(self, access_token: str, params: Dict[str, Any]) -> Dict[str, Any]:
        # 必填参数及类型
        required_fields = [
            ("offset", int),
            ("length", int),
            ("mids", str),
            ("startDate", str),
            ("endDate", str)
        ]
        for field, typ in required_fields:
            if field not in params:
                return {'code': 400, 'message': f'缺少必填参数: {field}', 'data': None}
            # 类型校验，允许空字符串（str）
            if typ is int and not isinstance(params[field], int):
                return {'code': 400, 'message': f'{field} 必须为整数', 'data': None}
            if typ is str and not isinstance(params[field], str):
                return {'code': 400, 'message': f'{field} 必须为字符串', 'data': None}
        # 组装必填参数
        query_data = {
            "offset": params["offset"],
            "length": params["length"],
            "mids": params["mids"],
            "startDate": params["startDate"],
            "endDate": params["endDate"]
        }
        # 选填参数及类型
        optional_fields = [
            ("platformCodeS", list),
            ("sids", str),
            ("currencyCode", str),
            ("searchField", str),
            ("searchValue", str),
            ("developers", list),
            ("cids", list),
            ("bids", list)
        ]
        for field, typ in optional_fields:
            if field in params:
                # 类型校验
                if typ is list and not isinstance(params[field], list):
                    return {'code': 400, 'message': f'{field} 必须为数组', 'data': None}
                if typ is str and not isinstance(params[field], str):
                    return {'code': 400, 'message': f'{field} 必须为字符串', 'data': None}
                query_data[field] = params[field]
        print(f"[RPA_Tornado] 查询多平台利润报表-sku - 请求参数: {query_data}")
        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/multiplatform/profit/report/sku",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            return resp_data
        except Exception as e:
            raise e 