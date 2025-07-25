import json
from tornado.web import RequestHandler
from app.services.statistics_service import StatisticsService
from .base import BaseHandler

class SalesReportAsinDailyListsHandler(BaseHandler):
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            service = StatisticsService()
            result = await service.get_sales_report_asin_daily_lists(self.access_token, data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class OrderProfitMSKUHandler(BaseHandler):
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            service = StatisticsService()
            result = await service.get_order_profit_msku(self.access_token, data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class SalesReportShopSummaryHandler(BaseHandler):
    async def post(self):
        """
        查询店铺汇总销量，支持按店铺维度查询店铺销量、销售额
        参数：
            sid: 店铺id数组，必填
            start_date: 报表开始时间，格式Y-m-d，必填
            end_date: 报表结束时间，格式Y-m-d，必填
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000
        返回：店铺销量汇总数据响应
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            required_params = ['sid', 'start_date', 'end_date']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            offset = data.get('offset', 0)
            length = data.get('length', 1000)
            from app.services.statistics_service import StatisticsService
            service = StatisticsService()
            result = await service.get_sales_report_shop_summary(self.access_token, {
                'sid': data['sid'],
                'start_date': data['start_date'],
                'end_date': data['end_date'],
                'offset': offset,
                'length': length
            })
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class ProductPerformanceHandler(BaseHandler):
    """
    查询产品表现
    分组: 统计
    路径: /bd/productPerformance/openApi/asinList
    """
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            # 参数校验（只校验必填，详细校验交给 service）
            required_params = ['offset', 'length', 'sort_field', 'sort_type', 'sid', 'start_date', 'end_date', 'summary_field']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            from app.services.statistics_service import StatisticsService
            service = StatisticsService()
            result = await service.get_product_performance(self.access_token, data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class ProductPerformanceTrendByHourHandler(RequestHandler):
    """
    查询asin360小时数据
    分组: 统计
    路径: /basicOpen/salesAnalysis/productPerformance/performanceTrendByHour
    """
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            required_params = ['sids', 'date_start', 'date_end', 'summary_field', 'summary_field_value']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            from app.services.statistics_service import StatisticsService
            service = StatisticsService()
            result = await service.get_product_performance_trend_by_hour(data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

class ProfitStatisticsAsinListHandler(RequestHandler):
    """
    查询利润统计-ASIN
    分组: 统计
    路径: /bd/profit/statistics/open/asin/list
    """
    async def post(self):
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            required_params = ['startDate', 'endDate']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            from app.services.statistics_service import StatisticsService
            service = StatisticsService()
            result = await service.get_profit_statistics_asin_list(data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 