# 多平台模块 API 文档

## 模块概述

**模块名称**: Multi Platform (多平台模块)  
**功能描述**: 负责跨平台数据整合、多平台销量统计、跨平台利润分析等功能  
**接口数量**: 12个  
**路由前缀**: `/api/basicOpen/`, `/api/bd/`, `/api/multi-platform/`  

## 接口列表

### 1. 多平台销量统计v2

**接口路径**: `/api/basicOpen/platformStatisticsV2/saleStat/pageList`  
**请求方法**: POST  
**功能描述**: 查询多平台销量统计数据  
**处理器**: SaleStatisticsV2Handler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| offset | int | 是 | 分页偏移量，默认0 | 0 |
| length | int | 是 | 分页长度，最小值20，默认1000 | 100 |
| start_date | string | 是 | 开始时间，格式Y-m-d | "2024-01-01" |
| end_date | string | 是 | 结束时间，格式Y-m-d | "2024-01-31" |
| date_unit | string | 是 | 时间单位 | "day" |
| result_type | int | 是 | 结果类型 | 1 |
| platformCodeS | array | 否 | 平台id数组 | ["10024"] |
| mids | string | 否 | 国家id，多个用英文逗号分隔 | "NA,MX,BR,US,CA" |
| sids | string | 否 | 店铺id，多个用英文逗号分隔 | "110424575139430912" |
| currencyCode | string | 否 | 币种code | "USD" |
| searchField | string | 否 | 搜索值类型：msku,local_sku,platform_order_no | "local_sku" |
| searchValue | string | 否 | 搜索值 | "123" |
| developers | array | 否 | 开发人 | [128581] |
| cids | array | 否 | 分类 | [14] |
| bids | array | 否 | 品牌 | [2] |

#### 请求示例

```json
{
  "offset": 0,
  "length": 100,
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "date_unit": "day",
  "result_type": 1,
  "platformCodeS": ["10024"],
  "currencyCode": "USD"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "platform_name": "Amazon",
        "sales_amount": 15000.50,
        "order_count": 125,
        "date": "2024-01-01"
      }
    ],
    "total": 1000
  }
}
```

### 2. 多平台店铺信息查询

**接口路径**: `/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list`  
**请求方法**: POST  
**功能描述**: 查询多平台店铺信息列表  
**处理器**: MultiPlatformSellerListHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| offset | int | 是 | 分页偏移量 | 0 |
| length | int | 是 | 分页长度，最小值20 | 20 |
| platform_codes | array | 否 | 平台代码列表 | ["amazon", "ebay"] |
| status | int | 否 | 店铺状态 | 1 |

#### 请求示例

```json
{
  "offset": 0,
  "length": 20,
  "platform_codes": ["amazon"],
  "status": 1
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [
      {
        "seller_id": "110424575139430912",
        "seller_name": "测试店铺",
        "platform_name": "Amazon",
        "marketplace": "US",
        "status": 1
      }
    ],
    "total": 50
  }
}
```

### 3. 多平台订单利润MSKU

**接口路径**: `/api/bd/profit/statistics/open/msku/list`  
**请求方法**: POST  
**功能描述**: 查询多平台订单利润MSKU数据（兼容老路由）  
**处理器**: MultiPlatformOrderProfitMSKUHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| startDate | string | 是 | 开始日期 | "2024-01-01" |
| endDate | string | 是 | 结束日期 | "2024-01-31" |
| offset | int | 否 | 分页偏移量 | 0 |
| length | int | 否 | 分页长度 | 100 |
| msku | string | 否 | MSKU筛选 | "TEST-MSKU-001" |

#### 请求示例

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
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
        "profit_amount": 1250.75,
        "sales_amount": 5000.00,
        "cost_amount": 3749.25,
        "order_count": 25
      }
    ],
    "total": 100
  }
}
```

### 4. 多平台结算利润-MSKU

**接口路径**: `/api/basicOpen/multiplatform/profit/report/msku`  
**请求方法**: POST  
**功能描述**: 查询多平台结算利润MSKU报表  
**处理器**: ProfitReportMSKUHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| startDate | string | 是 | 开始日期 | "2024-01-01" |
| endDate | string | 是 | 结束日期 | "2024-01-31" |
| offset | int | 否 | 分页偏移量 | 0 |
| length | int | 否 | 分页长度 | 100 |
| platform_codes | array | 否 | 平台代码 | ["amazon"] |

### 5. 多平台结算利润-SKU

**接口路径**: `/api/basicOpen/multiplatform/profit/report/sku`  
**请求方法**: POST  
**功能描述**: 查询多平台结算利润SKU报表  
**处理器**: ProfitReportSKUHandler  

### 6-12. 兼容性路由

以下是为了保持兼容性而提供的路由，功能与上述接口相同：

| 路由路径 | 对应功能 | 处理器 |
|---------|----------|--------|
| `/api/multi-platform/sale-statistics-v2` | 多平台销量统计v2 | SaleStatisticsV2Handler |
| `/api/multi-platform/sales-report-asin-daily-lists` | 多平台ASIN日销量报表 | MultiPlatformSalesReportAsinDailyListsHandler |
| `/api/multi-platform/order-profit-msku` | 多平台订单利润MSKU | MultiPlatformOrderProfitMSKUHandler |
| `/api/multi-platform/profit-report-msku` | 多平台结算利润-msku | ProfitReportMSKUHandler |
| `/api/multi-platform/profit-report-sku` | 多平台结算利润-sku | ProfitReportSKUHandler |
| `/api/multi-platform/seller-list` | 多平台店铺信息查询 | MultiPlatformSellerListHandler |
| `/api/multi-platform/profit-report-seller` | 多平台结算利润-店铺 | ProfitReportSellerHandler |

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 102 | 参数验证失败 | 检查必填参数和参数格式 |
| 400 | 请求参数错误 | 检查参数名称和数据类型 |
| 401 | 认证失败 | 检查access_token是否有效 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 使用示例

### Python 示例

```python
import requests
import json

# 查询多平台销量统计
url = "http://127.0.0.1:8888/api/basicOpen/platformStatisticsV2/saleStat/pageList"
data = {
    "offset": 0,
    "length": 100,
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "date_unit": "day",
    "result_type": 1
}

response = requests.post(url, json=data)
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))
```

### cURL 示例

```bash
# 查询多平台店铺信息
curl -X POST "http://127.0.0.1:8888/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list" \
  -H "Content-Type: application/json" \
  -d '{
    "offset": 0,
    "length": 20
  }'
```

## 注意事项

1. **分页参数**: `length` 参数最小值为20，建议不超过1000
2. **日期格式**: 所有日期参数必须使用 `YYYY-MM-DD` 格式
3. **认证机制**: 大部分接口需要有效的 `access_token`
4. **兼容性**: 提供了新旧两套路由，建议使用新路由
5. **性能优化**: 大数据量查询时建议使用分页

## 更新日志

- **v1.0.0** (2025-01-13): 初始版本，包含12个多平台相关接口
- 支持跨平台数据整合和统计分析
- 提供兼容性路由支持

---

> 📝 **相关文档**: [API总文档](./API_MASTER_DOCUMENTATION.md) | [项目README](../README.md)