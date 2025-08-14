# 退货追踪数据处理模块

## 概述

该模块用于处理退货订单数据，将JSON格式的订单数据按地区和平台分类，并导出为Excel文件。支持亚马逊和Shopify两个平台的订单处理，按美国、欧洲、英国三个地区进行分类。

## 功能特性

- ✅ **JSON数据解析**：安全解析JSON格式的订单数据文件
- ✅ **多平台支持**：支持亚马逊和Shopify两个电商平台
- ✅ **地区分类**：按美国、欧洲、英国三个地区自动分类
- ✅ **Excel导出**：为每个地区生成独立的Excel工作簿
- ✅ **数据验证**：包含完整的错误处理和数据验证机制
- ✅ **时间格式化**：自动将时间戳转换为可读的日期格式

## 文件结构

```
Return_tracking/
├── Return_tracking_processing.py  # 主处理模块
├── filter_amazon_orders.py        # 亚马逊订单过滤器
├── test.json                      # 测试数据文件（需要用户提供）
└── README.md                      # 本文档
```

## 依赖库

```python
import json          # JSON数据处理
import openpyxl      # Excel文件操作
from datetime import datetime  # 日期时间处理
import os           # 文件路径操作
```

## 安装依赖

```bash
pip install openpyxl
```

## 数据格式

### 输入数据格式

#### 支持的输入类型
模块支持两种输入方式：
1. **JSON文件路径**：传入JSON文件的路径字符串
2. **数据列表**：直接传入包含订单数据的Python列表

#### JSON文件格式
输入的JSON文件应包含订单数组，每个订单包含以下字段：

```json
[
  {
    "id": "订单ID",
    "fields": {
      "shopify站点": [{"name": "Amazon US"}],  // 或 "Shopify站点", "shopify_site"
      "订单号": "订单编号",
      "产品型号": [{"name": "产品型号名称"}],
      "数量": "订单数量",
      "购买渠道": {"name": "渠道名称"},
      "退货时间": "时间戳（毫秒）",
      "购买时间": "时间戳（毫秒）",
      "退货点": "退货地点",
      "客户是否寄回(寄回单号）": "寄回信息"
    }
  }
]
```

#### 数据列表格式
直接传入的数据列表格式与JSON文件内容相同：

```python
data_list = [
    {
        "id": "订单ID",
        "fields": {
            "shopify站点": [{"name": "Amazon US"}],
            "订单号": "订单编号",
            "产品型号": [{"name": "产品型号名称"}],
            "数量": "订单数量",
            "购买渠道": {"name": "渠道名称"},
            "退货时间": "时间戳（毫秒）",
            "购买时间": "时间戳（毫秒）",
            "退货点": "退货地点",
            "客户是否寄回(寄回单号）": "寄回信息"
        }
    }
]
```

### 输出数据格式（Excel）

每个地区生成一个Excel文件，包含三个工作表：

1. **亚马逊-买家退货-地区名**：亚马逊平台的退货订单
2. **shopfiy-地区名买家退货**：Shopify平台的退货订单  
3. **亚马逊移除-地区名**：空白表格（预留用于手动填写）

每个工作表包含以下列：

| 列名 | 说明 |
|------|------|
| 表中来源数据 | 固定值："退货统计表" |
| 店铺 | 店铺名称 |
| 订单号 | 订单编号 |
| 产品型号 | 产品型号名称 |
| 数量 | 订单数量 |
| 购买渠道 | 购买渠道名称 |
| 退货时间 | 退货日期（YYYY-MM-DD格式） |
| 购买时间 | 购买日期（YYYY-MM-DD格式） |
| 退货点 | 退货地点 |
| 客户是否寄回 | 客户寄回信息 |

## 使用方法

### 基本使用

1. **准备数据文件**：将订单数据保存为 `test.json` 文件，放在与脚本相同的目录下

2. **运行脚本**：
   ```bash
   python Return_tracking_processing.py
   ```

3. **查看结果**：脚本会在同目录下生成三个Excel文件：
   - `YYYY年MM月DD日退货追踪(美国).xlsx`
   - `YYYY年MM月DD日退货追踪(欧洲).xlsx`
   - `YYYY年MM月DD日退货追踪(英国).xlsx`

### 方式1：从JSON文件处理
```python
from Return_tracking_processing import process_orders, export_to_excel

# 处理JSON文件中的订单数据
results = process_orders('test.json')

# 导出到Excel
export_to_excel(results)

# 查看统计结果
print(f"亚马逊美国订单: {len(results['US_orders'])}")
print(f"亚马逊欧洲订单: {len(results['EU_orders'])}")
print(f"亚马逊英国订单: {len(results['UK_orders'])}")
print(f"Shopify美国订单: {len(results['shopfiy_US'])}")
print(f"Shopify欧洲订单: {len(results['shopfiy_EU'])}")
print(f"Shopify英国订单: {len(results['shopfiy_UK'])}")
```

