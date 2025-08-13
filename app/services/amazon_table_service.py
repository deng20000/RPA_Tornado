# amazon_table_service.py
# 亚马逊源表数据服务
# 负责处理亚马逊原始表数据、数据同步等业务逻辑

from app.auth.openapi import OpenApiBase
from app.config import settings
from typing import Optional, Dict, Any

class AmazonTableService:
    """亚马逊源表数据服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.api = OpenApiBase(
            host=settings.LLX_API_HOST,
            app_id=settings.LLX_APP_ID,
            app_secret=settings.LLX_APP_SECRET
        )
    
    async def get_access_token(self):
        """获取访问令牌"""
        token_dto = await self.api.generate_access_token()
        return token_dto.access_token
    
    async def get_amazon_table(self, params):
        """获取亚马逊源表数据"""
        # TODO: 实现具体的亚马逊源表数据获取逻辑
        pass
    
    async def get_removal_shipment_list(self, params):
        """
        查询亚马逊源报表-移除货件（新）
        查询 Reports-Fulfillment-Removal Shipment Detail 报表
        Args:
            params: 请求参数，包含sid、seller_id、start_date、end_date、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid和seller_id至少有一个
            if not params.get('sid') and not params.get('seller_id'):
                return {
                    'code': 400,
                    'message': 'sid和seller_id至少需要传递一个',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'offset': offset,
                'length': length,
                'search_field_time': params.get('search_field_time', 'last_updated_date')  # 添加默认的search_field_time
            }
            
            # sid优先级高于seller_id
            if params.get('sid'):
                query_data['sid'] = params['sid']
                
                # 4. 调用外部API获取移除货件报表数据
                # 注意：由于领星API中没有专门的removalShipmentList接口，
                # 这里使用removalOrderListNew接口来获取移除相关数据
                access_token = await self.get_access_token()
                resp = await self.api.request(
                    access_token=access_token,
                    route_name="/erp/sc/routing/data/order/removalOrderListNew",
                    method="POST",
                    req_body=query_data
                )
                
                return resp.model_dump()
                
            elif params.get('seller_id'):
                # 通过seller_id获取对应的所有sid，然后分别查询并合并结果
                seller_id = params['seller_id']
                
                # 获取seller_id对应的所有sid
                sid_list = await self._get_sid_list_by_seller_id(seller_id)
                if not sid_list:
                    return {
                        'code': 400,
                        'message': f'未找到seller_id {seller_id} 对应的店铺信息',
                        'data': None
                    }
                
                # 分别查询每个sid的数据并合并
                all_results = []
                access_token = await self.get_access_token()
                
                for sid in sid_list:
                    single_query_data = query_data.copy()
                    single_query_data['sid'] = sid
                    
                    try:
                        resp = await self.api.request(
                            access_token=access_token,
                            route_name="/erp/sc/routing/data/order/removalOrderListNew",
                            method="POST",
                            req_body=single_query_data
                        )
                        
                        result = resp.model_dump()
                        if result.get('code') == 0 and result.get('data'):
                            if isinstance(result['data'], list):
                                all_results.extend(result['data'])
                            elif isinstance(result['data'], dict) and 'list' in result['data']:
                                all_results.extend(result['data']['list'])
                    except Exception as e:
                        print(f"[WARNING] 查询sid {sid} 的移除货件数据失败: {str(e)}")
                        continue
                
                return {
                    'code': 0,
                    'message': 'success',
                    'data': all_results
                }

            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询移除货件报表失败: {str(e)}',
                'data': None
            }
    
    async def get_removal_order_list_new(self, params):
        """
        查询亚马逊源报表-移除订单（新）
        查询 Reports-Fulfillment-Removal Order Detail 报表
        Args:
            params: 请求参数，包含sid、start_date、end_date、offset、length、search_field_time
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date', 'search_field_time']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # search_field_time校验
            search_field_time = params.get('search_field_time')
            valid_search_fields = ['last_updated_date', 'request_date']
            if search_field_time not in valid_search_fields:
                return {
                    'code': 400,
                    'message': f'search_field_time必须为: {", ".join(valid_search_fields)}',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'search_field_time': search_field_time,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取移除订单报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/order/removalOrderListNew",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询移除订单报表失败: {str(e)}',
                'data': None
            }
    
    async def get_all_orders(self, params):
        """
        查询亚马逊源报表-所有订单
        查询 All Orders Report By last update 报表
        Args:
            params: 请求参数，包含sid、start_date、end_date、date_type、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # date_type校验
            date_type = params.get('date_type', 1)
            if date_type not in [1, 2]:
                return {
                    'code': 400,
                    'message': 'date_type必须为1（下单日期）或2（亚马逊订单更新时间）',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'date_type': date_type,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取所有订单报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/allOrders",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询所有订单报表失败: {str(e)}',
                'data': None
            }
    
    async def get_fba_orders(self, params):
        """
        查询亚马逊源报表-FBA订单
        查询 Amazon-Fulfilled Shipments Report 报表
        Args:
            params: 请求参数，包含sid、start_date、end_date、date_type、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # date_type校验
            date_type = params.get('date_type', 1)
            if date_type not in [1, 2]:
                return {
                    'code': 400,
                    'message': 'date_type必须为1（下单日期）或2（配送日期）',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'date_type': date_type,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取FBA订单报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/fbaOrders",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询FBA订单报表失败: {str(e)}',
                'data': None
            }
    
    async def get_fba_exchange_orders(self, params):
        """
        查询亚马逊源报表-FBA换货订单
        查询 Replacements Report 报表
        Args:
            params: 请求参数，包含sid、start_date、end_date、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取FBA换货订单报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/order/fbaExchangeOrderList",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询FBA换货订单报表失败: {str(e)}',
                'data': None
            }
    
    async def get_fba_refund_orders(self, params):
        """
        查询亚马逊源报表-FBA退货订单
        查询 FBA customer returns 报表
        Args:
            params: 请求参数，包含sid、start_date、end_date、date_type、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # date_type校验
            date_type = params.get('date_type', 1)
            if date_type not in [1, 2]:
                return {
                    'code': 400,
                    'message': 'date_type必须为1（退货时间）或2（更新时间）',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'date_type': date_type,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取FBA退货订单报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/refundOrders",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询FBA退货订单报表失败: {str(e)}',
                'data': None
            }
    
    async def get_fbm_return_orders(self, params):
        """
        查询亚马逊源报表-FBM退货订单
        查询 Returns Reports 报表
        Args:
            params: 请求参数，包含sid、start_date、end_date、date_type、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'start_date', 'end_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            for date_field in ['start_date', 'end_date']:
                try:
                    datetime.strptime(params[date_field], '%Y-%m-%d')
                except ValueError:
                    return {
                        'code': 400,
                        'message': f'{date_field}格式错误，应为YYYY-MM-DD',
                        'data': None
                    }
            
            # date_type校验
            date_type = params.get('date_type', 1)
            if date_type not in [1, 2]:
                return {
                    'code': 400,
                    'message': 'date_type必须为1（退货日期）或2（下单日期）',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'start_date': params['start_date'],
                'end_date': params['end_date'],
                'date_type': date_type,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取FBM退货订单报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/order/fbmReturnOrderList",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询FBM退货订单报表失败: {str(e)}',
                'data': None
            }
    
    async def get_manage_inventory(self, params):
        """
        查询亚马逊源报表-FBA库存
        查询 FBA Manage Inventory 报表
        Args:
            params: 请求参数，包含sid、offset、length
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取FBA库存报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/manageInventory",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询FBA库存报表失败: {str(e)}',
                'data': None
            }
    
    async def get_daily_inventory(self, params):
        """
        查询亚马逊源报表-每日库存
        查询 FBA Daily Inventory History Report 报表
        注意：由于亚马逊对应报表下线，2023年12月1日后不再更新此接口数据
        Args:
            params: 请求参数，包含sid、event_date、offset、length
        Returns:
            dict: 标准响应
        """
        from datetime import datetime
        try:
            # 1. 必填参数校验
            required_fields = ['sid', 'event_date']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # 日期格式校验
            event_date = params.get('event_date')
            try:
                datetime.strptime(event_date, '%Y-%m-%d')
            except ValueError:
                return {
                    'code': 400,
                    'message': 'event_date格式错误，应为YYYY-MM-DD',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'event_date': event_date,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取每日库存报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/dailyInventory",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询每日库存报表失败: {str(e)}',
                'data': None
            }
    
    async def get_afn_fulfillable_quantity(self, params):
        """
        查询亚马逊源报表-FBA可售库存
        查询 FBA Multi-Country Inventory Report 报表
        Args:
            params: 请求参数，包含sid、offset、length
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取FBA可售库存报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/getAfnFulfillableQuantity",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询FBA可售库存报表失败: {str(e)}',
                'data': None
            }
    
    async def get_reserved_inventory(self, params):
        """
        查询亚马逊源报表-预留库存
        查询 FBA Reserved Inventory Report 报表
        Args:
            params: 请求参数，包含sid、offset、length
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为正整数
            sid = params.get('sid')
            if not isinstance(sid, int) or sid <= 0:
                return {
                    'code': 400,
                    'message': 'sid必须为正整数',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 1000)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取预留库存报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/reservedInventory",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询预留库存报表失败: {str(e)}',
                'data': None
            }
    
    async def get_fba_age_list(self, params):
        """
        查询亚马逊源报表-库龄表
        查询 Manage Inventory Health 报表
        Args:
            params: 请求参数，包含sid、offset、length
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['sid']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # sid必须为字符串（支持多个店铺ID用逗号分隔）
            sid = params.get('sid')
            if not isinstance(sid, str) or not sid.strip():
                return {
                    'code': 400,
                    'message': 'sid必须为非空字符串',
                    'data': None
                }
            
            # offset和length校验
            offset = params.get('offset', 0)
            length = params.get('length', 20)
            
            if not isinstance(offset, int) or offset < 0:
                return {'code': 400, 'message': 'offset必须为非负整数', 'data': None}
            
            if not isinstance(length, int) or length <= 0 or length > 10000:
                return {'code': 400, 'message': 'length必须为1~10000的整数', 'data': None}
            
            # 3. 组装查询参数
            query_data = {
                'sid': sid,
                'offset': offset,
                'length': length
            }
            
            # 4. 调用外部API获取库龄表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/fba/fbaStock/getFbaAgeList",
                method="POST",
                req_body=query_data
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询库龄表失败: {str(e)}',
                'data': None
            }
    
    async def get_amazon_fulfilled_shipments_list(self, params):
        """
        查询亚马逊源报表-Amazon Fulfilled Shipments
        查询 Amazon Fulfilled Shipments 报表
        Args:
            params: 请求参数
        Returns:
            dict: 标准响应
        """
        try:
            # 调用外部API获取Amazon Fulfilled Shipments报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report/getAmazonFulfilledShipmentsList",
                method="POST",
                req_body=params
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询Amazon Fulfilled Shipments报表失败: {str(e)}',
                'data': None
            }
    
    async def get_amazon_fulfilled_shipments_list_v1(self, params):
        """
        查询亚马逊源报表-Amazon Fulfilled Shipments v1
        查询 Amazon Fulfilled Shipments 报表 v1版本
        Args:
            params: 请求参数
        Returns:
            dict: 标准响应
        """
        try:
            # 调用外部API获取Amazon Fulfilled Shipments v1报表数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/mws_report_v1/getAmazonFulfilledShipmentsList",
                method="POST",
                req_body=params
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询Amazon Fulfilled Shipments v1报表失败: {str(e)}',
                'data': None
            }
    
    async def get_adjustment_list(self, params):
        """
        查询亚马逊源报表-盘存记录
        Args:
            params: 请求参数
        Returns:
            dict: 标准响应
        """
        try:
            # 调用外部API获取盘存记录数据
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/openapi/mwsReport/adjustmentList",
                method="POST",
                req_body=params
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询盘存记录失败: {str(e)}',
                'data': None
            }
    
    async def create_report_export_task(self, params):
        """
        报告导出-创建导出任务
        Args:
            params: 请求参数，包含seller_id、report_type、marketplace_ids、region等
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['seller_id', 'report_type', 'marketplace_ids', 'region']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # seller_id必须为字符串
            seller_id = params.get('seller_id')
            if not isinstance(seller_id, str) or not seller_id.strip():
                return {
                    'code': 400,
                    'message': 'seller_id必须为非空字符串',
                    'data': None
                }
            
            # marketplace_ids必须为数组
            marketplace_ids = params.get('marketplace_ids')
            if not isinstance(marketplace_ids, list) or len(marketplace_ids) == 0:
                return {
                    'code': 400,
                    'message': 'marketplace_ids必须为非空数组',
                    'data': None
                }
            
            # region必须为指定值
            region = params.get('region')
            if region not in ['na', 'eu', 'fe']:
                return {
                    'code': 400,
                    'message': 'region必须为na、eu或fe',
                    'data': None
                }
            
            # 3. 调用外部API创建导出任务
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/report/create/reportExportTask",
                method="POST",
                req_body=params
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'创建报告导出任务失败: {str(e)}',
                'data': None
            }
    
    async def query_report_export_task(self, params):
        """
        报告导出-查询导出任务结果
        Args:
            params: 请求参数，包含seller_id、task_id、region
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['seller_id', 'task_id', 'region']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # seller_id必须为字符串
            seller_id = params.get('seller_id')
            if not isinstance(seller_id, str) or not seller_id.strip():
                return {
                    'code': 400,
                    'message': 'seller_id必须为非空字符串',
                    'data': None
                }
            
            # task_id必须为字符串
            task_id = params.get('task_id')
            if not isinstance(task_id, str) or not task_id.strip():
                return {
                    'code': 400,
                    'message': 'task_id必须为非空字符串',
                    'data': None
                }
            
            # region必须为指定值
            region = params.get('region')
            if region not in ['na', 'eu', 'fe']:
                return {
                    'code': 400,
                    'message': 'region必须为na、eu或fe',
                    'data': None
                }
            
            # 3. 调用外部API查询导出任务结果
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/report/query/reportExportTask",
                method="POST",
                req_body=params
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'查询报告导出任务结果失败: {str(e)}',
                'data': None
            }
    
    async def amazon_report_export_task(self, params):
        """
        报告导出-报告下载链接续期
        Args:
            params: 请求参数，包含region、seller_id、report_document_id
        Returns:
            dict: 标准响应
        """
        try:
            # 1. 必填参数校验
            required_fields = ['region', 'seller_id', 'report_document_id']
            for field in required_fields:
                if field not in params or params[field] is None:
                    return {
                        'code': 400,
                        'message': f'缺少必填参数: {field}',
                        'data': None
                    }
            
            # 2. 参数校验
            # seller_id必须为字符串
            seller_id = params.get('seller_id')
            if not isinstance(seller_id, str) or not seller_id.strip():
                return {
                    'code': 400,
                    'message': 'seller_id必须为非空字符串',
                    'data': None
                }
            
            # report_document_id必须为字符串
            report_document_id = params.get('report_document_id')
            if not isinstance(report_document_id, str) or not report_document_id.strip():
                return {
                    'code': 400,
                    'message': 'report_document_id必须为非空字符串',
                    'data': None
                }
            
            # region必须为指定值
            region = params.get('region')
            if region not in ['na', 'eu', 'fe']:
                return {
                    'code': 400,
                    'message': 'region必须为na、eu或fe',
                    'data': None
                }
            
            # 3. 调用外部API进行报告下载链接续期
            access_token = await self.get_access_token()
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/report/amazonReportExportTask",
                method="POST",
                req_body=params
            )
            
            return resp.model_dump()
            
        except Exception as e:
            return {
                'code': 500,
                'message': f'报告下载链接续期失败: {str(e)}',
                'data': None
            }
    
    async def _get_sid_list_by_seller_id(self, seller_id: str) -> list:
        """
        根据seller_id获取对应的所有sid列表
        Args:
            seller_id: 卖家ID
        Returns:
            list: sid列表
        """
        # 硬编码的seller_id到sid的映射关系
        # 这些数据来自于unprocessed_data目录下的amazon_seller_list.json文件
        seller_id_to_sid_mapping = {
            "A364119SDJA4QG": [505818, 505819, 505820, 505821],  # GL.iNet_NA
            "A3N83818QYC6JY": [516498, 516499, 516500, 516501, 516502, 516503, 516504, 516505, 516506, 516507],  # MIC-DE
            "A2EW9KKDYQK64I": [516508, 516509, 516510, 516511, 516512, 516513, 516514, 516515, 516516],  # GL.iNet_EU&UK
            "A3M67G05FKDBD7": [505881]  # GL.iNet_AU
        }
        
        return seller_id_to_sid_mapping.get(seller_id, [])