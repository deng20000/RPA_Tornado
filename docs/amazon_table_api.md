# 亚马逊源表数据模块 API 文档

## 模块概述

**模块名称**: Amazon Table Data (亚马逊源表数据模块)  
**功能描述**: 负责亚马逊原始数据的管理和查询，包括销售报表、库存报表、广告报表、财务报表等各类亚马逊源数据  
**接口数量**: 22个  
**路由前缀**: `/api/amazon-table/`  

## 接口列表

### 1. 销售报表数据查询

**接口路径**: `/api/amazon-table/sales-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊销售报表原始数据  
**处理器**: SalesReportHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| report_type | string | 否 | 报表类型 | "GET_MERCHANT_LISTINGS_ALL_DATA" |
| asin | string | 否 | ASIN筛选 | "B08N5WRWNW" |
| sku | string | 否 | SKU筛选 | "TEST-SKU-001" |
| page | int | 否 | 页码 | 1 |
| page_size | int | 否 | 每页数量 | 100 |

#### 请求示例

```json
{
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "report_type": "GET_MERCHANT_LISTINGS_ALL_DATA",
  "page": 1,
  "page_size": 100
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
        "record_id": "sales_20240101_001",
        "marketplace_id": "ATVPDKIKX0DER",
        "seller_id": "A1SELLER123",
        "asin": "B08N5WRWNW",
        "sku": "TEST-SKU-001",
        "product_name": "无线蓝牙耳机",
        "quantity": 5,
        "price": 99.99,
        "currency": "USD",
        "order_date": "2024-01-01 10:30:00",
        "settlement_date": "2024-01-03",
        "raw_data": {...}
      }
    ],
    "total": 2500,
    "page": 1,
    "page_size": 100
  }
}
```

### 2. 库存报表数据查询

**接口路径**: `/api/amazon-table/inventory-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊库存报表原始数据  
**处理器**: InventoryReportHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| report_date | string | 是 | 报表日期 | "2024-01-15" |
| fulfillment_channel | string | 否 | 配送渠道：FBA/FBM | "FBA" |
| asin | string | 否 | ASIN筛选 | "B08N5WRWNW" |
| sku | string | 否 | SKU筛选 | "TEST-SKU-001" |
| warehouse_id | string | 否 | 仓库ID | "FBA_US_EAST" |

#### 请求示例

```json
{
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "report_date": "2024-01-15",
  "fulfillment_channel": "FBA",
  "warehouse_id": "FBA_US_EAST"
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
        "record_id": "inv_20240115_001",
        "marketplace_id": "ATVPDKIKX0DER",
        "seller_id": "A1SELLER123",
        "asin": "B08N5WRWNW",
        "sku": "TEST-SKU-001",
        "fulfillment_channel": "FBA",
        "warehouse_id": "FBA_US_EAST",
        "available_quantity": 150,
        "reserved_quantity": 25,
        "inbound_quantity": 50,
        "report_date": "2024-01-15",
        "raw_data": {...}
      }
    ],
    "total": 500
  }
}
```

### 3. 广告报表数据查询

**接口路径**: `/api/amazon-table/advertising-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊广告报表原始数据  
**处理器**: AdvertisingReportHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| campaign_type | string | 否 | 广告类型：SP/SB/SD | "SP" |
| campaign_id | string | 否 | 广告活动ID | "12345678" |
| asin | string | 否 | ASIN筛选 | "B08N5WRWNW" |
| metrics | array | 否 | 指标筛选 | ["impressions", "clicks", "cost"] |

#### 请求示例

```json
{
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "campaign_type": "SP",
  "metrics": ["impressions", "clicks", "cost", "sales"]
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
        "record_id": "ad_20240101_001",
        "marketplace_id": "ATVPDKIKX0DER",
        "seller_id": "A1SELLER123",
        "campaign_id": "12345678",
        "campaign_name": "蓝牙耳机推广",
        "campaign_type": "SP",
        "asin": "B08N5WRWNW",
        "date": "2024-01-01",
        "impressions": 1250,
        "clicks": 85,
        "cost": 42.50,
        "sales": 299.97,
        "orders": 3,
        "raw_data": {...}
      }
    ],
    "total": 1000,
    "summary": {
      "total_impressions": 125000,
      "total_clicks": 8500,
      "total_cost": 4250.00,
      "total_sales": 29997.00,
      "total_orders": 300
    }
  }
}
```

### 4. 财务报表数据查询

**接口路径**: `/api/amazon-table/financial-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊财务报表原始数据  
**处理器**: FinancialReportHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| transaction_type | string | 否 | 交易类型 | "Order" |
| settlement_id | string | 否 | 结算ID | "12345678901234567890" |
| currency | string | 否 | 货币类型 | "USD" |

