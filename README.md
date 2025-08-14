<<<<<<< HEAD
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
=======
# RPA项目

## 财务部业务流程

| **流程名称**                     | **场景描述**                                                                 | **版本信息**                  |
|----------------------------------|-----------------------------------------------------------------------------|-------------------------------|
| 各店铺发货数据汇总 - 数据处理       | 财务每个月初汇总上个月各店铺的发货订单数据，快速获取产品名、料号、金额、数据、仓位 | 版本v1：newfile.py<br>版本v2：temp_newfile.py - 更新日期2025-6-5 |
| 天猫每月应收余额                 | 每月月底最后一天23:57分进行数据截图并发送邮箱                                 | 无                            |
| 沃尔玛（Walmart）下载            |                                                                             | 无                            |
| Tiktok下载                       |                                                                             | 无                            |
| 亚马逊下载                        |                                                                             | 无                            |
| 天猫和京东下载                    |                                                                             | 无                            |
| Shopify收款下载                   |                                                                             | 无                            |
| 退货跟踪                          | 业务人员每天需要登录领星及钉钉获取各店铺退货信息，并反馈给相关负责人            | process_returns.py                            |
| 京东POP月末余额数据截取           | 余额及明细                                                               | 无                            |
| 天猫和京东销售数据统计            | 1. 手工下载万里牛系统上月销售订单<br>2. 整合万里牛下载表格 - Excel               | 版本v1：process_excel.py      |

## ACE组业务流程

| **流程名称**                     | **场景描述**                                                                | **版本信息** |
|----------------------------------|-----------------------------------------------------------------------------|-------------|
| Crazyegg数据查看                  | 查看页面热图，分析页面点击情况                                              | 无          |
| 谷歌账户数据查看                  | 查看广告数据（CPC、ROAS、CPM、花费等）                                       | BpdData.py          |
| Sharesale账户数据查看             | 每日获取交易数据，每月17号导出上月交易数据                                  | dataupdate.py          |
| Shopify后台运营数据查看           | 查看各店铺数据转化率、用户数、销售额、活动情况、弃购、审核订单等              | publicblock.py          |
| Tradedoubler账户数据查看          | 查看每日交易数据，审核联盟客                                                 | 无          |
| Shipfy库存数据查看                 | 查看各店铺库存情况、销量情况                                                 | checkfiles.py;exceldetail.py          |
| 速卖通跟卖家卖家投诉              | 处理速卖通平台上与卖家相关的投诉问题                                        | 无          |
| 速卖通产品评价管理                | 管理速卖通平台上的产品评价                                                  | 无          |
| 速卖通产品评价自动回复            | 设置自动回复功能，对客户的产品评价进行及时响应                              | 无          |
| 半托管发货                        | 登录领星及钉钉表格，对每周商品信息进行整理，并汇总给业务人员                 | 无          |

## 销售部业务流程

| **流程名称**                     | **场景描述**                                                                                | **版本信息** |
|----------------------------------|------------------------------------------------------------------------------------------|-------------|
| 销售官网询盘自动收集、分发        | 官方询盘邮件发给sales邮箱，由Stella转发给其他销售人员，销售人员收到后跟进客户。希望实现自动化收集新建询盘线索、自动分配销售人员，并配合邮件转发确保信息传递无误。 | 无          |
| 小满CRM线索自动化                | 从ZOHO FORM模块收集到的信息后，同步在小满CRM线索模块新建对应的线索。                       | email.py、html_parser.py、module1.py          |

## 市场营销部业务流程

| **流程名称**                     | **场景描述**                                                                  | **版本信息** |
|----------------------------------|------------------------------------------------------------------------------|-------------|
| Mailchimp数据下载                 | 登录Mailchimp采集产品信息曝光度                                               | data_processing.py          |
| Yopto数据收集                     | 收集每个站点会员人数等数据，减少时间成本                                      | readcsv.py、publicBlock (2).py          |
| KOL/SVF管理系统                   | 每天查看不同网站内数据（views、comments等），并写入钉钉多维表格                 | getdata.py          |
| Zoho Form表单数据                 | 同步提交表单数据到市场部品牌数据里做记录                                     | 无          |

## 电商中心业务流程

| **流程名称**                     | **场景描述**                                                                    | **版本信息** |
|----------------------------------|--------------------------------------------------------------------------------|-------------|
| 电商中心_亚马逊新品销量汇总&退货数据汇总                 | 根据领星系统，分EU和NA地区，筛选一周的时间段，填写新品一周的销量数据  <br>1. 在领星系统上，选择EU和NA地区，筛选一周的时间段，下载退货数据报告<br>2. 在报表上筛选新品的SKU，分开EU和NA地区进行筛选，并分别填写NA和EU地区新品的退款数量以及买家评价到新品客户问题汇总表里 | 无          |

## 物流仓储业务流程

| **流程名称**                      | **场景描述**                                                                            | **版本信息** |
|-----------------------------------|--------------------------------------------------------------------------------------|-------------|
| 领星ERP系统对接保宏系统物流发货     | 领星ERP系统与保宏系统无法对接集货模式发货，目前是人工录入领星订单信息至保宏系统进行发货。待保宏仓库操作发货生成物流单号后，再手动回传订单单号至领星系统，并标发订单单号至平台后台。 | 领星保宏系统文件夹          |

## 人事行政部业务流程

| **流程名称**              | **场景描述**                                                      | **版本信息** |
|-------------------------|----------------------------------------------------------------|-------------|
| Boss直聘打招呼沟通        | 利用RPA+AI功能进行信息简历筛选，并将筛选结果通知业务人员，以优化招聘流程 | BOSS直聘文件夹          |

>>>>>>> 5632c898e30b9721290051c0be007930cf60ae0d
