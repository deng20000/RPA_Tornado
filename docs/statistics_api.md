# 统计模块 API 文档

## 模块概述

**模块名称**: Statistics (统计模块)  
**功能描述**: 负责各类数据统计和报表，包括销量数据统计、订单利润分析、产品表现监控等  
**接口数量**: 7个  
**路由前缀**: `/api/erp/sc/data/`, `/api/statistics/`, `/api/bd/`, `/api/basicOpen/`  

## 接口列表

### 1. 旧版销量报表ASIN日列表

**接口路径**: `/api/erp/sc/data/sales_report/asinDailyLists`  
**请求方法**: POST  
**功能描述**: 查询销量报表ASIN日列表数据  
**处理器**: SalesReportAsinDailyListsHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| sid | int | 是 | 店铺ID | 109 |
| event_date | string | 是 | 事件日期，格式YYYY-MM-DD | "2024-08-05" |
| asin_type | int | 否 | ASIN类型，1=父ASIN，2=子ASIN | 1 |
| type | int | 否 | 查询类型，1=销售额，2=销量，3=利润 | 1 |
| page | int | 否 | 页码，默认1 | 1 |
| page_size | int | 否 | 每页数量，默认20 | 20 |

#### 请求示例

```json
{
  "sid": 109,
  "event_date": "2024-08-05",
  "asin_type": 1,
  "type": 1,
  "page": 1,
  "page_size": 20
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "list": [
      {
        "asin": "B08N5WRWNW",
        "parent_asin": "B08N5WRWNW",
        "sales_amount": 1250.50,
        "sales_quantity": 25,
        "profit_amount": 375.15,
        "event_date": "2024-08-05"
      }
    ],
    "total": 150,
    "page": 1,
    "page_size": 20
  }
}
```

### 2. 订单利润MSKU查询

**接口路径**: `/api/statistics/order-profit-msku`  
**请求方法**: POST  
**功能描述**: 查询订单利润MSKU数据  
**处理器**: OrderProfitMSKUHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| sid | int | 否 | 店铺ID | 109 |
| msku | string | 否 | MSKU筛选 | "TEST-MSKU-001" |
| offset | int | 否 | 分页偏移量 | 0 |
| length | int | 否 | 分页长度 | 100 |

#### 请求示例

```json
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "sid": 109,
  "offset": 0,
  "length": 100
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "list": [
      {
        "msku": "TEST-MSKU-001",
        "order_count": 45,
        "sales_amount": 2250.75,
        "cost_amount": 1575.53,
        "profit_amount": 675.22,
        "profit_rate": 0.30
      }
    ],
    "total": 200
  }
}
```

### 3. 店铺汇总销量查询

**接口路径**: `/api/erp/sc/data/sales_report/sales`  
**请求方法**: POST  
**功能描述**: 查询店铺汇总销量数据  
**处理器**: SalesReportShopSummaryHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| sid | int | 是 | 店铺ID | 109 |
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| group_by | string | 否 | 分组方式：day/week/month | "day" |

#### 请求示例

```json
{
  "sid": 109,
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "group_by": "day"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "summary": {
      "total_sales_amount": 125000.50,
      "total_order_count": 2500,
      "avg_order_value": 50.00
    },
    "daily_data": [
      {
        "date": "2024-01-01",
        "sales_amount": 4500.25,
        "order_count": 90,
        "avg_order_value": 50.00
      }
    ]
  }
}
```

### 4. 查询产品表现

**接口路径**: `/api/bd/productPerformance/openApi/asinList`  
**请求方法**: POST  
**功能描述**: 查询产品表现数据，调用外部OpenAPI  
**处理器**: ProductPerformanceHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| offset | int | 是 | 分页偏移量，>=0 | 0 |
| length | int | 是 | 分页长度，1~10000 | 100 |
| sort_field | string | 是 | 排序字段 | "sales_amount" |
| sort_type | string | 是 | 排序方式，desc/asc | "desc" |
| sid | string/array | 是 | 店铺id，单店铺字符串，多店铺数组 | "109" |
| start_date | string | 是 | 开始日期，Y-m-d | "2024-01-01" |
| end_date | string | 是 | 结束日期，Y-m-d | "2024-01-31" |
| summary_field | string | 是 | 汇总行维度：asin/parent_asin/msku/sku | "asin" |
| search_field | string | 否 | 搜索字段 | "asin" |
| search_value | array | 否 | 搜索值 | ["B08N5WRWNW"] |
| mid | int | 否 | 站点id | 1 |
| extend_search | array | 否 | 表头筛选 | [] |
| currency_code | string | 否 | 货币类型 | "USD" |
| is_recently_enum | bool | 否 | 是否仅活跃商品 | true |

#### 请求示例

```json
{
  "offset": 0,
  "length": 100,
  "sort_field": "sales_amount",
  "sort_type": "desc",
  "sid": "109",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "summary_field": "asin",
  "currency_code": "USD"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "list": [
      {
        "asin": "B08N5WRWNW",
        "sales_amount": 5250.75,
        "sales_quantity": 105,
        "sessions": 2500,
        "conversion_rate": 0.042,
        "click_rate": 0.15
      }
    ],
    "total": 500
  }
}
```

