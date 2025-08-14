# amazon_table_routes.py
# 亚马逊源表数据模块路由
# 负责注册所有亚马逊源表数据相关的 API 路由

from app.handlers.amazon_table_handler import (
    RemovalShipmentListHandler,      # 移除货件报表查询
    RemovalOrderListNewHandler,      # 移除订单报表查询（新）
    AllOrdersHandler,                # 所有订单报表处理器
    FbaOrdersHandler,                # FBA订单报表处理器
    FbaExchangeOrdersHandler,        # FBA换货订单报表处理器
    FbaRefundOrdersHandler,          # FBA退货订单报表处理器
    FbmReturnOrdersHandler,          # FBM退货订单报表处理器
    ManageInventoryHandler,
    DailyInventoryHandler,
    AfnFulfillableQuantityHandler,
    ReservedInventoryHandler,
    FbaAgeListHandler,
    AmazonFulfilledShipmentsListHandler,
    AmazonFulfilledShipmentsListV1Handler,
    AdjustmentListHandler,
    CreateReportExportTaskHandler,
    QueryReportExportTaskHandler,
    AmazonReportExportTaskHandler
)

amazon_table_routes = [
    # 移除货件报表查询
    (r"/api/erp/sc/routing/data/order/removalShipmentList", RemovalShipmentListHandler),
    # 移除订单报表查询（新）
    (r"/api/erp/sc/routing/data/order/removalOrderListNew", RemovalOrderListNewHandler),
    # 所有订单报表查询
    (r"/api/erp/sc/data/mws_report/allOrders", AllOrdersHandler),
    # FBA订单报表查询
    (r"/api/erp/sc/data/mws_report/fbaOrders", FbaOrdersHandler),
    # FBA换货订单报表查询
    (r"/api/erp/sc/routing/data/order/fbaExchangeOrderList", FbaExchangeOrdersHandler),
    # FBA退货订单报表查询
    (r"/api/erp/sc/data/mws_report/refundOrders", FbaRefundOrdersHandler),
    # FBM退货订单报表查询
    (r"/api/erp/sc/routing/data/order/fbmReturnOrderList", FbmReturnOrdersHandler),
    
    # FBA库存报表
    (r"/api/erp/sc/data/mws_report/manageInventory", ManageInventoryHandler),
    
    # 每日库存报表
    (r"/api/erp/sc/data/mws_report/dailyInventory", DailyInventoryHandler),
    
    # FBA可售库存报表
    (r"/api/erp/sc/data/mws_report/getAfnFulfillableQuantity", AfnFulfillableQuantityHandler),
    
    # 预留库存报表
    (r"/api/erp/sc/data/mws_report/reservedInventory", ReservedInventoryHandler),
    
    # 库龄表
    (r"/api/erp/sc/routing/fba/fbaStock/getFbaAgeList", FbaAgeListHandler),
    
    # Amazon Fulfilled Shipments报表
    (r"/api/erp/sc/data/mws_report/getAmazonFulfilledShipmentsList", AmazonFulfilledShipmentsListHandler),
    
    # Amazon Fulfilled Shipments v1报表
    (r"/api/erp/sc/data/mws_report_v1/getAmazonFulfilledShipmentsList", AmazonFulfilledShipmentsListV1Handler),
    
    # 盘存记录
    (r"/api/basicOpen/openapi/mwsReport/adjustmentList", AdjustmentListHandler),
    
    # 创建报告导出任务
    (r"/api/basicOpen/report/create/reportExportTask", CreateReportExportTaskHandler),
    
    # 查询报告导出任务结果
    (r"/api/basicOpen/report/query/reportExportTask", QueryReportExportTaskHandler),
    
    # 报告下载链接续期
    (r"/api/basicOpen/report/amazonReportExportTask", AmazonReportExportTaskHandler),
]