# 认证相关依赖注入
# 提供认证和授权相关的依赖注入函数

from typing import Optional
from tornado.web import RequestHandler
from app.core.exceptions import AuthenticationError
from app.auth.openapi import OpenApiBase
from app.config import settings


def get_access_token(handler: RequestHandler) -> str:
    """获取访问令牌
    
    Args:
        handler: Tornado请求处理器
        
    Returns:
        str: 访问令牌
        
    Raises:
        AuthenticationError: 当令牌获取失败时抛出
    """
    try:
        # 从请求头或其他地方获取令牌
        token = handler.request.headers.get('Authorization')
        if not token:
            # 如果没有提供令牌，使用默认的API客户端获取
            api_client = OpenApiBase(
                settings.LLX_API_HOST, 
                settings.LLX_APP_ID, 
                settings.LLX_APP_SECRET
            )
            token = api_client.get_access_token()
        
        if not token:
            raise AuthenticationError("无法获取访问令牌")
            
        return token
    except Exception as e:
        raise AuthenticationError(f"令牌获取失败: {str(e)}")


def verify_token(token: str) -> bool:
    """验证访问令牌
    
    Args:
        token: 访问令牌
        
    Returns:
        bool: 令牌是否有效
    """
    try:
        # 这里可以添加令牌验证逻辑
        # 目前简单检查令牌是否为空
        return bool(token and len(token) > 0)
    except Exception:
        return False