#### 请求示例

```json
{
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "transaction_type": "Order",
  "currency": "USD"
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
        "record_id": "fin_20240101_001",
        "marketplace_id": "ATVPDKIKX0DER",
        "seller_id": "A1SELLER123",
        "settlement_id": "12345678901234567890",
        "transaction_type": "Order",
        "order_id": "123-4567890-1234567",
        "sku": "TEST-SKU-001",
        "quantity": 2,
        "product_sales": 199.98,
        "shipping_credits": 0.00,
        "gift_wrap_credits": 0.00,
        "promotional_rebates": -10.00,
        "sales_tax_collected": 16.00,
        "marketplace_facilitator_tax": 0.00,
        "selling_fees": -30.00,
        "fba_fees": -15.00,
        "other_transaction_fees": -2.50,
        "total_amount": 158.48,
        "currency": "USD",
        "posted_date": "2024-01-01",
        "raw_data": {...}
      }
    ],
    "total": 3000,
    "summary": {
      "total_sales": 59994.00,
      "total_fees": -14250.00,
      "net_amount": 45744.00
    }
  }
}
```

### 5. 订单报表数据查询

**接口路径**: `/api/amazon-table/order-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊订单报表原始数据  
**处理器**: OrderReportHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| order_status | string | 否 | 订单状态 | "Shipped" |
| fulfillment_channel | string | 否 | 配送渠道 | "FBA" |
| order_id | string | 否 | 订单ID | "123-4567890-1234567" |

#### 请求示例

```json
{
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "order_status": "Shipped",
  "fulfillment_channel": "FBA"
}
```

### 6. 退货报表数据查询

**接口路径**: `/api/amazon-table/return-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊退货报表原始数据  
**处理器**: ReturnReportHandler  

### 7. 费用报表数据查询

**接口路径**: `/api/amazon-table/fee-report`  
**请求方法**: POST  
**功能描述**: 查询亚马逊各类费用报表原始数据  
**处理器**: FeeReportHandler  

### 8. 库存调整报表查询

**接口路径**: `/api/amazon-table/inventory-adjustment`  
**请求方法**: POST  
**功能描述**: 查询库存调整记录  
**处理器**: InventoryAdjustmentHandler  

### 9. 移除订单报表查询

**接口路径**: `/api/amazon-table/removal-order`  
**请求方法**: POST  
**功能描述**: 查询移除订单报表数据  
**处理器**: RemovalOrderHandler  

### 10. 补货建议报表查询

**接口路径**: `/api/amazon-table/restock-recommendation`  
**请求方法**: POST  
**功能描述**: 查询补货建议报表数据  
**处理器**: RestockRecommendationHandler  

### 11. 产品排名报表查询

**接口路径**: `/api/amazon-table/product-ranking`  
**请求方法**: POST  
**功能描述**: 查询产品排名报表数据  
**处理器**: ProductRankingHandler  

### 12. 关键词排名报表查询

**接口路径**: `/api/amazon-table/keyword-ranking`  
**请求方法**: POST  
**功能描述**: 查询关键词排名报表数据  
**处理器**: KeywordRankingHandler  

### 13. 评论报表数据查询

**接口路径**: `/api/amazon-table/review-report`  
**请求方法**: POST  
**功能描述**: 查询产品评论报表数据  
**处理器**: ReviewReportHandler  

### 14. 品牌分析报表查询

