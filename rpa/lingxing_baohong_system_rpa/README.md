# 领星宝弘系统RPA

## 项目概述

该项目是基于领星ERP系统的自动化处理工具，主要用于处理订单数据、生成订单链接、提取订单信息，并进行货币转换等操作。项目使用xbot RPA框架实现自动化流程，支持批量数据处理和多货币转换功能。

## 功能特性

- 📦 **订单数据提取**：从JSON文件中批量提取订单信息
- 🔗 **订单链接生成**：根据订单号和工单号自动生成ERP系统链接
- 💱 **货币转换**：支持多种货币符号识别和转换
- 🤖 **RPA自动化**：基于xbot框架的自动化流程
- 📊 **批量处理**：支持大批量订单数据的自动化处理
- 🌐 **多平台支持**：支持不同电商平台的订单数据格式
- 📝 **数据验证**：自动验证数据完整性和格式正确性

## 文件结构

```
Lingxing Baohong System RPA/
├── module1.py          # 核心数据处理模块
├── get_url.py          # URL生成和订单信息提取模块
├── dateoutput.py       # 日期输出处理模块
├── test.py             # 测试文件
└── README.md           # 项目说明文档
```

## 核心模块说明

### module1.py - 核心数据处理模块

**主要功能**：
- 批量读取和解析JSON数据
- 提取订单详细信息
- 货币符号识别和转换
- 数据格式化和验证

**核心函数**：
```python
# 批量提取t.json文件内容
batch_extract_from_tjson(tjson_path)

# 从领星JSON数据中提取订单信息
extract_data_from_lingxin_json(input_data)

# 货币符号转换
get_currency_code(currency_symbol)
```

**支持的数据提取字段**：
- 订单基本信息（订单号、工单号、平台等）
- 商品信息（SKU、数量、价格等）
- 客户信息（姓名、地址、联系方式等）
- 物流信息（运费、重量、尺寸等）
- 财务信息（货币、汇率、总金额等）

### get_url.py - URL生成和订单信息提取模块

**主要功能**：
- 根据订单号和工单号生成ERP系统链接
- 从JSON数据中提取订单信息
- URL参数编码和处理
- 链接有效性验证

**核心函数**：
```python
# 生成订单链接
generate_order_links(order_number, wo_number)

# 提取订单信息
extract_order_info(json_file_path_or_data)
```

**生成的链接格式**：
```
https://erp.lingxing.com/erp/mmulti/mpOrderDetail?detailType=showDetail&route=/mpOrderManagement&tag_name=mpOrderDetail&orderType=&orderNumber={订单号}&woNumber={工单号}
```

### dateoutput.py - 日期输出处理模块

**主要功能**：
- 日期格式化处理
- 时间戳转换
- 日期范围计算
- 时区处理

### test.py - 测试模块

**主要功能**：
- 单元测试用例
- 功能验证测试
- 性能测试
- 数据完整性测试

## 使用方法

### 基本使用流程

1. **准备数据文件**：
   - 确保有包含订单数据的JSON文件
   - 数据格式符合领星ERP系统标准

2. **批量提取订单数据**：
```python
from module1 import batch_extract_from_tjson

# 批量提取t.json文件中的订单数据
results = batch_extract_from_tjson('path/to/t.json')
print(f"成功提取 {len(results)} 条订单记录")
```

3. **生成订单链接**：
```python
from get_url import generate_order_links

# 根据订单号和工单号生成链接
order_number = "ORD123456789"
wo_number = "WO987654321"
links = generate_order_links(order_number, wo_number)
print(f"生成的链接: {links[0]}")
```

4. **提取单个订单信息**：
```python
from get_url import extract_order_info

# 从JSON数据中提取订单信息
order_info = extract_order_info('path/to/order.json')
if order_info:
    print("订单信息提取成功")
    for link in order_info:
        print(f"订单链接: {link}")
```

### 高级使用

**货币转换功能**：
```python
from module1 import get_currency_code

# 货币符号转换
currency_code = get_currency_code('$')  # 返回 'USD'
currency_code = get_currency_code('€')  # 返回 'EUR'
currency_code = get_currency_code('¥')  # 返回 'CNY'
```

**批量处理示例**：
```python
import json
from module1 import extract_data_from_lingxin_json

# 批量处理多个JSON文件
json_files = ['order1.json', 'order2.json', 'order3.json']
all_results = []

for file_path in json_files:
    try:
        result = extract_data_from_lingxin_json(file_path)
        all_results.append(result)
        print(f"成功处理文件: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")

print(f"总共处理了 {len(all_results)} 个文件")
```

## 数据格式说明

### 输入数据格式（JSON）

```json
{
  "order_number": "ORD123456789",
  "wo_number": "WO987654321",
  "platform": "Amazon",
  "customer_info": {
    "name": "客户姓名",
    "email": "customer@example.com",
    "address": "客户地址"
  },
  "items": [
    {
      "sku": "PROD-001",
      "quantity": 2,
      "price": 29.99,
      "currency": "USD"
    }
  ],
  "shipping": {
    "method": "Standard",
    "cost": 5.99,
    "weight": 1.5
  },
  "total_amount": 65.97,
  "currency": "USD",
  "order_date": "2024-01-15T10:30:00Z"
}
```

### 输出数据格式

```python
{
    'order_number': 'ORD123456789',
    'wo_number': 'WO987654321',
    'platform': 'Amazon',
    'customer_name': '客户姓名',
    'total_amount': 65.97,
    'currency_code': 'USD',
    'order_date': '2024-01-15',
    'item_count': 2,
    'shipping_cost': 5.99,
    'erp_link': 'https://erp.lingxing.com/erp/mmulti/mpOrderDetail?...'
}
```