### 方式2：直接传入数据列表
```python
from Return_tracking_processing import process_orders, export_to_excel

# 准备数据列表
order_data = [
    {
        "id": "order_001",
        "fields": {
            "shopify站点": [{"name": "Amazon US"}],
            "订单号": "US-12345",
            "产品型号": [{"name": "产品A"}],
            "数量": 2,
            "购买渠道": {"name": "Amazon US"},
            "退货时间": "1640995200000",
            "购买时间": "1640908800000",
            "退货点": "美国仓库",
            "客户是否寄回(寄回单号）": "已寄回-US123"
        }
    },
    {
        "id": "order_002", 
        "fields": {
            "shopify站点": [{"name": "Shopify UK"}],
            "订单号": "UK-67890",
            "产品型号": [{"name": "产品B"}],
            "数量": 1,
            "购买渠道": {"name": "Shopify UK"},
            "退货时间": "1641081600000",
            "购买时间": "1640995200000",
            "退货点": "英国仓库",
            "客户是否寄回(寄回单号）": "未寄回"
        }
    }
]

# 直接处理数据列表
results = process_orders(order_data)

# 导出到Excel
export_to_excel(results)

# 查看统计结果
print(f"处理了 {sum(len(v) for v in results.values())} 条订单")
```

## 核心函数说明

### `process_orders(input_data)`

处理订单数据并按地区和平台分类。

**参数：**
- `input_data` (str | list): 
  - 如果是字符串：JSON数据文件路径
  - 如果是列表：包含订单数据的Python列表（格式与JSON文件内容相同）

**返回值：**
- `dict`: 包含各地区和平台订单数据的字典
  - `US_orders`: 亚马逊美国订单列表
  - `EU_orders`: 亚马逊欧洲订单列表  
  - `UK_orders`: 亚马逊英国订单列表
  - `shopfiy_US`: Shopify美国订单列表
  - `shopfiy_EU`: Shopify欧洲订单列表
  - `shopfiy_UK`: Shopify英国订单列表

**异常：**
- `FileNotFoundError`: 当传入文件路径但文件不存在时
- `json.JSONDecodeError`: 当JSON文件格式错误时
- `TypeError`: 当传入的数据类型不正确时
- `ValueError`: 当传入的数据格式不符合要求时

### `export_to_excel(results)`

将分类后的订单数据导出到Excel文件。

**参数：**
- `results` (dict): 由 `process_orders()` 返回的结果字典

**返回值：**
- `None`

### `safe_get(data, keys, default='')`

安全获取嵌套字典的值。

**参数：**
- `data` (dict): 要查询的字典数据
- `keys` (list): 键的路径列表
- `default`: 默认返回值

**返回值：**
- 获取到的值或默认值

## 地区分类规则

### 亚马逊平台

- **美国**：店铺名称包含 "Amazon US"
- **英国**：店铺名称包含 "Amazon UK"  
- **欧洲**：店铺名称包含 "Amazon" + 欧洲国家代码
  - 支持的国家代码：IT, DE, FR, ES, NL, SE, TR, PL, BE

### Shopify平台

- **美国**：店铺名称包含 "US" 且不包含 "Amazon"
- **英国**：店铺名称包含 "UK" 且不包含 "Amazon"
- **欧洲**：店铺名称包含欧洲国家代码且不包含 "Amazon"

## 错误处理

程序包含完善的错误处理机制：

1. **文件读取错误**：检查文件是否存在和可读
2. **JSON解析错误**：提供详细的错误位置信息
3. **数据格式错误**：安全处理缺失或格式错误的字段
4. **Excel导出错误**：捕获并报告文件写入错误

## 注意事项

1. **文件编码**：确保JSON文件使用UTF-8编码
2. **时间格式**：时间戳应为毫秒级别的数值
3. **站点字段**：支持多种站点字段名称格式（shopify站点、Shopify站点、shopify_site）
4. **内存使用**：大文件处理时注意内存使用情况

## 常见问题

### Q: 为什么某些订单没有被分类？

A: 检查以下几点：
- 订单是否包含有效的站点信息
- 站点名称是否符合分类规则
- JSON数据格式是否正确

### Q: 时间显示为空白怎么办？

A: 确保时间字段包含有效的时间戳（毫秒），如果时间戳为0或无效，会显示为空白。

### Q: Excel文件无法打开？

A: 检查：
- 文件路径是否有写入权限
- 是否有其他程序正在使用同名文件
- openpyxl库是否正确安装

## 更新日志

- **v1.0.0**: 初始版本，支持基本的订单分类和Excel导出功能
- 添加了完整的中文注释和错误处理机制

## 联系方式

如有问题或建议，请联系开发团队。