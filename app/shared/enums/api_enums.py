# API相关枚举类型
# 定义API请求、响应相关的枚举

from enum import Enum, IntEnum


class HTTPMethod(Enum):
    """HTTP请求方法枚举"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class ContentType(Enum):
    """内容类型枚举"""
    JSON = 'application/json'
    FORM = 'application/x-www-form-urlencoded'
    MULTIPART = 'multipart/form-data'
    TEXT = 'text/plain'
    HTML = 'text/html'
    XML = 'application/xml'
    CSV = 'text/csv'
    EXCEL = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class ResponseStatus(IntEnum):
    """响应状态枚举"""
    # 成功状态
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # 重定向状态
    MOVED_PERMANENTLY = 301
    FOUND = 302
    NOT_MODIFIED = 304
    
    # 客户端错误
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    
    # 服务器错误
    INTERNAL_SERVER_ERROR = 500
    INTERNAL_ERROR = 500  # 别名，保持兼容性
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504


class CacheStrategy(Enum):
    """缓存策略枚举"""
    NO_CACHE = 'no_cache'          # 不缓存
    SHORT_CACHE = 'short_cache'    # 短期缓存（1分钟）
    MEDIUM_CACHE = 'medium_cache'  # 中期缓存（5分钟）
    LONG_CACHE = 'long_cache'      # 长期缓存（1小时）
    PERSISTENT = 'persistent'       # 持久缓存


class LogLevel(Enum):
    """日志级别枚举"""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Environment(Enum):
    """环境类型枚举"""
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    STAGING = 'staging'
    PRODUCTION = 'production'


class RateLimitType(Enum):
    """限流类型枚举"""
    IP_BASED = 'ip_based'          # 基于IP限流
    USER_BASED = 'user_based'      # 基于用户限流
    API_BASED = 'api_based'        # 基于API限流
    GLOBAL = 'global'              # 全局限流