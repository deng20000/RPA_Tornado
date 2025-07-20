import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class StatisticsService:
    async def get_statistics(self, params):
        """获取统计数据"""
        pass
    
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
            request_data = {
                'sid': sid,
                'event_date': event_date,
                'asin_type': asin_type,
                'type': report_type,
                'offset': offset,
                'length': length
            }
            # TODO: 实现真实的销量报表查询逻辑
            raise NotImplementedError('请实现真实的销量报表ASIN日列表查询逻辑')
        except Exception as e:
            return {'code': 500, 'message': f'查询失败: {str(e)}', 'data': None}

    async def get_sales_report_asin_daily_lists_v2(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询销量、订单量、销售额（新版，支持按Asin或MSKU查询，原路由/erp/sc/data/sales_report/asinDailyLists）
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
            query_data = {
                'sid': sid,
                'event_date': event_date,
                'asin_type': asin_type,
                'type': report_type,
                'offset': offset,
                'length': length
            }
            from app.ecommerce_dashboard.services.common import api_request
            resp = await api_request("/erp/sc/data/sales_report/asinDailyLists", query_data)
            return resp
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
            from app.ecommerce_dashboard.services.common import api_request
            import json as _json
            
            print(f"[RPA_Tornado] 查询订单利润-MSKU - 请求参数: {request_data}")
            
            try:
                resp = await api_request("/basicOpen/finance/mreport/OrderProfit", request_data)
                
                # 保存调试信息
                now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_path = os.path.join("unprocessed_data", f"{now_str}_order_profit_msku.json")
                with open(file_path, "w", encoding='utf-8') as f:
                    _json.dump({
                        "request_data": request_data,
                        "response": resp,
                        "timestamp": datetime.now().isoformat()
                    }, f, ensure_ascii=False, indent=2)
                print(f"[DEBUG] 调试信息已保存到: {file_path}")
                
                return resp
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