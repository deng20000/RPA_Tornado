# RPA Tornado API 文档中心

欢迎使用 RPA Tornado 项目的 API 文档中心。本目录包含了完整的 API 接口文档，帮助开发者快速了解和使用系统提供的各种功能。

## 📚 文档结构

### 🏠 总览文档
- **[API 总文档](./API_MASTER_DOCUMENTATION.md)** - 系统概览、快速开始、认证机制等

### 📋 模块详细文档

#### 🌐 [多平台模块](./multi_platform_api.md)
- **接口数量**: 12个
- **主要功能**: 多平台数据同步、销量统计、利润分析、店铺管理
- **核心接口**: 销量统计、店铺信息、结算利润等

#### 📊 [统计模块](./statistics_api.md)
- **接口数量**: 7个
- **主要功能**: 数据统计分析、销量报表、订单利润、产品表现
- **核心接口**: ASIN日列表、订单利润MSKU、产品表现等

#### 🗃️ [基础数据模块](./base_data_api.md)
- **接口数量**: 5个
- **主要功能**: 系统基础数据管理、卖家信息、市场列表、汇率信息
- **核心接口**: 卖家信息、市场列表、分类数据、汇率查询、系统设置

#### 📦 [产品模块](./product_api.md)
- **接口数量**: 8个
- **主要功能**: 产品信息管理、搜索、同步、库存管理
- **核心接口**: 产品详情、搜索、同步、批量操作、库存查询等

#### 📈 [亚马逊源表数据模块](./amazon_table_api.md)
- **接口数量**: 22个
- **主要功能**: 亚马逊原始数据管理、各类报表查询、数据导出
- **核心接口**: 销售报表、库存报表、广告报表、财务报表等

## 🚀 快速开始

### 1. 环境准备
```bash
# 启动服务
cd RPA_Tornado
python main.py --environment=development
```

### 2. 健康检查
```bash
# 检查服务状态
curl http://127.0.0.1:8888/health
```

### 3. 接口测试
```python
import requests

# 测试多平台销量统计接口
url = "http://127.0.0.1:8888/api/basicOpen/platformStatisticsV2/saleStat/pageList"
data = {
    "offset": 0,
    "length": 20,
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "result_type": "summary",
    "date_unit": "day"
}

response = requests.post(url, json=data)
print(response.json())
```

## 📖 使用指南

### 认证机制
大部分接口需要有效的 access_token，请在请求头中包含：
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 通用响应格式
```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    // 具体数据内容
  }
}
```

### 错误处理
- `code: 0` - 成功
- `code: 400` - 参数错误
- `code: 401` - 认证失败
- `code: 403` - 权限不足
- `code: 500` - 服务器错误

## 🛠️ 开发工具

### Python SDK 示例
```python
class RPAAPI:
    def __init__(self, base_url="http://127.0.0.1:8888"):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
    
    def post(self, endpoint, data):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

# 使用示例
api = RPAAPI()
result = api.post("/api/basicOpen/platformStatisticsV2/saleStat/pageList", {
    "offset": 0,
    "length": 20,
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "result_type": "summary",
    "date_unit": "day"
})
```

### JavaScript SDK 示例
```javascript
class RPAAPI {
  constructor(baseUrl = 'http://127.0.0.1:8888') {
    this.baseUrl = baseUrl;
  }
  
  async post(endpoint, data) {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    return await response.json();
  }
}

// 使用示例
const api = new RPAAPI();
const result = await api.post('/api/basicOpen/platformStatisticsV2/saleStat/pageList', {
  offset: 0,
  length: 20,
  start_date: '2024-01-01',
  end_date: '2024-01-31',
  result_type: 'summary',
  date_unit: 'day'
});
```

## 📊 接口统计

| 模块 | 接口数量 | 完成度 | 测试状态 |
|------|----------|--------|----------|
| 多平台模块 | 12 | ✅ 100% | ✅ 已测试 |
| 统计模块 | 7 | ✅ 100% | ✅ 已测试 |
| 基础数据模块 | 5 | ✅ 100% | ⚠️ 部分测试 |
| 产品模块 | 8 | ✅ 100% | ⚠️ 部分测试 |
| 亚马逊源表数据模块 | 22 | ✅ 100% | ⚠️ 部分测试 |
| **总计** | **54** | **100%** | **大部分完成** |

## 🔧 常见问题

### Q: 接口返回 405 错误怎么办？
A: 检查请求方法是否正确，大部分接口支持 POST 请求。

### Q: 参数验证失败怎么办？
A: 检查必填参数是否提供，参数格式是否正确，特别注意日期格式和数据类型。

### Q: 如何获取 access_token？
A: 请联系系统管理员获取有效的访问令牌。

### Q: 接口响应慢怎么办？
A: 建议使用分页查询，控制查询的日期范围，避免一次性查询过多数据。

## 📞 技术支持

- **项目地址**: RPA_Tornado
- **文档更新**: 2025-08-13
- **API 版本**: v1.0.0
- **服务地址**: http://127.0.0.1:8888

## 📝 更新日志

### v1.0.0 (2025-08-13)
- ✅ 完成所有模块 API 文档编写
- ✅ 提供完整的接口测试示例
- ✅ 建立统一的文档结构
- ✅ 添加开发工具和 SDK 示例
- ✅ 完善错误处理和常见问题解答

---

> 💡 **提示**: 建议从 [API 总文档](./API_MASTER_DOCUMENTATION.md) 开始阅读，然后根据需要查看具体模块的详细文档。