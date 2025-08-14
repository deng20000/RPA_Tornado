# 统计模块路由
# 负责注册所有统计相关的 API 路由

from app.handlers.statistics_handler import (
    SalesReportAsinDailyListsHandler,           # 旧版销量报表ASIN日列表
    OrderProfitMSKUHandler,                     # 订单利润MSKU查询
    SalesReportShopSummaryHandler,              # 店铺汇总销量查询
    ProductPerformanceHandler,                  # 查询产品表现
    ProductPerformanceTrendByHourHandler,       # 查询asin360小时数据
    ProfitStatisticsAsinListHandler,            # 利润统计-ASIN
)

# 导入亚马逊源表处理器中的移除货件处理器
from app.handlers.amazon_table_handler import (
    RemovalShipmentListHandler,                 # 移除货件报表查询
)

statistics_routes = [
    ("/api/erp/sc/data/sales_report/asinDailyLists", SalesReportAsinDailyListsHandler),  # 旧版销量报表ASIN日列表
    ("/api/statistics/order-profit-msku", OrderProfitMSKUHandler),  # 订单利润MSKU查询
    ("/api/erp/sc/data/sales_report/sales", SalesReportShopSummaryHandler),  # 店铺汇总销量查询
    ("/api/bd/productPerformance/openApi/asinList", ProductPerformanceHandler),  # 查询产品表现
    ("/api/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour", ProductPerformanceTrendByHourHandler),  # 查询asin360小时数据
    ("/api/bd/profit/statistics/open/asin/list", ProfitStatisticsAsinListHandler),  # 利润统计-ASIN
    ("/api/basicOpen/finance/mreport/OrderProfit", OrderProfitMSKUHandler),  # 统计-订单利润MSKU
    ("/api/erp/sc/statistic/removalShipment/list", RemovalShipmentListHandler),  # 移除货件报表查询
]