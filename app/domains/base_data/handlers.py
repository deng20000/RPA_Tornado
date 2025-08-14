# 基础数据领域处理器
# 处理基础数据相关的HTTP请求

import json
import logging
from typing import Any, Dict, Optional

from tornado.web import RequestHandler
from tornado.escape import json_decode

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError
from ...shared.response_formatter import ResponseFormatter
from ...shared.constants.error_codes import ErrorCodes
from ...schemas.base_data_schemas import (
    SellerInfoRequest,
    MarketplaceListRequest,
    CategoryListRequest,
    CurrencyRateRequest,
    SettingsRequest,
    UpdateSettingRequest
)
from .services import BaseDataService

# 配置日志
logger = logging.getLogger(__name__)


class BaseDataHandler(RequestHandler):
    """基础数据处理器基类"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = BaseDataService()
    
    def set_default_headers(self):
        """设置默认响应头"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    
    async def options(self, *args):
        """处理OPTIONS请求"""
        self.set_status(204)
        self.finish()
    
    def write_response(self, data: Dict[str, Any]):
        """写入响应数据"""
        self.write(ResponseFormatter.to_json(data))
    
    def handle_error(self, error: Exception):
        """处理错误"""
        logger.error(f"处理请求时发生错误: {str(error)}", exc_info=True)
        
        if isinstance(error, ValidationError):
            response = ResponseFormatter.validation_error(str(error))
            self.set_status(400)
        elif isinstance(error, BusinessLogicError):
            response = ResponseFormatter.error(ErrorCodes.BUSINESS_ERROR, str(error))
            self.set_status(400)
        else:
            response = ResponseFormatter.error(ErrorCodes.INTERNAL_SERVER_ERROR, "服务器内部错误")
            self.set_status(500)
        
        self.write_response(response)
    
    def parse_json_body(self) -> Dict[str, Any]:
        """解析JSON请求体"""
        try:
            if self.request.body:
                return json_decode(self.request.body)
            return {}
        except (ValueError, TypeError) as e:
            raise ValidationError(f"无效的JSON格式: {str(e)}")


class SellerInfoHandler(BaseDataHandler):
    """店铺信息处理器"""
    
    async def get(self):
        """获取店铺信息"""
        try:
            # 从查询参数获取店铺ID
            sid = self.get_argument('sid', None)
            if not sid:
                raise ValidationError("店铺ID不能为空")
            
            # 创建请求对象
            request_data = SellerInfoRequest(
                sid=sid,
                include_details=self.get_argument('include_details', 'false').lower() == 'true'
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_seller_info(
                sid=request_data.sid,
                include_details=request_data.include_details
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取店铺信息"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = SellerInfoRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_seller_info(
                sid=request_data.sid,
                include_details=request_data.include_details
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class MarketplaceListHandler(BaseDataHandler):
    """市场列表处理器"""
    
    async def get(self):
        """获取市场列表"""
        try:
            # 从查询参数获取参数
            country_code = self.get_argument('country_code', None)
            active_only = self.get_argument('active_only', 'true').lower() == 'true'
            
            # 创建请求对象
            request_data = MarketplaceListRequest(
                country_code=country_code,
                active_only=active_only
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_marketplace_list(
                country_code=request_data.country_code,
                active_only=request_data.active_only
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取市场列表"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = MarketplaceListRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_marketplace_list(
                country_code=request_data.country_code,
                active_only=request_data.active_only
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class CategoryListHandler(BaseDataHandler):
    """分类列表处理器"""
    
    async def get(self):
        """获取分类列表"""
        try:
            # 从查询参数获取参数
            marketplace = self.get_argument('marketplace', None)
            parent_category = self.get_argument('parent_category', None)
            level = self.get_argument('level', None)
            
            # 创建请求对象
            request_data = CategoryListRequest(
                marketplace=marketplace,
                parent_category=parent_category,
                level=int(level) if level else None
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_category_list(
                marketplace=request_data.marketplace,
                parent_category=request_data.parent_category,
                level=request_data.level
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取分类列表"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = CategoryListRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_category_list(
                marketplace=request_data.marketplace,
                parent_category=request_data.parent_category,
                level=request_data.level
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class CurrencyRateHandler(BaseDataHandler):
    """汇率处理器"""
    
    async def get(self):
        """获取汇率"""
        try:
            # 从查询参数获取参数
            from_currency = self.get_argument('from_currency', None)
            to_currency = self.get_argument('to_currency', None)
            date = self.get_argument('date', None)
            
            # 创建请求对象
            request_data = CurrencyRateRequest(
                from_currency=from_currency,
                to_currency=to_currency,
                date=date
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_currency_rate(
                from_currency=request_data.from_currency,
                to_currency=request_data.to_currency,
                date=request_data.date
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取汇率"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = CurrencyRateRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_currency_rate(
                from_currency=request_data.from_currency,
                to_currency=request_data.to_currency,
                date=request_data.date
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class SettingsHandler(BaseDataHandler):
    """设置处理器"""
    
    async def get(self):
        """获取设置"""
        try:
            # 从查询参数获取参数
            category = self.get_argument('category', None)
            key = self.get_argument('key', None)
            
            # 创建请求对象
            request_data = SettingsRequest(
                category=category,
                key=key
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_settings(
                category=request_data.category,
                key=request_data.key
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取设置"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = SettingsRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_settings(
                category=request_data.category,
                key=request_data.key
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def put(self):
        """更新设置"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = UpdateSettingRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.update_setting(
                category=request_data.category,
                key=request_data.key,
                value=request_data.value,
                description=request_data.description
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)