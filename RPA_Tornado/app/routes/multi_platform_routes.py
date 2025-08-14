# 多平台模块路由
# 负责注册所有多平台相关的 API 路由

from app.handlers.multi_platform_handler import (
    MultiPlatformSellerListHandler,             # 多平台店铺信息查询
    SaleStatisticsV2Handler,                    # 多平台销量统计v2
    ProfitReportSellerHandler,                  # 多平台结算利润-店铺
    SalesReportAsinDailyListsHandler as MultiPlatformSalesReportAsinDailyListsHandler, # 多平台ASIN日销量报表
    OrderProfitMSKUHandler as MultiPlatformOrderProfitMSKUHandler,                     # 多平台订单利润MSKU
    ProfitReportMSKUHandler,                    # 多平台结算利润-msku
    ProfitReportSKUHandler,                     # 多平台结算利润-sku
)

multi_platform_routes = [
    ("/api/basicOpen/platformStatisticsV2/saleStat/pageList", SaleStatisticsV2Handler),  # 多平台销量统计v2
    ("/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list", MultiPlatformSellerListHandler),  # 多平台店铺信息查询
    ("/api/bd/profit/statistics/open/msku/list", MultiPlatformOrderProfitMSKUHandler),  # 多平台订单利润MSKU（兼容老路由）
    ("/api/basicOpen/multiplatform/profit/report/msku", ProfitReportMSKUHandler),  # 多平台结算利润-msku
    ("/api/basicOpen/multiplatform/profit/report/sku", ProfitReportSKUHandler),  # 多平台结算利润-sku
    ("/api/multi-platform/sale-statistics-v2", SaleStatisticsV2Handler),  # 多平台销量统计v2（兼容路由）
    ("/api/multi-platform/sales-report-asin-daily-lists", MultiPlatformSalesReportAsinDailyListsHandler),  # 多平台ASIN日销量报表
    ("/api/multi-platform/order-profit-msku", MultiPlatformOrderProfitMSKUHandler),  # 多平台订单利润MSKU
    ("/api/multi-platform/profit-report-msku", ProfitReportMSKUHandler),  # 多平台结算利润-msku
    ("/api/multi-platform/profit-report-sku", ProfitReportSKUHandler),  # 多平台结算利润-sku
    ("/api/multi-platform/seller-list", MultiPlatformSellerListHandler),  # 多平台店铺信息查询
    ("/api/multi-platform/profit-report-seller", ProfitReportSellerHandler),  # 多平台结算利润-店铺
] 