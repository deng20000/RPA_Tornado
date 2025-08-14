# 多平台模块数据传输对象模式
# 定义多平台相关的请求和响应数据结构

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .base_schemas import BaseRequest, BaseResponse, PaginationRequest, DateRangeRequest
from ..shared.enums.business_enums import Platform, OperationType


@dataclass
class MultiPlatformRequest(BaseRequest):
    """多平台请求模式"""
    platforms: List[str] = field(default_factory=list)  # 平台列表
    marketplace: Optional[str] = None  # 市场
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.platforms:
            errors.append("平台列表不能为空")
        
        # 验证平台是否有效
        valid_platforms = [p.value for p in Platform]
        for platform in self.platforms:
            if platform not in valid_platforms:
                errors.append(f"无效的平台: {platform}")
                
        return errors


@dataclass
class MultiPlatformResponse(BaseResponse):
    """多平台响应模式"""
    data: Dict[str, Any] = field(default_factory=dict)  # 按平台分组的数据


@dataclass
class PlatformSyncRequest(BaseRequest):
    """平台同步请求模式"""
    sid: str = ''  # 店铺ID
    platform: str = ''  # 平台
    sync_type: str = ''  # 同步类型: full, incremental
    data_types: List[str] = field(default_factory=list)  # 数据类型列表
    force_sync: bool = False  # 是否强制同步
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.platform:
            errors.append("平台不能为空")
            
        # 验证平台是否有效
        valid_platforms = [p.value for p in Platform]
        if self.platform not in valid_platforms:
            errors.append(f"无效的平台: {self.platform}")
            
        if self.sync_type not in ['full', 'incremental']:
            errors.append("同步类型只能是 full 或 incremental")
            
        if not self.data_types:
            errors.append("数据类型列表不能为空")
            
        # 验证数据类型
        valid_data_types = ['products', 'orders', 'inventory', 'reviews', 'advertising']
        for data_type in self.data_types:
            if data_type not in valid_data_types:
                errors.append(f"无效的数据类型: {data_type}")
                
        return errors


@dataclass
class SyncTaskInfo:
    """同步任务信息"""
    task_id: str = ''
    sid: str = ''
    platform: str = ''
    sync_type: str = ''
    data_types: List[str] = field(default_factory=list)
    status: str = ''  # pending, running, completed, failed
    progress: float = 0.0  # 进度百分比
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_message: Optional[str] = None
    records_processed: int = 0
    records_total: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'sid': self.sid,
            'platform': self.platform,
            'platform_name': Platform.get_description(self.platform),
            'sync_type': self.sync_type,
            'data_types': self.data_types,
            'status': self.status,
            'progress': self.progress,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'error_message': self.error_message,
            'records_processed': self.records_processed,
            'records_total': self.records_total
        }


@dataclass
class PlatformSyncResponse(BaseResponse):
    """平台同步响应模式"""
    data: Optional[SyncTaskInfo] = None


@dataclass
class SyncStatusRequest(BaseRequest):
    """同步状态请求模式"""
    task_id: Optional[str] = None  # 任务ID
    sid: Optional[str] = None      # 店铺ID
    platform: Optional[str] = None # 平台
    status: Optional[str] = None   # 状态筛选
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        # 至少需要一个筛选条件
        if not any([self.task_id, self.sid, self.platform]):
            errors.append("至少需要提供 task_id、sid 或 platform 中的一个")
            
        return errors


@dataclass
class SyncStatusResponse(BaseResponse):
    """同步状态响应模式"""
    data: List[SyncTaskInfo] = field(default_factory=list)


@dataclass
class PlatformDataRequest(PaginationRequest, DateRangeRequest):
    """平台数据请求模式"""
    sid: str = ''  # 店铺ID
    platform: str = ''  # 平台
    data_type: str = ''  # 数据类型
    filters: Dict[str, Any] = field(default_factory=dict)  # 筛选条件
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.platform:
            errors.append("平台不能为空")
            
        if not self.data_type:
            errors.append("数据类型不能为空")
            
        # 验证平台是否有效
        valid_platforms = [p.value for p in Platform]
        if self.platform not in valid_platforms:
            errors.append(f"无效的平台: {self.platform}")
            
        # 验证数据类型
        valid_data_types = ['products', 'orders', 'inventory', 'reviews', 'advertising']
        if self.data_type not in valid_data_types:
            errors.append(f"无效的数据类型: {self.data_type}")
            
        return errors


@dataclass
class PlatformDataResponse(BaseResponse):
    """平台数据响应模式"""
    data: List[Dict[str, Any]] = field(default_factory=list)
    total: int = 0
    platform: str = ''
    data_type: str = ''


