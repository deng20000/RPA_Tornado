# amazon_table_handler.py
# 亚马逊源表数据处理器
# 负责处理亚马逊原始表数据相关的HTTP请求

import json
from tornado.web import RequestHandler
from app.services.amazon_table_service import AmazonTableService
from .base import BaseHandler

class RemovalShipmentListHandler(BaseHandler):
    """
    查询亚马逊源报表-移除货件（新）
    查询 Reports-Fulfillment-Removal Shipment Detail 报表
    报表为seller_id维度，按sid请求会返回对应seller_id下所有移除订单数据
    分组: 亚马逊源表数据
    路径: /erp/sc/statistic/removalShipment/list
    """
    
    async def post(self):
        """
        处理移除货件报表查询请求
        
        请求参数:
        - sid: 店铺ID（可选，与seller_id二选一）
        - seller_id: 卖家ID（可选，与sid二选一）
        - start_date: 开始日期，格式YYYY-MM-DD（必填）
        - end_date: 结束日期，格式YYYY-MM-DD（必填）
        - offset: 偏移量，默认0（可选）
        - length: 返回数量，默认1000，最大10000（可选）
        """
        try:
            # 解析请求体
            data = json.loads(self.request.body.decode('utf-8'))
            
            # 参数校验
            required_fields = ['start_date', 'end_date']
            for field in required_fields:
                if field not in data or data[field] is None:
                    self.set_status(400)
                    self.write({
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    })
                    return
            
            # sid和seller_id至少需要一个
            seller_id = data.get('seller_id')
            if not data.get('sid') and not seller_id:
                self.set_status(400)
                self.write({
                    'code': 400,
                    'message': 'sid和seller_id至少需要传递一个',
                    'data': None
                })
                return
            
            # 如果seller_id是数组，处理多个seller_id的情况
            if seller_id and isinstance(seller_id, list):
                if len(seller_id) == 0:
                    self.set_status(400)
                    self.write({
                        'code': 400,
                        'message': 'seller_id数组不能为空',
                        'data': None
                    })
                    return
                # 对于多个seller_id，我们需要分别查询然后合并结果
                all_results = []
                service = AmazonTableService()
                
                for single_seller_id in seller_id:
                    # 为每个seller_id创建单独的查询参数
                    single_data = data.copy()
                    single_data['seller_id'] = single_seller_id
                    if 'sid' in single_data:
                        del single_data['sid']  # 移除sid，使用seller_id
                    
                    result = await service.get_removal_shipment_list(single_data)
                    if result.get('code') == 200 and result.get('data'):
                        if isinstance(result['data'], list):
                            all_results.extend(result['data'])
                        elif isinstance(result['data'], dict) and 'list' in result['data']:
                            all_results.extend(result['data']['list'])
                
                # 返回合并后的结果
                self.set_header('Content-Type', 'application/json')
                self.write(json.dumps({
                    'code': 200,
                    'message': '查询成功',
                    'data': all_results
                }, ensure_ascii=False))
                return
            
            # 调用亚马逊源表数据服务
            service = AmazonTableService()
            result = await service.get_removal_shipment_list(data)
            
            # 返回结果
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError:
            self.set_status(400)
            self.write({
                'code': 400,
                'message': '请求体格式错误，请使用有效的JSON格式',
                'data': None
            })
        except Exception as e:
            print(f"[ERROR] RemovalShipmentListHandler: {str(e)}")
            self.set_status(500)
            self.write({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            })


class RemovalOrderListNewHandler(BaseHandler):
    """移除订单报表查询处理器（新）"""
    
    async def post(self):
        """
        处理移除订单报表查询请求
        查询 Reports-Fulfillment-Removal Order Detail 报表
        """
        try:
            # 解析请求参数
            request_data = json.loads(self.request.body)
            
            # 提取参数
            params = {
                'sid': request_data.get('sid'),
                'start_date': request_data.get('start_date'),
                'end_date': request_data.get('end_date'),
                'search_field_time': request_data.get('search_field_time', 'last_updated_date'),
                'offset': request_data.get('offset', 0),
                'length': request_data.get('length', 1000)
            }
            
            # 参数校验
            if not params.get('sid'):
                self.write({
                    'code': 400,
                    'message': '缺少必填参数: sid',
                    'data': None
                })
                return
            
            if not params.get('start_date') or not params.get('end_date'):
                self.write({
                    'code': 400,
                    'message': '缺少必填参数: start_date 或 end_date',
                    'data': None
                })
                return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_removal_order_list_new(params)
            
            # 返回结果
            self.write(result)
            
        except json.JSONDecodeError:
            self.write({
                'code': 400,
                'message': '请求体格式错误，请使用有效的JSON格式',
                'data': None
            })
        except Exception as e:
            self.write({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            })


