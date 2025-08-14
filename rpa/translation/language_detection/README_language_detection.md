# 语言检测工具使用指南

## 安装依赖

```bash
pip install langdetect pandas
```

## 基本用法

### 1. 简单文本检测

```python
from langdetect import detect

# 检测单个文本
text = "你好，世界"
language = detect(text)
print(f"语言: {language}")  # 输出: zh-cn
```

### 2. 使用我们的工具类

```python
from language_detection_utils import LanguageDetector

detector = LanguageDetector()

# 检测语言
result = detector.detect_language("Hello world")
print(result)
# 输出: {'code': 'en', 'name': '英语', 'confidence': 0.714}

# 检查是否为中文
is_chinese = detector.is_chinese("你好")
print(is_chinese)  # 输出: True
```

### 3. 在 DataFrame 中使用

```python
import pandas as pd
from language_detection_utils import LanguageDetector

# 创建数据
data = {
    'fee_name': ["Service Charge", "服务费", "手续费"],
    'description': ["Standard fee", "标准费用", "交易费用"]
}
df = pd.DataFrame(data)

# 检测语言
detector = LanguageDetector()
result_df = detector.detect_dataframe_languages(df, ['fee_name', 'description'])

print(result_df)
```

## 主要功能

### LanguageDetector 类方法

1. **detect_language(text)**
   - 检测文本语言
   - 返回: `{'code': 'zh-cn', 'name': '中文(简体)', 'confidence': 0.999}`

2. **is_chinese(text)**
   - 检查是否为中文
   - 返回: `True/False`

3. **is_english(text)**
   - 检查是否为英语
   - 返回: `True/False`

4. **filter_by_language(texts, target_language)**
   - 过滤指定语言的文本
   - 返回: 过滤后的文本列表

5. **detect_dataframe_languages(df, text_columns)**
   - 检测 DataFrame 中指定列的语言
   - 返回: 添加了语言检测结果的 DataFrame

6. **analyze_text_patterns(text)**
   - 分析文本模式（字符类型、数量等）
   - 返回: 模式分析字典

## 支持的语言

- `zh-cn`: 中文(简体)
- `zh-tw`: 中文(繁体)
- `en`: 英语
- `ja`: 日语
- `ko`: 韩语
- `fr`: 法语
- `de`: 德语
- `es`: 西班牙语
- `pt`: 葡萄牙语
- `it`: 意大利语
- `ru`: 俄语
- `ar`: 阿拉伯语
- `hi`: 印地语
- `th`: 泰语
- `vi`: 越南语

## 实际应用示例

### 1. 过滤中文费用项目

```python
# 假设你有一个费用项目列表
fee_items = ["Service Charge", "服务费", "手续费", "Processing Fee", "平台使用费"]

# 过滤出中文费用项目
detector = LanguageDetector()
chinese_fees = detector.filter_by_language(fee_items, 'zh-cn')
print(chinese_fees)  # ['服务费', '手续费', '平台使用费']
```

### 2. 分析 Excel 数据中的语言分布

```python
import pandas as pd
from language_detection_utils import LanguageDetector

# 读取 Excel 文件
df = pd.read_excel('your_file.xlsx')

# 检测指定列的语言
detector = LanguageDetector()
result_df = detector.detect_dataframe_languages(df, ['fee_name', 'description'])

# 统计语言分布
language_counts = result_df['fee_name_language_code'].value_counts()
print("语言分布:")
print(language_counts)
```

### 3. 处理混合语言文本

```python
# 对于混合语言文本，可以分析字符模式
text = "Mixed text 混合文本"
pattern = detector.analyze_text_patterns(text)
print(pattern)
# 输出包含中英文字符数量的详细信息
```

## 注意事项

1. **短文本**: 对于很短的文本（少于3个字符），检测可能不准确
2. **混合语言**: 对于混合语言文本，会返回主要语言
3. **特殊字符**: 包含大量数字或特殊字符的文本可能影响检测准确性
4. **性能**: 处理大量文本时，建议批量处理以提高效率

## 错误处理

工具会自动处理以下情况：
- 空值或 NaN 值
- 检测失败的情况
- 未知语言

所有错误情况都会返回相应的默认值，不会导致程序崩溃。 