@dataclass
class CrossPlatformAnalysisRequest(DateRangeRequest):
    """跨平台分析请求模式"""
    sid: str = ''  # 店铺ID
    platforms: List[str] = field(default_factory=list)  # 平台列表
    metrics: List[str] = field(default_factory=list)    # 指标列表
    group_by: str = 'platform'  # 分组方式: platform, date, product
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.platforms:
            errors.append("平台列表不能为空")
            
        if not self.metrics:
            errors.append("指标列表不能为空")
            
        # 验证平台
        valid_platforms = [p.value for p in Platform]
        for platform in self.platforms:
            if platform not in valid_platforms:
                errors.append(f"无效的平台: {platform}")
                
        # 验证指标
        valid_metrics = ['sales', 'orders', 'profit', 'inventory', 'reviews']
        for metric in self.metrics:
            if metric not in valid_metrics:
                errors.append(f"无效的指标: {metric}")
                
        if self.group_by not in ['platform', 'date', 'product']:
            errors.append("分组方式只能是 platform, date, product")
            
        return errors


@dataclass
class CrossPlatformAnalysisItem:
    """跨平台分析项"""
    group_key: str = ''  # 分组键
    platform: str = ''
    metrics: Dict[str, Any] = field(default_factory=dict)  # 指标数据
    period: Optional[str] = None  # 时间周期
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'group_key': self.group_key,
            'platform': self.platform,
            'platform_name': Platform.get_description(self.platform),
            'metrics': self.metrics
        }
        
        if self.period:
            result['period'] = self.period
            
        return result


@dataclass
class CrossPlatformAnalysisResponse(BaseResponse):
    """跨平台分析响应模式"""
    data: List[CrossPlatformAnalysisItem] = field(default_factory=list)
    summary: Optional[Dict[str, Any]] = None
    group_by: str = 'platform'


@dataclass
class PlatformConfigRequest(BaseRequest):
    """平台配置请求模式"""
    sid: str = ''  # 店铺ID
    platform: str = ''  # 平台
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.platform:
            errors.append("平台不能为空")
            
        # 验证平台是否有效
        valid_platforms = [p.value for p in Platform]
        if self.platform not in valid_platforms:
            errors.append(f"无效的平台: {self.platform}")
            
        return errors


@dataclass
class PlatformConfig:
    """平台配置信息"""
    sid: str = ''
    platform: str = ''
    api_credentials: Dict[str, str] = field(default_factory=dict)  # API凭证（敏感信息会被掩码）
    sync_settings: Dict[str, Any] = field(default_factory=dict)    # 同步设置
    rate_limits: Dict[str, int] = field(default_factory=dict)      # 限流设置
    is_active: bool = True
    last_sync_time: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        # 掩码敏感信息
        masked_credentials = {}
        for key, value in self.api_credentials.items():
            if 'secret' in key.lower() or 'token' in key.lower() or 'key' in key.lower():
                masked_credentials[key] = '***'
            else:
                masked_credentials[key] = value
                
        return {
            'sid': self.sid,
            'platform': self.platform,
            'platform_name': Platform.get_description(self.platform),
            'api_credentials': masked_credentials,
            'sync_settings': self.sync_settings,
            'rate_limits': self.rate_limits,
            'is_active': self.is_active,
            'last_sync_time': self.last_sync_time
        }


@dataclass
class PlatformConfigResponse(BaseResponse):
    """平台配置响应模式"""
    data: Optional[PlatformConfig] = None


@dataclass
class UpdatePlatformConfigRequest(BaseRequest):
    """更新平台配置请求模式"""
    sid: str = ''
    platform: str = ''
    api_credentials: Optional[Dict[str, str]] = None
    sync_settings: Optional[Dict[str, Any]] = None
    rate_limits: Optional[Dict[str, int]] = None
    is_active: Optional[bool] = None
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.platform:
            errors.append("平台不能为空")
            
        # 验证平台是否有效
        valid_platforms = [p.value for p in Platform]
        if self.platform not in valid_platforms:
            errors.append(f"无效的平台: {self.platform}")
            
        # 至少需要更新一个字段
        if not any([
            self.api_credentials,
            self.sync_settings,
            self.rate_limits,
            self.is_active is not None
        ]):
            errors.append("至少需要更新一个配置项")
            
        return errors


@dataclass
class UpdatePlatformConfigResponse(BaseResponse):
    """更新平台配置响应模式"""
    message: str = "平台配置更新成功"