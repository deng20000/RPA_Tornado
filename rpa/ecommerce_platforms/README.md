# 电商平台RPA工具集

## 项目概述

本目录包含针对各大电商平台的RPA自动化处理工具，用于数据采集、订单处理、库存管理等业务流程自动化。

## 平台工具

### 速卖通 (AliExpress)
- **文件**: `aliexpress_data_processor.py`
- **功能**: 速卖通领星后台数据处理
- **主要特性**:
  - 处理合并单元格并填充数据
  - 后台订单数据格式化
  - 订单状态更新和跟踪
  - 多仓库发货数据处理
  - 半托仓发货数据管理
  - 自动创建核对表单

### 京东 (JingDong)
- **目录**: `jingdong/`
- **功能**: 京东平台数据处理
- **主要文件**:
  - `jingdong.py`: 主要处理逻辑
  - `dateprocessing.py`: 日期数据处理
  - `process_jingdong_data.py`: 数据处理工具
  - `inspect_excel.py`: Excel文件检查工具

### Shopee
- **目录**: `shopee/`
- **功能**: Shopee平台数据处理
- **主要文件**:
  - `shopee_processing.py`: Shopee数据处理主程序

### Google Watch
- **目录**: `google_watch/`
- **功能**: Google数据监控和表格处理
- **主要文件**:
  - `google_data.py`: Google数据处理
  - `check_sheets.py`: 表格检查工具
  - `tests/`: 测试文件目录

## 使用说明

### 环境要求
- Python 3.8+
- pandas, numpy, openpyxl 等依赖包
- 相应平台的API访问权限

### 快速开始

1. **安装依赖**
   ```bash
   pip install pandas numpy openpyxl
   ```

2. **运行速卖通数据处理器**
   ```bash
   python aliexpress_data_processor.py
   ```

3. **运行其他平台工具**
   ```bash
   # 京东数据处理
   python jingdong/jingdong.py
   
   # Shopee数据处理
   python shopee/shopee_processing.py
   
   # Google数据监控
   python google_watch/google_data.py
   ```

## 注意事项

1. **文件路径**: 确保输入文件路径正确
2. **文件权限**: 确保Excel文件未被其他程序占用
3. **数据备份**: 处理前请备份原始数据
4. **错误处理**: 程序包含详细的错误提示和日志输出

## 维护说明

- 定期更新平台API接口
- 根据平台规则变化调整处理逻辑
- 添加新的测试用例确保功能稳定性