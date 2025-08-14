# FBA退货订单数据处理系统

## 📋 项目概述

这是一个用于处理Amazon FBA退货订单数据的自动化处理系统。系统能够自动筛选、清洗和分析退货数据，并生成结构化的报告。支持销量数据集成，自动匹配退货数据与销量数据，确保数据完整性。

## 🏗️ 代码架构

### 重构后的模块化设计

经过重构，代码采用了模块化设计，将不同的功能逻辑分离到独立的函数中，大大提升了代码的可读性和可维护性。

#### 核心组件

1. **FilterConfig 配置类**
   - 集中管理所有筛选配置
   - 包含国家列表、产品MSKU、必需列名等配置
   - 便于统一修改和维护

2. **数据处理函数**
   - `clean_and_preprocess_data()`: 数据清洗和预处理
   - `apply_business_filters()`: 应用业务筛选逻辑
   - `print_data_analysis()`: 打印数据分析报告
   - `create_sheet3_data()`: 创建客户问题分析数据结构
   - `save_results_to_excel()`: 保存结果到Excel
   - `convert_sales_data_format()`: 销量数据格式转换
   - `read_processed_file_content()`: 读取处理完成后的Excel文件内容（只读取处理后的结果数据，不包含原始数据）

3. **主处理函数**
   - `process_fba_returns()`: 主要的数据处理流程
   - `main()`: 程序入口点

## 🔧 功能特性

### 数据筛选条件

- **地区筛选**: 支持EU Amazon和US Amazon平台
- **产品筛选**: 针对特定MSKU产品（GL-BE3600, GL-X2000, GL-RM1等）
- **时间筛选**: 自动获取上周时间范围
- **内容筛选**: 过滤有效的买家备注

### 销量数据集成

- **多格式支持**: 支持字典格式和列表格式的销量数据输入
- **自动匹配**: 直接根据MSKU和平台名称匹配销量数据
- **数据完整性**: 确保所有销量数据中的SKU+平台组合都出现在最终结果中
- **零值处理**: 对于没有退货记录的销量数据，自动设置退货数量为0

### 输出格式

脚本会在原Excel文件中创建两个新的工作表：

#### "周度销量数据"
包含以下列：
- 地区/平台
- MSKU
- 销量
- 退货数量
- 退货开始日期
- 退货结束日期

#### "客户问题分析"
包含以下列：
- 來源
- 產品
- 平台
- 負責部門
- 問題總結
- 需要注意?
- 优先级
- 重要性
- 軟/硬件問題
- 项目部跟进措施及进展
- 評價原文
- 退貨原因
- 問題類型
- 電商運營改善策略
- 退貨地址
- MAC地址
- tracking No
- Order Number
- 获取数据日期（格式：YYYY-MM-DD，默认为当天）

## 📊 数据流程

```
原始Excel数据 
    ↓
数据清洗和预处理
    ↓
应用业务筛选条件
    ↓
生成分析报告
    ↓
销量数据格式转换（支持字典/列表格式）
    ↓
按MSKU和平台分组合计退货数量
    ↓
匹配销量数据（直接根据MSKU和平台名称）
    ↓
确保所有销量数据组合都出现在结果中
    ↓
创建"周度销量数据"和"客户问题分析"工作表
    ↓
保存到Excel文件
```

### 数据处理特点

1. **数据完整性保证**: 确保所有销量数据中的SKU+平台组合都会出现在最终结果中，即使没有对应的退货记录
2. **直接匹配**: 移除了复杂的平台映射逻辑，直接根据MSKU和平台名称进行匹配
3. **多格式支持**: 自动识别和转换字典格式和列表格式的销量数据
4. **零值处理**: 对于没有退货记录的销量数据，自动设置退货数量为0

## 🚀 使用方法

### 基本使用

