# multi_platform_service.py
# 用于多平台相关的业务逻辑
from app.auth.openapi import OpenApiBase
from app.config import settings
from typing import Optional, Dict, Any, List
from datetime import datetime
import json as _json
import os

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UNPROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, 'unprocessed_data')
os.makedirs(UNPROCESSED_DATA_DIR, exist_ok=True)


# 多平台服务类
# 描述功能：
# 1. 查询多平台店铺信息 -> get_seller_list
# 参数：offset: 分页偏移量，默认值为0
# 参数：length: 分页长度，上限200，默认值为200
# 参数：platform_code: 平台code数组，默认值为None
# 参数：is_sync: 店铺同步状态 1-启用 0-停用，默认值为None
# 参数：status: 店铺授权状态 1-正常授权 0-授权失败，默认值为None
# 返回：多平台店铺信息数据响应


class MultiPlatformService:
    def __init__(self):
        self.host = settings.LLX_API_HOST
        self.app_id = settings.LLX_APP_ID
        self.app_secret = settings.LLX_APP_SECRET
        self.api = OpenApiBase(self.host, self.app_id, self.app_secret)

    async def get_access_token(self) -> str:
        token = await self.api.generate_access_token()
        return token.access_token

    async def get_seller_list(
        self,
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
        access_token = await self.get_access_token()
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
            import json as _json, os
            from datetime import datetime
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(UNPROCESSED_DATA_DIR, f"{now_str}_multi_platform_seller_list_error.json")
            with open(file_path, "w", encoding='utf-8') as f:
                _json.dump({
                    "query_data": query_data,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            raise e

    async def get_sale_statistics_v2(
        self,
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
        access_token = await self.get_access_token()
        
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
            import json as _json, os
            from datetime import datetime
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(UNPROCESSED_DATA_DIR, f"{now_str}_sale_statistics_v2_error.json")
            with open(file_path, "w", encoding='utf-8') as f:
                _json.dump({
                    "query_data": query_data,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            raise e

    async def get_profit_report_seller(
        self,
        offset: int,
        length: int,
        startDate: str,
        endDate: str,
        platformCodeS: Optional[List[str]] = None,
        mids: Optional[str] = None,
        sids: Optional[str] = None,
        currencyCode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        查询结算利润（利润报表）-店铺
        Args:
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000
            startDate: 开始时间【结算日期】，闭区间，格式：Y-m-d
            endDate: 结束时间【结算日期】，闭区间，格式：Y-m-d
            platformCodeS: 平台id数组
            mids: 国家id，多个使用英文逗号分隔
            sids: 店铺id，多个使用英文逗号分隔
            currencyCode: 币种code
        Returns:
            dict: 利润报表数据响应
        """
        access_token = await self.get_access_token()
        query_data = {
            "offset": offset,
            "length": length,
            "startDate": startDate,
            "endDate": endDate
        }
        if platformCodeS is not None:
            query_data["platformCodeS"] = platformCodeS
        if mids is not None:
            query_data["mids"] = mids
        if sids is not None:
            query_data["sids"] = sids
        if currencyCode is not None:
            query_data["currencyCode"] = currencyCode

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
            import json as _json, os
            from datetime import datetime
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(UNPROCESSED_DATA_DIR, f"{now_str}_profit_report_seller_error.json")
            with open(file_path, "w", encoding='utf-8') as f:
                _json.dump({
                    "query_data": query_data,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            raise e

    async def get_profit_report_msku(
        self,
        offset: int,
        length: int,
        platformCodeS=None,
        mids=None,
        sids=None,
        currencyCode=None,
        startDate=None,
        endDate=None,
        searchField=None,
        searchValue=None,
        developers=None,
        cids=None,
        bids=None
    ) -> Dict[str, Any]:
        """
        查询多平台结算利润（利润报表）-msku
        """
        access_token = await self.get_access_token()
        query_data = {
            "offset": offset,
            "length": length,
            "startDate": startDate,
            "endDate": endDate
        }
        if platformCodeS is not None:
            query_data["platformCodeS"] = platformCodeS
        if mids is not None:
            query_data["mids"] = mids
        if sids is not None:
            query_data["sids"] = sids
        if currencyCode is not None:
            query_data["currencyCode"] = currencyCode
        if searchField is not None:
            query_data["searchField"] = searchField
        if searchValue is not None:
            query_data["searchValue"] = searchValue
        if developers is not None:
            query_data["developers"] = developers
        if cids is not None:
            query_data["cids"] = cids
        if bids is not None:
            query_data["bids"] = bids

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
            import json as _json, os
            from datetime import datetime
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(UNPROCESSED_DATA_DIR, f"{now_str}_profit_report_msku_error.json")
            with open(file_path, "w", encoding='utf-8') as f:
                _json.dump({
                    "query_data": query_data,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            raise e

    async def get_profit_report_sku(
        self,
        offset: int,
        length: int,
        platformCodeS=None,
        mids=None,
        sids=None,
        currencyCode=None,
        startDate=None,
        endDate=None,
        searchField=None,
        searchValue=None,
        developers=None,
        cids=None,
        bids=None
    ) -> Dict[str, Any]:
        """
        查询多平台结算利润（利润报表）-sku
        """
        access_token = await self.get_access_token()
        query_data = {
            "offset": offset,
            "length": length,
            "mids": mids,
            "startDate": startDate,
            "endDate": endDate
        }
        if platformCodeS is not None:
            query_data["platformCodeS"] = platformCodeS
        if sids is not None:
            query_data["sids"] = sids
        if currencyCode is not None:
            query_data["currencyCode"] = currencyCode
        if searchField is not None:
            query_data["searchField"] = searchField
        if searchValue is not None:
            query_data["searchValue"] = searchValue
        if developers is not None:
            query_data["developers"] = developers
        if cids is not None:
            query_data["cids"] = cids
        if bids is not None:
            query_data["bids"] = bids

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
            import json as _json, os
            from datetime import datetime
            now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(UNPROCESSED_DATA_DIR, f"{now_str}_profit_report_sku_error.json")
            with open(file_path, "w", encoding='utf-8') as f:
                _json.dump({
                    "query_data": query_data,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            raise e 