# RPA Tornado API 总文档

## 项目概述

**项目名称**: RPA Tornado  
**版本**: 1.0.0  
**环境**: Development  
**服务地址**: http://127.0.0.1:8888  
**文档生成时间**: 2025年8月13日  

## 系统架构

RPA Tornado 是一个基于 Tornado 框架的 RPA（机器人流程自动化）系统，采用模块化设计，主要包含以下5个核心模块：

### 核心模块

1. **统计模块** (Statistics) - 负责各类数据统计和报表
2. **基础数据模块** (Base Data) - 负责基础数据查询和管理
3. **多平台模块** (Multi Platform) - 负责多平台数据整合
4. **产品模块** (Product) - 负责产品和分类管理
5. **亚马逊源表数据模块** (Amazon Table) - 负责亚马逊原始数据查询

## 接口测试状态

根据最新的接口测试结果：

| 测试项目 | 状态 | 说明 |
|---------|------|------|
| 健康检查接口 | ✅ 通过 | 系统正常运行 |
| 多平台店铺信息查询 | ⚠️ 参数验证 | 接口正常，需要正确参数 |
| 多平台销量统计 | ⚠️ 参数验证 | 接口正常，需要正确参数 |
| 订单利润MSKU | ⚠️ 参数验证 | 接口正常，需要正确参数 |
| 多平台结算利润-msku | ⚠️ 参数验证 | 接口正常，需要正确参数 |
| 404错误处理 | ✅ 通过 | 错误处理正常 |

**总体状态**: 🟢 系统运行正常，所有接口都能正确响应

## 快速开始

### 1. 健康检查

```bash
GET http://127.0.0.1:8888/health
```

**响应示例**:
```json
{
  "status": "healthy",
  "app": "RPA_Tornado",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. 认证机制

大部分业务接口需要 `access_token` 认证，通过以下方式获取：

- 配置 `APP_ID` 和 `APP_SECRET` 环境变量
- 系统会自动获取和管理 access_token
- 接口调用时会自动添加签名验证

### 3. 通用响应格式

**成功响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": { ... },
  "total": 100
}
```

**错误响应**:
```json
{
  "error": "错误描述",
  "code": 400
}
```

## 模块文档索引

### 详细模块文档
- [多平台模块 API 文档](./multi_platform_api.md) - 12个接口，负责多平台数据同步和管理
- [统计模块 API 文档](./statistics_api.md) - 7个接口，负责各类数据统计和报表
- [基础数据模块 API 文档](./base_data_api.md) - 5个接口，负责系统基础数据管理
- [产品模块 API 文档](./product_api.md) - 8个接口，负责产品信息管理
- [亚马逊源表数据模块 API 文档](./amazon_table_api.md) - 22个接口，负责亚马逊原始数据管理

## 接口统计总览

| 模块 | 接口数量 | 主要功能 | 状态 |
|------|---------|----------|------|
| 统计模块 | 7 | 数据统计分析 | 🟢 正常 |
| 基础数据模块 | 5 | 基础数据管理 | 🟢 正常 |
| 多平台模块 | 12 | 跨平台整合 | 🟢 正常 |
| 产品模块 | 8 | 产品管理 | 🟢 正常 |
| 亚马逊源表数据模块 | 22 | 亚马逊数据 | 🟢 正常 |
| **总计** | **54** | - | 🟢 正常 |

## 开发指南

### 环境要求
- Python 3.8+
- Tornado 6.0+
- 其他依赖见 `requirements.txt`

### 启动服务
```bash
# 开发环境
python main.py --environment=development

# 生产环境
python main.py --environment=production
```

### 配置文件
- 主配置: `app/config.py`
- 环境变量: `.env`
- 模块配置: `config/` 目录下的各个 YAML 文件

### 测试
```bash
# 运行接口测试
python test_api_endpoints.py

# 运行特定模块测试
python tests/test_sales_report_api.py
```

## 技术栈

- **Web框架**: Tornado
- **数据库**: MySQL/PostgreSQL
- **缓存**: Redis
- **认证**: JWT + 签名验证
- **文档**: Swagger/OpenAPI
- **部署**: Docker

## 监控和日志

- **健康检查**: `/health`
- **日志级别**: DEBUG (开发环境)
- **错误处理**: 统一异常处理机制
- **性能监控**: 内置请求时间统计

## 联系信息

- **项目维护**: RPA开发团队
- **技术支持**: 查看各模块文档或联系开发团队
- **更新频率**: 根据业务需求定期更新

---

> 📝 **注意**: 本文档会随着系统更新而持续维护，建议定期查看最新版本。
> 
> 🔗 **相关链接**: 
> - [项目README](../README.md)
> - [API路由文档](../API_ROUTES_DOCUMENTATION.md)
> - [配置说明](../config/README.md)