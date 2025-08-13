import asyncio
import jwt
from datetime import datetime, timedelta
from tornado.web import RequestHandler
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


class AuthMiddleware:
    """
    认证中间件
    处理JWT token验证和用户认证
    """
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.jwt_secret = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        
    def process_request(self, handler: RequestHandler):
        """
        处理请求前的认证检查
        """
        # 跳过不需要认证的路径
        skip_paths = ['/health', '/api/docs', '/swagger', '/static']
        if any(handler.request.path.startswith(path) for path in skip_paths):
            return
            
        # 获取Authorization头
        auth_header = handler.request.headers.get('Authorization')
        if not auth_header:
            handler.set_status(401)
            handler.write({'error': 'Missing Authorization header'})
            handler.finish()
            return
            
        # 验证Bearer token格式
        try:
            scheme, token = auth_header.split(' ', 1)
            if scheme.lower() != 'bearer':
                raise ValueError('Invalid scheme')
        except ValueError:
            handler.set_status(401)
            handler.write({'error': 'Invalid Authorization header format'})
            handler.finish()
            return
            
        # 验证JWT token
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.algorithm])
            handler.current_user = payload
        except jwt.ExpiredSignatureError:
            handler.set_status(401)
            handler.write({'error': 'Token has expired'})
            handler.finish()
            return
        except jwt.InvalidTokenError:
            handler.set_status(401)
            handler.write({'error': 'Invalid token'})
            handler.finish()
            return
            
    def generate_token(self, user_data: dict) -> str:
        """
        生成JWT token
        """
        payload = {
            **user_data,
            'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.algorithm)