**接口路径**: `/api/amazon-table/brand-analytics`  
**请求方法**: POST  
**功能描述**: 查询品牌分析报表数据  
**处理器**: BrandAnalyticsHandler  

### 15. 市场篮子分析报表

**接口路径**: `/api/amazon-table/market-basket`  
**请求方法**: POST  
**功能描述**: 查询市场篮子分析报表数据  
**处理器**: MarketBasketHandler  

### 16. 重复购买行为报表

**接口路径**: `/api/amazon-table/repeat-purchase`  
**请求方法**: POST  
**功能描述**: 查询重复购买行为报表数据  
**处理器**: RepeatPurchaseHandler  

### 17. 搜索词报表查询

**接口路径**: `/api/amazon-table/search-term`  
**请求方法**: POST  
**功能描述**: 查询搜索词报表数据  
**处理器**: SearchTermHandler  

### 18. 业务报表数据查询

**接口路径**: `/api/amazon-table/business-report`  
**请求方法**: POST  
**功能描述**: 查询业务报表数据  
**处理器**: BusinessReportHandler  

### 19. 税务报表数据查询

**接口路径**: `/api/amazon-table/tax-report`  
**请求方法**: POST  
**功能描述**: 查询税务报表数据  
**处理器**: TaxReportHandler  

### 20. 促销报表数据查询

**接口路径**: `/api/amazon-table/promotion-report`  
**请求方法**: POST  
**功能描述**: 查询促销活动报表数据  
**处理器**: PromotionReportHandler  

### 21. 数据同步状态查询

**接口路径**: `/api/amazon-table/sync-status`  
**请求方法**: POST  
**功能描述**: 查询数据同步状态  
**处理器**: SyncStatusHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| report_type | string | 否 | 报表类型 | "sales-report" |
| sync_date | string | 否 | 同步日期 | "2024-01-15" |
| status | string | 否 | 同步状态 | "completed" |

#### 请求示例

```json
{
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "report_type": "sales-report",
  "sync_date": "2024-01-15"
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
        "sync_id": "sync_20240115_001",
        "marketplace_id": "ATVPDKIKX0DER",
        "seller_id": "A1SELLER123",
        "report_type": "sales-report",
        "sync_date": "2024-01-15",
        "status": "completed",
        "start_time": "2024-01-15 02:00:00",
        "end_time": "2024-01-15 02:15:00",
        "records_processed": 2500,
        "records_success": 2485,
        "records_failed": 15,
        "error_message": null
      }
    ],
    "summary": {
      "total_syncs": 30,
      "success_rate": 95.5,
      "last_sync_time": "2024-01-15 02:15:00"
    }
  }
}
```

### 22. 数据导出功能

**接口路径**: `/api/amazon-table/export`  
**请求方法**: POST  
**功能描述**: 导出亚马逊源表数据  
**处理器**: DataExportHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| report_type | string | 是 | 报表类型 | "sales-report" |
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| seller_id | string | 是 | 卖家ID | "A1SELLER123" |
| start_date | string | 是 | 开始日期 | "2024-01-01" |
| end_date | string | 是 | 结束日期 | "2024-01-31" |
| export_format | string | 否 | 导出格式：csv/xlsx/json | "xlsx" |
| filters | object | 否 | 筛选条件 | {...} |
| email | string | 否 | 发送邮箱 | "user@example.com" |

#### 请求示例

```json
{
  "report_type": "sales-report",
  "marketplace_id": "ATVPDKIKX0DER",
  "seller_id": "A1SELLER123",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "export_format": "xlsx",
  "filters": {
    "asin": "B08N5WRWNW"
  },
  "email": "user@example.com"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "导出任务已创建",
  "data": {
    "export_id": "export_20240115_143000_001",
    "status": "processing",
    "estimated_records": 2500,
    "estimated_completion": "2024-01-15 14:35:00",
    "download_url": null,
    "email_notification": true
  }
}
```

## 通用参数说明

### 报表类型
- `sales-report`: 销售报表
- `inventory-report`: 库存报表
- `advertising-report`: 广告报表
- `financial-report`: 财务报表
- `order-report`: 订单报表
- `return-report`: 退货报表
- `fee-report`: 费用报表

