# lingxing_service.py
# 用于领星相关的业务逻辑 
from app.auth.openapi import OpenApiBase
from app.models.record import OrderListResponse
from typing import Optional, Dict, Any
from app.config import settings
import json as _json
import os
from datetime import datetime

class LingxingService:
    def __init__(self):
        self.host = settings.LLX_API_HOST
        self.app_id = settings.LLX_APP_ID
        self.app_secret = settings.LLX_APP_SECRET
        self.api = OpenApiBase(self.host, self.app_id, self.app_secret)

    async def get_access_token(self) -> str:
        token = await self.api.generate_access_token()
        return token.access_token

    async def fetch_order_list(self, start_time: int, end_time: int, offset: int = 0, length: int = 20, order_status: int = 5, date_type: str = 'global_purchase_time', platform_code: Optional[list] = None) -> OrderListResponse:
        if platform_code is None:
            platform_code = [i for i in range(10001, 10039)]
        access_token = await self.get_access_token()
        query_data = {
            "start_time": start_time,
            "end_time": end_time,
            "date_type": date_type,
            "offset": offset,
            "length": length,
            "order_status": order_status,
            "platform_code": platform_code
        }
        print("[RPA_Tornado] 请求参数:", query_data)
        resp = await self.api.request(
            access_token=access_token,
            route_name="/pb/mp/order/v2/list",
            method="POST",
            req_body=query_data
        )
        resp_data = resp.model_dump()
        # 自动化比对信息保存
        compare_info = {
            "access_token": access_token,
            "query_data": query_data,
            # 下面两项需在 sign.py 里用全局变量/单例/文件等方式传递
            # "sign_raw": ...,
            # "sign": ...,
            "response": resp_data
        }
        # 新增：保存到 unprocessed_data 文件夹，文件名为 'YYYY-MM-DD_HH-MM-SS_compare_tornado.json'
        folder = 'unprocessed_data'
        os.makedirs(folder, exist_ok=True)
        now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join(folder, f'{now_str}_compare_tornado.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            _json.dump(compare_info, f, ensure_ascii=False, indent=2)
        if resp_data.get("code") != 0:
            raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
        # 保证 data 字段为 list 类型
        if isinstance(resp_data.get("data"), dict) and "list" in resp_data["data"]:
            resp_data["data"] = resp_data["data"]["list"]
        if resp_data.get("data") is None:
            resp_data["data"] = []
        return OrderListResponse(**resp_data) 

    async def fetch_order_list_custom(self, query_data: dict):
        """
        通用自定义参数请求，适配不同业务场景
        """
        access_token = await self.get_access_token()
        resp = await self.api.request(
            access_token=access_token,
            route_name="/basicOpen/platformStatisticsV2/saleStat/pageList",
            method="POST",
            req_body=query_data
        )
        resp_data = resp.model_dump()
        return resp_data 