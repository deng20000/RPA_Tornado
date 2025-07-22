# RPA_Tornado 项目说明

---

## 一、项目结构

- `app/ecommerce_dashboard/handlers/stat_handler.py`  电商数据看板主接口
- `app/ecommerce_dashboard/services/stat_service.py`  电商数据看板主业务逻辑
- `app/ecommerce_dashboard/services/common.py`        通用API请求工具
- `app/ecommerce_dashboard/routes.py`                 路由注册
- `main.py`                                          启动入口，统一管理所有接口

---

## 二、依赖安装

建议使用虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

---

## 三、环境配置

请在 `app/config.py` 中配置 API HOST、APP_ID、APP_SECRET 等参数。

---

## 四、项目启动

在项目根目录下执行：

```bash
python RPA_Tornado/main.py
```

启动后访问接口如：
- POST http://127.0.0.1:8888/api/ecommerce/sale_stat

---

## 五、主要接口一览（分组并列：统计、基础数据、多平台）

### 统计
| 路径 | 方法 | 功能简介 | 原始路由 |
|------|------|----------|----------|
| /api/basicOpen/finance/mreport/OrderProfit | POST | 订单利润MSKU查询 | /api/basicOpen/finance/mreport/OrderProfit |
| /api/bd/profit/statistics/open/msku/list | POST | 订单利润MSKU查询（兼容老路由） | /api/bd/profit/statistics/open/msku/list |
| /api/statistics/order-profit-msku | POST | 统计-订单利润MSKU | /api/statistics/order-profit-msku |
| /api/statistics/sales-report-asin-daily-lists | POST | 统计-销量报表ASIN日列表 | /api/statistics/sales-report-asin-daily-lists |
| /api/erp/sc/data/sales_report/sales | POST | 查询店铺汇总销量 | /erp/sc/data/sales_report/sales |

### 基础数据
| 路径 | 方法 | 功能简介 | 原始路由 |
|------|------|----------|----------|
| /api/erp/sc/routing/finance/currency/currencyMonth | POST | 查询汇率 | /api/erp/sc/routing/finance/currency/currencyMonth |
| /api/erp/sc/data/seller/lists | GET | 查询亚马逊店铺列表 | /api/erp/sc/data/seller/lists |
| /api/erp/sc/data/seller/allMarketplace | GET | 查询亚马逊市场列表 | /api/erp/sc/data/seller/allMarketplace |
| /api/erp/sc/data/worldState/lists | POST | 查询世界州/省列表 | /api/erp/sc/data/worldState/lists |
| /api/erp/sc/routing/common/file/download | POST | 下载产品附件 | /api/erp/sc/routing/common/file/download |
| /api/erp/sc/routing/customized/file/download | POST | 定制化附件下载 | /api/erp/sc/routing/customized/file/download |
| /api/erp/sc/data/account/lists | GET | 查询ERP用户信息列表 | /api/erp/sc/data/account/lists |

### 多平台
| 路径 | 方法 | 功能简介 | 原始路由 |
|------|------|----------|----------|
| /api/basicOpen/platformStatisticsV2/saleStat/pageList | POST | 查询销量统计列表v2 | /api/basicOpen/platformStatisticsV2/saleStat/pageList |
| /api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list | POST | 查询多平台店铺基础信息 | /api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list |
| /api/basicOpen/multiplatform/profit/report/msku | POST | 多平台结算利润（利润报表）-msku | /api/basicOpen/multiplatform/profit/report/msku |
| /api/basicOpen/multiplatform/profit/report/sku | POST | 多平台结算利润（利润报表）-sku | /api/basicOpen/multiplatform/profit/report/sku |

---

### 接口映射与限流说明