### 同步状态
- `pending`: 等待中
- `processing`: 处理中
- `completed`: 已完成
- `failed`: 失败
- `cancelled`: 已取消

### 配送渠道
- `FBA`: 亚马逊配送
- `FBM`: 卖家自配送
- `Mixed`: 混合配送

### 广告类型
- `SP`: Sponsored Products (商品推广)
- `SB`: Sponsored Brands (品牌推广)
- `SD`: Sponsored Display (展示型推广)

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 参数验证失败 | 检查必填参数和参数格式 |
| 401 | 认证失败 | 检查access_token是否有效 |
| 403 | 权限不足 | 检查用户权限 |
| 404 | 数据不存在 | 检查查询条件是否正确 |
| 429 | 请求频率过高 | 降低请求频率 |
| 500 | 服务器内部错误 | 联系技术支持 |
| 503 | 服务暂时不可用 | 稍后重试 |

## 使用示例

### Python 示例

```python
import requests
import json
from datetime import datetime, timedelta

class AmazonTableAPI:
    def __init__(self, base_url="http://127.0.0.1:8888"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def get_sales_report(self, marketplace_id, seller_id, start_date, end_date, **kwargs):
        """查询销售报表数据"""
        url = f"{self.base_url}/api/amazon-table/sales-report"
        data = {
            "marketplace_id": marketplace_id,
            "seller_id": seller_id,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_inventory_report(self, marketplace_id, seller_id, report_date, **kwargs):
        """查询库存报表数据"""
        url = f"{self.base_url}/api/amazon-table/inventory-report"
        data = {
            "marketplace_id": marketplace_id,
            "seller_id": seller_id,
            "report_date": report_date,
            **kwargs
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_advertising_report(self, marketplace_id, seller_id, start_date, end_date, **kwargs):
        """查询广告报表数据"""
        url = f"{self.base_url}/api/amazon-table/advertising-report"
        data = {
            "marketplace_id": marketplace_id,
            "seller_id": seller_id,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_financial_report(self, marketplace_id, seller_id, start_date, end_date, **kwargs):
        """查询财务报表数据"""
        url = f"{self.base_url}/api/amazon-table/financial-report"
        data = {
            "marketplace_id": marketplace_id,
            "seller_id": seller_id,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_sync_status(self, marketplace_id, seller_id, **kwargs):
        """查询同步状态"""
        url = f"{self.base_url}/api/amazon-table/sync-status"
        data = {
            "marketplace_id": marketplace_id,
            "seller_id": seller_id,
            **kwargs
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def export_data(self, report_type, marketplace_id, seller_id, start_date, end_date, **kwargs):
        """导出数据"""
        url = f"{self.base_url}/api/amazon-table/export"
        data = {
            "report_type": report_type,
            "marketplace_id": marketplace_id,
            "seller_id": seller_id,
            "start_date": start_date,
            "end_date": end_date,
            **kwargs
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

# 使用示例
if __name__ == "__main__":
    api = AmazonTableAPI()
    
    marketplace_id = "ATVPDKIKX0DER"
    seller_id = "A1SELLER123"
    start_date = "2024-01-01"
    end_date = "2024-01-31"
    
    # 查询销售报表
    sales_data = api.get_sales_report(
        marketplace_id=marketplace_id,
        seller_id=seller_id,
        start_date=start_date,
        end_date=end_date,
        page=1,
        page_size=100
    )
    print("销售报表:", json.dumps(sales_data, indent=2, ensure_ascii=False))
    
    # 查询库存报表
    inventory_data = api.get_inventory_report(
        marketplace_id=marketplace_id,
        seller_id=seller_id,
        report_date="2024-01-15",
        fulfillment_channel="FBA"
    )
    print("库存报表:", json.dumps(inventory_data, indent=2, ensure_ascii=False))
    
    # 查询广告报表
    ad_data = api.get_advertising_report(
        marketplace_id=marketplace_id,
        seller_id=seller_id,
        start_date=start_date,
        end_date=end_date,
        campaign_type="SP"
    )
    print("广告报表:", json.dumps(ad_data, indent=2, ensure_ascii=False))
    
    # 查询同步状态
    sync_status = api.get_sync_status(
        marketplace_id=marketplace_id,
        seller_id=seller_id,
        report_type="sales-report"
    )
    print("同步状态:", json.dumps(sync_status, indent=2, ensure_ascii=False))
    
    # 导出数据
    export_result = api.export_data(
        report_type="sales-report",
        marketplace_id=marketplace_id,
        seller_id=seller_id,
        start_date=start_date,
        end_date=end_date,
        export_format="xlsx",
        email="user@example.com"
    )
    print("导出结果:", json.dumps(export_result, indent=2, ensure_ascii=False))
```

