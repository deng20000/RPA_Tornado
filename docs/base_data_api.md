# 基础数据模块 API 文档

## 模块概述

**模块名称**: Base Data (基础数据模块)  
**功能描述**: 提供系统基础数据管理，包括卖家信息、市场列表、分类数据、汇率信息、系统设置等  
**接口数量**: 5个  
**路由前缀**: `/api/base-data/`  

## 接口列表

### 1. 卖家信息查询

**接口路径**: `/api/base-data/seller-info`  
**请求方法**: GET, POST  
**功能描述**: 查询卖家基础信息  
**处理器**: SellerInfoHandler  

#### 请求参数 (GET)

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| seller_id | int | 否 | 卖家ID | 123 |
| status | int | 否 | 状态筛选，1=启用，0=禁用 | 1 |

#### 请求参数 (POST)

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| seller_id | int | 否 | 卖家ID | 123 |
| seller_name | string | 否 | 卖家名称 | "测试卖家" |
| email | string | 否 | 邮箱地址 | "test@example.com" |
| status | int | 否 | 状态筛选 | 1 |
| page | int | 否 | 页码，默认1 | 1 |
| page_size | int | 否 | 每页数量，默认20 | 20 |

#### GET 请求示例

```bash
GET /api/base-data/seller-info?seller_id=123&status=1
```

#### POST 请求示例

```json
{
  "seller_id": 123,
  "seller_name": "测试卖家",
  "status": 1,
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
        "seller_id": 123,
        "seller_name": "测试卖家",
        "email": "test@example.com",
        "phone": "+86-13800138000",
        "company_name": "测试公司",
        "status": 1,
        "created_time": "2024-01-01 10:00:00",
        "updated_time": "2024-01-10 15:30:00"
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20
  }
}
```

### 2. 市场列表查询

**接口路径**: `/api/base-data/marketplace-list`  
**请求方法**: GET, POST  
**功能描述**: 查询亚马逊市场列表信息  
**处理器**: MarketplaceListHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| marketplace_id | string | 否 | 市场ID | "ATVPDKIKX0DER" |
| country_code | string | 否 | 国家代码 | "US" |
| currency_code | string | 否 | 货币代码 | "USD" |
| status | int | 否 | 状态，1=启用，0=禁用 | 1 |

#### 请求示例

```json
{
  "country_code": "US",
  "status": 1
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
        "marketplace_id": "ATVPDKIKX0DER",
        "marketplace_name": "Amazon.com",
        "country_code": "US",
        "country_name": "美国",
        "currency_code": "USD",
        "domain": "amazon.com",
        "status": 1,
        "timezone": "America/New_York"
      },
      {
        "marketplace_id": "A1PA6795UKMFR9",
        "marketplace_name": "Amazon.de",
        "country_code": "DE",
        "country_name": "德国",
        "currency_code": "EUR",
        "domain": "amazon.de",
        "status": 1,
        "timezone": "Europe/Berlin"
      }
    ],
    "total": 15
  }
}
```

### 3. 分类列表查询

**接口路径**: `/api/base-data/category-list`  
**请求方法**: GET, POST  
**功能描述**: 查询产品分类列表信息  
**处理器**: CategoryListHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| category_id | int | 否 | 分类ID | 1001 |
| parent_id | int | 否 | 父分类ID，0表示顶级分类 | 0 |
| marketplace_id | string | 否 | 市场ID | "ATVPDKIKX0DER" |
| level | int | 否 | 分类层级，1-5 | 1 |
| keyword | string | 否 | 分类名称关键词 | "电子" |
| status | int | 否 | 状态，1=启用，0=禁用 | 1 |

#### 请求示例

```json
{
  "parent_id": 0,
  "marketplace_id": "ATVPDKIKX0DER",
  "level": 1,
  "status": 1
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
        "category_id": 1001,
        "category_name": "电子产品",
        "category_name_en": "Electronics",
        "parent_id": 0,
        "level": 1,
        "marketplace_id": "ATVPDKIKX0DER",
        "browse_node_id": "172282",
        "path": "电子产品",
        "status": 1,
        "sort_order": 1,
        "has_children": true
      },
      {
        "category_id": 1002,
        "category_name": "家居用品",
        "category_name_en": "Home & Kitchen",
        "parent_id": 0,
        "level": 1,
        "marketplace_id": "ATVPDKIKX0DER",
        "browse_node_id": "284507",
        "path": "家居用品",
        "status": 1,
        "sort_order": 2,
        "has_children": true
      }
    ],
    "total": 25
  }
}
```

### 4. 汇率信息查询

**接口路径**: `/api/base-data/currency-rate`  
**请求方法**: GET, POST  
**功能描述**: 查询货币汇率信息  
**处理器**: CurrencyRateHandler  

