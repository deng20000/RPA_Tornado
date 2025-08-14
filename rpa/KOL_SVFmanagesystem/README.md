# KOL/SVF管理系统

## 项目概述

该系统用于管理KOL（Key Opinion Leader）和SVF（Social Video Feedback）数据，每天自动查看不同网站的数据（如观看量、评论数等），并将数据写入钉钉多维表格。系统支持多平台数据采集，特别针对YouTube平台进行了深度优化。

## 功能特性

- 📊 **多平台数据采集**：支持YouTube等多个社交媒体平台
- 🔄 **自动数据更新**：定时获取最新的观看量、点赞数、评论数等数据
- 📋 **钉钉集成**：自动将数据同步到钉钉多维表格
- 🎯 **YouTube专项支持**：专门针对YouTube平台的数据提取和分析
- 📈 **数据分析**：提供订阅者、观看量、互动数据的统计分析
- 🔍 **智能筛选**：支持按平台、时间、数据类型进行筛选

## 文件结构

```
KOL_SVFmanagesystem/
├── extract_data.py        # 数据提取主模块
├── update_extract_data.py # 数据更新模块
├── youtubeapi.py          # YouTube API接口模块
├── 1.txt                  # 配置或数据文件
└── README.md              # 项目说明文档
```

## 核心模块说明

### extract_data.py
数据提取主模块，负责：
- 从JSON文件中提取YouTube记录
- 筛选特定平台的数据
- 处理链接和数据验证
- 导出处理后的数据

**主要功能**：
```python
# 提取YouTube平台记录
records = extract_youtube_records('text.json')

# 获取特定ID的记录
record = get_record_by_id('text.json', record_id)

# 导出数据到JSON
export_to_json(data, 'output.json')
```

### update_extract_data.py
数据更新模块，负责：
- 定期更新已有数据
- 增量数据处理
- 数据同步管理
- 错误处理和重试机制

### youtubeapi.py
YouTube API接口模块，负责：
- YouTube API调用
- 视频数据获取
- 频道信息提取
- API配额管理

## 数据结构

### 输入数据格式
```json
[
  {
    "id": "记录ID",
    "fields": {
      "Platforms": [{"name": "Youtube"}],
      "Review Link": {"link": "视频链接"},
      "Views": "观看量",
      "Likes": "点赞数",
      "Comments": "评论数",
      "Subscribers": "订阅者数"
    },
    "link": "记录链接"
  }
]
```

### 输出数据格式
```json
{
  "记录ID": {
    "Views": "观看量",
    "Likes": "点赞数", 
    "Comments": "评论数",
    "Subscribers": "订阅者数",
    "link": "记录链接"
  },
  "Review Link": "视频链接"
}
```

## 使用方法

### 基本使用

1. **提取YouTube数据**：
   ```python
   from extract_data import extract_youtube_records
   
   # 从JSON文件提取YouTube记录
   records = extract_youtube_records('text.json')
   print(f"找到 {len(records)} 条YouTube记录")
   ```

2. **获取特定记录**：
   ```python
   from extract_data import get_record_by_id
   
   # 获取指定ID的记录
   record = get_record_by_id('text.json', 'record_id')
   if record:
       print("记录详情:", record)
   ```

3. **导出数据**：
   ```python
   from extract_data import export_to_json
   
   # 导出数据到文件
   export_to_json(data, 'output.json')
   ```

### 交互式使用

运行主程序进行交互式操作：
```bash
python extract_data.py
```

系统会显示所有YouTube记录，用户可以选择要导出的记录ID。

## 数据采集指标

### YouTube平台指标
- **Views（观看量）**: 视频总观看次数
- **Likes（点赞数）**: 视频获得的点赞数量
- **Comments（评论数）**: 视频下的评论总数
- **Subscribers（订阅者）**: 频道订阅者数量

### 数据验证
系统会自动验证：
- 链接有效性检查
- 数据完整性验证
- 格式正确性校验
- 缺失数据处理（标记为'-1'）

## 配置说明

### 平台配置
```python
# 支持的平台列表
SUPPORTED_PLATFORMS = ['Youtube', 'Facebook', 'Instagram', 'TikTok']

# 必需字段配置
REQUIRED_FIELDS = ['Views', 'Likes', 'Comments', 'Subscribers']
```

### API配置
- YouTube API密钥配置
- 请求频率限制设置
- 错误重试次数配置

## 依赖库

```python
import json          # JSON数据处理
import requests      # HTTP请求（用于API调用）
import time          # 时间处理
import logging       # 日志记录
```

## 安装依赖

```bash
pip install requests
```

## 错误处理

### 常见错误类型
1. **链接无效**: Review Link为'-1'或链接格式错误
2. **数据缺失**: 必需字段为空或不存在
3. **API限制**: YouTube API配额超限
4. **网络错误**: 请求超时或连接失败

### 错误处理机制
- 自动重试机制
- 错误日志记录
- 数据备份和恢复
- 异常状态通知

## 数据流程

1. **数据读取**: 从JSON文件或API获取原始数据
2. **平台筛选**: 筛选出YouTube平台的记录
3. **数据验证**: 检查链接有效性和数据完整性
4. **数据提取**: 提取关键指标数据
5. **格式转换**: 转换为标准输出格式
6. **数据导出**: 保存到文件或同步到钉钉

## 定时任务

### 自动更新配置
```python
# 每日更新时间设置
UPDATE_TIME = "09:00"  # 每天上午9点更新

# 更新频率设置
UPDATE_INTERVAL = 24  # 24小时更新一次
```

### 钉钉集成
- 自动同步到钉钉多维表格
- 数据变化通知
- 异常情况报警

## 监控和维护

### 数据质量监控
- 数据完整性检查
- 异常值检测
- 趋势分析报告

### 系统维护
- 定期清理临时文件
- API配额使用监控
- 性能优化建议

## 版本信息

- **当前版本**: v1.0
- **最后更新**: 2025年1月
- **维护状态**: 活跃维护中

## 注意事项

1. **API限制**: 注意YouTube API的调用频率限制
2. **数据隐私**: 确保遵守各平台的数据使用政策
3. **链接有效性**: 定期检查和更新失效链接
4. **数据备份**: 定期备份重要数据

## 技术支持

如有问题或建议，请联系开发团队。系统支持扩展到其他社交媒体平台，可根据业务需求进行定制开发。