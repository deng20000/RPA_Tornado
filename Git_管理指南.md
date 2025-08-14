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

## 👤 Git 账号管理与切换

### 1. 查看当前Git配置
```bash
# 查看全局配置
git config --global --list

# 查看当前仓库配置
git config --list

# 查看用户名和邮箱
git config user.name
git config user.email
```

### 2. 全局账号切换
```bash
# 设置全局用户名和邮箱（影响所有仓库）
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱@example.com"

# 示例：切换到工作账号
git config --global user.name "John Doe"
git config --global user.email "john.doe@company.com"

# 示例：切换到个人账号
git config --global user.name "JohnPersonal"
git config --global user.email "john.personal@gmail.com"
```

### 3. 单个项目账号设置
```bash
# 在项目目录下设置（仅影响当前项目）
cd /path/to/your/project
git config user.name "项目专用用户名"
git config user.email "项目专用邮箱@example.com"

# 示例：为当前RPA项目设置特定账号
cd c:\Users\Johnthan\Desktop\new_rpa
git config user.name "RPA Developer"
git config user.email "rpa.dev@company.com"
```

### 4. 多账号管理策略

#### 方案一：项目级配置（推荐）
```bash
# 为不同类型的项目设置不同账号
# 工作项目
git config user.name "Work Name"
git config user.email "work@company.com"

# 个人项目
git config user.name "Personal Name"
git config user.email "personal@gmail.com"
```

#### 方案二：使用Git别名快速切换
```bash
# 设置切换别名（已配置完成）
git config --global alias.work-account "!git config user.name 'John than' && git config user.email '85759703+deng20000@users.noreply.github.com'"
git config --global alias.personal-account "!git config user.name 'John than' && git config user.email 'personal@example.com'"

# 使用别名快速切换
git work-account      # 切换到工作账号（GitHub账号）
git personal-account  # 切换到个人账号（需要修改邮箱为实际个人邮箱）

# 查看当前配置
git config user.name   # 查看当前用户名
git config user.email  # 查看当前邮箱
```

**注意：** 个人账号的邮箱地址设置为示例地址，请根据需要修改为实际的个人邮箱：
```bash
git config --global alias.personal-account "!git config user.name 'John than' && git config user.email 'your-personal@email.com'"
```

### 5. SSH密钥管理

#### 当前配置状态
您的SSH配置已经正常工作，使用单个ED25519密钥连接GitHub：
- 密钥文件：`~/.ssh/id_ed25519`
- GitHub账号：`deng20000`
- 连接测试：`ssh -T git@github.com`

### 6. 远程仓库配置

#### 问题解决：推送到错误的远程仓库

**问题现象：** 使用个人账号时推送到了 GitLab 而不是 GitHub

**原因分析：** 当前仓库的远程地址配置指向了 GitLab

**解决步骤：**

1. **检查当前远程配置**
   ```bash
   git remote -v
   ```

2. **修改远程地址为 GitHub**
   ```bash
   # 修改为 GitHub 地址
   git remote set-url origin git@github.com:deng20000/仓库名.git
   ```

3. **创建 GitHub 仓库（如果不存在）**
   - 访问 [GitHub](https://github.com)
   - 点击右上角的 "+" 号，选择 "New repository"
   - 输入仓库名称（如：new_rpa）
   - 选择公开或私有
   - 点击 "Create repository"

4. **推送到 GitHub**
   ```bash
   # 确保使用工作账号配置
   git work-account
   
   # 推送到 GitHub
   git push origin master
   # 或者强制推送（如果需要）
   git push -f origin master
   ```

**当前状态：** 远程地址已修改为 `git@github.com:deng20000/new_rpa.git`，但需要在 GitHub 上创建对应的仓库。

#### 查看当前SSH密钥
```bash
# 查看公钥内容
Get-Content ~/.ssh/id_ed25519.pub

# 测试GitHub连接
ssh -T git@github.com
```

#### 如需生成新的SSH密钥（可选）
```bash
# 生成ED25519密钥（推荐）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 生成RSA密钥（兼容性更好）
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

#### 当前SSH配置文件 (~/.ssh/config)
```bash
# GitHub 工作账号 (当前账号 deng20000)
Host github
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking no

# GitHub 标准配置 (兼容性)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking no

# 工作项目 - GitLab GL-iNet
Host gitlab-work
    HostName gitlab.gl-inet.net
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    StrictHostKeyChecking no
```

#### SSH连接验证
```bash
# 测试GitHub连接
ssh -T git@github.com
# 预期输出：Hi deng20000! You've successfully authenticated...

# 测试GitLab连接
ssh -T git@gitlab-work
```

#### 使用远程仓库地址
```bash
# GitHub仓库（使用当前deng20000账号）
git remote add origin git@github.com:deng20000/repository.git

# GitLab工作项目
git remote add origin git@gitlab-work:project/repository.git

# 修改现有远程地址
git remote set-url origin git@github.com:deng20000/new-repository.git
```

### 6. 验证账号配置
```bash
# 检查当前配置
git config user.name
git config user.email

# 测试SSH连接
ssh -T git@github-work
ssh -T git@github-personal

# 查看最近提交的作者信息
git log --oneline -5 --pretty=format:"%h %an <%ae> %s"
```

### 7. 常见问题解决

#### 问题1：提交后发现用错了账号
```bash
# 修改最近一次提交的作者信息
git commit --amend --author="正确的用户名 <正确的邮箱@example.com>"

# 修改多个提交的作者信息（谨慎使用）
git rebase -i HEAD~3  # 修改最近3个提交
```

#### 问题2：忘记当前使用的是哪个账号
```bash
# 快速查看当前账号信息
git config user.name && git config user.email

# 或者创建一个别名
git config --global alias.whoami '!git config user.name && git config user.email'
git whoami  # 使用别名查看
```

#### 问题3：需要临时使用不同账号提交
```bash
# 单次提交使用指定作者
git commit --author="临时用户名 <临时邮箱@example.com>" -m "提交信息"
```

### 8. 最佳实践建议

1. **项目开始前先设置账号**：避免后续修改提交历史
2. **使用项目级配置**：为不同项目设置合适的账号
3. **定期检查配置**：确保使用正确的账号进行提交
4. **备份SSH密钥**：避免密钥丢失导致的访问问题
5. **文档化账号策略**：在团队中统一账号管理规范

## 📞 支持

如果在使用过程中遇到问题，请参考：
- [Git 官方文档](https://git-scm.com/docs)
- [.gitignore 模板](https://github.com/github/gitignore)
- [Git 账号配置指南](https://docs.github.com/en/get-started/getting-started-with-git/setting-your-username-in-git)
- 项目 README.md 文件