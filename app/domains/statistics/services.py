# 统计领域服务
# 处理统计相关的业务逻辑

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError, NotFoundError
from ...shared.enums.business_enums import AsinType, ReportType
from ...shared.constants.business_constants import (
    DEFAULT_BATCH_SIZE,
    MAX_BATCH_SIZE,
    DATE_FORMAT
)

# 导入原有的服务（临时兼容）
try:
    from ...services.statistics_service import StatisticsService as OriginalStatisticsService
except ImportError:
    OriginalStatisticsService = None


class StatisticsService:
    """统计服务"""
    
    def __init__(self):
        # 临时兼容原有服务
        self._original_service = OriginalStatisticsService() if OriginalStatisticsService else None
    
    async def get_sales_report(
        self,
        sid: str,
        asin_type: int,
        asin: Optional[str] = None,
        event_date: Optional[str] = None,
        marketplace: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取销量报表
        
        Args:
            sid: 店铺ID
            asin_type: ASIN类型
            asin: ASIN或MSKU
            event_date: 事件日期
            marketplace: 市场
            page: 页码
            page_size: 每页大小
            
        Returns:
            销量报表数据
        """
        try:
            # 参数验证
            if not sid:
                raise ValidationError("店铺ID不能为空")
            
            if not event_date:
                raise ValidationError("事件日期不能为空")
            
            # 验证日期格式
            try:
                datetime.strptime(event_date, DATE_FORMAT)
            except ValueError:
                raise ValidationError("日期格式不正确，应为YYYY-MM-DD")
            
            # 验证ASIN类型
            if asin_type not in [AsinType.ASIN, AsinType.MSKU]:
                raise ValidationError("ASIN类型无效")
            
            # 验证分页参数
            if page < 1:
                raise ValidationError("页码必须大于0")
            
            if page_size < 1 or page_size > MAX_BATCH_SIZE:
                raise ValidationError(f"每页大小必须在1-{MAX_BATCH_SIZE}之间")
            
            # 如果有原有服务，优先使用
            if self._original_service:
                try:
                    # 调用原有服务方法
                    if hasattr(self._original_service, 'get_sales_report_asin_daily_lists'):
                        result = await self._call_original_service(
                            'get_sales_report_asin_daily_lists',
                            {
                                'sid': sid,
                                'asin_type': asin_type,
                                'asin': asin,
                                'event_date': event_date,
                                'marketplace': marketplace
                            }
                        )
                        
                        # 处理分页
                        data = result if isinstance(result, list) else []
                        total = len(data)
                        start_idx = (page - 1) * page_size
                        end_idx = start_idx + page_size
                        paginated_data = data[start_idx:end_idx]
                        
                        return {
                            'data': paginated_data,
                            'total': total
                        }
                except Exception as e:
                    # 如果原有服务调用失败，记录错误并继续使用新逻辑
                    print(f"调用原有服务失败: {e}")
            
            # 新的业务逻辑实现
            return await self._get_sales_report_new(
                sid, asin_type, asin, event_date, marketplace, page, page_size
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取销量报表失败: {str(e)}")
    
    async def get_order_profit(
        self,
        sid: str,
        msku: Optional[str] = None,
        order_id: Optional[str] = None,
        marketplace: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取订单利润数据"""
        try:
            # 参数验证
            if not sid:
                raise ValidationError("店铺ID不能为空")
            
            # 验证分页参数
            if page < 1:
                raise ValidationError("页码必须大于0")
            
            if page_size < 1 or page_size > MAX_BATCH_SIZE:
                raise ValidationError(f"每页大小必须在1-{MAX_BATCH_SIZE}之间")
            
            # 如果有原有服务，优先使用
            if self._original_service:
                try:
                    if hasattr(self._original_service, 'get_order_profit_msku'):
                        result = await self._call_original_service(
                            'get_order_profit_msku',
                            {
                                'sid': sid,
                                'msku': msku,
                                'order_id': order_id,
                                'marketplace': marketplace,
                                'start_date': start_date,
                                'end_date': end_date
                            }
                        )
                        
                        # 处理分页
                        data = result if isinstance(result, list) else []
                        total = len(data)
                        start_idx = (page - 1) * page_size
                        end_idx = start_idx + page_size
                        paginated_data = data[start_idx:end_idx]
                        
                        return {
                            'data': paginated_data,
                            'total': total
                        }
                except Exception as e:
                    print(f"调用原有服务失败: {e}")
            
            # 新的业务逻辑实现
            return await self._get_order_profit_new(
                sid, msku, order_id, marketplace, start_date, end_date, page, page_size
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取订单利润失败: {str(e)}")
    
    async def get_product_performance(
        self,
        sid: str,
        asin: Optional[str] = None,
        marketplace: Optional[str] = None,
        report_type: int = ReportType.SALES,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取产品表现数据"""
        try:
            # 参数验证
            if not sid:
                raise ValidationError("店铺ID不能为空")
            
            if report_type not in [ReportType.SALES, ReportType.QUANTITY, ReportType.ORDERS]:
                raise ValidationError("报表类型无效")
            
            # 验证分页参数
            if page < 1:
                raise ValidationError("页码必须大于0")
            
            if page_size < 1 or page_size > MAX_BATCH_SIZE:
                raise ValidationError(f"每页大小必须在1-{MAX_BATCH_SIZE}之间")
            
            # 新的业务逻辑实现
            return await self._get_product_performance_new(
                sid, asin, marketplace, report_type, start_date, end_date, page, page_size
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取产品表现失败: {str(e)}")
    
    async def get_profit_statistics(
        self,
        sid: str,
        marketplace: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        group_by: str = 'day'
    ) -> Dict[str, Any]:
        """获取利润统计数据"""
        try:
            # 参数验证
            if not sid:
                raise ValidationError("店铺ID不能为空")
            
            if group_by not in ['day', 'week', 'month']:
                raise ValidationError("分组方式只能是 day, week, month")
            
            # 新的业务逻辑实现
            return await self._get_profit_statistics_new(
                sid, marketplace, start_date, end_date, group_by
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取利润统计失败: {str(e)}")
    
    async def get_shipment_removal(
        self,
        sid: str,
        removal_order_id: Optional[str] = None,
        disposition: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取移除货件报表"""
        try:
            # 参数验证
            if not sid:
                raise ValidationError("店铺ID不能为空")
            
            # 验证分页参数
            if page < 1:
                raise ValidationError("页码必须大于0")
            
            if page_size < 1 or page_size > MAX_BATCH_SIZE:
                raise ValidationError(f"每页大小必须在1-{MAX_BATCH_SIZE}之间")
            
            # 新的业务逻辑实现
            return await self._get_shipment_removal_new(
                sid, removal_order_id, disposition, start_date, end_date, page, page_size
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取移除货件报表失败: {str(e)}")
    
    async def _call_original_service(self, method_name: str, params: Dict[str, Any]) -> Any:
        """调用原有服务方法"""
        if not self._original_service:
            raise BusinessLogicError("原有服务不可用")
        
        method = getattr(self._original_service, method_name, None)
        if not method:
            raise BusinessLogicError(f"方法 {method_name} 不存在")
        
        # 如果是异步方法
        if asyncio.iscoroutinefunction(method):
            return await method(**params)
        else:
            # 如果是同步方法，在线程池中执行
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: method(**params))
    
    async def _get_sales_report_new(
        self, sid: str, asin_type: int, asin: Optional[str],
        event_date: str, marketplace: Optional[str], page: int, page_size: int
    ) -> Dict[str, Any]:
        """新的销量报表实现"""
        # TODO: 实现新的销量报表逻辑
        # 这里应该连接数据库或调用外部API获取数据
        
        # 模拟数据（实际应该从数据库获取）
        mock_data = [
            {
                'asin': 'B001TEST001',
                'title': '测试产品1',
                'sales_amount': 1500.00,
                'sales_quantity': 50,
                'order_count': 25,
                'marketplace': marketplace or 'US',
                'event_date': event_date
            },
            {
                'asin': 'B001TEST002',
                'title': '测试产品2',
                'sales_amount': 2300.00,
                'sales_quantity': 75,
                'order_count': 40,
                'marketplace': marketplace or 'US',
                'event_date': event_date
            }
        ]
        
        # 如果指定了ASIN，进行筛选
        if asin:
            mock_data = [item for item in mock_data if item['asin'] == asin]
        
        # 分页处理
        total = len(mock_data)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = mock_data[start_idx:end_idx]
        
        return {
            'data': paginated_data,
            'total': total
        }
    
    async def _get_order_profit_new(
        self, sid: str, msku: Optional[str], order_id: Optional[str],
        marketplace: Optional[str], start_date: Optional[str], end_date: Optional[str],
        page: int, page_size: int
    ) -> Dict[str, Any]:
        """新的订单利润实现"""
        # TODO: 实现新的订单利润逻辑
        
        # 模拟数据
        mock_data = [
            {
                'order_id': 'ORDER001',
                'msku': 'MSKU001',
                'asin': 'B001TEST001',
                'title': '测试产品1',
                'quantity': 2,
                'unit_price': 30.00,
                'total_amount': 60.00,
                'cost': 40.00,
                'profit': 20.00,
                'profit_margin': 33.33,
                'marketplace': marketplace or 'US',
                'order_date': '2024-01-15'
            }
        ]
        
        # 筛选逻辑
        if msku:
            mock_data = [item for item in mock_data if item['msku'] == msku]
        if order_id:
            mock_data = [item for item in mock_data if item['order_id'] == order_id]
        
        # 分页处理
        total = len(mock_data)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = mock_data[start_idx:end_idx]
        
        return {
            'data': paginated_data,
            'total': total
        }
    
    async def _get_product_performance_new(
        self, sid: str, asin: Optional[str], marketplace: Optional[str],
        report_type: int, start_date: Optional[str], end_date: Optional[str],
        page: int, page_size: int
    ) -> Dict[str, Any]:
        """新的产品表现实现"""
        # TODO: 实现新的产品表现逻辑
        
        # 模拟数据
        mock_data = [
            {
                'asin': 'B001TEST001',
                'title': '测试产品1',
                'marketplace': marketplace or 'US',
                'sales_rank': 1500,
                'category_rank': 25,
                'review_count': 150,
                'review_rating': 4.5,
                'price': 30.00,
                'sales_amount': 1500.00,
                'sales_quantity': 50,
                'conversion_rate': 12.5,
                'click_through_rate': 8.2
            }
        ]
        
        # 筛选逻辑
        if asin:
            mock_data = [item for item in mock_data if item['asin'] == asin]
        
        # 分页处理
        total = len(mock_data)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = mock_data[start_idx:end_idx]
        
        return {
            'data': paginated_data,
            'total': total
        }
    
    async def _get_profit_statistics_new(
        self, sid: str, marketplace: Optional[str], start_date: Optional[str],
        end_date: Optional[str], group_by: str
    ) -> Dict[str, Any]:
        """新的利润统计实现"""
        # TODO: 实现新的利润统计逻辑
        
        # 模拟数据
        mock_data = [
            {
                'period': '2024-01-15',
                'total_sales': 5000.00,
                'total_cost': 3000.00,
                'total_profit': 2000.00,
                'profit_margin': 40.0,
                'order_count': 100,
                'product_count': 25
            }
        ]
        
        summary = {
            'total_sales': sum(item['total_sales'] for item in mock_data),
            'total_profit': sum(item['total_profit'] for item in mock_data),
            'avg_profit_margin': sum(item['profit_margin'] for item in mock_data) / len(mock_data)
        }
        
        return {
            'data': mock_data,
            'summary': summary
        }
    
    async def _get_shipment_removal_new(
        self, sid: str, removal_order_id: Optional[str], disposition: Optional[str],
        start_date: Optional[str], end_date: Optional[str], page: int, page_size: int
    ) -> Dict[str, Any]:
        """新的移除货件报表实现"""
        # TODO: 实现新的移除货件报表逻辑
        
        # 模拟数据
        mock_data = [
            {
                'removal_order_id': 'REMOVAL001',
                'request_date': '2024-01-15',
                'order_status': 'Completed',
                'order_type': 'Return',
                'sku': 'SKU001',
                'fnsku': 'FNSKU001',
                'disposition': 'Return',
                'requested_quantity': 10,
                'cancelled_quantity': 0,
                'disposed_quantity': 10,
                'shipped_quantity': 10
            }
        ]
        
        # 筛选逻辑
        if removal_order_id:
            mock_data = [item for item in mock_data if item['removal_order_id'] == removal_order_id]
        if disposition:
            mock_data = [item for item in mock_data if item['disposition'] == disposition]
        
        # 分页处理
        total = len(mock_data)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_data = mock_data[start_idx:end_idx]
        
        return {
            'data': paginated_data,
            'total': total
        }