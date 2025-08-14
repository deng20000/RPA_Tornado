# RPA项目 - UV环境管理

## 概述

本项目使用 [uv](https://github.com/astral-sh/uv) 作为Python包管理器和环境管理工具。uv是一个快速的Python包安装器和解析器，用Rust编写。

## 快速开始

### 1. 安装uv

#### Windows
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 初始化项目环境

运行自动设置脚本：
```bash
python setup_env.py
```

或者手动设置：
```bash
# 同步依赖
uv sync

# 更新锁文件
uv lock
```

## 项目结构

```
rpa/
├── pyproject.toml          # 项目配置和依赖
├── uv.lock                 # 依赖锁定文件
├── .uv/                    # uv配置目录
│   └── config.toml        # uv配置
├── Makefile               # 常用命令快捷方式
├── setup_env.py           # 环境设置脚本
├── .gitignore             # Git忽略文件
└── UV_SETUP.md           # 本文档
```

## 常用命令

### 环境管理

```bash
# 安装生产依赖
uv sync --no-dev

# 安装开发依赖
uv sync

# 更新锁文件
uv lock

# 清理缓存
uv cache clean
```

### 运行脚本

```bash
# 运行Python脚本
uv run python process_returns.py
uv run python process_excel.py
uv run python BpdData.py
uv run python newfile.py

# 运行测试
uv run pytest

# 代码检查
uv run flake8 .

# 代码格式化
uv run black .

# 类型检查
uv run mypy .
```

### 使用Makefile快捷命令

```bash
# 查看所有可用命令
make help

# 安装依赖
make install          # 生产依赖
make install-dev      # 开发依赖

# 代码质量
make test             # 运行测试
make lint             # 代码检查
make format           # 代码格式化
make check            # 类型检查

# 运行RPA脚本
make run-returns      # 运行退货处理
make run-excel        # 运行Excel处理
make run-bpd          # 运行BPD数据处理
make run-newfile      # 运行新文件处理

# 清理
make clean            # 清理缓存和临时文件
```

## 依赖管理

### 添加新依赖

```bash
# 添加生产依赖
uv add package_name

# 添加开发依赖
uv add --dev package_name

# 添加特定版本
uv add package_name==1.2.3
```

### 移除依赖

```bash
# 移除依赖
uv remove package_name

# 移除开发依赖
uv remove --dev package_name
```

### 更新依赖

```bash
# 更新所有依赖
uv lock --upgrade

# 更新特定依赖
uv lock --upgrade-package package_name
```

## 项目依赖说明

### 核心依赖

- **数据处理**: pandas, numpy, openpyxl
- **网络请求**: requests, aiohttp, urllib3
- **系统操作**: psutil
- **数据解析**: chardet, beautifulsoup4, lxml
- **加密安全**: pycryptodome, cryptography
- **数据序列化**: orjson, PyYAML
- **语言检测**: langdetect, polyglot
- **浏览器自动化**: DrissionPage
- **数据验证**: pydantic
- **异步支持**: anyio
- **终端输出**: colorama

### 开发依赖

- **测试**: pytest, pytest-asyncio, pytest-cov
- **代码质量**: black, flake8, mypy

## 虚拟环境

uv会自动创建和管理虚拟环境，无需手动创建。虚拟环境位于项目根目录的`.venv`文件夹中。

### 激活虚拟环境

```bash
# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# 或者直接使用uv run（推荐）
uv run python script.py
```

## 故障排除

### 常见问题

1. **uv命令未找到**
   - 确保uv已正确安装
   - 重新启动终端
   - 检查PATH环境变量

2. **依赖安装失败**
   - 检查网络连接
   - 尝试使用国内镜像源
   - 清理缓存：`uv cache clean`

3. **权限问题**
   - Windows: 以管理员身份运行PowerShell
   - Linux/macOS: 使用sudo（如果需要）

### 重置环境

```bash
# 删除虚拟环境
rm -rf .venv

# 重新同步
uv sync
```

## 最佳实践

1. **始终使用uv run运行脚本**，而不是直接激活虚拟环境
2. **定期更新锁文件**：`uv lock`
3. **在添加新依赖前检查现有依赖**
4. **使用make命令简化操作**
5. **保持依赖版本的一致性**

## 贡献指南

1. 在添加新依赖前，请更新`pyproject.toml`
2. 运行`make test`确保测试通过
3. 运行`make lint`和`make format`保持代码质量
4. 提交前运行`uv lock`更新锁文件

## 更多信息

- [uv官方文档](https://docs.astral.sh/uv/)
- [uv GitHub仓库](https://github.com/astral-sh/uv)
- [Python包管理最佳实践](https://packaging.python.org/guides/) 