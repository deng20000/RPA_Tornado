# -*- coding: utf-8 -*-
"""
电商数据看板处理器
处理电商数据看板相关的HTTP请求
"""

import logging
import traceback
from datetime import datetime
from typing import Any, Dict, Optional

from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode
from pydantic import ValidationError

from app.services.dashboard_service import DashboardService
from app.schemas.dashboard_schemas import (
    SyncShopDataRequest,
    SyncExchangeRateRequest,
    SyncSalesDataRequest,
    ShopListRequest,
    SalesStatisticsRequest,
    CurrencyConversionRequest,
    ErrorResponse,
    SuccessResponse
)
from app.core.exceptions import (
    ValidationException,
    BusinessException,
    DatabaseException
)
from app.core.response import ResponseHandler

# 配置日志记录器
logger = logging.getLogger(__name__)


class BaseDashboardHandler(RequestHandler):
    """电商数据看板基础处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboard_service = DashboardService()
        self.response_handler = ResponseHandler()
    
    def set_default_headers(self):
        """设置默认响应头"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    
    def options(self, *args):
        """处理预检请求"""
        self.set_status(204)
        self.finish()
    
    def write_error(self, status_code: int, **kwargs):
        """自定义错误响应"""
        error_message = "Internal Server Error"
        error_details = None
        
        if "exc_info" in kwargs:
            exc_type, exc_value, exc_traceback = kwargs["exc_info"]
            if isinstance(exc_value, ValidationException):
                status_code = 400
                error_message = str(exc_value)
                error_details = getattr(exc_value, 'details', None)
            elif isinstance(exc_value, BusinessException):
                status_code = 422
                error_message = str(exc_value)
                error_details = getattr(exc_value, 'details', None)
            elif isinstance(exc_value, DatabaseException):
                status_code = 500
                error_message = "数据库操作失败"
                logger.error(f"数据库错误: {exc_value}")
            else:
                logger.error(f"未处理的异常: {exc_value}")
                logger.error(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        error_response = ErrorResponse(
            code=status_code,
            message=error_message,
            details=error_details,
            timestamp=datetime.now().isoformat()
        )
        
        self.set_status(status_code)
        self.write(error_response.dict())
        self.finish()
    
    def parse_request_body(self, schema_class):
        """解析请求体并验证"""
        try:
            if not self.request.body:
                raise ValidationException("请求体不能为空")
            
            body_data = json_decode(self.request.body)
            return schema_class(**body_data)
        except (ValueError, TypeError) as e:
            raise ValidationException(f"JSON格式错误: {str(e)}")
        except ValidationError as e:
            raise ValidationException(f"参数验证失败: {str(e)}")
    
    def get_query_params(self, schema_class):
        """获取并验证查询参数"""
        try:
            params = {}
            for key in self.request.arguments:
                value = self.get_argument(key)
                params[key] = value
            return schema_class(**params)
        except ValidationError as e:
            raise ValidationException(f"查询参数验证失败: {str(e)}")
    
    def write_success_response(self, data: Any = None, message: str = "操作成功", code: int = 200):
        """写入成功响应"""
        response = SuccessResponse(
            code=code,
            message=message,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        self.write(response.dict())
        self.finish()


class SyncShopDataHandler(BaseDashboardHandler):
    """同步店铺数据处理器"""
    
    async def post(self):
        """同步店铺数据"""
        try:
            # 解析请求参数
            request_data = self.parse_request_body(SyncShopDataRequest)
            
            logger.info(f"开始同步店铺数据，访问令牌: {request_data.access_token[:10]}...")
            
            # 调用服务层同步数据
            result = await self.dashboard_service.sync_shop_data(request_data.access_token)
            
            logger.info(f"店铺数据同步完成，新增: {result['synced_count']} 条记录")
            
            self.write_success_response(
                data=result,
                message="店铺数据同步成功"
            )
            
        except Exception as e:
            logger.error(f"同步店铺数据失败: {str(e)}")
            raise


class SyncExchangeRateHandler(BaseDashboardHandler):
    """同步汇率数据处理器"""
    
    async def post(self):
        """同步汇率数据"""
        try:
            # 解析请求参数
            request_data = self.parse_request_body(SyncExchangeRateRequest)
            
            logger.info(f"开始同步汇率数据，目标日期: {request_data.target_date}")
            
            # 调用服务层同步数据
            result = await self.dashboard_service.sync_exchange_rate_data(
                request_data.access_token,
                request_data.target_date
            )
            
            logger.info(f"汇率数据同步完成，新增: {result['synced_count']} 条记录")
            
            self.write_success_response(
                data=result,
                message="汇率数据同步成功"
            )
            
        except Exception as e:
            logger.error(f"同步汇率数据失败: {str(e)}")
            raise


class SyncSalesDataHandler(BaseDashboardHandler):
    """同步销售数据处理器"""
    
    async def post(self):
        """同步销售数据"""
        try:
            # 解析请求参数
            request_data = self.parse_request_body(SyncSalesDataRequest)
            
            logger.info(f"开始同步销售数据，时间范围: {request_data.start_date} - {request_data.end_date}")
            
            # 调用服务层同步数据
            result = await self.dashboard_service.sync_sales_data_with_period(
                request_data.access_token,
                request_data.start_date,
                request_data.end_date
            )
            
            logger.info(f"销售数据同步完成，新增: {result['synced_count']} 条记录")
            
            self.write_success_response(
                data=result,
                message="销售数据同步成功"
            )
            
        except Exception as e:
            logger.error(f"同步销售数据失败: {str(e)}")
            raise


class DashboardSummaryHandler(BaseDashboardHandler):
    """数据看板摘要处理器"""
    
    async def get(self):
        """获取数据看板摘要信息"""
        try:
            logger.info("获取数据看板摘要信息")
            
            # 调用服务层获取摘要数据
            summary_data = await self.dashboard_service.get_dashboard_summary()
            
            logger.info("数据看板摘要信息获取成功")
            
            self.write_success_response(
                data=summary_data,
                message="获取数据看板摘要成功"
            )
            
        except Exception as e:
            logger.error(f"获取数据看板摘要失败: {str(e)}")
            raise


class ShopListHandler(BaseDashboardHandler):
    """店铺列表处理器"""
    
    async def get(self):
        """获取店铺列表"""
        try:
            # 解析查询参数
            query_params = self.get_query_params(ShopListRequest)
            
            logger.info(f"获取店铺列表，页码: {query_params.page}，每页: {query_params.page_size}")
            
            # 调用服务层获取店铺列表
            shop_list = await self.dashboard_service.get_shop_list(
                page=query_params.page,
                page_size=query_params.page_size,
                platform=query_params.platform
            )
            
            logger.info(f"店铺列表获取成功，共 {shop_list['total']} 条记录")
            
            self.write_success_response(
                data=shop_list,
                message="获取店铺列表成功"
            )
            
        except Exception as e:
            logger.error(f"获取店铺列表失败: {str(e)}")
            raise


class SalesStatisticsHandler(BaseDashboardHandler):
    """销售统计处理器"""
    
    async def get(self):
        """获取销售统计数据"""
        try:
            # 解析查询参数
            query_params = self.get_query_params(SalesStatisticsRequest)
            
            logger.info(f"获取销售统计，时间范围: {query_params.start_date} - {query_params.end_date}")
            
            # 调用服务层获取销售统计
            statistics = await self.dashboard_service.get_sales_statistics(
                start_date=query_params.start_date,
                end_date=query_params.end_date,
                shop_id=query_params.shop_id,
                currency=query_params.currency
            )
            
            logger.info("销售统计数据获取成功")
            
            self.write_success_response(
                data=statistics,
                message="获取销售统计成功"
            )
            
        except Exception as e:
            logger.error(f"获取销售统计失败: {str(e)}")
            raise


class CurrencyConversionHandler(BaseDashboardHandler):
    """货币转换处理器"""
    
    async def post(self):
        """货币转换"""
        try:
            # 解析请求参数
            request_data = self.parse_request_body(CurrencyConversionRequest)
            
            logger.info(f"货币转换: {request_data.amount} {request_data.from_currency} -> {request_data.to_currency}")
            
            # 调用服务层进行货币转换
            conversion_result = await self.dashboard_service.convert_currency(
                amount=request_data.amount,
                from_currency=request_data.from_currency,
                to_currency=request_data.to_currency,
                conversion_date=request_data.conversion_date
            )
            
            logger.info("货币转换完成")
            
            self.write_success_response(
                data=conversion_result,
                message="货币转换成功"
            )
            
        except Exception as e:
            logger.error(f"货币转换失败: {str(e)}")
            raise


class HealthCheckHandler(BaseDashboardHandler):
    """健康检查处理器"""
    
    async def get(self):
        """健康检查"""
        try:
            # 检查数据库连接
            health_status = await self.dashboard_service.health_check()
            
            if health_status['status'] == 'healthy':
                self.write_success_response(
                    data=health_status,
                    message="服务运行正常"
                )
            else:
                self.set_status(503)
                self.write({
                    'code': 503,
                    'message': '服务不可用',
                    'data': health_status,
                    'timestamp': datetime.now().isoformat()
                })
                self.finish()
                
        except Exception as e:
            logger.error(f"健康检查失败: {str(e)}")
            self.set_status(503)
            self.write({
                'code': 503,
                'message': '服务不可用',
                'data': {'status': 'unhealthy', 'error': str(e)},
                'timestamp': datetime.now().isoformat()
            })
            self.finish()


# 导出所有处理器
__all__ = [
    'BaseDashboardHandler',
    'SyncShopDataHandler',
    'SyncExchangeRateHandler',
    'SyncSalesDataHandler',
    'DashboardSummaryHandler',
    'ShopListHandler',
    'SalesStatisticsHandler',
    'CurrencyConversionHandler',
    'HealthCheckHandler'
]