# 领星API项目

## 项目概述

该项目是基于领星(Lingxing) OpenAPI的Python SDK封装，用于自动化处理电商数据，包括订单管理、库存管理、商品管理等功能。项目采用异步编程模式，提供高效的API调用和数据处理能力。

## 功能特性

- 🔐 **OAuth认证**：支持访问令牌获取和刷新
- 📦 **订单管理**：查询、创建、更新订单信息
- 🏪 **商品管理**：商品分类、库存管理
- 🔄 **异步处理**：基于asyncio的高性能异步API调用
- 🛡️ **安全加密**：支持AES加密和数字签名
- 📊 **数据处理**：自动化数据同步和处理
- 🧪 **单元测试**：完整的测试覆盖

## 项目结构

```
Lingxing_apiProject/
├── main.py                    # 项目入口文件
├── Lingxing_Auth/             # 核心API模块
│   ├── __init__.py           # 模块初始化
│   ├── openapi.py            # OpenAPI基础类
│   ├── demo.py               # 使用示例
│   ├── http_util.py          # HTTP请求工具
│   ├── resp_schema.py        # 响应数据模型
│   ├── sign.py               # 数字签名工具
│   ├── aes.py                # AES加密工具
│   ├── shopfiy_look.py       # Shopify集成模块
│   ├── requirements.txt      # 依赖库列表
│   ├── README.md             # 模块说明文档
│   ├── CHANGELOG.md          # 版本更新日志
│   └── tests/                # 单元测试目录
│       ├── __init__.py
│       ├── conftest.py       # 测试配置
│       └── test_openapi.py   # API测试用例
└── README.md                 # 项目说明文档
```

## 核心模块说明

### openapi.py - OpenAPI基础类
提供领星API的核心功能：
- **访问令牌管理**：获取和刷新access_token
- **API请求封装**：统一的请求接口
- **错误处理**：完善的异常处理机制
- **签名验证**：请求签名和验证

**主要方法**：
```python
# 获取访问令牌
token_resp = await op_api.generate_access_token()

# 刷新访问令牌
token_resp = await op_api.refresh_token(refresh_token)

# 发起API请求
resp = await op_api.request(access_token, route_name, method, req_params, req_body)
```

### demo.py - 使用示例
演示如何使用API进行：
- 订单查询和管理
- 商品分类操作
- 数据处理和保存
- 错误处理和重试

### http_util.py - HTTP请求工具
封装HTTP请求功能：
- 异步HTTP客户端
- 请求重试机制
- 响应数据解析
- 超时处理

### resp_schema.py - 响应数据模型
定义API响应的数据结构：
- AccessTokenDto：访问令牌数据模型
- ResponseResult：通用响应结果模型
- 数据验证和类型检查

### sign.py - 数字签名工具
提供API请求的安全功能：
- 请求参数签名
- 签名验证
- 时间戳处理

### aes.py - AES加密工具
提供数据加密功能：
- AES加密/解密
- 密钥管理
- 数据安全传输

## 快速开始

### 环境要求
- Python >= 3.8.3
- asyncio支持
- 相关依赖库（见requirements.txt）

### 安装依赖
```bash
cd Lingxing_Auth
pip install -r requirements.txt
```

### 基本使用

1. **配置API凭证**：
```python
# 设置环境变量（推荐）
export API_HOST="https://api.lingxing.com"
export APP_ID="your_app_id"
export APP_SECRET="your_app_secret"
```

2. **运行示例程序**：
```bash
python main.py
```

3. **自定义使用**：
```python
import asyncio
from Lingxing_Auth.openapi import OpenApiBase

async def main():
    # 初始化API客户端
    op_api = OpenApiBase("host", "appId", "appSecret")
    
    # 获取访问令牌
    token_resp = await op_api.generate_access_token()
    print(f"Access Token: {token_resp.access_token}")
    
    # 查询订单列表
    req_params = {
        "page": 1,
        "limit": 10,
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    
    resp = await op_api.request(
        token_resp.access_token,
        "/api/orders/list",
        "GET",
        req_params=req_params
    )
    
    if resp.code == 200:
        print(f"查询成功，共找到 {len(resp.data)} 条订单")
    else:
        print(f"查询失败：{resp.message}")

if __name__ == '__main__':
    asyncio.run(main())
```