## 货币支持

### 支持的货币符号

| 符号 | 货币代码 | 货币名称 |
|------|----------|----------|
| $ | USD | 美元 |
| € | EUR | 欧元 |
| £ | GBP | 英镑 |
| ¥ | CNY | 人民币 |
| ¥ | JPY | 日元 |
| ₹ | INR | 印度卢比 |
| C$ | CAD | 加拿大元 |
| A$ | AUD | 澳大利亚元 |
| ₩ | KRW | 韩元 |
| ₽ | RUB | 俄罗斯卢布 |

### 货币转换功能

系统支持两种货币转换模式：

1. **在线转换**（需要forex-python库）：
   - 实时汇率获取
   - 高精度转换
   - 支持更多货币

2. **离线转换**（内置映射）：
   - 快速响应
   - 无网络依赖
   - 基础货币支持

## RPA自动化流程

### xbot框架集成

项目基于xbot RPA框架，支持：
- 可视化流程设计
- 模块化调用
- 异常处理机制
- 日志记录功能

### 自动化流程示例

```python
import xbot
from xbot import print, sleep

def automated_order_processing():
    """自动化订单处理流程"""
    try:
        # 1. 读取订单数据
        print("开始读取订单数据...")
        orders = batch_extract_from_tjson('orders.json')
        
        # 2. 处理每个订单
        for i, order in enumerate(orders, 1):
            print(f"处理第 {i} 个订单...")
            
            # 生成订单链接
            links = generate_order_links(
                order.get('order_number'),
                order.get('wo_number')
            )
            
            # 保存处理结果
            order['erp_links'] = links
            
            # 添加延迟避免系统过载
            sleep(1)
        
        print(f"成功处理 {len(orders)} 个订单")
        return orders
        
    except Exception as e:
        print(f"自动化流程执行失败: {e}")
        return None
```

## 配置说明

### 环境配置

```python
# 基础配置
CONFIG = {
    'base_url': 'https://erp.lingxing.com',
    'timeout': 30,
    'retry_count': 3,
    'delay_between_requests': 1,
    'log_level': 'INFO'
}

# 货币配置
CURRENCY_CONFIG = {
    'default_currency': 'USD',
    'precision': 2,
    'use_online_rates': False
}
```

### 文件路径配置

```python
# 文件路径设置
FILE_PATHS = {
    'input_dir': './data/input/',
    'output_dir': './data/output/',
    'log_dir': './logs/',
    'temp_dir': './temp/'
}
```

## 依赖库

### 必需依赖
```python
xbot                # RPA自动化框架
json                # JSON数据处理
os                  # 操作系统接口
ast                 # 抽象语法树
urllib.parse        # URL解析
```

### 可选依赖
```python
forex-python        # 在线货币转换（可选）
requests           # HTTP请求（可选）
pandas             # 数据分析（可选）
```

### 安装依赖

```bash
# 安装基础依赖
pip install xbot

# 安装可选依赖（用于增强功能）
pip install forex-python requests pandas
```

## 错误处理

### 常见错误类型

1. **文件读取错误**：
   - JSON文件格式错误
   - 文件路径不存在
   - 权限不足

2. **数据格式错误**：
   - 必需字段缺失
   - 数据类型不匹配
   - 编码问题

3. **网络连接错误**：
   - URL生成失败
   - 网络超时
   - 服务器响应错误

### 错误处理示例

```python
def safe_extract_data(file_path):
    """安全的数据提取函数"""
    try:
        result = extract_data_from_lingxin_json(file_path)
        return result
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return None
    except json.JSONDecodeError:
        print(f"错误：文件 {file_path} 不是有效的JSON格式")
        return None
    except KeyError as e:
        print(f"错误：缺少必需字段 {e}")
        return None
    except Exception as e:
        print(f"未知错误：{e}")
        return None
```

## 性能优化

### 批量处理优化

```python
def optimized_batch_processing(file_list, batch_size=100):
    """优化的批量处理函数"""
    results = []
    
    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i + batch_size]
        batch_results = []
        
        for file_path in batch:
            result = extract_data_from_lingxin_json(file_path)
            if result:
                batch_results.append(result)
        
        results.extend(batch_results)
        print(f"已处理 {len(results)} / {len(file_list)} 个文件")
    
    return results
```

### 内存优化

- 使用生成器处理大文件
- 及时释放不需要的变量
- 分批处理大量数据

## 监控和日志

### 日志配置

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rpa_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 性能监控

```python
import time

def monitor_performance(func):
    """性能监控装饰器"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"函数 {func.__name__} 执行时间: {execution_time:.2f} 秒")
        
        return result
    return wrapper
```

## 版本信息

- **当前版本**: v1.0
- **最后更新**: 2025年1月
- **维护状态**: 活跃维护中
- **兼容性**: xbot框架 v2.0+

## 注意事项

1. **数据安全**: 确保订单数据的安全性和隐私保护
2. **系统负载**: 批量处理时注意控制并发数量
3. **网络稳定**: 确保网络连接稳定，避免数据丢失
4. **版本兼容**: 注意xbot框架版本兼容性
5. **错误处理**: 实现完善的错误处理和重试机制

## 技术支持

- 查看xbot官方文档
- 联系开发团队获取技术支持
- 提交问题到项目Issues页面

## 许可证

本项目遵循相关开源许可证，使用时请遵守相关条款。