# 数据传输对象(DTO)模块
# 定义API请求和响应的数据结构

from .base_schemas import BaseRequest, BaseResponse, PaginationRequest, PaginationResponse
from .statistics_schemas import (
    SalesReportRequest,
    SalesReportResponse,
    OrderProfitRequest,
    OrderProfitResponse,
    ProductPerformanceRequest,
    ProductPerformanceResponse
)
from .base_data_schemas import (
    BaseDataRequest,
    BaseDataResponse,
    SellerInfoRequest,
    SellerInfoResponse
)
from .multi_platform_schemas import (
    MultiPlatformRequest,
    MultiPlatformResponse,
    PlatformSyncRequest,
    PlatformSyncResponse
)
from .product_schemas import (
    ProductRequest,
    ProductResponse,
    ProductListRequest,
    ProductListResponse
)

__all__ = [
    # 基础模式
    'BaseRequest',
    'BaseResponse',
    'PaginationRequest',
    'PaginationResponse',
    
    # 统计模块
    'SalesReportRequest',
    'SalesReportResponse',
    'OrderProfitRequest',
    'OrderProfitResponse',
    'ProductPerformanceRequest',
    'ProductPerformanceResponse',
    
    # 基础数据模块
    'BaseDataRequest',
    'BaseDataResponse',
    'SellerInfoRequest',
    'SellerInfoResponse',
    
    # 多平台模块
    'MultiPlatformRequest',
    'MultiPlatformResponse',
    'PlatformSyncRequest',
    'PlatformSyncResponse',
    
    # 产品模块
    'ProductRequest',
    'ProductResponse',
    'ProductListRequest',
    'ProductListResponse'
]