#### 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| from_currency | string | 否 | 源货币代码 | "USD" |
| to_currency | string | 否 | 目标货币代码 | "CNY" |
| date | string | 否 | 查询日期，格式YYYY-MM-DD | "2024-01-15" |
| latest | bool | 否 | 是否获取最新汇率 | true |

#### 请求示例

```json
{
  "from_currency": "USD",
  "to_currency": "CNY",
  "latest": true
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
        "from_currency": "USD",
        "to_currency": "CNY",
        "exchange_rate": 7.2345,
        "rate_date": "2024-01-15",
        "source": "央行",
        "updated_time": "2024-01-15 09:30:00"
      },
      {
        "from_currency": "EUR",
        "to_currency": "CNY",
        "exchange_rate": 7.8901,
        "rate_date": "2024-01-15",
        "source": "央行",
        "updated_time": "2024-01-15 09:30:00"
      }
    ],
    "total": 10
  }
}
```

### 5. 系统设置管理

**接口路径**: `/api/base-data/settings`  
**请求方法**: GET, POST, PUT  
**功能描述**: 系统设置的查询、创建和更新  
**处理器**: SettingsHandler  

#### GET 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| setting_key | string | 否 | 设置键名 | "system.timezone" |
| category | string | 否 | 设置分类 | "system" |

#### POST/PUT 请求参数

| 参数名 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| setting_key | string | 是 | 设置键名 | "system.timezone" |
| setting_value | string | 是 | 设置值 | "Asia/Shanghai" |
| category | string | 否 | 设置分类 | "system" |
| description | string | 否 | 设置描述 | "系统时区设置" |
| is_public | bool | 否 | 是否公开，默认false | false |

#### GET 请求示例

```bash
GET /api/base-data/settings?category=system
```

#### POST 请求示例

```json
{
  "setting_key": "system.timezone",
  "setting_value": "Asia/Shanghai",
  "category": "system",
  "description": "系统时区设置",
  "is_public": false
}
```

#### PUT 请求示例

```json
{
  "setting_key": "system.timezone",
  "setting_value": "America/New_York",
  "description": "更新系统时区为纽约时间"
}
```

#### 响应示例

```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "list": [
      {
        "setting_id": 1,
        "setting_key": "system.timezone",
        "setting_value": "Asia/Shanghai",
        "category": "system",
        "description": "系统时区设置",
        "is_public": false,
        "created_time": "2024-01-01 10:00:00",
        "updated_time": "2024-01-15 14:30:00"
      },
      {
        "setting_id": 2,
        "setting_key": "system.language",
        "setting_value": "zh-CN",
        "category": "system",
        "description": "系统默认语言",
        "is_public": true,
        "created_time": "2024-01-01 10:00:00",
        "updated_time": "2024-01-01 10:00:00"
      }
    ],
    "total": 15
  }
}
```

## 通用参数说明

### 状态码
- `1`: 启用/正常
- `0`: 禁用/停用
- `-1`: 删除

### 分页参数
- `page`: 页码，从1开始
- `page_size`: 每页数量，默认20，最大100

### 日期格式
- 统一使用 `YYYY-MM-DD` 格式
- 时间格式：`YYYY-MM-DD HH:mm:ss`

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 参数验证失败 | 检查必填参数和参数格式 |
| 401 | 认证失败 | 检查access_token是否有效 |
| 403 | 权限不足 | 检查用户权限 |
| 404 | 资源不存在 | 检查请求的资源ID是否正确 |
| 409 | 数据冲突 | 检查是否存在重复数据 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 使用示例

### Python 示例

```python
import requests
import json

class BaseDataAPI:
    def __init__(self, base_url="http://127.0.0.1:8888"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def get_seller_info(self, seller_id=None, status=1):
        """查询卖家信息"""
        url = f"{self.base_url}/api/base-data/seller-info"
        params = {}
        if seller_id:
            params['seller_id'] = seller_id
        if status is not None:
            params['status'] = status
        
        response = requests.get(url, params=params)
        return response.json()
    
    def get_marketplace_list(self, country_code=None):
        """查询市场列表"""
        url = f"{self.base_url}/api/base-data/marketplace-list"
        data = {}
        if country_code:
            data['country_code'] = country_code
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_category_list(self, parent_id=0, marketplace_id=None):
        """查询分类列表"""
        url = f"{self.base_url}/api/base-data/category-list"
        data = {
            'parent_id': parent_id,
            'status': 1
        }
        if marketplace_id:
            data['marketplace_id'] = marketplace_id
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_currency_rate(self, from_currency, to_currency):
        """查询汇率信息"""
        url = f"{self.base_url}/api/base-data/currency-rate"
        data = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'latest': True
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()
    
    def get_settings(self, category=None):
        """查询系统设置"""
        url = f"{self.base_url}/api/base-data/settings"
        params = {}
        if category:
            params['category'] = category
        
        response = requests.get(url, params=params)
        return response.json()
    
    def update_setting(self, setting_key, setting_value, description=None):
        """更新系统设置"""
        url = f"{self.base_url}/api/base-data/settings"
        data = {
            'setting_key': setting_key,
            'setting_value': setting_value
        }
        if description:
            data['description'] = description
        
        response = requests.put(url, json=data, headers=self.headers)
        return response.json()

# 使用示例
if __name__ == "__main__":
    api = BaseDataAPI()
    
    # 查询卖家信息
    sellers = api.get_seller_info(status=1)
    print("卖家信息:", json.dumps(sellers, indent=2, ensure_ascii=False))
    
    # 查询美国市场信息
    us_marketplace = api.get_marketplace_list(country_code="US")
    print("美国市场:", json.dumps(us_marketplace, indent=2, ensure_ascii=False))
    
    # 查询顶级分类
    categories = api.get_category_list(parent_id=0)
    print("顶级分类:", json.dumps(categories, indent=2, ensure_ascii=False))
    
    # 查询USD到CNY汇率
    rate = api.get_currency_rate("USD", "CNY")
    print("汇率信息:", json.dumps(rate, indent=2, ensure_ascii=False))
    
    # 查询系统设置
    settings = api.get_settings(category="system")
    print("系统设置:", json.dumps(settings, indent=2, ensure_ascii=False))
```