| API Path（转发路由） | 原路由 | 请求协议 | 请求方式 | 令牌桶容量 | 简要说明 |
|---------------------|--------|----------|----------|------------|----------|
| /api/ecommerce/sale_stat | /basicOpen/platformStatisticsV2/saleStat/pageList | HTTPS | POST | 10 | 电商销售统计 |
| /api/base-data/currency-exchange-rate | /erp/sc/routing/finance/currency/currencyMonth | HTTPS | POST | 10 | 查询汇率 |
| /api/base-data/file-attachment-download | /erp/sc/routing/common/file/download | HTTPS | POST | 10 | 下载产品附件 |
| /api/base-data/customized-file-download | /erp/sc/routing/customized/file/download | HTTPS | POST | 10 | 定制化附件下载 |
| /api/base-data/batch-edit-seller-name | /erp/sc/data/seller/batchEditSellerName | HTTPS | POST | 10 | 批量修改店铺名称 |
| /api/multi-platform/sale-statistics-v2 | /basicOpen/platformStatisticsV2/saleStat/pageList | HTTPS | POST | 10 | 多平台销量统计 |
| /api/multi-platform/sales-report-asin-daily-lists | /basicOpen/platformStatisticsV2/saleStat/pageList | HTTPS | POST | 10 | 多平台ASIN日销量报表 |
| /api/statistics/order-profit-msku | /bd/profit/statistics/open/msku/list | HTTPS | POST | 10 | 订单利润MSKU查询 |
| /api/erp/sc/data/sales_report/asinDailyLists | /erp/sc/data/sales_report/asinDailyLists | HTTPS | POST | 5 | 查询销量、订单量、销售额 |
| ... | ... | ... | ... | ... | ... |

> 说明：如需补充更多接口原路由或限流参数，请参考源码 service 层的 api_request/route_name 字段或联系后端开发。

---

## 六、接口参数与示例（按功能分组）

### 多平台
- 路径：`/api/basicOpen/platformStatisticsV2/saleStat/pageList`  
- 方法：POST
- 原始路由：`/basicOpen/platformStatisticsV2/saleStat/pageList`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list`  
- 方法：POST
- 原始路由：`/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/basicOpen/multiplatform/profit/report/msku`
- 方法：POST
- 原始路由：`/api/basicOpen/multiplatform/profit/report/msku`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/basicOpen/multiplatform/profit/report/sku`
- 方法：POST
- 原始路由：`/api/basicOpen/multiplatform/profit/report/sku`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 20 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 是 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 统计
- 路径：`/api/basicOpen/finance/mreport/OrderProfit`
- 方法：POST
- 原始路由：`/basicOpen/finance/mreport/OrderProfit`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/bd/profit/statistics/open/msku/list`
- 方法：POST
- 原始路由：`/bd/profit/statistics/open/msku/list`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/statistics/order-profit-msku`
- 方法：POST
- 原始路由：`/statistics/order-profit-msku`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/statistics/sales-report-asin-daily-lists`
- 方法：POST
- 原始路由：`/statistics/sales-report-asin-daily-lists`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 基础数据
- 路径：`/api/erp/sc/routing/finance/currency/currencyMonth`
- 方法：POST
- 原始路由：`/erp/sc/routing/finance/currency/currencyMonth`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | date | string | 否 | 汇率月份，格式YYYY-MM | 2023-08 |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/data/seller/lists`
- 方法：GET
- 原始路由：`/erp/sc/data/seller/lists`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/data/seller/allMarketplace`
- 方法：GET
- 原始路由：`/erp/sc/data/seller/allMarketplace`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/data/worldState/lists`
- 方法：POST
- 原始路由：`/erp/sc/data/worldState/lists`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/routing/common/file/download`
- 方法：POST
- 原始路由：`/erp/sc/routing/common/file/download`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/routing/customized/file/download`
- 方法：POST
- 原始路由：`/erp/sc/routing/customized/file/download`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 20 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 是 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/data/account/lists`
- 方法：GET
- 原始路由：`/erp/sc/data/account/lists`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量，默认0 | 0 |
  | length | int | 是 | 分页长度，默认1000 | 100 |
  | platformCodeS | array | 否 | 平台id数组 | ["10024"] |
  | mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
  | sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
  | currencyCode | string | 否 | 币种code | "USD" |
  | startDate | string | 是 | 开始时间，Y-m-d | 2024-09-01 |
  | endDate | string | 是 | 结束时间，Y-m-d | 2024-09-30 |
  | searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
  | searchValue | string | 否 | 搜索值 | "123" |
  | developers | array | 否 | 开发人 | [128581] |
  | cids | array | 否 | 分类 | [14] |
  | bids | array | 否 | 品牌 | [2] |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/erp/sc/data/sales_report/sales`
