# 基础数据模块路由
# 负责注册所有基础数据相关的 API 路由

from app.handlers.base_data_handler import (
    CurrencyExchangeRateHandler,                # 查询汇率
    AmazonSellerListHandler,                    # 查询亚马逊店铺列表
    AmazonMarketplaceListHandler,               # 查询亚马逊市场列表
    WorldStateListHandler,                      # 查询世界州/省列表
    FileAttachmentDownloadHandler,              # 下载产品附件
    CustomizedFileDownloadHandler,              # 定制化附件下载
    ErpUserListHandler,                         # 查询ERP用户信息列表
    BatchEditSellerNameHandler,                 # 批量修改店铺名称
)

base_data_routes = [
    ("/api/erp/sc/routing/finance/currency/currencyMonth", CurrencyExchangeRateHandler),  # 查询汇率
    ("/api/erp/sc/data/seller/lists", AmazonSellerListHandler),  # 查询亚马逊店铺列表
    ("/api/erp/sc/data/seller/allMarketplace", AmazonMarketplaceListHandler),  # 查询亚马逊市场列表
    ("/api/erp/sc/data/worldState/lists", WorldStateListHandler),  # 查询世界州/省列表
    ("/api/erp/sc/routing/common/file/download", FileAttachmentDownloadHandler),  # 下载产品附件
    ("/api/erp/sc/routing/customized/file/download", CustomizedFileDownloadHandler),  # 定制化附件下载
    ("/api/erp/sc/data/account/lists", ErpUserListHandler),  # 查询ERP用户信息列表
    ("/api/erp/sc/data/seller/batchEditSellerName", BatchEditSellerNameHandler),  # 批量修改店铺名称
] 