```python
# 直接运行脚本
python data_pro.py

# 或者在代码中调用
import data_pro

# 基本使用（不带销量数据）
data_pro.main('your_file.xlsx')

# 带销量数据使用（字典格式）
sales_data = {
    "GL-BE3600": {"EU Amazon": 1000, "US Amazon": 800},
    "GL-X2000": {"EU Amazon": 1200, "US Amazon": 900},
    "GL-RM1": {"EU Amazon": 133, "US Amazon": 502}
}
data_pro.main('your_file.xlsx', sales_data)

# 带销量数据使用（列表格式）
sales_data = [
    {'SKU': 'GL-X2000', '平台': 'US Amazon', '数量': '29'}, 
    {'SKU': 'GL-BE3600', '平台': 'US Amazon', '数量': '581'}, 
    {'SKU': 'GL-RM1', '平台': 'US Amazon', '数量': '502'}, 
    {'SKU': 'GL-X2000', '平台': 'EU Amazon', '数量': '14'}, 
    {'SKU': 'GL-BE3600', '平台': 'EU Amazon', '数量': '150'},
    {'SKU': 'GL-RM1', '平台': 'EU Amazon', '数量': '133'},
    {'SKU': 'GL-BE3600', '平台': 'Shopee', '数量': '13'},
    {'SKU': 'GL-RM1', '平台': 'Shopee', '数量': '25'}
]
data_pro.main('your_file.xlsx', sales_data)

# 直接调用处理函数
data_pro.process_fba_returns('your_file.xlsx', sales_data)

# 读取处理完成后的文件内容
result = data_pro.read_processed_file_content('your_file.xlsx')
print(f"筛选后的退货订单数据: {len(result['筛选后的退货订单数据'])} 条")
print(f"周度销量数据: {len(result['周度销量数据'])} 条")
print(f"客户问题分析: {len(result['客户问题分析'])} 条")
```

### 参数说明
- `file_path`: Excel文件的完整路径（字符串类型，必需参数）
- `sales_data`: 可选的销量数据，支持两种格式：
  
  **字典格式**: `{"产品MSKU": {"平台名": 销量数量}}`
  ```python
  sales_data = {
      "GL-BE3600": {"EU Amazon": 1000, "US Amazon": 800},
      "GL-X2000": {"EU Amazon": 1200, "US Amazon": 900}
  }
  ```
  
  **列表格式**: `[{'SKU': 'MSKU', '平台': '平台名', '数量': '销量数量'}, ...]`
  ```python
  sales_data = [
      {'SKU': 'GL-X2000', '平台': 'US Amazon', '数量': '29'}, 
      {'SKU': 'GL-BE3600', '平台': 'US Amazon', '数量': '581'}, 
      {'SKU': 'GL-RM1', '平台': 'EU Amazon', '数量': '133'}
  ]
  ```
  
  - 如果不提供，函数仍可正常运行，只是销量数据为0
  - 列表格式会自动转换为字典格式进行处理
  - 支持的字段名: SKU/MSKU, 平台/platform, 数量/quantity/销量
  - 支持的平台名称: US Amazon, EU Amazon, Shopee, Walmart等
  - 系统会确保所有销量数据中的SKU+平台组合都出现在最终结果中

### 自定义配置

```python
from data_pro import FilterConfig

# 修改目标产品
FilterConfig.TARGET_MSKU = ["NEW-PRODUCT-001", "NEW-PRODUCT-002"]

# 添加新的目标国家
FilterConfig.EU_COUNTRIES.append('挪威')
```

## 📁 文件结构

```
翻译/
├── data_pro.py                 # 主要处理逻辑
├── verify_sales.py             # 销量数据验证脚本
├── test_refactored_code.py     # 测试脚本
├── README.md                   # 项目说明文档
└── [Excel文件]                 # 待处理的数据文件
```

## 🔍 代码重构优势

### 重构前的问题
- 所有逻辑混在一个大函数中
- 配置项散布在代码各处
- 难以测试和调试
- 代码可读性差

### 重构后的改进
- ✅ **模块化设计**: 每个函数职责单一明确
- ✅ **配置集中**: 所有配置项统一管理
- ✅ **易于测试**: 每个函数可独立测试
- ✅ **可读性强**: 主流程清晰，逻辑分明
- ✅ **易于维护**: 修改某个功能不影响其他部分

## 🧪 测试

### 功能测试
运行测试脚本验证代码功能：

```bash
python test_refactored_code.py
```

测试内容包括：
- 配置类功能测试
- 数据处理流程测试
- 代码结构验证

### 销量数据验证
运行验证脚本检查销量数据处理结果：

```bash
python verify_sales.py
```

验证内容包括：
- 销量数据统计和分析
- 退货数量统计和分析
- 按平台分组的数据统计
- 数据完整性检查

## ⚙️ 配置说明

