import json
import pytest
from tornado.httpclient import HTTPRequest
from tornado.testing import AsyncHTTPTestCase, gen_test
from datetime import datetime, timedelta
from main import make_app

class TestBaseDataHandler(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    @gen_test
    async def test_currency_exchange_rate(self):
        # 默认获取昨天月份,格式为 YYYY-MM
        yesterday = datetime.now() - timedelta(days=1)
        date = yesterday.strftime("%Y-%m")
        # 测试汇率查询接口（GET）
        response = await self.http_client.fetch(self.get_url(f'/api/base-data/currency-exchange-rate?date={date}'))
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_amazon_seller_list(self):
        # 测试亚马逊店铺列表接口（GET）
        response = await self.http_client.fetch(self.get_url('/api/base-data/amazon-seller-list'))
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_amazon_marketplace_list(self):
        # 测试亚马逊市场列表接口（GET）
        response = await self.http_client.fetch(self.get_url('/api/base-data/amazon-marketplace-list'))
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_world_state_list(self):
        # 测试世界州/省列表接口（POST）
        body = json.dumps({'country_code': 'US'})
        request = HTTPRequest(
            self.get_url('/api/base-data/world-state-list'),
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        response = await self.http_client.fetch(request)
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_file_attachment_download(self):
        # 测试下载产品附件接口（POST）
        body = json.dumps({'file_id': 1209})
        request = HTTPRequest(
            self.get_url('/api/base-data/file-attachment-download'),
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        response = await self.http_client.fetch(request)
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_customized_file_download(self):
        # 测试定制化附件下载接口（POST）
        body = json.dumps({'file_id': '123121211'})
        request = HTTPRequest(
            self.get_url('/api/base-data/customized-file-download'),
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        response = await self.http_client.fetch(request)
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_erp_user_list(self):
        # 测试ERP用户信息列表接口（GET）
        response = await self.http_client.fetch(self.get_url('/api/base-data/erp-user-list'))
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data

    @gen_test
    async def test_batch_edit_seller_name(self):
        # 测试批量修改店铺名称接口（POST）
        body = json.dumps({'sid_name_list': [{'sid': 1, 'name': '店铺1'}]})
        request = HTTPRequest(
            self.get_url('/api/base-data/batch-edit-seller-name'),
            method='POST',
            body=body,
            headers={'Content-Type': 'application/json'}
        )
        response = await self.http_client.fetch(request)
        assert response.code == 200
        data = json.loads(response.body.decode())
        assert 'code' in data 