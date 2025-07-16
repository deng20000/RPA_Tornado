# lingxing_auth.py
# 用于领星认证相关的 Tornado RequestHandler 
import tornado.web
import asyncio
from datetime import datetime, timedelta
from app.services.lingxing_service import LingxingService
from app.staging.file_store import save_json
from app.routes import route

@route('/api/lingxing/orders', methods=['POST'])
class LingxingOrderHandler(tornado.web.RequestHandler):
    async def post(self):
        """
        请求体可选参数：result_type, date_unit, data_type, 其他参数
        result_type=3 每日电商总销售额
        result_type=1 热门SKU销量查看
        """
        try:
            body = self.request.body.decode('utf-8')
            print("收到请求体:", body)
            params = tornado.escape.json_decode(body) if body else {}
        except Exception as e:
            print("JSON解码失败:", e, "body内容:", self.request.body)
            params = {}
        result_type = params.get("result_type")
        service = LingxingService()
        try:
            if result_type == 3:
                # 每日电商总销售额
                print("处理每日电商总销售额逻辑")
                # 组装参数
                query_data = {
                    "result_type": 3,
                    "date_unit": params.get("date_unit", 4),
                    "data_type": params.get("data_type", 6),
                    **params
                }
                order_list = await service.fetch_order_list_custom(query_data)
                self.write({"code": 0, "msg": "success", "data": order_list})
            elif result_type == 1:
                # 热门SKU销量查看
                print("处理热门SKU销量逻辑")
                query_data = {
                    "result_type": 1,
                    "date_unit": params.get("date_unit", 4),
                    "data_type": params.get("data_type", 6),
                    **params
                }
                order_list = await service.fetch_order_list_custom(query_data)
                self.write({"code": 0, "msg": "success", "data": order_list})
            else:
                print("参数错误或未指定result_type")
                self.set_status(400)
                self.write({"code": 1, "msg": "参数错误或未指定result_type"})
        except Exception as e:
            print("业务处理异常:", e)
            self.set_status(500)
            self.write({"code": 1, "msg": str(e)}) 