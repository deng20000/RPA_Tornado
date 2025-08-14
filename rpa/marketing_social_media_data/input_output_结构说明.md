# Input/Output 文件夹结构说明

## 文件夹结构

```
市场部社媒账号数据/
├── input/                   # 输入文件夹
│   ├── dingding_fields.json     # 钉钉字段数据（必要）
│   ├── dingding_allfields.json  # 钉钉所有数据（必要）
│   ├── fb_fetch_inf.json       # Facebook原始数据（可选）
│   ├── youtube_fetch_inf.json  # Youtube原始数据（可选）
│   ├── instagram_fetch_inf.json # Instagram原始数据（可选）
│   ├── linkedin_fetch_inf.json # LinkedIn原始数据（可选）
│   └── x_fetch_inf.json       # X原始数据（可选）
├── output/                  # 输出文件夹
│   ├── optimized_data_structure_update.json  # 最终优化数据结构
│   ├── mapping_report.json                   # 映射成功率报告
│   ├── fb_fetch_inf_update.json            # Facebook处理结果
│   ├── youtube_fetch_inf_update.json       # Youtube处理结果（如存在）
│   ├── instagram_fetch_inf_update.json     # Instagram处理结果（如存在）
│   ├── linkedin_fetch_inf_update.json      # LinkedIn处理结果（如存在）
│   └── x_fetch_inf_update.json            # X处理结果（如存在）
└── 其他程序文件...
```

## 输入文件说明

### 必要文件（必须存在）
- **dingding_fields.json**: 钉钉多维表字段信息
- **dingding_allfields.json**: 钉钉多维表所有数据

### 可选文件（根据需要使用）
- **fb_fetch_inf.json**: Facebook原始数据
- **youtube_fetch_inf.json**: Youtube原始数据
- **instagram_fetch_inf.json**: Instagram原始数据
- **linkedin_fetch_inf.json**: LinkedIn原始数据
- **x_fetch_inf.json**: X原始数据

## 输出文件说明

### 主要输出文件
- **optimized_data_structure_update.json**: 最终优化的数据结构
- **mapping_report.json**: 映射成功率报告

### 平台处理结果
- **fb_fetch_inf_update.json**: Facebook数据处理结果
- **youtube_fetch_inf_update.json**: Youtube数据处理结果
- **instagram_fetch_inf_update.json**: Instagram数据处理结果
- **linkedin_fetch_inf_update.json**: LinkedIn数据处理结果
- **x_fetch_inf_update.json**: X数据处理结果

## 使用方法

### 1. 准备输入文件
将您的数据文件放入 `input/` 文件夹中：

```bash
# 必要文件
cp your_dingding_fields.json input/dingding_fields.json
cp your_dingding_allfields.json input/dingding_allfields.json

# 可选文件（根据平台）
cp your_fb_data.json input/fb_fetch_inf.json
cp your_youtube_data.json input/youtube_fetch_inf.json
# ... 其他平台数据
```

### 2. 运行程序
```bash
python main_data_process.py
```

### 3. 查看结果
所有输出文件都会保存在 `output/` 文件夹中：

```bash
ls output/
# 查看生成的文件
```

## 文件格式要求

### 钉钉字段数据 (dingding_fields.json)
```json
{
  "data": {
    "field_1": "New Fans",
    "field_2": "Posts Published",
    "field_3": "Posts Impressions",
    "field_4": "Posts Engagement"
  }
}
```

### 钉钉所有数据 (dingding_allfields.json)
```json
{
  "data": {
    "record_1": "2025.07+TestAccount+FB",
    "record_2": "2025.07+TestAccount2+Youtube",
    "record_3": "2025.07+TestAccount3+Instagram"
  }
}
```

### Facebook原始数据 (fb_fetch_inf.json)
```json
{
  "response": {
    "fb-fans-123": {"count": 150},
    "fb-fans-456": {"count": 250},
    "fb-post-published": {"count": 15},
    "fb-post-impressions": {"count": 5000}
  }
}
```

## 自动化检查

系统会自动：

1. **检查input文件夹**: 如果不存在会自动创建
2. **检查output文件夹**: 如果不存在会自动创建
3. **验证必要文件**: 检查input文件夹中的必要文件是否存在
4. **处理可选文件**: 根据存在的可选文件进行相应处理
5. **生成输出文件**: 将所有结果保存到output文件夹

## 错误处理

如果缺少必要文件，系统会显示：
```
错误：缺少必要的输入文件 input/dingding_fields.json
错误：缺少必要的输入文件 input/dingding_allfields.json
```

## 测试验证

运行测试脚本检查文件状态：
```bash
python simple_test.py
```

这会显示：
- ✅ 存在的文件
- ❌ 缺失的文件
- 文件夹状态
- 处理结果

## 优势

1. **清晰的文件组织**: 输入和输出完全分离
2. **易于管理**: 所有相关文件集中存放
3. **自动化处理**: 自动创建文件夹和检查文件
4. **错误提示**: 清晰的错误信息指导用户
5. **可扩展性**: 易于添加新的平台数据文件 