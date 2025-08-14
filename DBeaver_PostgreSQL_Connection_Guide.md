# 📊 DBeaver PostgreSQL 连接配置指南

## 🔍 当前数据库配置信息

根据Docker容器检查结果，您的PostgreSQL数据库配置如下：

### 📋 连接参数
- **服务器地址**: `localhost` 或 `127.0.0.1`
- **端口**: `5432`
- **数据库名**: `rpa_tornado`
- **用户名**: `dbadmin`
- **密码**: `dbadmin123`

## 🚀 DBeaver 连接步骤

### 1. 创建新连接
1. 打开 DBeaver
2. 点击 "新建连接" 或使用快捷键 `Ctrl+Shift+O`
3. 选择 "PostgreSQL"

### 2. 配置连接参数
在连接配置窗口中填入以下信息：

#### 主要设置
- **服务器主机**: `localhost`
- **端口**: `5432`
- **数据库**: `rpa_tornado`
- **用户名**: `dbadmin`
- **密码**: `dbadmin123`

#### 高级设置（可选）
- **连接超时**: 20秒
- **SSL模式**: 禁用（本地开发环境）

### 3. 测试连接
1. 点击 "测试连接" 按钮
2. 如果配置正确，应该显示 "连接成功"
3. 点击 "完成" 保存连接

## 🔧 常见问题解决

### ❌ 连接被拒绝
**原因**: PostgreSQL容器未运行
**解决方案**:
```bash
# 检查容器状态
docker ps

# 如果容器未运行，启动容器
docker start postgres-rpa
```

### ❌ 密码认证失败
**原因**: 用户名或密码错误
**解决方案**: 确保使用正确的凭据：
- 用户名: `dbadmin`
- 密码: `dbadmin123`

### ❌ 数据库不存在
**原因**: 数据库名称错误
**解决方案**: 确保数据库名为 `rpa_tornado`

## 📝 连接字符串示例

如果您需要使用连接字符串格式：
```
postgresql://dbadmin:dbadmin123@localhost:5432/rpa_tornado
```

## 🔍 验证连接

连接成功后，您可以执行以下SQL查询来验证：
```sql
-- 查看数据库版本
SELECT version();

-- 查看当前用户
SELECT current_user;

-- 查看当前数据库
SELECT current_database();

-- 查看所有表
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

## 📞 技术支持

如果仍然遇到连接问题，请检查：
1. Docker容器是否正在运行
2. 防火墙设置是否阻止了5432端口
3. PostgreSQL服务是否正常启动

---
*最后更新: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')*