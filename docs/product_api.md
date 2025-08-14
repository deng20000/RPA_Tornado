# 产品模块 API 文档

## 模块概述

**模块名称**: Product (产品模块)  
**功能描述**: 负责产品信息管理，包括产品详情查询、多属性产品管理、产品数据同步等  
**接口数量**: 8个  
**路由前缀**: `/api/product/`, `/api/basicOpen/product/`  

## 接口列表

### 1. 查询多属性产品详情

**接口路径**: `/api/product/multi-attribute-details`  
**请求方法**: POST  
**功能描述**: 查询具有多个属性的产品详细信息  
**处理器**: MultiAttributeProductDetailsHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| product_id | int | 否 | 产品ID | 12345 |
| asin | string | 否 | 产品ASIN | "B08N5WRWNW" |
| parent_asin | string | 否 | 父ASIN | "B08N5WRWNW" |
| sku | string | 否 | SKU编码 | "TEST-SKU-001" |
| msku | string | 否 | MSKU编码 | "TEST-MSKU-001" |
| marketplace_id | string | 否 | 市场ID | "ATVPDKIKX0DER" |
| include_variants | bool | 否 | 是否包含变体信息 | true |
| include_images | bool | 否 | 是否包含图片信息 | true |
| include_attributes | bool | 否 | 是否包含属性信息 | true |

#### 请求示例

```json
{
  "asin": "B08N5WRWNW",
  "marketplace_id": "ATVPDKIKX0DER",
  "include_variants": true,
  "include_images": true,
  "include_attributes": true
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "product_id": 12345,
    "asin": "B08N5WRWNW",
    "parent_asin": "B08N5WRWNW",
    "title": "无线蓝牙耳机 - 降噪版",
    "brand": "TestBrand",
    "category": "电子产品",
    "price": 99.99,
    "currency": "USD",
    "marketplace_id": "ATVPDKIKX0DER",
    "status": "Active",
    "created_time": "2024-01-01 10:00:00",
    "updated_time": "2024-01-15 14:30:00",
    "attributes": [
      {
        "attribute_name": "颜色",
        "attribute_value": "黑色",
        "attribute_type": "color"
      },
      {
        "attribute_name": "尺寸",
        "attribute_value": "标准版",
        "attribute_type": "size"
      }
    ],
    "variants": [
      {
        "variant_asin": "B08N5WRWN1",
        "sku": "TEST-SKU-001-BLACK",
        "color": "黑色",
        "size": "标准版",
        "price": 99.99,
        "inventory": 150
      },
      {
        "variant_asin": "B08N5WRWN2",
        "sku": "TEST-SKU-001-WHITE",
        "color": "白色",
        "size": "标准版",
        "price": 99.99,
        "inventory": 120
      }
    ],
    "images": [
      {
        "image_url": "https://example.com/image1.jpg",
        "image_type": "main",
        "sort_order": 1
      },
      {
        "image_url": "https://example.com/image2.jpg",
        "image_type": "variant",
        "sort_order": 2
      }
    ]
  }
}
```

### 2. 产品信息同步

**接口路径**: `/api/product/sync`  
**请求方法**: POST  
**功能描述**: 同步产品信息到外部系统或从外部系统同步  
**处理器**: ProductSyncHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| sync_type | string | 是 | 同步类型：import/export | "import" |
| source | string | 是 | 数据源：amazon/manual/api | "amazon" |
| product_ids | array | 否 | 产品ID列表 | [12345, 12346] |
| asins | array | 否 | ASIN列表 | ["B08N5WRWNW"] |
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| force_update | bool | 否 | 是否强制更新 | false |
| sync_images | bool | 否 | 是否同步图片 | true |
| sync_attributes | bool | 否 | 是否同步属性 | true |

#### 请求示例

```json
{
  "sync_type": "import",
  "source": "amazon",
  "asins": ["B08N5WRWNW", "B08N5WRWN1"],
  "marketplace_id": "ATVPDKIKX0DER",
  "force_update": false,
  "sync_images": true,
  "sync_attributes": true
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "同步任务已启动",
  "data": {
    "task_id": "sync_20240115_143000_001",
    "status": "processing",
    "total_count": 2,
    "processed_count": 0,
    "success_count": 0,
    "failed_count": 0,
    "start_time": "2024-01-15 14:30:00",
    "estimated_completion": "2024-01-15 14:35:00"
  }
}
```

