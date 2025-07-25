from tornado.web import RequestHandler
from app.middleware.auth import AccessTokenManager

# 获取access_token
class BaseHandler(RequestHandler):
    async def prepare(self):
        self.access_token = await AccessTokenManager.get_token() 