## API功能模块

### 订单管理
- 订单列表查询
- 订单详情获取
- 订单状态更新
- 订单创建和修改

### 商品管理
- 商品分类管理
- 库存查询和更新
- 商品信息同步
- SKU管理

### 数据同步
- 自动数据同步
- 增量数据更新
- 数据验证和清洗
- 异常数据处理

## 配置说明

### 环境变量配置
```bash
# API服务器地址
API_HOST=https://api.lingxing.com

# 应用凭证
APP_ID=your_application_id
APP_SECRET=your_application_secret

# 可选配置
API_TIMEOUT=30          # 请求超时时间（秒）
MAX_RETRIES=3          # 最大重试次数
RETRY_DELAY=1          # 重试延迟（秒）
```

### 请求配置
```python
# 请求头配置
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Lingxing-Python-SDK/1.0"
}

# 超时配置
TIMEOUT_CONFIG = {
    "connect": 10,    # 连接超时
    "read": 30,       # 读取超时
    "total": 60       # 总超时
}
```

## 错误处理

### 常见错误类型
1. **认证错误**：APP_ID或APP_SECRET无效
2. **令牌过期**：access_token已过期，需要刷新
3. **请求限制**：API调用频率超限
4. **网络错误**：连接超时或网络异常
5. **数据错误**：请求参数格式错误

### 错误处理示例
```python
try:
    resp = await op_api.request(access_token, route, method, params)
    if resp.code == 200:
        # 处理成功响应
        process_data(resp.data)
    else:
        # 处理业务错误
        handle_business_error(resp.code, resp.message)
except ValueError as e:
    # 处理认证错误
    print(f"认证失败: {e}")
except Exception as e:
    # 处理其他异常
    print(f"请求异常: {e}")
```

## 测试

### 运行单元测试
```bash
cd Lingxing_Auth
python -m pytest tests/ -v
```

### 测试覆盖率
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### 测试配置
测试使用 `conftest.py` 进行配置，包括：
- 测试环境设置
- Mock数据准备
- 测试夹具定义

## 性能优化

### 异步处理
- 使用asyncio进行并发请求
- 连接池复用
- 请求批处理

### 缓存策略
- 访问令牌缓存
- 响应数据缓存
- 本地数据缓存

### 监控和日志
- 请求性能监控
- 错误日志记录
- API调用统计

## 安全考虑

### 凭证安全
- 使用环境变量存储敏感信息
- 避免在代码中硬编码凭证
- 定期轮换API密钥

### 数据传输安全
- HTTPS加密传输
- 请求签名验证
- 数据加密存储

### 访问控制
- 令牌有效期管理
- API访问频率限制
- 权限范围控制

## 依赖库

主要依赖（详见requirements.txt）：
```
aiohttp>=3.8.0      # 异步HTTP客户端
pydantic>=1.10.0    # 数据验证和序列化
cryptography>=3.4.0 # 加密功能
pytest>=7.0.0       # 单元测试框架
pytest-asyncio      # 异步测试支持
```

## 版本信息

- **当前版本**: v1.0
- **Python要求**: >= 3.8.3
- **最后更新**: 2025年1月
- **维护状态**: 活跃维护中

## 更新日志

详见 `Lingxing_Auth/CHANGELOG.md` 文件。

## 注意事项

1. **API限制**: 注意领星API的调用频率限制
2. **令牌管理**: 及时刷新过期的访问令牌
3. **数据安全**: 妥善保管API凭证和敏感数据
4. **错误处理**: 实现完善的错误处理和重试机制
5. **版本兼容**: 关注API版本更新和兼容性

## 技术支持

- 查看官方文档：[领星开放平台](https://open.lingxing.com)
- 提交问题：项目Issues页面
- 技术交流：开发团队联系方式

## 许可证

本项目遵循相关开源许可证，具体使用请遵守领星API服务条款。