### 3. 产品搜索

**接口路径**: `/api/product/search`  
**请求方法**: POST  
**功能描述**: 根据多种条件搜索产品信息  
**处理器**: ProductSearchHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| keyword | string | 否 | 关键词搜索 | "蓝牙耳机" |
| asin | string | 否 | ASIN精确匹配 | "B08N5WRWNW" |
| sku | string | 否 | SKU精确匹配 | "TEST-SKU-001" |
| brand | string | 否 | 品牌筛选 | "TestBrand" |
| category | string | 否 | 分类筛选 | "电子产品" |
| marketplace_id | string | 否 | 市场ID | "ATVPDKIKX0DER" |
| price_min | float | 否 | 最低价格 | 50.0 |
| price_max | float | 否 | 最高价格 | 200.0 |
| status | string | 否 | 状态筛选 | "Active" |
| sort_field | string | 否 | 排序字段 | "price" |
| sort_order | string | 否 | 排序方式：asc/desc | "desc" |
| page | int | 否 | 页码 | 1 |
| page_size | int | 否 | 每页数量 | 20 |

#### 请求示例

```json
{
  "keyword": "蓝牙耳机",
  "marketplace_id": "ATVPDKIKX0DER",
  "price_min": 50.0,
  "price_max": 200.0,
  "status": "Active",
  "sort_field": "price",
  "sort_order": "desc",
  "page": 1,
  "page_size": 20
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "搜索成功",
  "data": {
    "list": [
      {
        "product_id": 12345,
        "asin": "B08N5WRWNW",
        "title": "无线蓝牙耳机 - 降噪版",
        "brand": "TestBrand",
        "price": 99.99,
        "currency": "USD",
        "status": "Active",
        "image_url": "https://example.com/image1.jpg",
        "marketplace_id": "ATVPDKIKX0DER"
      }
    ],
    "total": 150,
    "page": 1,
    "page_size": 20,
    "total_pages": 8
  }
}
```

### 4. 产品批量操作

**接口路径**: `/api/product/batch-operation`  
**请求方法**: POST  
**功能描述**: 对多个产品执行批量操作  
**处理器**: ProductBatchOperationHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| operation | string | 是 | 操作类型：update/delete/activate/deactivate | "update" |
| product_ids | array | 是 | 产品ID列表 | [12345, 12346] |
| update_data | object | 否 | 更新数据（operation=update时必填） | {...} |
| reason | string | 否 | 操作原因 | "批量更新价格" |

#### 请求示例

```json
{
  "operation": "update",
  "product_ids": [12345, 12346, 12347],
  "update_data": {
    "price": 89.99,
    "status": "Active"
  },
  "reason": "促销活动价格调整"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "批量操作已完成",
  "data": {
    "operation_id": "batch_20240115_143000_001",
    "total_count": 3,
    "success_count": 2,
    "failed_count": 1,
    "results": [
      {
        "product_id": 12345,
        "status": "success",
        "message": "更新成功"
      },
      {
        "product_id": 12346,
        "status": "success",
        "message": "更新成功"
      },
      {
        "product_id": 12347,
        "status": "failed",
        "message": "产品不存在"
      }
    ]
  }
}
```

### 5. 产品库存查询

**接口路径**: `/api/product/inventory`  
**请求方法**: POST  
**功能描述**: 查询产品库存信息  
**处理器**: ProductInventoryHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| product_ids | array | 否 | 产品ID列表 | [12345] |
| asins | array | 否 | ASIN列表 | ["B08N5WRWNW"] |
| skus | array | 否 | SKU列表 | ["TEST-SKU-001"] |
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| warehouse_id | string | 否 | 仓库ID | "FBA_US_EAST" |
| low_stock_threshold | int | 否 | 低库存阈值 | 10 |

#### 请求示例

