from langdetect import detect, detect_langs
import pandas as pd

def detect_language_example():
    """演示 langdetect 的基本用法"""
    
    # 测试文本
    texts = [
        "Hello, how are you today?",
        "你好，今天过得怎么样？",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "こんにちは、お元気ですか？"
    ]
    
    print("=== 语言检测示例 ===")
    for text in texts:
        try:
            # 检测主要语言
            lang = detect(text)
            # 检测所有可能的语言及其概率
            langs = detect_langs(text)
            print(f"文本: {text[:30]}...")
            print(f"主要语言: {lang}")
            print(f"所有语言: {langs}")
            print("-" * 50)
        except Exception as e:
            print(f"检测失败: {e}")

# def detect_language_in_dataframe():
#     """在 DataFrame 中检测语言"""
    
#     # 创建示例数据
#     data = {
#         'text': [
#             "Hello world",
#             "你好世界",
#             "Bonjour le monde",
#             "Hola mundo",
#             "こんにちは世界"
#         ],
#         'description': [
#             "This is English text",
#             "这是中文文本",
#             "Ceci est du texte français",
#             "Este es texto en español",
#             "これは日本語のテキストです"
#         ]
#     }
    
#     df = pd.DataFrame(data)
    
#     print("\n=== DataFrame 语言检测 ===")
    
#     # 检测 'text' 列的语言
#     df['text_language'] = df['text'].apply(lambda x: detect(x) if pd.notna(x) else None)
    
#     # 检测 'description' 列的语言
#     df['description_language'] = df['description'].apply(lambda x: detect(x) if pd.notna(x) else None)
    
#     print(df)
    
#     return df

# def filter_chinese_text():
#     """过滤出中文文本"""
    
#     texts = [
#         "Hello world",
#         "你好世界",
#         "Bonjour le monde",
#         "这是中文文本",
#         "こんにちは世界",
#         "Hola mundo"
#     ]
    
#     print("\n=== 过滤中文文本 ===")
    
#     chinese_texts = []
#     for text in texts:
#         try:
#             lang = detect(text)
#             if lang == 'zh-cn' or lang == 'zh-tw':
#                 chinese_texts.append(text)
#                 print(f"中文文本: {text}")
#         except:
#             continue
    
#     return chinese_texts

if __name__ == "__main__":
    # 运行所有示例
    detect_language_example()
    # df = detect_language_in_dataframe()
    # chinese_texts = filter_chinese_text() 