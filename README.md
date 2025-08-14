# RPA自动化项目集合

本仓库包含两个独立的自动化项目：

## 🚀 项目概览

### 1. RPA_Tornado - 企业级RPA后端服务
基于Tornado框架的高性能RPA系统，专注于电商数据处理和统计报表。这是一个完整的Web API服务，提供数据处理、统计分析和报表生成功能。

### 2. rpa - RPA脚本工具集
独立的RPA自动化脚本项目，涵盖财务、销售、市场营销、电商、物流仓储和人事行政等多个业务领域的自动化流程。每个脚本都可以独立运行，解决特定的业务自动化需求。

---

## 📁 项目结构

```
new_rpa/
├── RPA_Tornado/           # Tornado后端服务项目（Web API服务）
│   ├── app/               # 应用核心代码
│   │   ├── handlers/      # API处理器
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务服务
│   │   └── utils/         # 工具函数
│   ├── config/            # 配置文件
│   ├── docs/              # API文档
│   ├── scripts/           # 部署脚本
│   ├── tests/             # 测试代码
│   ├── main.py            # 应用入口
│   └── requirements.txt   # 依赖包
├── rpa/                   # 独立RPA脚本项目
│   ├── scripts/           # 通用脚本工具
│   ├── projects/          # 按部门分类的项目
│   ├── ecommerce_platforms/ # 电商平台RPA脚本
│   ├── KOL_SVFmanagesystem/ # KOL管理系统
│   ├── Return_tracking/   # 退货跟踪系统
│   ├── boss_zhipin_rpa/   # Boss直聘RPA
│   ├── marketing_social_media_data/ # 社媒数据处理
│   ├── translation/       # 翻译工具
│   ├── tests/             # 测试代码
│   ├── pyproject.toml     # 项目配置
│   └── requirements.txt   # 依赖包
├── database_tests/        # 数据库连接测试
├── DBeaver_PostgreSQL_Connection_Guide.md
├── PostgreSQL_Container_Setup_Summary.md
└── README.md              # 本文件
```

## 🚀 RPA_Tornado - 企业级后端服务

**项目定位：** 基于Tornado框架的高性能Web API服务，专注于电商数据处理和统计分析。

**核心功能：**
- 🔄 电商平台数据统计和分析
- 🔗 多平台数据整合和同步
- 📊 实时数据处理和报表生成
- 🌐 RESTful API接口服务
- 📈 业务数据可视化
- 🔐 用户认证和权限管理

**技术架构：**
- **后端框架：** Tornado Web Framework
- **数据库：** PostgreSQL
- **容器化：** Docker + Docker Compose
- **API文档：** Swagger/OpenAPI
- **开发语言：** Python 3.8+
- **部署方式：** 容器化部署

**快速启动：**
```bash
cd RPA_Tornado
docker-compose up -d
# 访问 http://localhost:8888
```

---

## 🛠 rpa - 独立脚本工具集

**项目定位：** 独立的RPA自动化脚本项目，解决各业务部门的具体自动化需求。

**业务覆盖：**
- 💰 **财务部：** 发货数据汇总、退货跟踪、销售统计
- 📈 **销售部：** 询盘收集、CRM线索管理、客户跟进
- 📱 **市场部：** 社媒数据采集、KOL管理、邮件营销
- 🛒 **电商中心：** 平台数据同步、库存管理、订单处理
- 📦 **物流仓储：** ERP系统对接、发货管理
- 👥 **人事行政：** 招聘流程自动化、简历筛选

**技术特点：**
- 🔧 模块化设计，每个脚本独立运行
- 🌍 多平台支持（Windows/macOS/Linux）
- 🔌 丰富的API集成（领星、钉钉、YouTube等）
- 📊 强大的数据处理和分析能力
- 🛡️ 完善的错误处理和日志记录
- 📦 使用uv进行现代化包管理

**快速启动：**
```bash
cd rpa
# 安装uv包管理器
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# 初始化环境
uv sync
# 运行脚本
uv run python scripts/process_returns.py
```

---

## 🚀 快速开始

### 环境要求
- **Python**: 3.8+
- **数据库**: PostgreSQL 12+
- **容器**: Docker & Docker Compose (推荐)
- **包管理**: uv (rpa项目) / pip (RPA_Tornado项目)

### 1. 克隆项目
```bash
git clone https://github.com/deng20000/RPA_Tornado.git
cd new_rpa
```