```json
{
  "asins": ["B08N5WRWNW", "B08N5WRWN1"],
  "marketplace_id": "ATVPDKIKX0DER",
  "warehouse_id": "FBA_US_EAST",
  "low_stock_threshold": 10
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
        "product_id": 12345,
        "asin": "B08N5WRWNW",
        "sku": "TEST-SKU-001",
        "marketplace_id": "ATVPDKIKX0DER",
        "warehouse_id": "FBA_US_EAST",
        "available_quantity": 150,
        "reserved_quantity": 25,
        "total_quantity": 175,
        "low_stock_alert": false,
        "last_updated": "2024-01-15 14:00:00"
      },
      {
        "product_id": 12346,
        "asin": "B08N5WRWN1",
        "sku": "TEST-SKU-002",
        "marketplace_id": "ATVPDKIKX0DER",
        "warehouse_id": "FBA_US_EAST",
        "available_quantity": 8,
        "reserved_quantity": 2,
        "total_quantity": 10,
        "low_stock_alert": true,
        "last_updated": "2024-01-15 14:00:00"
      }
    ],
    "summary": {
      "total_products": 2,
      "low_stock_count": 1,
      "out_of_stock_count": 0
    }
  }
}
```

### 6. 产品价格历史

**接口路径**: `/api/product/price-history`  
**请求方法**: POST  
**功能描述**: 查询产品价格变化历史  
**处理器**: ProductPriceHistoryHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| product_id | int | 否 | 产品ID | 12345 |
| asin | string | 否 | ASIN | "B08N5WRWNW" |
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| start_date | string | 否 | 开始日期 | "2024-01-01" |
| end_date | string | 否 | 结束日期 | "2024-01-31" |
| price_type | string | 否 | 价格类型：list/sale/cost | "list" |

#### 请求示例

```json
{
  "asin": "B08N5WRWNW",
  "marketplace_id": "ATVPDKIKX0DER",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "price_type": "list"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "查询成功",
  "data": {
    "product_info": {
      "product_id": 12345,
      "asin": "B08N5WRWNW",
      "title": "无线蓝牙耳机 - 降噪版",
      "current_price": 99.99
    },
    "price_history": [
      {
        "date": "2024-01-01",
        "price": 109.99,
        "price_type": "list",
        "change_reason": "初始价格"
      },
      {
        "date": "2024-01-15",
        "price": 99.99,
        "price_type": "list",
        "change_reason": "促销活动"
      }
    ],
    "statistics": {
      "min_price": 99.99,
      "max_price": 109.99,
      "avg_price": 104.99,
      "price_changes": 1
    }
  }
}
```

### 7. 产品评论分析

**接口路径**: `/api/product/review-analysis`  
**请求方法**: POST  
**功能描述**: 分析产品评论数据  
**处理器**: ProductReviewAnalysisHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| asin | string | 是 | ASIN | "B08N5WRWNW" |
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| start_date | string | 否 | 开始日期 | "2024-01-01" |
| end_date | string | 否 | 结束日期 | "2024-01-31" |
| rating_filter | int | 否 | 评分筛选：1-5星 | 5 |
| include_content | bool | 否 | 是否包含评论内容 | true |

#### 请求示例

```json
{
  "asin": "B08N5WRWNW",
  "marketplace_id": "ATVPDKIKX0DER",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "include_content": true
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "分析完成",
  "data": {
    "product_info": {
      "asin": "B08N5WRWNW",
      "title": "无线蓝牙耳机 - 降噪版"
    },
    "review_summary": {
      "total_reviews": 1250,
      "average_rating": 4.3,
      "rating_distribution": {
        "5_star": 650,
        "4_star": 350,
        "3_star": 150,
        "2_star": 75,
        "1_star": 25
      }
    },
    "sentiment_analysis": {
      "positive": 75.2,
      "neutral": 18.5,
      "negative": 6.3
    },
    "keyword_analysis": [
      {
        "keyword": "音质",
        "frequency": 320,
        "sentiment": "positive"
      },
      {
        "keyword": "电池",
        "frequency": 180,
        "sentiment": "positive"
      },
      {
        "keyword": "连接",
        "frequency": 95,
        "sentiment": "negative"
      }
    ]
  }
}
```

### 8. 产品竞争分析

**接口路径**: `/api/basicOpen/product/competitive-analysis`  
**请求方法**: POST  
**功能描述**: 分析产品竞争情况  
**处理器**: ProductCompetitiveAnalysisHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| asin | string | 是 | 目标产品ASIN | "B08N5WRWNW" |
| marketplace_id | string | 是 | 市场ID | "ATVPDKIKX0DER" |
| category | string | 否 | 分类限制 | "电子产品" |
| price_range | object | 否 | 价格范围 | {"min": 50, "max": 200} |
| competitor_count | int | 否 | 竞争对手数量限制 | 10 |

