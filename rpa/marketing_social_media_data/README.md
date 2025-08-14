# 市场部社媒账号数据处理系统

## 项目概述

这是一个用于处理社交媒体平台数据的系统，支持多平台数据整合和处理。系统采用双主线处理架构，能够处理钉钉多维表数据和各社交媒体平台的源数据。

## 系统架构

### 双主线处理
1. **主线1：钉钉多维表数据处理**
   - 处理钉钉多维表的字段信息和数据记录
   - 筛选昨天数据，提取基础信息
   - 标准化各平台的字段列表
   - 生成优化的数据结构

2. **主线2：网站源数据处理**
   - 处理各社交媒体平台的原始数据
   - 实现字段映射和数据转换
   - 支持Facebook、Youtube、Instagram、LinkedIn、X等平台

### 支持平台
- **Facebook**: 粉丝数、发布内容、互动数据等
- **Youtube**: 订阅者、观看量、互动数据等
- **Instagram**: 关注者、互动、浏览量等
- **LinkedIn**: 关注者、发布内容、页面数据等
- **X**: 关注者、推文数据等

## 文件结构

```
市场部社媒账号数据/
├── main_data_process.py      # 主程序入口
├── platform_config.py        # 平台配置文件
├── facebook_processor.py     # Facebook数据处理器
├── test_processor.py         # 测试脚本
├── 数据处理流程图.md         # 流程图和伪代码设计
├── README.md                # 项目说明文档
├── dingding_fields.json     # 钉钉字段数据（输入）
├── dingding_allfields.json  # 钉钉所有数据（输入）
├── fb_fetch_inf.json       # Facebook原始数据（输入）
└── optimized_data_structure_update.json  # 最终输出文件
```

## 核心功能

### 1. 数据筛选
- 自动筛选昨天的数据记录
- 支持多种数据格式的解析

### 2. 字段标准化
- 为不同平台定义标准字段列表
- 自动映射平台特定字段到标准字段

### 3. 数据映射
- 使用前缀模糊匹配进行字段映射
- 支持jsonpath模板提取数据
- 自动聚合多个匹配字段的值

### 4. 结构优化
- 采用`fields_dict + records`的优化结构
- 减少数据冗余，提高查询效率

## 使用方法

### 1. 环境准备
确保Python环境中安装了必要的依赖：
```bash
pip install json datetime typing
```

### 2. 输入文件准备
- `dingding_fields.json`: 钉钉多维表字段信息
- `dingding_allfields.json`: 钉钉多维表所有数据
- `fb_fetch_inf.json`: Facebook原始数据（可选）
- 其他平台的源数据文件（可选）

### 3. 运行程序
```bash
python main_data_process.py
```

### 4. 运行测试
```bash
python test_processor.py
```

## 输出文件

### 主要输出
- `optimized_data_structure_update.json`: 最终优化的数据结构
- `mapping_report.json`: 映射报告，包含成功率统计

### 中间文件
- `fb_fetch_inf_update.json`: Facebook处理后的数据
- 其他平台的更新文件（如存在）

## 数据结构

### 优化数据结构示例
```json
{
  "metadata": {
    "creation_date": "2024-12-19 10:30:00",
    "yesterday_date": "2024.12",
    "total_records": 3,
    "total_fields": 4,
    "description": "优化的数据结构，结合记录ID和字段映射"
  },
  "fields_dict": {
    "field_1": "New Fans",
    "field_2": "Posts Published",
    "field_3": "Posts Impressions",
    "field_4": "Posts Engagement"
  },
  "records": {
    "record_1": {
      "basic_info": {
        "time": "2024.12",
        "social_account": "TestAccount",
        "channel": "FB",
        "raw_value": "2024.12+TestAccount+FB"
      },
      "available_fields": [
        "New Fans", "Posts Published", "Posts Impressions",
        "Posts Engagement", "Posts Reactions", "Posts Comments",
        "Posts Shares", "Posts Video Plays"
      ],
      "fields": {
        "New Fans": 400,
        "Posts Published": 15,
        "Posts Impressions": 5000,
        "Posts Engagement": 300
      }
    }
  }
}
```

## 扩展性

### 添加新平台
1. 在`platform_config.py`中添加新平台的字段定义
2. 创建对应的处理器类（参考`facebook_processor.py`）
3. 在主程序中添加新平台的处理逻辑

### 自定义字段映射
1. 修改`platform_config.py`中的字段映射关系
2. 更新对应处理器的映射逻辑

## 错误处理

系统包含完善的错误处理机制：
- 文件不存在检查
- JSON格式验证
- 数据格式异常处理
- 映射失败统计

## 性能优化

- 使用前缀匹配减少遍历次数
- 优化数据结构减少内存占用
- 支持增量更新，避免重复处理

## 维护说明

- 定期更新平台字段映射关系
- 监控映射成功率
- 根据新平台API调整数据处理逻辑

## 联系信息

如有问题或建议，请联系开发团队。 