class AllOrdersHandler(BaseHandler):
    """查询亚马逊源报表-所有订单处理器"""
    
    async def post(self):
        """处理所有订单报表查询请求"""
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write(json.dumps({
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }, ensure_ascii=False))
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_all_orders(params)
            
            # 返回响应
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.write(json.dumps({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, ensure_ascii=False))


class FbaOrdersHandler(BaseHandler):
    """查询亚马逊源报表-FBA订单处理器"""
    
    async def post(self):
        """处理FBA订单报表查询请求"""
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write(json.dumps({
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }, ensure_ascii=False))
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_fba_orders(params)
            
            # 返回响应
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.write(json.dumps({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, ensure_ascii=False))


class FbaExchangeOrdersHandler(BaseHandler):
    """查询亚马逊源报表-FBA换货订单处理器"""
    
    async def post(self):
        """处理FBA换货订单报表查询请求"""
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write(json.dumps({
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }, ensure_ascii=False))
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_fba_exchange_orders(params)
            
            # 返回响应
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.write(json.dumps({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, ensure_ascii=False))


class FbaRefundOrdersHandler(BaseHandler):
    """查询亚马逊源报表-FBA退货订单处理器"""
    
    async def post(self):
        """处理FBA退货订单报表查询请求"""
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write(json.dumps({
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }, ensure_ascii=False))
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_fba_refund_orders(params)
            
            # 返回响应
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.write(json.dumps({
                'code': 500,
                'message': f'服务器内部错误: {str(e)}',
                'data': None
            }, ensure_ascii=False))


class FbmReturnOrdersHandler(BaseHandler):
    """FBM退货订单报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid', 'date_type', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_fbm_return_orders(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询FBM退货订单报表失败: {str(e)}')


class ManageInventoryHandler(BaseHandler):
    """FBA库存报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_manage_inventory(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询FBA库存报表失败: {str(e)}')


class DailyInventoryHandler(BaseHandler):
    """每日库存报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid', 'event_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_daily_inventory(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询每日库存报表失败: {str(e)}')


class AfnFulfillableQuantityHandler(BaseHandler):
    """FBA可售库存报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_afn_fulfillable_quantity(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询FBA可售库存报表失败: {str(e)}')


class ReservedInventoryHandler(BaseHandler):
    """预留库存报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_reserved_inventory(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询预留库存报表失败: {str(e)}')


class FbaAgeListHandler(BaseHandler):
    """库龄表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_fba_age_list(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询库龄表失败: {str(e)}')


class AmazonFulfilledShipmentsListHandler(BaseHandler):
    """Amazon Fulfilled Shipments报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_amazon_fulfilled_shipments_list(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询Amazon Fulfilled Shipments报表失败: {str(e)}')


class AmazonFulfilledShipmentsListV1Handler(BaseHandler):
    """Amazon Fulfilled Shipments v1报表处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_amazon_fulfilled_shipments_list_v1(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询Amazon Fulfilled Shipments v1报表失败: {str(e)}')


class AdjustmentListHandler(BaseHandler):
    """盘存记录处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.get_adjustment_list(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询盘存记录失败: {str(e)}')


class CreateReportExportTaskHandler(BaseHandler):
    """创建报告导出任务处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['seller_id', 'report_type', 'marketplace_ids', 'region']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.create_report_export_task(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'创建报告导出任务失败: {str(e)}')


class QueryReportExportTaskHandler(BaseHandler):
    """查询报告导出任务结果处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['seller_id', 'task_id', 'region']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.query_report_export_task(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'查询报告导出任务结果失败: {str(e)}')


class AmazonReportExportTaskHandler(BaseHandler):
    """报告下载链接续期处理器"""
    
    async def post(self):
        try:
            # 解析请求参数
            params = self.get_request_params()
            
            # 必填参数校验
            required_fields = ['region', 'seller_id', 'report_document_id']
            for field in required_fields:
                if field not in params or params[field] is None:
                    self.write_error(400, f'缺少必填参数: {field}')
                    return
            
            # 调用服务层获取数据
            service = AmazonTableService()
            result = await service.amazon_report_export_task(params)
            
            self.write_json(result)
            
        except Exception as e:
            self.write_error(500, f'报告下载链接续期失败: {str(e)}')