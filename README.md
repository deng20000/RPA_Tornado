# RPA 项目集合

这是一个包含多个自动化项目的仓库，主要包含以下两个独立项目：

## 📁 项目结构

### 🚀 RPA_Tornado
基于 Tornado 框架的电商数据处理后端 API 系统
- **技术栈**: Python, Tornado, PostgreSQL, SQLAlchemy
- **功能**: 电商数据统计、多平台数据整合、API 服务
- **文档**: [RPA_Tornado/README.md](./RPA_Tornado/README.md)

### 🤖 rpa
各种 RPA 自动化脚本和工具集合
- **技术栈**: Python, Selenium, API 集成
- **功能**: 网站自动化、数据抓取、业务流程自动化
- **文档**: [rpa/README.md](./rpa/README.md)

### 🗄️ database_tests
数据库连接测试脚本
- PostgreSQL 连接测试
- DBeaver 连接配置

## 🔧 环境配置

### Python 虚拟环境
```bash
# 激活虚拟环境
.venv\Scripts\activate

# 安装依赖
pip install -r RPA_Tornado/requirements.txt
pip install -r rpa/requirements.txt
```

### 数据库配置
参考以下文档进行数据库配置：
- [PostgreSQL 容器设置摘要](./PostgreSQL_Container_Setup_Summary.md)
- [DBeaver PostgreSQL 连接指南](./DBeaver_PostgreSQL_Connection_Guide.md)

## 📚 文档导航

- **RPA_Tornado API 文档**: [RPA_Tornado/docs/](./RPA_Tornado/docs/)
- **RPA 脚本文档**: [rpa/README.md](./rpa/README.md)
- **数据库配置**: [PostgreSQL_Container_Setup_Summary.md](./PostgreSQL_Container_Setup_Summary.md)

## 🚀 快速开始

### 启动 RPA_Tornado 服务
```bash
cd RPA_Tornado
python main.py
```

### 运行 RPA 脚本
```bash
cd rpa
# 查看具体脚本的使用方法
python scripts/quick_start.py
```

## 📝 项目特点

- **模块化设计**: 每个项目独立维护，互不干扰
- **统一环境**: 共享 Python 虚拟环境和数据库配置
- **完整文档**: 每个项目都有详细的使用文档
- **测试覆盖**: 包含数据库连接测试和功能测试

## 🤝 贡献指南

1. 每个子项目都有独立的开发流程
2. 修改前请阅读对应项目的 README.md
3. 遵循现有的代码风格和项目结构
4. 提交前运行相关测试

## 📞 联系方式

如有问题，请查看各项目的文档或提交 Issue。
