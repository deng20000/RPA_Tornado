# 统计领域处理器
# 处理统计相关的HTTP请求

import json
import traceback
from typing import Any, Dict

from tornado.web import RequestHandler

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError
from ...shared.response_formatter import ResponseFormatter
from ...schemas.statistics_schemas import (
    SalesReportRequest,
    OrderProfitRequest,
    ProductPerformanceRequest,
    ProfitStatisticsRequest,
    ShipmentRemovalRequest
)
from .services import StatisticsService


class BaseStatisticsHandler(RequestHandler):
    """统计模块基础处理器"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.statistics_service = StatisticsService()
    
    def set_default_headers(self):
        """设置默认响应头"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    
    def options(self, *args):
        """处理OPTIONS请求"""
        self.set_status(204)
        self.finish()
    
    def write_response(self, response_data: Dict[str, Any], status_code: int = 200):
        """写入响应数据"""
        self.set_status(status_code)
        self.write(ResponseFormatter.to_json(response_data))
        self.finish()
    
    def handle_error(self, error: Exception):
        """处理错误"""
        response = ResponseFormatter.from_exception(error)
        status_code = ResponseFormatter.get_http_status(response.get('code', 500))
        self.write_response(response, status_code)
    
    def parse_json_body(self) -> Dict[str, Any]:
        """解析JSON请求体"""
        try:
            if self.request.body:
                return json.loads(self.request.body.decode('utf-8'))
            return {}
        except json.JSONDecodeError as e:
            raise ValidationError("请求体JSON格式错误", details={"error": str(e)})


class SalesReportHandler(BaseStatisticsHandler):
    """销量报表处理器"""
    
    async def post(self):
        """获取销量报表"""
        try:
            # 解析请求数据
            request_data = self.parse_json_body()
            request = SalesReportRequest.from_dict(request_data)
            
            # 验证请求参数
            errors = request.validate()
            if errors:
                response = ResponseFormatter.validation_error(errors)
                self.write_response(response, 400)
                return
            
            # 调用服务层
            result = await self.statistics_service.get_sales_report(
                sid=request.sid,
                asin_type=request.asin_type,
                asin=request.asin,
                event_date=request.event_date,
                marketplace=request.marketplace,
                page=request.page,
                page_size=request.page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result.get('data', []),
                total=result.get('total', 0),
                page=request.page,
                page_size=request.page_size,
                message="销量报表查询成功"
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class OrderProfitHandler(BaseStatisticsHandler):
    """订单利润处理器"""
    
    async def post(self):
        """获取订单利润数据"""
        try:
            # 解析请求数据
            request_data = self.parse_json_body()
            request = OrderProfitRequest.from_dict(request_data)
            
            # 验证请求参数
            errors = request.validate()
            if errors:
                response = ResponseFormatter.validation_error(errors)
                self.write_response(response, 400)
                return
            
            # 调用服务层
            result = await self.statistics_service.get_order_profit(
                sid=request.sid,
                msku=request.msku,
                order_id=request.order_id,
                marketplace=request.marketplace,
                start_date=request.start_date,
                end_date=request.end_date,
                page=request.page,
                page_size=request.page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result.get('data', []),
                total=result.get('total', 0),
                page=request.page,
                page_size=request.page_size,
                message="订单利润查询成功"
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class ProductPerformanceHandler(BaseStatisticsHandler):
    """产品表现处理器"""
    
    async def post(self):
        """获取产品表现数据"""
        try:
            # 解析请求数据
            request_data = self.parse_json_body()
            request = ProductPerformanceRequest.from_dict(request_data)
            
            # 验证请求参数
            errors = request.validate()
            if errors:
                response = ResponseFormatter.validation_error(errors)
                self.write_response(response, 400)
                return
            
            # 调用服务层
            result = await self.statistics_service.get_product_performance(
                sid=request.sid,
                asin=request.asin,
                marketplace=request.marketplace,
                report_type=request.report_type,
                start_date=request.start_date,
                end_date=request.end_date,
                page=request.page,
                page_size=request.page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result.get('data', []),
                total=result.get('total', 0),
                page=request.page,
                page_size=request.page_size,
                message="产品表现查询成功"
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class ProfitStatisticsHandler(BaseStatisticsHandler):
    """利润统计处理器"""
    
    async def post(self):
        """获取利润统计数据"""
        try:
            # 解析请求数据
            request_data = self.parse_json_body()
            request = ProfitStatisticsRequest.from_dict(request_data)
            
            # 验证请求参数
            errors = request.validate()
            if errors:
                response = ResponseFormatter.validation_error(errors)
                self.write_response(response, 400)
                return
            
            # 调用服务层
            result = await self.statistics_service.get_profit_statistics(
                sid=request.sid,
                marketplace=request.marketplace,
                start_date=request.start_date,
                end_date=request.end_date,
                group_by=request.group_by
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(
                data=result.get('data', []),
                message="利润统计查询成功"
            )
            if 'summary' in result:
                response['meta'] = {'summary': result['summary']}
            
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class ShipmentRemovalHandler(BaseStatisticsHandler):
    """移除货件报表处理器"""
    
    async def post(self):
        """获取移除货件报表"""
        try:
            # 解析请求数据
            request_data = self.parse_json_body()
            request = ShipmentRemovalRequest.from_dict(request_data)
            
            # 验证请求参数
            errors = request.validate()
            if errors:
                response = ResponseFormatter.validation_error(errors)
                self.write_response(response, 400)
                return
            
            # 调用服务层
            result = await self.statistics_service.get_shipment_removal(
                sid=request.sid,
                removal_order_id=request.removal_order_id,
                disposition=request.disposition,
                start_date=request.start_date,
                end_date=request.end_date,
                page=request.page,
                page_size=request.page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result.get('data', []),
                total=result.get('total', 0),
                page=request.page,
                page_size=request.page_size,
                message="移除货件报表查询成功"
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)