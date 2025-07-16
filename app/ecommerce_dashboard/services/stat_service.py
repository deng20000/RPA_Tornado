from app.ecommerce_dashboard.services.common import api_request

class SalesService:
    async def get_daily_sales(self, params):
        query_data = {
            "result_type": 3,  # 销售额
            "date_unit": 4,   # 日
            "data_type": 6,   # 店铺
            **params
        }
        return await api_request("/basicOpen/platformStatisticsV2/saleStat/pageList", query_data)

    async def get_hot_sku_sales(self, params):
        query_data = {
            "result_type": 1,  # 销量
            "date_unit": 4,   # 日
            "data_type": 6,   # 店铺
            **params
        }
        return await api_request("/basicOpen/platformStatisticsV2/saleStat/pageList", query_data) 