#### 请求示例

```json
{
  "asin": "B08N5WRWNW",
  "marketplace_id": "ATVPDKIKX0DER",
  "category": "电子产品",
  "price_range": {
    "min": 50,
    "max": 200
  },
  "competitor_count": 10
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "分析完成",
  "data": {
    "target_product": {
      "asin": "B08N5WRWNW",
      "title": "无线蓝牙耳机 - 降噪版",
      "price": 99.99,
      "rating": 4.3,
      "review_count": 1250
    },
    "competitors": [
      {
        "asin": "B08COMPETITOR1",
        "title": "竞品蓝牙耳机A",
        "price": 89.99,
        "rating": 4.1,
        "review_count": 980,
        "similarity_score": 0.85
      },
      {
        "asin": "B08COMPETITOR2",
        "title": "竞品蓝牙耳机B",
        "price": 119.99,
        "rating": 4.5,
        "review_count": 1580,
        "similarity_score": 0.78
      }
    ],
    "market_analysis": {
      "price_position": "middle",
      "rating_position": "above_average",
      "market_share_estimate": 12.5,
      "competitive_advantage": ["价格优势", "评论数量"],
      "improvement_suggestions": ["提升评分", "增加功能"]
    }
  }
}
```

## 通用参数说明

### 产品状态
- `Active`: 正常销售
- `Inactive`: 暂停销售
- `Discontinued`: 已停产
- `Draft`: 草稿状态

### 同步类型
- `import`: 从外部导入
- `export`: 导出到外部
- `sync`: 双向同步

### 价格类型
- `list`: 标价
- `sale`: 促销价
- `cost`: 成本价
- `wholesale`: 批发价

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 参数验证失败 | 检查必填参数和参数格式 |
| 401 | 认证失败 | 检查access_token是否有效 |
| 403 | 权限不足 | 检查用户权限 |
| 404 | 产品不存在 | 检查产品ID或ASIN是否正确 |
| 409 | 数据冲突 | 检查是否存在重复数据 |
| 429 | 请求频率过高 | 降低请求频率 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 使用示例

### Python 示例

```python
import requests
import json
from datetime import datetime, timedelta

class ProductAPI:
    def __init__(self, base_url="http://127.0.0.1:8888"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def get_product_details(self, asin, marketplace_id="ATVPDKIKX0DER"):
        """查询产品详情"""
        url = f"{self.base_url}/api/product/multi-attribute-details"
        data = {
            "asin": asin,
            "marketplace_id": marketplace_id,
            "include_variants": True,
            "include_images": True,
            "include_attributes": True
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def search_products(self, keyword, marketplace_id="ATVPDKIKX0DER", page=1, page_size=20):
        """搜索产品"""
        url = f"{self.base_url}/api/product/search"
        data = {
            "keyword": keyword,
            "marketplace_id": marketplace_id,
            "status": "Active",
            "page": page,
            "page_size": page_size
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def sync_products(self, asins, marketplace_id="ATVPDKIKX0DER"):
        """同步产品信息"""
        url = f"{self.base_url}/api/product/sync"
        data = {
            "sync_type": "import",
            "source": "amazon",
            "asins": asins,
            "marketplace_id": marketplace_id,
            "sync_images": True,
            "sync_attributes": True
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_inventory(self, asins, marketplace_id="ATVPDKIKX0DER"):
        """查询库存信息"""
        url = f"{self.base_url}/api/product/inventory"
        data = {
            "asins": asins,
            "marketplace_id": marketplace_id,
            "low_stock_threshold": 10
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_price_history(self, asin, marketplace_id="ATVPDKIKX0DER", days=30):
        """查询价格历史"""
        url = f"{self.base_url}/api/product/price-history"
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        data = {
            "asin": asin,
            "marketplace_id": marketplace_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "price_type": "list"
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def batch_update_products(self, product_ids, update_data, reason=""):
        """批量更新产品"""
        url = f"{self.base_url}/api/product/batch-operation"
        data = {
            "operation": "update",
            "product_ids": product_ids,
            "update_data": update_data,
            "reason": reason
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

# 使用示例
if __name__ == "__main__":
    api = ProductAPI()
    
    # 查询产品详情
    product = api.get_product_details("B08N5WRWNW")
    print("产品详情:", json.dumps(product, indent=2, ensure_ascii=False))
    
    # 搜索产品
    search_results = api.search_products("蓝牙耳机")
    print("搜索结果:", json.dumps(search_results, indent=2, ensure_ascii=False))
    
    # 查询库存
    inventory = api.get_inventory(["B08N5WRWNW"])
    print("库存信息:", json.dumps(inventory, indent=2, ensure_ascii=False))
    
    # 查询价格历史
    price_history = api.get_price_history("B08N5WRWNW", days=30)
    print("价格历史:", json.dumps(price_history, indent=2, ensure_ascii=False))
```