### 5. 查询ASIN360小时数据

**接口路径**: `/api/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour`  
**请求方法**: POST  
**功能描述**: 查询产品表现小时级趋势数据  
**处理器**: ProductPerformanceTrendByHourHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| sids | array | 是 | 店铺ID数组 | [109] |
| date_start | string | 是 | 开始日期 | "2024-01-01" |
| date_end | string | 是 | 结束日期 | "2024-01-31" |
| summary_field | string | 是 | 汇总字段：parent_asin/asin/msku/sku/spu | "asin" |
| summary_field_value | string | 是 | 汇总字段值 | "B08N5WRWNW" |

#### 请求示例

```json
{
  "sids": [109],
  "date_start": "2024-01-01",
  "date_end": "2024-01-31",
  "summary_field": "asin",
  "summary_field_value": "B08N5WRWNW"
}
```

### 6. 利润统计-ASIN

**接口路径**: `/api/bd/profit/statistics/open/asin/list`  
**请求方法**: POST  
**功能描述**: 查询ASIN级别的利润统计数据  
**处理器**: ProfitStatisticsAsinListHandler  

### 7. 统计-订单利润MSKU (兼容接口)

**接口路径**: `/api/basicOpen/finance/mreport/OrderProfit`  
**请求方法**: POST  
**功能描述**: 统计订单利润MSKU数据（兼容接口）  
**处理器**: OrderProfitMSKUHandler  

## 通用参数说明

### 分页参数
- `offset`: 分页偏移量，从0开始
- `length`: 分页长度，建议不超过1000
- `page`: 页码，从1开始
- `page_size`: 每页数量

### 日期参数
- 格式要求：`YYYY-MM-DD`
- 时间范围：建议不超过90天
- 时区：默认使用系统时区

### 排序参数
- `sort_field`: 排序字段
- `sort_type`: 排序方式，`desc`(降序) 或 `asc`(升序)

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 参数验证失败 | 检查必填参数和参数格式 |
| 401 | 认证失败 | 检查access_token是否有效 |
| 403 | 权限不足 | 检查用户权限 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 使用示例

### Python 示例

```python
import requests
import json
from datetime import datetime, timedelta

# 查询销量报表ASIN日列表
def get_sales_report():
    url = "http://127.0.0.1:8888/api/erp/sc/data/sales_report/asinDailyLists"
    data = {
        "sid": 109,
        "event_date": "2024-08-05",
        "asin_type": 1,
        "type": 1
    }
    
    response = requests.post(url, json=data)
    return response.json()

# 查询订单利润MSKU
def get_order_profit():
    url = "http://127.0.0.1:8888/api/statistics/order-profit-msku"
    data = {
        "start_date": "2024-01-01",
        "end_date": "2024-01-31",
        "sid": 109,
        "offset": 0,
        "length": 100
    }
    
    response = requests.post(url, json=data)
    return response.json()

# 使用示例
if __name__ == "__main__":
    # 获取销量报表
    sales_data = get_sales_report()
    print("销量报表:", json.dumps(sales_data, indent=2, ensure_ascii=False))
    
    # 获取利润数据
    profit_data = get_order_profit()
    print("利润数据:", json.dumps(profit_data, indent=2, ensure_ascii=False))
```

### JavaScript 示例

```javascript
// 查询产品表现数据
async function getProductPerformance() {
  const url = 'http://127.0.0.1:8888/api/bd/productPerformance/openApi/asinList';
  const data = {
    offset: 0,
    length: 100,
    sort_field: 'sales_amount',
    sort_type: 'desc',
    sid: '109',
    start_date: '2024-01-01',
    end_date: '2024-01-31',
    summary_field: 'asin'
  };
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    
    const result = await response.json();
    console.log('产品表现数据:', result);
    return result;
  } catch (error) {
    console.error('请求失败:', error);
  }
}
```

## 性能优化建议

1. **分页查询**: 大数据量时使用分页，避免一次性查询过多数据
2. **日期范围**: 控制查询的日期范围，建议不超过90天
3. **缓存策略**: 对于不经常变化的数据，可以使用缓存
4. **并发控制**: 避免同时发起过多请求

## 注意事项

1. **认证要求**: 大部分接口需要有效的access_token
2. **参数验证**: 严格按照接口文档提供参数
3. **日期格式**: 统一使用YYYY-MM-DD格式
4. **数据权限**: 只能查询有权限的店铺数据
5. **API限流**: 注意接口调用频率限制

## 更新日志

- **v1.0.0** (2025-01-13): 初始版本，包含7个统计相关接口
- 支持销量报表、利润分析、产品表现等功能
- 提供完整的参数验证和错误处理

---

> 📝 **相关文档**: [API总文档](./API_MASTER_DOCUMENTATION.md) | [多平台模块文档](./multi_platform_api.md)