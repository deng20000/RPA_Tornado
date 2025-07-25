# base_data_service.py
# 用于基础数据相关的业务逻辑
from app.auth.openapi import OpenApiBase
from app.config import settings
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import json as _json
import os


class BaseDataService:

    def __init__(self):
        self.api = OpenApiBase(settings.LLX_API_HOST, settings.LLX_APP_ID, settings.LLX_APP_SECRET)

    async def get_currency_exchange_rate(self, access_token: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        查询汇率 - 获取亚马逊系统【设置】>【汇率管理】中的汇率数据
        Args:
            date: 汇率月份，格式为 YYYY-MM，默认为昨天所在月份
        Returns:
            dict: 汇率数据响应
        """
        # 如果没有提供日期，默认使用昨天所在月份
        if date is None:
            yesterday = datetime.now() - timedelta(days=1)
            date = yesterday.strftime("%Y-%m")

        # 构建请求参数
        query_data = {
            "date": date
        }

        print(f"[RPA_Tornado] 查询汇率 - 请求参数: {query_data}")

        try:
            # 调用API获取汇率数据
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/finance/currency/currencyMonth",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": query_data,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            # 检查API响应状态
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 汇率查询成功 - 月份: {date}")
            return resp_data

        except Exception as e:
            raise e

    async def get_amazon_seller_list(self, access_token: str) -> Dict[str, Any]:
        """
        查询亚马逊店铺列表 - 查询企业已授权到领星ERP的全部亚马逊店铺信息
        Returns:
            dict: 店铺列表数据响应
        """
        print(f"[RPA_Tornado] 查询亚马逊店铺列表")
        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/seller/lists",
                method="GET",
                req_body=None
            )
            resp_data = resp.model_dump()
            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": None,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            print(f"[RPA_Tornado] 店铺列表查询成功")
            return resp_data
        except Exception as e:
            raise e

    async def get_amazon_marketplace_list(self, access_token: str) -> Dict[str, Any]:
        """
        查询亚马逊市场列表 - 查询亚马逊所有市场列表数据
        Returns:
            dict: 市场列表数据响应
        """
        print(f"[RPA_Tornado] 查询亚马逊市场列表")
        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/seller/allMarketplace",
                method="GET",
                req_body=None
            )
            resp_data = resp.model_dump()
            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": None,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            print(f"[RPA_Tornado] 市场列表查询成功")
            return resp_data
        except Exception as e:
            raise e

    async def get_world_state_list(self, access_token: str, country_code: str) -> Dict[str, Any]:
        """
        查询世界州/省列表 - 根据国家代码查询对应的州/省列表
        Args:
            country_code: 国家code，查询亚马逊市场列表接口对应字段【code】
        Returns:
            dict: 州/省列表数据响应
        """
        # 构建请求参数
        query_data = {
            "country_code": country_code
        }

        print(f"[RPA_Tornado] 查询世界州/省列表 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/worldState/lists",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": query_data,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 州/省列表查询成功 - 国家代码: {country_code}")
            return resp_data

        except Exception as e:
            raise e

    async def download_file_attachment(self, access_token: str, file_id: int) -> Dict[str, Any]:
        """
        下载附件 - 支持下载产品附件
        Args:
            file_id: 附件id【取对应功能接口返回结果中的附件id值】
        Returns:
            dict: 下载结果数据响应
        """
        # 构建请求参数
        query_data = {
            "file_id": file_id
        }

        print(f"[RPA_Tornado] 下载附件 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/common/file/download",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": query_data,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 附件下载成功 - 文件ID: {file_id}")
            return resp_data

        except Exception as e:
            raise e

    async def download_customized_file(self, access_token: str, file_id: str) -> Dict[str, Any]:
        """
        定制化附件下载接口 - 下载订单详情中的附件
        Args:
            file_id: 附件文件id(订单详情接口中附件id字段)
        Returns:
            dict: 下载结果数据响应
        """
        # 构建请求参数
        query_data = {
            "file_id": file_id
        }

        print(f"[RPA_Tornado] 定制化附件下载 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/customized/file/download",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": query_data,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 定制化附件下载成功 - 文件ID: {file_id}")
            return resp_data

        except Exception as e:
            raise e

    async def get_erp_user_list(self, access_token: str) -> Dict[str, Any]:
        """
        查询ERP用户信息列表 - 查询企业开启的全部ERP账号数据
        Returns:
            dict: ERP用户列表数据响应
        """
        print(f"[RPA_Tornado] 查询ERP用户信息列表")
        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/account/lists",
                method="GET",
                req_body=None
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": None,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] ERP用户列表查询成功")
            return resp_data

        except Exception as e:
            raise e


    async def batch_edit_seller_name(self, access_token: str, sid_name_list: list) -> Dict[str, Any]:
        """
        批量修改店铺名称 - 最多可批量修改10个店铺名称
        Args:
            sid_name_list: 批量修改店铺数组，每个元素包含sid(店铺id)和name(店铺名称)
        Returns:
            dict: 批量修改结果数据响应
        """
        # 构建请求参数
        query_data = {
            "sid_name_list": sid_name_list
        }

        print(f"[RPA_Tornado] 批量修改店铺名称 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/seller/batchEditSellerName",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": query_data,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 批量修改店铺名称成功")
            return resp_data

        except Exception as e:
            raise e 