# 小满CRM线索自动化系统

## 项目概述

该系统用于自动化处理小满CRM线索管理，实现从ZOHO FORM模块收集信息后，自动在小满CRM线索模块新建对应的线索。系统通过API接口实现数据的自动同步和处理。

## 功能特性

- ✅ **自动登录**：支持小满CRM系统的自动登录认证
- ✅ **线索创建**：自动在小满CRM中创建新的线索记录
- ✅ **数据同步**：从ZOHO FORM获取数据并同步到小满CRM
- ✅ **用户管理**：支持用户信息的处理和管理
- ✅ **数据输入**：支持多种数据输入格式和处理方式

## 文件结构

```
xiaomang_CRM/
├── xiaomang_login.py      # 小满CRM登录模块
├── xiaomang_in.py         # 数据输入处理模块
├── xiaomang_inputdata.py  # 数据输入管理模块
├── dpuser.py              # 用户数据处理模块
├── t.py                   # 测试文件
└── README.md              # 项目说明文档
```

## 核心模块说明

### xiaomang_login.py
小满CRM系统登录模块，负责：
- 用户身份验证
- 会话管理
- API接口调用
- 登录状态维护

### xiaomang_in.py
数据输入处理模块，负责：
- 处理来自ZOHO FORM的数据
- 数据格式转换
- 数据验证和清洗

### xiaomang_inputdata.py
数据输入管理模块，负责：
- 管理数据输入流程
- 协调各个模块的数据处理
- 错误处理和日志记录

### dpuser.py
用户数据处理模块，负责：
- 用户信息管理
- 用户数据处理
- 用户权限验证

## 使用方法

### 基本使用

1. **配置登录信息**：
   ```python
   from xiaomang_login import XiaomanCRM
   
   # 创建CRM实例
   crm = XiaomanCRM()
   
   # 执行登录
   crm.login()
   ```

2. **处理线索数据**：
   ```python
   # 导入数据处理模块
   from xiaomang_inputdata import process_lead_data
   
   # 处理线索数据
   lead_data = {
       'name': '客户姓名',
       'email': '客户邮箱',
       'phone': '联系电话',
       'company': '公司名称'
   }
   
   # 提交线索到小满CRM
   result = process_lead_data(lead_data)
   ```

## 依赖库

```python
import requests      # HTTP请求处理
import urllib3       # URL处理
import json          # JSON数据处理
import sys           # 系统相关功能
```

## 安装依赖

```bash
pip install requests urllib3
```

## 配置说明

### API配置
- **登录API**: `https://login-api.xiaoman.cn/read/login`
- **线索提交API**: `https://crm.xiaoman.cn/api/leadV2Write/submitLead`

### 认证信息
系统使用账号密码方式进行认证，需要配置：
- 用户账号
- 加密后的密码
- 验证码（如需要）

## 注意事项

1. **安全性**：
   - 密码已进行加密处理
   - 建议定期更新认证信息
   - 不要在代码中硬编码敏感信息

2. **错误处理**：
   - 系统包含完整的错误处理机制
   - 支持重试机制
   - 提供详细的错误日志

3. **数据格式**：
   - 确保输入数据格式正确
   - 必填字段不能为空
   - 数据类型需要匹配API要求

## 业务流程

1. **数据收集**：从ZOHO FORM收集客户信息
2. **数据处理**：清洗和验证数据格式
3. **系统登录**：自动登录小满CRM系统
4. **线索创建**：在CRM中创建新的线索记录
5. **结果反馈**：返回处理结果和状态信息

## 维护说明

- 定期检查API接口状态
- 监控系统运行日志
- 及时更新依赖库版本
- 备份重要配置信息

## 版本信息

- **当前版本**: v1.0
- **最后更新**: 2025年1月
- **维护状态**: 活跃维护中

## 联系方式

如有问题或建议，请联系开发团队。