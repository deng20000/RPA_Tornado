import json
from tornado.web import RequestHandler
from app.services.statistics_service import StatisticsService

class SalesReportAsinDailyListsHandler(RequestHandler):
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            service = StatisticsService()
            result = await service.get_sales_report_asin_daily_lists(data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class OrderProfitMSKUHandler(RequestHandler):
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            service = StatisticsService()
            result = await service.get_order_profit_msku(data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class SalesReportAsinDailyListsV2Handler(RequestHandler):
    async def post(self):
        """
        查询销量、订单量、销售额（新版，支持按Asin或MSKU查询，原路由/erp/sc/data/sales_report/asinDailyLists）
        参数：
            sid: 店铺id，必填
            event_date: 报表时间【站点时间】，格式：Y-m-d，必填
            asin_type: 查询维度，1-asin, 2-msku，默认1
            type: 类型，1-销售额, 2-销量, 3-订单量，默认1
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000
        返回：销量报表数据响应
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            # 校验必填参数
            required_params = ['sid', 'event_date']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            from app.services.statistics_service import StatisticsService
            service = StatisticsService()
            result = await service.get_sales_report_asin_daily_lists_v2(data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 