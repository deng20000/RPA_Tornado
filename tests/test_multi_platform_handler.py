import json
import pytest
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase, gen_test
from main import make_app

class TestMultiPlatformHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    async def test_multi_platform_seller_list(self):
        # 测试多平台店铺信息查询接口（POST）
        body = json.dumps({
            'offset': 0,
            'length': 200,
            'is_sync': 1,
            'status': 1
        })
        request = HTTPRequest(
            self.get_url('/api/multi-platform/seller-list'),
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        response = await self.http_client.fetch(request)
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data 