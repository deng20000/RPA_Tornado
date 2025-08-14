# 常量定义模块
# 定义项目中使用的各种常量

from .api_constants import *
from .error_codes import *
from .business_constants import *

__all__ = [
    # API相关常量
    'DEFAULT_PAGE_SIZE',
    'MAX_PAGE_SIZE',
    'DEFAULT_TIMEOUT',
    
    # 错误码
    'SUCCESS_CODE',
    'VALIDATION_ERROR_CODE',
    'AUTH_ERROR_CODE',
    
    # 业务常量
    'ASIN_TYPE_ASIN',
    'ASIN_TYPE_MSKU',
    'REPORT_TYPE_SALES',
    'REPORT_TYPE_QUANTITY',
    'REPORT_TYPE_ORDERS'
]