### cURL 示例

```bash
# 查询卖家信息 (GET)
curl -X GET "http://127.0.0.1:8888/api/base-data/seller-info?status=1"

# 查询市场列表 (POST)
curl -X POST "http://127.0.0.1:8888/api/base-data/marketplace-list" \
  -H "Content-Type: application/json" \
  -d '{
    "country_code": "US",
    "status": 1
  }'

# 查询分类列表
curl -X POST "http://127.0.0.1:8888/api/base-data/category-list" \
  -H "Content-Type: application/json" \
  -d '{
    "parent_id": 0,
    "marketplace_id": "ATVPDKIKX0DER",
    "status": 1
  }'

# 查询汇率信息
curl -X POST "http://127.0.0.1:8888/api/base-data/currency-rate" \
  -H "Content-Type: application/json" \
  -d '{
    "from_currency": "USD",
    "to_currency": "CNY",
    "latest": true
  }'

# 查询系统设置
curl -X GET "http://127.0.0.1:8888/api/base-data/settings?category=system"

# 更新系统设置
curl -X PUT "http://127.0.0.1:8888/api/base-data/settings" \
  -H "Content-Type: application/json" \
  -d '{
    "setting_key": "system.timezone",
    "setting_value": "Asia/Shanghai",
    "description": "更新系统时区"
  }'
```

## 数据字典

### 卖家状态
- `1`: 正常
- `0`: 禁用
- `-1`: 删除

### 市场代码
- `ATVPDKIKX0DER`: 美国 (amazon.com)
- `A1PA6795UKMFR9`: 德国 (amazon.de)
- `A1RKKUPIHCS9HS`: 西班牙 (amazon.es)
- `A13V1IB3VIYZZH`: 法国 (amazon.fr)
- `APJ6JRA9NG5V4`: 意大利 (amazon.it)
- `A1F83G8C2ARO7P`: 英国 (amazon.co.uk)
- `A21TJRUUN4KGV`: 印度 (amazon.in)
- `AAHKV2X7AFYLW`: 墨西哥 (amazon.com.mx)
- `A2Q3Y263D00KWC`: 巴西 (amazon.com.br)
- `A39IBJ37TRP1C6`: 澳大利亚 (amazon.com.au)
- `A1VC38T7YXB528`: 日本 (amazon.co.jp)

### 货币代码
- `USD`: 美元
- `EUR`: 欧元
- `GBP`: 英镑
- `JPY`: 日元
- `CNY`: 人民币
- `CAD`: 加拿大元
- `AUD`: 澳大利亚元

## 性能优化建议

1. **缓存策略**: 基础数据变化频率低，建议使用缓存
2. **分页查询**: 大数据量时使用分页
3. **索引优化**: 对常用查询字段建立索引
4. **数据预加载**: 系统启动时预加载常用基础数据

## 注意事项

1. **数据一致性**: 基础数据修改需要考虑对其他模块的影响
2. **权限控制**: 系统设置修改需要管理员权限
3. **数据验证**: 严格验证输入参数的合法性
4. **缓存更新**: 数据修改后及时更新相关缓存
5. **日志记录**: 重要操作需要记录操作日志

## 更新日志

- **v1.0.0** (2025-01-13): 初始版本，包含5个基础数据接口
- 支持卖家信息、市场列表、分类数据、汇率信息、系统设置管理
- 提供GET、POST、PUT多种请求方式
- 完善的参数验证和错误处理机制

---

> 📝 **相关文档**: [API总文档](./API_MASTER_DOCUMENTATION.md) | [统计模块文档](./statistics_api.md) | [多平台模块文档](./multi_platform_api.md)