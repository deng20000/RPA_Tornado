import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from app.config import settings
from app.auth.openapi import OpenApiBase
class StatisticsService:
    def __init__(self):
        self.host = settings.LLX_API_HOST
        self.app_id = settings.LLX_APP_ID
        self.app_secret = settings.LLX_APP_SECRET
        self.api = OpenApiBase(self.host, self.app_id, self.app_secret)

    async def get_access_token(self) -> str:
        token = await self.api.generate_access_token()
        return token.access_token

    async def openapi_post(self, route_name, query_data):
        access_token = await self.get_access_token()
        resp = await self.api.request(
            access_token=access_token,
            route_name=route_name,
            method="POST",
            req_body=query_data
        )
        resp_data = resp.model_dump()
        if resp_data.get("code") not in (0, 200):
            return {
                'code': resp_data.get("code", 500),
                'message': resp_data.get("message", "外部API错误"),
                'data': resp_data.get("data")
            }
        return resp_data

    async def get_sales_report_asin_daily_lists(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询销量、订单量、销售额
        支持按Asin或MSKU查询销量、订单量、销售额
        Args:
            params: 请求参数
                - sid: 店铺id，必填
                - event_date: 报表时间，格式Y-m-d，必填
                - asin_type: 查询维度，1-asin, 2-msku，默认1
                - type: 类型，1-销售额, 2-销量, 3-订单量，默认1
                - offset: 分页偏移量，默认0
                - length: 分页长度，默认1000
        Returns:
            Dict包含查询结果
        """
        try:
            # 参数校验
            required_fields = ['sid', 'event_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            sid = params['sid']
            event_date = params['event_date']
            asin_type = params.get('asin_type', 1)
            report_type = params.get('type', 1)
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            if not isinstance(sid, int):
                return {'code': 400, 'message': 'sid必须是整数类型', 'data': None}
            if not isinstance(event_date, str):
                return {'code': 400, 'message': 'event_date必须是字符串类型', 'data': None}
            try:
                datetime.strptime(event_date, '%Y-%m-%d')
            except ValueError:
                return {'code': 400, 'message': 'event_date格式错误，应为Y-m-d格式', 'data': None}
            if asin_type not in [1, 2]:
                return {'code': 400, 'message': 'asin_type只能是1(asin)或2(msku)', 'data': None}
            if report_type not in [1, 2, 3]:
                return {'code': 400, 'message': 'type只能是1(销售额)、2(销量)或3(订单量)', 'data': None}
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须是非负整数', 'data': None}
            if not isinstance(length, int) or length <= 0:
                return {'code': 400, 'message': 'length必须是正整数', 'data': None}
            query_data = {
                'sid': sid,
                'event_date': event_date,
                'asin_type': asin_type,
                'type': report_type,
                'offset': offset,
                'length': length
            }
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/sales_report/asinDailyLists",
                method="POST",
                req_body=query_data
            )
            return resp.model_dump()
        except Exception as e:
            return {'code': 500, 'message': f'查询失败: {str(e)}', 'data': None}

    async def get_order_profit_msku(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询订单利润-MSKU
        唯一键：sid+msku
        Args:
            params: 请求参数
                - offset: 分页偏移量，默认0
                - length: 分页长度，默认20，上限5000
                - sids: 店铺id数组
                - startDate: 查询开始时间，必填
                - endDate: 查询结束时间，必填
                - searchField: 搜索值类型，可选
                - searchValue: 搜索的值，数组
                - currencyCode: 币种code
        Returns:
            Dict包含查询结果
        """
        try:
            # 校验必填参数
            required_fields = ['startDate', 'endDate']
            for field in required_fields:
                if field not in params or not params[field]:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            # 获取参数
            offset = params.get('offset', 0)
            length = params.get('length', 20)
            sids = params.get('sids', None)
            startDate = params['startDate']
            endDate = params['endDate']
            searchField = params.get('searchField', None)
            searchValue = params.get('searchValue', None)
            currencyCode = params.get('currencyCode', None)

            # 校验分页参数
            if not isinstance(offset, int) or offset < 0:
                return {
                    'code': 400,
                    'message': 'offset必须是非负整数',
                    'data': None
                }
            if not isinstance(length, int) or length <= 0 or length > 5000:
                return {
                    'code': 400,
                    'message': 'length必须为1~5000的整数',
                    'data': None
                }
            # 校验sids
            if sids is not None and not (isinstance(sids, list) and all(isinstance(x, int) for x in sids)):
                return {
                    'code': 400,
                    'message': 'sids必须为整数数组',
                    'data': None
                }
            # 校验searchField
            valid_fields = ['seller_sku', 'asin', 'local_name', 'local_sku']
            if searchField is not None and searchField not in valid_fields:
                return {
                    'code': 400,
                    'message': f'searchField可选值: {valid_fields}',
                    'data': None
                }
            # 校验searchValue
            if searchValue is not None and not isinstance(searchValue, list):
                return {
                    'code': 400,
                    'message': 'searchValue必须为数组',
                    'data': None
                }
            # 校验currencyCode
            valid_currencies = ['原币种','CNY','USD','EUR','JPY','AUD','CAD','MXN','GBP','INR','AED','SGD','SAR','BRL','SEK','PLN','TRY','HKD']
            if currencyCode is not None and currencyCode not in valid_currencies:
                return {
                    'code': 400,
                    'message': f'currencyCode可选值: {valid_currencies}',
                    'data': None
                }
            # 校验日期格式
            def check_date(date_str):
                for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S'):
                    try:
                        datetime.strptime(date_str, fmt)
                        return True
                    except ValueError:
                        continue
                return False
            if not check_date(startDate):
                return {
                    'code': 400,
                    'message': 'startDate格式错误，应为Y-m-d或Y-m-d H:i:s',
                    'data': None
                }
            if not check_date(endDate):
                return {
                    'code': 400,
                    'message': 'endDate格式错误，应为Y-m-d或Y-m-d H:i:s',
                    'data': None
                }
            # 构建请求参数
            request_data = {
                'offset': offset,
                'length': length,
                'sids': sids,
                'startDate': startDate,
                'endDate': endDate,
                'searchField': searchField,
                'searchValue': searchValue,
                'currencyCode': currencyCode
            }
            
            # 调用领星API获取订单利润-MSKU数据
            import json as _json
            
            print(f"[RPA_Tornado] 查询订单利润-MSKU - 请求参数: {request_data}")
            
            try:
                access_token = await self.get_access_token()
                resp = await self.api.request(
                    access_token=access_token,
                    route_name="/basicOpen/finance/mreport/OrderProfit",
                    method="POST",
                    req_body=request_data
                )
                
                # 保存调试信息
                now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_path = os.path.join("unprocessed_data", f"{now_str}_order_profit_msku.json")
                with open(file_path, "w", encoding='utf-8') as f:
                    _json.dump({
                        "request_data": request_data,
                        "response": resp.model_dump(),
                        "timestamp": datetime.now().isoformat()
                    }, f, ensure_ascii=False, indent=2)
                print(f"[DEBUG] 调试信息已保存到: {file_path}")
                
                return resp.model_dump()
            except Exception as e:
                # 保存错误信息
                now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_path = os.path.join("unprocessed_data", f"{now_str}_order_profit_msku_error.json")
                with open(file_path, "w", encoding='utf-8') as f:
                    _json.dump({
                        "request_data": request_data,
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    }, f, ensure_ascii=False, indent=2)
                print(f"[DEBUG] 错误信息已保存到: {file_path}")
                raise e
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询失败: {str(e)}',
                'data': None
            } 

    async def get_sales_report_shop_summary(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询店铺汇总销量，支持按店铺维度查询店铺销量、销售额
        Args:
            params: 请求参数
                - sid: 店铺id数组，必填
                - start_date: 报表开始时间，格式Y-m-d，必填
                - end_date: 报表结束时间，格式Y-m-d，必填
                - offset: 分页偏移量，默认0
                - length: 分页长度，默认1000
        Returns:
            Dict包含查询结果
        """
        try:
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            query_data = {
                'sid': params['sid'],
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'offset': params.get('offset', 0),
                'length': params.get('length', 1000)
            }
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/sales_report/sales",
                method="POST",
                req_body=query_data
            )
            return resp.model_dump()
        except Exception as e:
            return {'code': 500, 'message': f'查询失败: {str(e)}', 'data': None} 

    async def get_product_performance(self, params):
        """
        查询产品表现，调用外部OpenAPI
        Args:
            params: 请求参数，详见接口文档
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['offset', 'length', 'sort_field', 'sort_type', 'sid', 'start_date', 'end_date', 'summary_field', 'avg_volume']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            # 2. 类型与取值校验
            if not isinstance(params['offset'], int) or params['offset'] < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            if not isinstance(params['length'], int) or params['length'] <= 0 or params['length'] > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            valid_sort_fields = [
                'volume', 'order_items', 'amount', 'volume_chain_ratio', 'order_chain_ratio', 'amount_chain_ratio',
                'b2b_volume', 'b2b_order_items', 'promotion_volume', 'promotion_amount', 'promotion_order_items',
                'promotion_discount', 'avg_volume'
            ]
            if params['sort_field'] not in valid_sort_fields:
                return {'code': 400, 'message': f'sort_field可选值: {valid_sort_fields}', 'data': None}
            if params['sort_type'] not in ['desc', 'asc']:
                return {'code': 400, 'message': 'sort_type可选值: desc, asc', 'data': None}
            # sid 可以为字符串或数组
            if not (isinstance(params['sid'], (str, list))):
                return {'code': 400, 'message': 'sid必须为字符串或数组', 'data': None}
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {'code': 400, 'message': f'{date_field}格式错误，应为Y-m-d', 'data': None}
            valid_summary_fields = ['asin', 'parent_asin', 'msku', 'sku']
            if params['summary_field'] not in valid_summary_fields:
                return {'code': 400, 'message': f'summary_field可选值: {valid_summary_fields}', 'data': None}
            # 3. 组装 query_data
            query_data = {
                'offset': params['offset'],
                'length': params['length'],
                'sort_field': params['sort_field'],
                'sort_type': params['sort_type'],
                'sid': params['sid'],
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'summary_field': params['summary_field'],
                'avg_volume': params['avg_volume']
            }
            # 可选参数
            if 'search_field' in params:
                query_data['search_field'] = params['search_field']
            if 'search_value' in params:
                query_data['search_value'] = params['search_value']
            if 'mid' in params:
                query_data['mid'] = params['mid']
            if 'extend_search' in params:
                query_data['extend_search'] = params['extend_search']
            if 'currency_code' in params:
                query_data['currency_code'] = params['currency_code']
            if 'is_recently_enum' in params:
                query_data['is_recently_enum'] = params['is_recently_enum']
            # 4. 调用外部API
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/bd/productPerformance/openApi/asinList",
                method="POST",
                req_body=query_data
            )
            return resp.model_dump()
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询失败: {str(e)}',
                'data': None
            } 

    async def get_product_performance_trend_by_hour(self, params):
        """
        查询asin360小时数据，调用外部OpenAPI
        Args:
            params: 请求参数，详见接口文档
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            required_fields = ['sids', 'date_start', 'date_end', 'summary_field', 'summary_field_value']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            # sids 必须为字符串，且最多200个
            if not isinstance(params['sids'], str):
                return {'code': 400, 'message': 'sids必须为字符串，多个用英文逗号隔开', 'data': None}
            if len(params['sids'].split(',')) > 200:
                return {'code': 400, 'message': 'sids最多支持200个', 'data': None}
            # 日期格式校验
            for date_field in ['date_start', 'date_end']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {'code': 400, 'message': f'{date_field}格式错误，应为Y-m-d', 'data': None}
            valid_summary_fields = ['parent_asin', 'asin', 'msku', 'sku', 'spu']
            if params['summary_field'] not in valid_summary_fields:
                return {'code': 400, 'message': f'summary_field可选值: {valid_summary_fields}', 'data': None}
            # 组装 query_data
            query_data = {
                'sids': params['sids'],
                'date_start': params['date_start'],
                'date_end': params['date_end'],
                'summary_field': params['summary_field'],
                'summary_field_value': params['summary_field_value']
            }
            # 调用外部API
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour",
                method="POST",
                req_body=query_data
            )
            return resp.model_dump()
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询失败: {str(e)}',
                'data': None
            } 

    async def get_profit_statistics_asin_list(self, params):
        """
        查询利润统计-ASIN，调用外部OpenAPI
        Args:
            params: 请求参数，详见接口文档
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            required_fields = ['startDate', 'endDate']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            # 校验时间格式
            for date_field in ['startDate', 'endDate']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {'code': 400, 'message': f'{date_field}格式错误，应为Y-m-d', 'data': None}
            # 校验时间跨度不超过7天
            start = datetime.strptime(params['startDate'], '%Y-%m-%d')
            end = datetime.strptime(params['endDate'], '%Y-%m-%d')
            if (end - start).days > 7:
                return {'code': 400, 'message': '开始结束时间间隔不能超过7天', 'data': None}
            # 组装 query_data
            query_data = {}
            for k in ['offset', 'length', 'mids', 'sids', 'startDate', 'endDate', 'searchField', 'searchValue', 'currencyCode']:
                if k in params:
                    query_data[k] = params[k]
            # offset/length 校验
            if 'offset' in query_data and (not isinstance(query_data['offset'], int) or query_data['offset'] < 0):
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            if 'length' in query_data:
                if not isinstance(query_data['length'], int) or query_data['length'] <= 0 or query_data['length'] > 10000:
                    return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            # 调用外部API
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/bd/profit/statistics/open/asin/list",
                method="POST",
                req_body=query_data
            )
            return resp.model_dump()
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询失败: {str(e)}',
                'data': None
            } 