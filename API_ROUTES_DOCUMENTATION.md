# RPA Tornado API 路由文档

本文档详细说明了 RPA Tornado 项目中各个模块的 API 路由信息。

## 项目架构概览

项目采用模块化设计，主要包含以下5个核心模块：

1. **统计模块** (Statistics) - 负责各类数据统计和报表
2. **基础数据模块** (Base Data) - 负责基础数据查询和管理
3. **多平台模块** (Multi Platform) - 负责多平台数据整合
4. **产品模块** (Product) - 负责产品和分类管理
5. **亚马逊源表数据模块** (Amazon Table) - 负责亚马逊原始数据查询

---

## 1. 统计模块 (Statistics Module)

**文件位置**: `app/routes/statistics_routes.py`

### 路由列表

| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/erp/sc/data/sales_report/asinDailyLists` | SalesReportAsinDailyListsHandler | 旧版销量报表ASIN日列表 |
| `/api/statistics/order-profit-msku` | OrderProfitMSKUHandler | 订单利润MSKU查询 |
| `/api/erp/sc/data/sales_report/sales` | SalesReportShopSummaryHandler | 店铺汇总销量查询 |
| `/api/bd/productPerformance/openApi/asinList` | ProductPerformanceHandler | 查询产品表现 |
| `/api/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour` | ProductPerformanceTrendByHourHandler | 查询asin360小时数据 |
| `/api/bd/profit/statistics/open/asin/list` | ProfitStatisticsAsinListHandler | 利润统计-ASIN |
| `/api/basicOpen/finance/mreport/OrderProfit` | OrderProfitMSKUHandler | 统计-订单利润MSKU |

### 主要功能
- 销量数据统计和分析
- 订单利润分析
- 产品表现监控
- ASIN级别的数据统计

---

## 2. 基础数据模块 (Base Data Module)

**文件位置**: `app/routes/base_data_routes.py`

### 路由列表

| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/erp/sc/routing/finance/currency/currencyMonth` | CurrencyExchangeRateHandler | 查询汇率 |
| `/api/erp/sc/data/seller/lists` | AmazonSellerListHandler | 查询亚马逊店铺列表 |
| `/api/erp/sc/data/seller/allMarketplace` | AmazonMarketplaceListHandler | 查询亚马逊市场列表 |
| `/api/erp/sc/data/worldState/lists` | WorldStateListHandler | 查询世界州/省列表 |
| `/api/erp/sc/routing/common/file/download` | FileAttachmentDownloadHandler | 下载产品附件 |
| `/api/erp/sc/routing/customized/file/download` | CustomizedFileDownloadHandler | 定制化附件下载 |
| `/api/erp/sc/data/account/lists` | ErpUserListHandler | 查询ERP用户信息列表 |
| `/api/erp/sc/data/seller/batchEditSellerName` | BatchEditSellerNameHandler | 批量修改店铺名称 |

### 主要功能
- 汇率数据查询
- 店铺和市场信息管理
- 地理位置数据查询
- 文件下载服务
- 用户信息管理

---

## 3. 多平台模块 (Multi Platform Module)

**文件位置**: `app/routes/multi_platform_routes.py`

### 路由列表

| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/basicOpen/platformStatisticsV2/saleStat/pageList` | SaleStatisticsV2Handler | 多平台销量统计v2 |
| `/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list` | MultiPlatformSellerListHandler | 多平台店铺信息查询 |
| `/api/bd/profit/statistics/open/msku/list` | MultiPlatformOrderProfitMSKUHandler | 多平台订单利润MSKU（兼容老路由） |
| `/api/basicOpen/multiplatform/profit/report/msku` | ProfitReportMSKUHandler | 多平台结算利润-msku |
| `/api/basicOpen/multiplatform/profit/report/sku` | ProfitReportSKUHandler | 多平台结算利润-sku |
| `/api/multi-platform/sale-statistics-v2` | SaleStatisticsV2Handler | 多平台销量统计v2（兼容路由） |
| `/api/multi-platform/sales-report-asin-daily-lists` | MultiPlatformSalesReportAsinDailyListsHandler | 多平台ASIN日销量报表 |
| `/api/multi-platform/order-profit-msku` | MultiPlatformOrderProfitMSKUHandler | 多平台订单利润MSKU |
| `/api/multi-platform/profit-report-msku` | ProfitReportMSKUHandler | 多平台结算利润-msku |
| `/api/multi-platform/profit-report-sku` | ProfitReportSKUHandler | 多平台结算利润-sku |
| `/api/multi-platform/seller-list` | MultiPlatformSellerListHandler | 多平台店铺信息查询 |
| `/api/multi-platform/profit-report-seller` | ProfitReportSellerHandler | 多平台结算利润-店铺 |

### 主要功能
- 跨平台数据整合
- 多平台销量统计
- 跨平台利润分析
- 多平台店铺管理

---

## 4. 产品模块 (Product Module)

**文件位置**: `app/routes/product_routes.py`

### 路由列表

| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/erp/sc/routing/data/local_inventory/productList` | LocalProductListHandler | 查询本地产品列表 |
| `/api/erp/sc/routing/data/product/list` | ProductListHandler | 获取产品列表 |
| `/api/erp/sc/routing/data/product/create` | ProductCreateHandler | 创建产品 |
| `/api/erp/sc/routing/data/product/update` | ProductUpdateHandler | 更新产品 |
| `/api/erp/sc/routing/data/product/delete` | ProductDeleteHandler | 删除产品 |
| `/api/erp/sc/routing/data/product/category/list` | ProductCategoryListHandler | 获取产品分类列表 |
| `/api/erp/sc/routing/data/product/category/create` | ProductCategoryCreateHandler | 创建产品分类 |
| `/api/erp/sc/routing/data/product/category/update` | ProductCategoryUpdateHandler | 更新产品分类 |
| `/api/erp/sc/routing/data/product/category/delete` | ProductCategoryDeleteHandler | 删除产品分类 |

