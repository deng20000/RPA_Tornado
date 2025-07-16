import tornado.web
from tornado.testing import AsyncHTTPTestCase, gen_test
from app.ecommerce_dashboard.handlers.stat_handler import SaleStatHandler
from app.ecommerce_dashboard.routes import routes
import os
import json
from app.ecommerce_dashboard.handlers.stat_handler import process_to_usd_cleaned_sale_stat_3


def make_body(result_type):
    return {
        "result_type": result_type
        # 其他参数使用handler默认值
    }

class TestSaleStatHandler(AsyncHTTPTestCase):
    def get_app(self):
        return tornado.web.Application(routes)

    @gen_test
    async def test_daily_sales(self):
        response = await self.http_client.fetch(
            self.get_url("/api/ecommerce/sale_stat"),
            method="POST",
            body=tornado.escape.json_encode(make_body(3)),
            headers={"Content-Type": "application/json"}
        )
        assert response.code == 200
        data = tornado.escape.json_decode(response.body)
        assert data["code"] == 0
        assert "data" in data

    @gen_test
    async def test_hot_sku(self):
        response = await self.http_client.fetch(
            self.get_url("/api/ecommerce/sale_stat"),
            method="POST",
            body=tornado.escape.json_encode(make_body(1)),
            headers={"Content-Type": "application/json"}
        )
        assert response.code == 200
        data = tornado.escape.json_decode(response.body)
        assert data["code"] == 0
        assert "data" in data 