# Git 管理指南

本文档说明如何在 `new_rpa` 项目中正确使用 Git 进行版本控制，特别是针对两个独立子项目的管理策略。

## 📁 项目结构概述

```
new_rpa/                    # 根项目（包含两个独立子项目）
├── .gitignore             # 根目录通用忽略规则
├── RPA_Tornado/           # Web API 服务项目
│   ├── .gitignore         # Tornado 特定忽略规则
│   └── ...
├── rpa/                   # RPA 脚本工具集
│   ├── .gitignore         # RPA 特定忽略规则
│   └── ...
└── README.md
```

## 🔧 .gitignore 文件管理策略

### 1. 分层忽略规则

#### 根目录 `.gitignore` - 通用规则
```gitignore
# Python 通用文件
__pycache__/
*.pyc
*.pyo

# 虚拟环境
.venv/
venv/

# IDE 配置
.vscode/
.idea/

# 操作系统文件
.DS_Store
Thumbs.db

# 日志和临时文件
*.log
*.tmp
```

#### RPA_Tornado/.gitignore - Web 服务特定
```gitignore
# Tornado 特定
*.manifest
*.spec

# 上传文件
uploads/
static/uploads/

# 配置文件
config/local.yaml
config/production.yaml

# 性能分析
*.prof
*.cprofile
```

#### rpa/.gitignore - RPA 特定
```gitignore
# RPA 数据文件
*.xlsx
*.csv
*.json

# 自动化输出
output/
downloads/
results/

# 浏览器数据
user_data/
cookies.txt

# 敏感配置
api_keys.json
credentials.json
```

### 2. 忽略规则优先级

1. **子目录规则优先**：子目录的 `.gitignore` 会覆盖父目录的规则
2. **就近原则**：Git 会使用最接近文件的 `.gitignore` 规则
3. **累积效应**：所有层级的 `.gitignore` 规则都会生效

## 📋 最佳实践

### 1. 文件组织原则

- **通用规则放根目录**：所有 Python 项目都需要的忽略规则
- **特定规则放子目录**：只有特定项目需要的忽略规则
- **避免重复**：不要在子目录重复根目录已有的规则

### 2. 敏感数据保护

#### 🔒 必须忽略的文件类型
```gitignore
# 配置文件
*.ini
*.env
secrets.json
credentials.json
api_keys.json

# 数据文件（可能包含敏感信息）
*.xlsx
*.csv
*.json

# 数据库文件
*.db
*.sqlite
*.sqlite3

# 认证文件
*.key
*.pem
*.p12
```

#### ✅ 可以提交的文件
```gitignore
# 模板文件（不包含真实数据）
!**/template*.xlsx
!**/example*.csv
!**/config_template.json
!**/schema*.json
```

### 3. 项目特定建议

#### RPA_Tornado 项目
- 忽略所有上传文件和用户数据
- 保护生产环境配置文件
- 忽略性能分析和调试文件
- 保留 API 文档和模板文件

#### rpa 项目
- 忽略所有业务数据文件
- 保护 API 密钥和登录凭据
- 忽略自动化脚本的输出文件
- 保留示例和模板文件

## 🚀 Git 工作流建议

### 1. 提交前检查
```bash
# 检查将要提交的文件
git status

# 查看具体变更
git diff

# 确保没有敏感文件
git ls-files --others --ignored --exclude-standard
```

### 2. 分支管理
```bash
# 为不同项目创建特性分支
git checkout -b feature/tornado-api-update
git checkout -b feature/rpa-automation-script

# 独立提交不同项目的变更
git add RPA_Tornado/
git commit -m "feat(tornado): 添加新的API端点"

git add rpa/
git commit -m "feat(rpa): 新增Boss直聘自动化脚本"
```

### 3. 提交信息规范
```bash
# 使用项目前缀区分不同子项目
git commit -m "feat(tornado): 添加用户认证功能"
git commit -m "fix(rpa): 修复Excel数据处理bug"
git commit -m "docs(root): 更新项目文档"
git commit -m "chore(gitignore): 优化忽略规则"
```

## ⚠️ 注意事项

### 1. 避免的操作
- ❌ 不要在子项目的 `.gitignore` 中重复根目录的规则
- ❌ 不要提交包含真实业务数据的文件
- ❌ 不要提交包含 API 密钥或密码的配置文件
- ❌ 不要忽略重要的项目配置模板文件

### 2. 推荐的操作
- ✅ 定期检查 `.gitignore` 规则的有效性
- ✅ 为敏感配置文件创建模板版本
- ✅ 使用环境变量管理敏感信息
- ✅ 在 README 中说明配置文件的设置方法

### 3. 紧急情况处理

如果意外提交了敏感文件：
```bash
# 从 Git 历史中完全删除文件
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/sensitive/file' \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（谨慎使用）
git push origin --force --all
```

## 📞 支持

如果在使用过程中遇到问题，请参考：
- [Git 官方文档](https://git-scm.com/docs)
- [.gitignore 模板](https://github.com/github/gitignore)
- 项目 README.md 文件