### 主要功能
- 产品信息管理（CRUD操作）
- 产品分类管理
- 本地库存产品查询

---

## 5. 亚马逊源表数据模块 (Amazon Table Module)

**文件位置**: `app/routes/amazon_table_routes.py`

### 路由列表

#### 订单相关报表
| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/erp/sc/routing/data/order/removalShipmentList` | RemovalShipmentListHandler | 移除货件报表查询 |
| `/api/erp/sc/routing/data/order/removalOrderListNew` | RemovalOrderListNewHandler | 移除订单报表查询（新） |
| `/api/erp/sc/data/mws_report/allOrders` | AllOrdersHandler | 所有订单报表查询 |
| `/api/erp/sc/data/mws_report/fbaOrders` | FbaOrdersHandler | FBA订单报表查询 |
| `/api/erp/sc/routing/data/order/fbaExchangeOrderList` | FbaExchangeOrdersHandler | FBA换货订单报表查询 |
| `/api/erp/sc/data/mws_report/refundOrders` | FbaRefundOrdersHandler | FBA退货订单报表查询 |
| `/api/erp/sc/routing/data/order/fbmReturnOrderList` | FbmReturnOrdersHandler | FBM退货订单报表查询 |

#### 库存相关报表
| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/erp/sc/data/mws_report/manageInventory` | ManageInventoryHandler | FBA库存报表 |
| `/api/erp/sc/data/mws_report/dailyInventory` | DailyInventoryHandler | 每日库存报表 |
| `/api/erp/sc/data/mws_report/getAfnFulfillableQuantity` | AfnFulfillableQuantityHandler | FBA可售库存报表 |
| `/api/erp/sc/data/mws_report/reservedInventory` | ReservedInventoryHandler | 预留库存报表 |
| `/api/erp/sc/routing/fba/fbaStock/getFbaAgeList` | FbaAgeListHandler | 库龄表 |

#### 发货相关报表
| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/erp/sc/data/mws_report/getAmazonFulfilledShipmentsList` | AmazonFulfilledShipmentsListHandler | Amazon Fulfilled Shipments报表 |
| `/api/erp/sc/data/mws_report_v1/getAmazonFulfilledShipmentsList` | AmazonFulfilledShipmentsListV1Handler | Amazon Fulfilled Shipments v1报表 |

#### 其他报表
| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/basicOpen/openapi/mwsReport/adjustmentList` | AdjustmentListHandler | 盘存记录 |

#### 报告导出功能
| 路由路径 | 处理器 | 功能描述 |
|---------|--------|----------|
| `/api/basicOpen/report/create/reportExportTask` | CreateReportExportTaskHandler | 创建报告导出任务 |
| `/api/basicOpen/report/query/reportExportTask` | QueryReportExportTaskHandler | 查询报告导出任务结果 |
| `/api/basicOpen/report/amazonReportExportTask` | AmazonReportExportTaskHandler | 报告下载链接续期 |

### 主要功能
- 亚马逊原始数据查询
- 订单、库存、发货等各类报表
- 报告导出和下载功能

---

## 路由注册机制

所有路由通过 `app/routes/__init__.py` 文件进行统一注册：

```python
from .statistics_routes import statistics_routes
from .base_data_routes import base_data_routes
from .multi_platform_routes import multi_platform_routes
from .product_routes import product_routes
from .amazon_table_routes import amazon_table_routes

routes = statistics_routes + base_data_routes + multi_platform_routes + product_routes + amazon_table_routes
```

## 总计统计

- **统计模块**: 7个路由
- **基础数据模块**: 8个路由
- **多平台模块**: 12个路由
- **产品模块**: 9个路由
- **亚马逊源表数据模块**: 18个路由

**总计**: 54个API路由

---

## 注意事项

1. 所有路由都支持POST请求方式
2. 部分路由存在兼容性版本（如多平台模块中的v2版本）
3. 亚马逊源表数据模块包含最多的路由，主要用于各类报表查询
4. 每个模块都有对应的处理器(Handler)和服务(Service)层
5. 路由设计遵循RESTful API规范

---

*文档生成时间: 2024年12月31日*
*项目版本: RPA Tornado v1.0*