### JavaScript 示例

```javascript
class ProductAPI {
  constructor(baseUrl = 'http://127.0.0.1:8888') {
    this.baseUrl = baseUrl;
    this.headers = {
      'Content-Type': 'application/json'
    };
  }
  
  async getProductDetails(asin, marketplaceId = 'ATVPDKIKX0DER') {
    const url = `${this.baseUrl}/api/product/multi-attribute-details`;
    const data = {
      asin: asin,
      marketplace_id: marketplaceId,
      include_variants: true,
      include_images: true,
      include_attributes: true
    };
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(data)
      });
      return await response.json();
    } catch (error) {
      console.error('获取产品详情失败:', error);
      throw error;
    }
  }
  
  async searchProducts(keyword, options = {}) {
    const url = `${this.baseUrl}/api/product/search`;
    const data = {
      keyword: keyword,
      marketplace_id: options.marketplaceId || 'ATVPDKIKX0DER',
      status: 'Active',
      page: options.page || 1,
      page_size: options.pageSize || 20,
      ...options
    };
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(data)
      });
      return await response.json();
    } catch (error) {
      console.error('搜索产品失败:', error);
      throw error;
    }
  }
  
  async getInventory(asins, marketplaceId = 'ATVPDKIKX0DER') {
    const url = `${this.baseUrl}/api/product/inventory`;
    const data = {
      asins: asins,
      marketplace_id: marketplaceId,
      low_stock_threshold: 10
    };
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: this.headers,
        body: JSON.stringify(data)
      });
      return await response.json();
    } catch (error) {
      console.error('获取库存信息失败:', error);
      throw error;
    }
  }
}

// 使用示例
async function example() {
  const api = new ProductAPI();
  
  try {
    // 查询产品详情
    const product = await api.getProductDetails('B08N5WRWNW');
    console.log('产品详情:', product);
    
    // 搜索产品
    const searchResults = await api.searchProducts('蓝牙耳机', {
      price_min: 50,
      price_max: 200
    });
    console.log('搜索结果:', searchResults);
    
    // 查询库存
    const inventory = await api.getInventory(['B08N5WRWNW']);
    console.log('库存信息:', inventory);
    
  } catch (error) {
    console.error('API调用失败:', error);
  }
}
```

## 性能优化建议

1. **缓存策略**: 对产品基础信息使用缓存，减少数据库查询
2. **分页查询**: 大数据量搜索时使用分页
3. **异步处理**: 同步操作使用异步任务处理
4. **索引优化**: 对ASIN、SKU等常用查询字段建立索引
5. **图片优化**: 使用CDN加速图片加载

## 注意事项

1. **数据一致性**: 产品信息修改需要同步到相关系统
2. **权限控制**: 不同用户对产品的操作权限不同
3. **数据验证**: 严格验证产品数据的完整性和合法性
4. **API限流**: 注意外部API的调用频率限制
5. **错误处理**: 完善的错误处理和重试机制

## 更新日志

- **v1.0.0** (2025-01-13): 初始版本，包含8个产品管理接口
- 支持产品详情查询、搜索、同步、批量操作等功能
- 提供库存管理、价格历史、评论分析、竞争分析等高级功能
- 完善的参数验证和错误处理机制

---

> 📝 **相关文档**: [API总文档](./API_MASTER_DOCUMENTATION.md) | [统计模块文档](./statistics_api.md) | [基础数据模块文档](./base_data_api.md) | [多平台模块文档](./multi_platform_api.md)