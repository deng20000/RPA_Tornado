from polyglot.detect import Detector
import pandas as pd

def polyglot_detect_example():
    """演示 polyglot 的基本用法"""
    
    # 测试文本
    texts = [
        "Hello, how are you today?",
        "你好，今天过得怎么样？",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "こんにちは、お元気ですか？"
    ]
    
    print("=== Polyglot 语言检测示例 ===")
    for text in texts:
        try:
            # 创建检测器
            detector = Detector(text)
            
            # 获取主要语言
            primary_lang = detector.language
            # 获取所有检测到的语言
            languages = detector.languages
            
            print(f"文本: {text[:30]}...")
            print(f"主要语言: {primary_lang.name} (代码: {primary_lang.code})")
            print(f"置信度: {primary_lang.confidence:.2f}")
            print(f"所有语言: {[(lang.name, lang.code, lang.confidence) for lang in languages]}")
            print("-" * 50)
        except Exception as e:
            print(f"检测失败: {e}")

def polyglot_dataframe_example():
    """在 DataFrame 中使用 polyglot"""
    
    # 创建示例数据
    data = {
        'text': [
            "Hello world",
            "你好世界",
            "Bonjour le monde",
            "Hola mundo",
            "こんにちは世界"
        ],
        'description': [
            "This is English text",
            "这是中文文本",
            "Ceci est du texte français",
            "Este es texto en español",
            "これは日本語のテキストです"
        ]
    }
    
    df = pd.DataFrame(data)
    
    print("\n=== Polyglot DataFrame 语言检测 ===")
    
    def detect_lang(text):
        """检测文本语言"""
        if pd.isna(text):
            return None
        try:
            detector = Detector(text)
            return detector.language.code
        except:
            return None
    
    # 检测语言
    df['text_language'] = df['text'].apply(detect_lang)
    df['description_language'] = df['description'].apply(detect_lang)
    
    print(df)
    
    return df

def compare_langdetect_polyglot():
    """比较 langdetect 和 polyglot 的结果"""
    
    from langdetect import detect
    
    texts = [
        "Hello world",
        "你好世界",
        "Bonjour le monde",
        "Hola mundo",
        "こんにちは世界"
    ]
    
    print("\n=== 比较 langdetect 和 polyglot ===")
    print(f"{'文本':<20} {'langdetect':<15} {'polyglot':<15}")
    print("-" * 50)
    
    for text in texts:
        try:
            # langdetect
            langdetect_result = detect(text)
            
            # polyglot
            detector = Detector(text)
            polyglot_result = detector.language.code
            
            print(f"{text[:18]:<20} {langdetect_result:<15} {polyglot_result:<15}")
        except Exception as e:
            print(f"{text[:18]:<20} {'ERROR':<15} {'ERROR':<15}")

if __name__ == "__main__":
    # 运行所有示例
    polyglot_detect_example()
    df = polyglot_dataframe_example()
    compare_langdetect_polyglot() 