- 方法：POST
- 原始路由：`/erp/sc/data/sales_report/sales`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | sid | array(int) | 是 | 店铺id数组 | [109] |
  | start_date | string | 是 | 报表开始时间，Y-m-d | 2020-01-01 |
  | end_date | string | 是 | 报表结束时间，Y-m-d | 2024-08-05 |
  | offset | int | 否 | 分页偏移量，默认0 | 0 |
  | length | int | 否 | 分页长度，默认1000 | 1000 |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/bd/productPerformance/openApi/asinList`
- 方法：POST
- 原始路由：`/bd/productPerformance/openApi/asinList`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 是 | 分页偏移量 | 0 |
  | length | int | 是 | 分页长度，最大10000 | 20 |
  | sort_field | string | 是 | 排序字段 | volume |
  | sort_type | string | 是 | 排序方式，desc/asc | desc |
  | search_field | string | 否 | 搜索字段 | asin |
  | search_value | array | 否 | 搜索值，最多50个 | ["B085M7NH7K"] |
  | mid | int | 否 | 站点id | 1 |
  | sid | string/array | 是 | 店铺id，单店铺传字符串，多店铺传数组 | [1,109] |
  | start_date | string | 是 | 开始日期，Y-m-d | 2024-08-01 |
  | end_date | string | 是 | 结束日期，Y-m-d | 2024-08-07 |
  | extend_search | array | 否 | 表头筛选 | - |
  | summary_field | string | 是 | 汇总行维度 | asin |
  | currency_code | string | 否 | 货币类型 | CNY |
  | is_recently_enum | boolean | 否 | 是否仅查询活跃商品 | true |
  | avg_volume | string | 是 | 平均销量 | volume |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour`
- 方法：POST
- 原始路由：`/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | sids | string | 是 | 店铺id，多个用英文逗号隔开，最大200 | "136,139" |
  | date_start | string | 是 | 开始时间，Y-m-d | 2024-09-24 |
  | date_end | string | 是 | 结束时间，Y-m-d | 2024-09-24 |
  | summary_field | string | 是 | 查询维度：parent_asin/asin/msku/sku/spu | spu |
  | summary_field_value | string | 是 | 查询维度值 | 10886 |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- 路径：`/api/bd/profit/statistics/open/asin/list`
- 方法：POST
- 原始路由：`/api/bd/profit/statistics/open/asin/list`
- 主要参数：
  | 参数名 | 类型 | 必填 | 说明 | 示例 |
  |--------|------|------|------|------|
  | offset | int | 否 | 分页偏移量 | 0 |
  | length | int | 否 | 分页长度，上限10000 | 1000 |
  | mids | array | 否 | 站点id | [2] |
  | sids | array | 否 | 店铺id | [17] |
  | startDate | string | 是 | 开始时间，Y-m-d，间隔不超过7天 | 2022-09-21 |
  | endDate | string | 是 | 结束时间，Y-m-d，间隔不超过7天 | 2022-09-25 |
  | searchField | string | 否 | 搜索值类型，asin | asin |
  | searchValue | array | 否 | 搜索值 | ["B07DFKF00SG"] |
  | currencyCode | string | 否 | 币种code | CNY |
- 返回：
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

---

## 七、测试

运行测试用例：
```bash
pytest RPA_Tornado/tests/test_ecommerce_dashboard.py -s
```

---

## 八、扩展说明

如有更多子项目或接口需求，建议仿照本结构扩展即可。

---

> 文档自动生成自 swagger.yaml，详细参数和返回结构请参考 swagger 文件或源码注释。 "# RPA_Tornado" 
