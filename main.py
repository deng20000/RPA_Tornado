from app.ecommerce_dashboard.routes import routes as ecommerce_routes
from app.handlers.base_data_handler import (
    CurrencyExchangeRateHandler, AmazonSellerListHandler, AmazonMarketplaceListHandler,
    WorldStateListHandler, FileAttachmentDownloadHandler, CustomizedFileDownloadHandler,
    ErpUserListHandler, BatchEditSellerNameHandler
)
from app.handlers.multi_platform_handler import MultiPlatformSellerListHandler, SaleStatisticsV2Handler, ProfitReportSellerHandler, SalesReportAsinDailyListsHandler, OrderProfitMSKUHandler, ProfitReportMSKUHandler, ProfitReportSKUHandler
from app.handlers.statistics_handler import SalesReportAsinDailyListsHandler, OrderProfitMSKUHandler

all_routes = []
all_routes += ecommerce_routes

# 批量调整为 /api+原路由
all_routes += [
    (r'/api/erp/sc/routing/finance/currency/currencyMonth', CurrencyExchangeRateHandler),
    (r'/api/erp/sc/data/seller/lists', AmazonSellerListHandler),
    (r'/api/erp/sc/data/seller/allMarketplace', AmazonMarketplaceListHandler),
    (r'/api/erp/sc/data/worldState/lists', WorldStateListHandler),
    (r'/api/erp/sc/routing/common/file/download', FileAttachmentDownloadHandler),
    (r'/api/erp/sc/routing/customized/file/download', CustomizedFileDownloadHandler),
    (r'/api/erp/sc/data/account/lists', ErpUserListHandler),
    (r'/api/erp/sc/data/seller/batchEditSellerName', BatchEditSellerNameHandler),
]

all_routes += [
    (r'/api/basicOpen/platformStatisticsV2/saleStat/pageList', SaleStatisticsV2Handler),
    (r'/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list', MultiPlatformSellerListHandler),
    (r'/api/basicOpen/finance/mreport/OrderProfit', OrderProfitMSKUHandler),
    (r'/api/bd/profit/statistics/open/msku/list', OrderProfitMSKUHandler),
    (r'/api/erp/sc/data/sales_report/asinDailyLists', SalesReportAsinDailyListsHandler),
    (r'/api/basicOpen/multiplatform/profit/report/msku', ProfitReportMSKUHandler),
    (r'/api/basicOpen/multiplatform/profit/report/sku', ProfitReportSKUHandler),
]

import tornado.ioloop
import tornado.web

def make_app():
    """创建 Tornado 应用实例，供测试和生产使用"""
    return tornado.web.Application(all_routes, debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado server started at http://127.0.0.1:8888 (debug mode)")
    tornado.ioloop.IOLoop.current().start() 