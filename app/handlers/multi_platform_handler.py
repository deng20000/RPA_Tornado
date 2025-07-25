import json
from tornado.web import RequestHandler
from app.services.multi_platform_service import MultiPlatformService
from app.services.statistics_service import StatisticsService
from .base import BaseHandler

# 多平台店铺信息查询接口
class MultiPlatformSellerListHandler(BaseHandler):
    async def post(self):
        """
        查询多平台店铺基础信息，支持分页、平台类型、同步状态、授权状态等参数。
        参数：
            offset: 分页偏移量，默认0
            length: 分页长度，默认200
            platform_code: 平台code数组，可选
            is_sync: 店铺同步状态 1-启用 0-停用，可选
            status: 店铺授权状态 1-正常授权 0-授权失败，可选
        返回：多平台店铺信息数据响应
        """
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            offset = data.get('offset', 0)
            length = data.get('length', 200)
            platform_code = data.get('platform_code', None)
            is_sync = data.get('is_sync', None)
            status = data.get('status', None)

            # 类型转换
            if platform_code is not None and isinstance(platform_code, list):
                platform_code = [int(x) for x in platform_code]
            elif platform_code is not None and isinstance(platform_code, str):
                platform_code = [int(x) for x in platform_code.split(',')]

            service = MultiPlatformService()
            result = await service.get_seller_list(
                self.access_token,
                offset=int(offset) if offset is not None else 0,
                length=int(length) if length is not None else 200,
                platform_code=platform_code,
                is_sync=int(is_sync) if is_sync is not None else None,
                status=int(status) if status is not None else None
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 销量统计列表v2查询接口
class SaleStatisticsV2Handler(BaseHandler):
    async def post(self):
        """
        查询销量统计列表v2，支持多平台销量统计查询。
        参数：
            start_date: 开始日期【下单时间】，格式：Y-m-d，时间间隔最长不超过90天
            end_date: 结束日期【下单时间】，格式：Y-m-d，时间间隔最长不超过90天
            result_type: 汇总类型 1-销量 2-订单量 3-销售额
            date_unit: 统计时间指标 1-年 2-月 3-周 4-日
            data_type: 统计数据维度 1-ASIN 2-父体 3-MSKU 4-SKU 5-SPU 6-店铺
            page: 分页页码，默认1
            length: 分页大小，默认20
            sids: 店铺id数组，多个使用英文逗号分隔
        返回：销量统计数据响应
        """
        try:
            # 处理空请求体的情况
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            
            data = json.loads(body)
            
            # 验证必填参数
            required_params = ['start_date', 'end_date', 'result_type', 'date_unit', 'data_type']
            for param in required_params:
                if param not in data or not data[param]:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            
            service = MultiPlatformService()
            result = await service.get_sale_statistics_v2(
                self.access_token,
                start_date=data['start_date'],
                end_date=data['end_date'],
                result_type=data['result_type'],
                date_unit=data['date_unit'],
                data_type=data['data_type'],
                page=data.get('page'),
                length=data.get('length'),
                sids=data.get('sids')
            )
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 

# 查询结算利润（利润报表）-店铺接口
class ProfitReportSellerHandler(BaseHandler):
    async def post(self):
        """
        查询结算利润（利润报表）-店铺，支持多平台利润报表查询。
        参数：
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000
            startDate: 开始时间【结算日期】，闭区间，格式：Y-m-d
            endDate: 结束时间【结算日期】，闭区间，格式：Y-m-d
            platformCodeS: 平台id数组
            mids: 国家id，多个使用英文逗号分隔
            sids: 店铺id，多个使用英文逗号分隔
            currencyCode: 币种code
        返回：利润报表数据响应
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            # 校验必填参数
            required_params = ['offset', 'length', 'startDate', 'endDate']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            service = MultiPlatformService()
            result = await service.get_profit_report_seller(self.access_token, data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 

# 销量报表ASIN日列表查询接口
class SalesReportAsinDailyListsHandler(BaseHandler):
    async def post(self):
        """
        查询销量、订单量、销售额
        支持按Asin或MSKU查询销量、订单量、销售额
        
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
            # 处理空请求体的情况
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            
            data = json.loads(body)
            
            # 验证必填参数
            required_params = ['sid', 'event_date']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            
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

# 订单利润-MSKU 查询接口
class OrderProfitMSKUHandler(BaseHandler):
    async def post(self):
        """
        查询订单利润-MSKU
        唯一键：sid+msku
        """
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

# 多平台结算利润（利润报表）-msku 查询接口
class ProfitReportMSKUHandler(BaseHandler):
    async def post(self):
        """
        查询多平台结算利润（利润报表）-msku
        参数：
            offset: 分页偏移量，默认0，必填
            length: 分页长度，默认1000，必填
            platformCodeS: 平台id数组，可选
            mids: 国家id，多个使用英文逗号分隔，可选
            sids: 店铺id，多个使用英文逗号分隔，可选
            currencyCode: 币种code，可选
            startDate: 开始时间，必填
            endDate: 结束时间，必填
            searchField: 搜索值类型，可选
            searchValue: 搜索值，可选
            developers: 开发人，可选
            cids: 分类，可选
            bids: 品牌，可选
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            # 校验必填参数
            required_params = ['offset', 'length', 'startDate', 'endDate']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            service = MultiPlatformService()
            result = await service.get_profit_report_msku(self.access_token, data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 

# 多平台结算利润（利润报表）-sku 查询接口
class ProfitReportSKUHandler(BaseHandler):
    async def post(self):
        """
        查询多平台结算利润（利润报表）-sku
        参数：
            offset: 分页偏移量，默认0，必填
            length: 分页长度，默认1000，必填
            platformCodeS: 平台id数组，可选
            mids: 国家id，多个使用英文逗号分隔，必填
            sids: 店铺id，多个使用英文逗号分隔，可选
            currencyCode: 币种code，可选
            startDate: 开始时间，必填
            endDate: 结束时间，必填
            searchField: 搜索值类型，可选
            searchValue: 搜索值，可选
            developers: 开发人，可选
            cids: 分类，可选
            bids: 品牌，可选
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
            data = json.loads(body)
            # 校验必填参数
            required_params = ['offset', 'length', 'mids', 'startDate', 'endDate']
            for param in required_params:
                if param not in data or data[param] is None:
                    self.set_status(400)
                    self.write({'error': f'{param} 参数不能为空'})
                    return
            service = MultiPlatformService()
            result = await service.get_profit_report_sku(self.access_token, data)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 