### FilterConfig 配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| EU_COUNTRIES | 欧洲国家列表 | ['英国', '德国', '法国', ...] |
| US_COUNTRIES | 美洲国家列表 | ['美国', '加拿大', '墨西哥'] |
| TARGET_MSKU | 目标产品型号 | ["GL-BE3600", "GL-X2000"] |
| REQUIRED_COLUMNS | 必需的Excel列 | ['国家', 'MSKU', '退货数量', ...] |
| SHEET3_COLUMNS | Sheet3输出列 | ['來源', '產品', '平台', '获取数据日期', ...] |

## 📈 性能优化

- 使用pandas进行高效数据处理
- 避免重复的数据操作
- 优化内存使用
- 清晰的错误处理机制

## 🛠️ 错误处理和故障排除

### 常见错误

#### 1. "Invalid file path or buffer object type: <class 'dict'>"
**原因**: 传递了字典类型而不是文件路径字符串给函数
**解决方案**: 
```python
# ❌ 错误的调用方式
process_fba_returns({"file": "test.xlsx"})

# ✅ 正确的调用方式
process_fba_returns("test.xlsx")
process_fba_returns("test.xlsx", {"product1": {"US Amazon": 100}})  # 带销量数据
```

#### 2. 参数类型错误
**原因**: sales_data参数不是字典或列表类型
**解决方案**:
```python
# ❌ 错误的sales_data类型
process_fba_returns("test.xlsx", "not_a_dict")

# ✅ 正确的sales_data类型（字典格式）
sales_data = {"GL-BE3600": {"EU Amazon": 1000, "US Amazon": 800}}
process_fba_returns("test.xlsx", sales_data)

# ✅ 正确的sales_data类型（列表格式）
sales_data = [{'SKU': 'GL-BE3600', '平台': 'US Amazon', '数量': '800'}]
process_fba_returns("test.xlsx", sales_data)
```

#### 3. 文件被占用错误
**原因**: Excel文件被其他程序（如Excel）打开
**解决方案**: 关闭Excel程序后重新运行脚本

#### 4. 平台名称不匹配
**原因**: 销量数据中的平台名称与系统预期不一致
**解决方案**: 使用标准平台名称（US Amazon, EU Amazon, Shopee, Walmart）

#### 5. 销量数据行数不匹配
**原因**: 输入的销量数据项数与输出行数不一致
**解决方案**: 系统会自动确保所有销量数据中的SKU+平台组合都出现在最终结果中

### 调试技巧
1. 使用 `verify_sales.py` 验证处理结果
2. 检查销量数据格式是否正确
3. 确认平台名称使用标准格式
4. 使用调试模式查看数据处理过程
5. 确保文件路径使用绝对路径或正确的相对路径

## 🔄 版本历史

### v2.3.0 (当前版本)
- ✅ 移除平台映射逻辑，直接使用平台名称匹配
- ✅ 删除退货率列，简化数据结构
- ✅ 确保所有销量数据中的SKU+平台组合都出现在最终结果中
- ✅ 更新销量数据平台名称为US Amazon和EU Amazon
- ✅ 添加verify_sales.py验证脚本
- ✅ 优化数据完整性处理逻辑
- ✅ 改进错误处理和调试功能

### v2.2.0
- ✅ 添加列表格式销量数据支持
- ✅ 自动转换列表格式为字典格式
- ✅ 支持多种字段名变体（SKU/MSKU, 平台/platform, 数量/quantity/销量）
- ✅ 更新工作表名称：Sheet2→"周度销量数据"，Sheet3→"客户问题分析"
- ✅ 增强数据格式兼容性和错误处理
- ✅ 添加列表格式使用示例和测试

### v2.1.0
- ✅ 添加销量数据支持和退货比例计算
- ✅ 增强参数类型检查和错误处理
- ✅ 添加详细的错误信息和调试功能
- ✅ 创建使用示例和测试脚本
- ✅ 改进文档和故障排除指南

### v2.0.0
- ✅ 重构代码结构，提高可读性和可维护性
- ✅ 将筛选逻辑抽离为独立函数
- ✅ 添加配置类统一管理筛选条件
- ✅ 增强错误处理和数据验证
- ✅ 优化数据处理流程
- ✅ 添加详细的代码注释和文档

### v1.0.0
- ✅ 基础的数据处理功能
- ✅ Excel文件读取和写入
- ✅ 基本筛选逻辑

## 🤝 贡献指南

1. 修改配置时，请更新 `FilterConfig` 类
2. 添加新功能时，请创建独立的函数
3. 确保所有修改都有相应的测试
4. 保持代码风格一致性

## 📞 支持

如有问题或建议，请联系开发团队。