### cURL 示例

```bash
# 查询销售报表数据
curl -X POST "http://127.0.0.1:8888/api/amazon-table/sales-report" \
  -H "Content-Type: application/json" \
  -d '{
    "marketplace_id": "ATVPDKIKX0DER",
    "seller_id": "A1SELLER123",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "page": 1,
    "page_size": 100
  }'

# 查询库存报表数据
curl -X POST "http://127.0.0.1:8888/api/amazon-table/inventory-report" \
  -H "Content-Type: application/json" \
  -d '{
    "marketplace_id": "ATVPDKIKX0DER",
    "seller_id": "A1SELLER123",
    "report_date": "2024-01-15",
    "fulfillment_channel": "FBA"
  }'

# 查询广告报表数据
curl -X POST "http://127.0.0.1:8888/api/amazon-table/advertising-report" \
  -H "Content-Type: application/json" \
  -d '{
    "marketplace_id": "ATVPDKIKX0DER",
    "seller_id": "A1SELLER123",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "campaign_type": "SP"
  }'

# 导出数据
curl -X POST "http://127.0.0.1:8888/api/amazon-table/export" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "sales-report",
    "marketplace_id": "ATVPDKIKX0DER",
    "seller_id": "A1SELLER123",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "export_format": "xlsx"
  }'
```

## 数据字典

### 亚马逊市场ID
- `ATVPDKIKX0DER`: 美国
- `A1PA6795UKMFR9`: 德国
- `A1RKKUPIHCS9HS`: 西班牙
- `A13V1IB3VIYZZH`: 法国
- `APJ6JRA9NG5V4`: 意大利
- `A1F83G8C2ARO7P`: 英国
- `A21TJRUUN4KGV`: 印度
- `A1VC38T7YXB528`: 日本

### 订单状态
- `Pending`: 待处理
- `Unshipped`: 未发货
- `PartiallyShipped`: 部分发货
- `Shipped`: 已发货
- `Cancelled`: 已取消
- `Unfulfillable`: 无法履行

### 交易类型
- `Order`: 订单
- `Refund`: 退款
- `Adjustment`: 调整
- `FBAInventoryFee`: FBA库存费
- `Subscription`: 订阅费
- `Other`: 其他

## 性能优化建议

1. **索引优化**: 对日期、marketplace_id、seller_id等常用查询字段建立索引
2. **分区表**: 按日期对大表进行分区
3. **缓存策略**: 对不经常变化的数据使用缓存
4. **批量处理**: 大数据量操作使用批量处理
5. **异步导出**: 大数据量导出使用异步任务

## 注意事项

1. **数据隐私**: 严格保护卖家敏感数据
2. **API限流**: 注意亚马逊API的调用频率限制
3. **数据一致性**: 确保源数据的完整性和一致性
4. **错误处理**: 完善的错误处理和重试机制
5. **监控告警**: 建立数据同步监控和告警机制

## 更新日志

- **v1.0.0** (2025-01-13): 初始版本，包含22个亚马逊源表数据接口
- 支持销售、库存、广告、财务等各类报表数据查询
- 提供数据同步状态监控和数据导出功能
- 完善的参数验证和错误处理机制

---

> 📝 **相关文档**: [API总文档](./API_MASTER_DOCUMENTATION.md) | [统计模块文档](./statistics_api.md) | [基础数据模块文档](./base_data_api.md) | [产品模块文档](./product_api.md) | [多平台模块文档](./multi_platform_api.md)