### 2. RPA_Tornado 后端服务启动
```bash
cd RPA_Tornado

# 方式一：Docker 启动（推荐）
docker-compose up -d

# 方式二：本地启动
pip install -r requirements.txt
python main.py

# 访问服务
# API服务: http://localhost:8888
# Swagger文档: http://localhost:8888/docs
```

### 3. rpa 脚本工具使用
```bash
cd rpa

# 安装uv包管理器（如未安装）
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 初始化环境
uv sync

# 运行具体脚本
uv run python scripts/process_returns.py
uv run python scripts/BpdData.py
```

---

## 📖 项目文档

### 核心文档
- 📋 [RPA_Tornado API文档](./RPA_Tornado/docs/API_MASTER_DOCUMENTATION.md)
- 🛠 [rpa脚本使用指南](./rpa/README.md)
- 🗄️ [数据库配置指南](./DBeaver_PostgreSQL_Connection_Guide.md)
- 🐳 [PostgreSQL容器设置](./PostgreSQL_Container_Setup_Summary.md)

### API接口访问
- **Swagger UI**: http://localhost:8888/docs
- **API Base URL**: http://localhost:8888/api/v1
- **数据库连接**: postgresql://dbadmin:dbadmin123@127.0.0.1:5432/rpa_tornado

---

## 🔧 环境配置

### RPA_Tornado 配置
创建 `.env` 文件：
```env
# 数据库配置
DATABASE_URL=postgresql://dbadmin:dbadmin123@127.0.0.1:5432/rpa_tornado

# 服务配置
API_HOST=0.0.0.0
API_PORT=8888
DEBUG=True

# 安全配置
SECRET_KEY=your_secret_key
JWT_SECRET=your_jwt_secret
```

### rpa 项目配置
各模块独立配置，参考具体模块的 `config.py` 文件。

### 🗄️ database_tests
数据库连接测试脚本
- PostgreSQL 连接测试
- DBeaver 连接配置

---

## 🧪 测试

### RPA_Tornado 测试
```bash
cd RPA_Tornado
pytest tests/ -v
```

### rpa 脚本测试
```bash
cd rpa
uv run pytest tests/ -v
```

### 数据库连接测试
```bash
python database_tests/test_pg_connection.py
```

---

## 🛠 开发指南

### 代码规范
- ✅ 遵循 PEP 8 编码规范
- 📝 使用中文注释
- 🧪 编写单元测试
- 🏷️ 使用类型提示
- 📚 更新相关文档

### 项目贡献
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/新功能`)
3. 提交更改 (`git commit -m '添加新功能'`)
4. 推送分支 (`git push origin feature/新功能`)
5. 创建 Pull Request

---

## 📊 项目特色

### 🚀 RPA_Tornado 优势
- ⚡ **高性能**: 基于Tornado异步框架
- 🔄 **实时处理**: 支持实时数据同步
- 📈 **数据分析**: 强大的统计和报表功能
- 🔌 **API优先**: 完整的RESTful API设计
- 🐳 **容器化**: Docker一键部署
- 📚 **文档完善**: Swagger自动生成API文档

### 🛠 rpa 脚本优势
- 🎯 **业务导向**: 针对具体业务场景设计
- 🔧 **模块化**: 每个脚本独立运行
- 🌍 **跨平台**: 支持Windows/macOS/Linux
- 📊 **数据处理**: 强大的Excel、CSV处理能力
- 🔌 **API集成**: 集成多个第三方服务API
- 📦 **现代化**: 使用uv进行包管理

---

## 📞 技术支持

- 🐛 **Bug报告**: [创建Issue](https://github.com/deng20000/RPA_Tornado/issues)
- 💡 **功能建议**: [功能请求](https://github.com/deng20000/RPA_Tornado/issues)
- 📖 **文档问题**: 查看各项目README文档
- 🤝 **技术交流**: 联系开发团队

---

## 📄 许可证

本项目采用 MIT 许可证，详情请查看 [LICENSE](LICENSE) 文件。

---

## 🔄 版本信息

- **当前版本**: v2.1.0
- **最后更新**: 2025年1月
- **维护状态**: 🟢 活跃开发中
- **Python支持**: 3.8+ 
- **数据库支持**: PostgreSQL 12+

---

**💡 项目愿景**: 为企业提供高效、可靠、易用的RPA自动化解决方案，助力数字化转型和业务流程优化。
