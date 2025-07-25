import asyncio
from datetime import datetime, timedelta
from app.auth.openapi import OpenApiBase
from app.config import settings

# AccessTokenManager 用于全局管理 access_token，避免每次请求都重新获取
class AccessTokenManager:
    _access_token = None  # 缓存 access_token
    _expire_time = None   # 缓存 access_token 的过期时间
    _lock = asyncio.Lock()  # 异步锁，防止并发获取 token 时重复请求

    @classmethod
    async def get_token(cls):
        """
        获取有效的 access_token。
        如果缓存中有且未过期，则直接返回缓存的 token；
        否则重新请求外部 API 获取，并更新缓存。
        """
        async with cls._lock:
            now = datetime.now()
            # 检查缓存是否有效
            if cls._access_token and cls._expire_time and now < cls._expire_time:
                return cls._access_token
            # 缓存无效，重新获取
            api = OpenApiBase(settings.LLX_API_HOST, settings.LLX_APP_ID, settings.LLX_APP_SECRET)
            token_obj = await api.generate_access_token()
            cls._access_token = token_obj.access_token
            # 提前1分钟过期，防止边界问题
            cls._expire_time = now + timedelta(seconds=token_obj.expires_in - 60)
            return cls._access_token 