# 多平台领域处理器
# 处理多平台相关的HTTP请求

import json
import logging
from typing import Any, Dict, Optional

from tornado.web import RequestHandler
from tornado.escape import json_decode

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError
from ...shared.response_formatter import ResponseFormatter
from ...shared.constants.error_codes import ErrorCodes
from ...schemas.multi_platform_schemas import (
    PlatformSyncRequest,
    SyncStatusRequest,
    PlatformDataRequest,
    CrossPlatformAnalysisRequest,
    PlatformConfigRequest,
    UpdatePlatformConfigRequest
)
from .services import MultiPlatformService

# 配置日志
logger = logging.getLogger(__name__)


class MultiPlatformHandler(RequestHandler):
    """多平台处理器基类"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = MultiPlatformService()
    
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


class PlatformSyncHandler(MultiPlatformHandler):
    """平台同步处理器"""
    
    async def post(self):
        """启动平台数据同步"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = PlatformSyncRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.start_platform_sync(
                platforms=request_data.platforms,
                sync_type=request_data.sync_type,
                data_types=request_data.data_types,
                start_date=request_data.start_date,
                end_date=request_data.end_date,
                force_sync=request_data.force_sync
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def get(self):
        """获取同步任务列表"""
        try:
            # 从查询参数获取参数
            platform = self.get_argument('platform', None)
            status = self.get_argument('status', None)
            page = int(self.get_argument('page', '1'))
            page_size = int(self.get_argument('page_size', '20'))
            
            # 调用服务
            result = await self.service.get_sync_tasks(
                platform=platform,
                status=status,
                page=page,
                page_size=page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result['data'],
                total=result['total'],
                page=page,
                page_size=page_size
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class SyncStatusHandler(MultiPlatformHandler):
    """同步状态处理器"""
    
    async def get(self):
        """获取同步状态"""
        try:
            # 从查询参数获取参数
            task_id = self.get_argument('task_id', None)
            platform = self.get_argument('platform', None)
            
            # 创建请求对象
            request_data = SyncStatusRequest(
                task_id=task_id,
                platform=platform
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_sync_status(
                task_id=request_data.task_id,
                platform=request_data.platform
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取同步状态"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = SyncStatusRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_sync_status(
                task_id=request_data.task_id,
                platform=request_data.platform
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class PlatformDataHandler(MultiPlatformHandler):
    """平台数据处理器"""
    
    async def get(self):
        """获取平台数据"""
        try:
            # 从查询参数获取参数
            platform = self.get_argument('platform', None)
            data_type = self.get_argument('data_type', None)
            start_date = self.get_argument('start_date', None)
            end_date = self.get_argument('end_date', None)
            page = int(self.get_argument('page', '1'))
            page_size = int(self.get_argument('page_size', '20'))
            
            # 创建请求对象
            request_data = PlatformDataRequest(
                platform=platform,
                data_type=data_type,
                start_date=start_date,
                end_date=end_date,
                page=page,
                page_size=page_size
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_platform_data(
                platform=request_data.platform,
                data_type=request_data.data_type,
                start_date=request_data.start_date,
                end_date=request_data.end_date,
                page=request_data.page,
                page_size=request_data.page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result['data'],
                total=result['total'],
                page=page,
                page_size=page_size
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取平台数据"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = PlatformDataRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_platform_data(
                platform=request_data.platform,
                data_type=request_data.data_type,
                start_date=request_data.start_date,
                end_date=request_data.end_date,
                page=request_data.page,
                page_size=request_data.page_size
            )
            
            # 返回成功响应
            response = ResponseFormatter.paginated(
                data=result['data'],
                total=result['total'],
                page=request_data.page,
                page_size=request_data.page_size
            )
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class CrossPlatformAnalysisHandler(MultiPlatformHandler):
    """跨平台分析处理器"""
    
    async def get(self):
        """获取跨平台分析数据"""
        try:
            # 从查询参数获取参数
            platforms = self.get_argument('platforms', '').split(',') if self.get_argument('platforms', '') else None
            analysis_type = self.get_argument('analysis_type', None)
            start_date = self.get_argument('start_date', None)
            end_date = self.get_argument('end_date', None)
            group_by = self.get_argument('group_by', 'day')
            
            # 创建请求对象
            request_data = CrossPlatformAnalysisRequest(
                platforms=platforms,
                analysis_type=analysis_type,
                start_date=start_date,
                end_date=end_date,
                group_by=group_by
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_cross_platform_analysis(
                platforms=request_data.platforms,
                analysis_type=request_data.analysis_type,
                start_date=request_data.start_date,
                end_date=request_data.end_date,
                group_by=request_data.group_by
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取跨平台分析数据"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = CrossPlatformAnalysisRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_cross_platform_analysis(
                platforms=request_data.platforms,
                analysis_type=request_data.analysis_type,
                start_date=request_data.start_date,
                end_date=request_data.end_date,
                group_by=request_data.group_by
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)


class PlatformConfigHandler(MultiPlatformHandler):
    """平台配置处理器"""
    
    async def get(self):
        """获取平台配置"""
        try:
            # 从查询参数获取参数
            platform = self.get_argument('platform', None)
            config_type = self.get_argument('config_type', None)
            
            # 创建请求对象
            request_data = PlatformConfigRequest(
                platform=platform,
                config_type=config_type
            )
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_platform_config(
                platform=request_data.platform,
                config_type=request_data.config_type
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def post(self):
        """通过POST获取平台配置"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = PlatformConfigRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.get_platform_config(
                platform=request_data.platform,
                config_type=request_data.config_type
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)
    
    async def put(self):
        """更新平台配置"""
        try:
            # 解析请求体
            body_data = self.parse_json_body()
            
            # 创建请求对象
            request_data = UpdatePlatformConfigRequest.from_dict(body_data)
            
            # 验证请求
            request_data.validate()
            
            # 调用服务
            result = await self.service.update_platform_config(
                platform=request_data.platform,
                config_type=request_data.config_type,
                config_data=request_data.config_data,
                description=request_data.description
            )
            
            # 返回成功响应
            response = ResponseFormatter.success(result)
            self.write_response(response)
            
        except Exception as e:
            self.handle_error(e)