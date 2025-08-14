from langdetect import detect, detect_langs, LangDetectException
import pandas as pd
import re

class LanguageDetector:
    """语言检测工具类"""
    
    def __init__(self):
        # 语言代码映射
        self.language_names = {
            'zh-cn': '中文(简体)',
            'zh-tw': '中文(繁体)',
            'en': '英语',
            'ja': '日语',
            'ko': '韩语',
            'fr': '法语',
            'de': '德语',
            'es': '西班牙语',
            'pt': '葡萄牙语',
            'it': '意大利语',
            'ru': '俄语',
            'ar': '阿拉伯语',
            'hi': '印地语',
            'th': '泰语',
            'vi': '越南语'
        }
    
    def detect_language(self, text):
        """
        检测文本语言
        
        Args:
            text: 要检测的文本
            
        Returns:
            dict: 包含语言代码、语言名称和置信度的字典
        """
        if not text or pd.isna(text):
            return {'code': None, 'name': None, 'confidence': 0.0}
        
        try:
            # 检测主要语言
            lang_code = detect(text)
            
            # 获取所有语言及其概率
            languages = detect_langs(text)
            
            # 找到主要语言的置信度
            confidence = 0.0
            for lang in languages:
                if lang.lang == lang_code:
                    confidence = lang.prob
                    break
            
            # 获取语言名称
            lang_name = self.language_names.get(lang_code, lang_code)
            
            return {
                'code': lang_code,
                'name': lang_name,
                'confidence': confidence
            }
            
        except LangDetectException:
            return {'code': 'unknown', 'name': '未知', 'confidence': 0.0}
        except Exception as e:
            print(f"语言检测错误: {e}")
            return {'code': 'error', 'name': '错误', 'confidence': 0.0}
    
    def is_chinese(self, text):
        """
        检查文本是否为中文
        
        Args:
            text: 要检查的文本
            
        Returns:
            bool: 是否为中文
        """
        result = self.detect_language(text)
        return result['code'] in ['zh-cn', 'zh-tw']
    
    def is_english(self, text):
        """
        检查文本是否为英语
        
        Args:
            text: 要检查的文本
            
        Returns:
            bool: 是否为英语
        """
        result = self.detect_language(text)
        return result['code'] == 'en'
    
    def filter_by_language(self, texts, target_language='zh-cn'):
        """
        根据语言过滤文本列表
        
        Args:
            texts: 文本列表
            target_language: 目标语言代码
            
        Returns:
            list: 过滤后的文本列表
        """
        filtered_texts = []
        for text in texts:
            if pd.notna(text) and self.detect_language(text)['code'] == target_language:
                filtered_texts.append(text)
        return filtered_texts
    
    def detect_dataframe_languages(self, df, text_columns):
        """
        检测 DataFrame 中指定列的语言
        
        Args:
            df: pandas DataFrame
            text_columns: 要检测的列名列表
            
        Returns:
            DataFrame: 添加了语言检测结果的 DataFrame
        """
        result_df = df.copy()
        
        for col in text_columns:
            if col in df.columns:
                # 检测语言
                lang_results = df[col].apply(self.detect_language)
                
                # 添加语言代码列
                result_df[f'{col}_language_code'] = [r['code'] for r in lang_results]
                
                # 添加语言名称列
                result_df[f'{col}_language_name'] = [r['name'] for r in lang_results]
                
                # 添加置信度列
                result_df[f'{col}_confidence'] = [r['confidence'] for r in lang_results]
        
        return result_df
    
    def analyze_text_patterns(self, text):
        """
        分析文本模式，辅助语言检测
        
        Args:
            text: 要分析的文本
            
        Returns:
            dict: 包含各种模式分析结果的字典
        """
        if not text or pd.isna(text):
            return {}
        
        analysis = {
            'length': len(str(text)),
            'has_chinese_chars': bool(re.search(r'[\u4e00-\u9fff]', str(text))),
            'has_english_chars': bool(re.search(r'[a-zA-Z]', str(text))),
            'has_numbers': bool(re.search(r'\d', str(text))),
            'has_special_chars': bool(re.search(r'[^\w\s\u4e00-\u9fff]', str(text))),
            'chinese_char_count': len(re.findall(r'[\u4e00-\u9fff]', str(text))),
            'english_char_count': len(re.findall(r'[a-zA-Z]', str(text))),
            'number_count': len(re.findall(r'\d', str(text)))
        }
        
        return analysis

def main():
    """演示语言检测工具的使用"""
    
    detector = LanguageDetector()
    
    # 测试文本
    test_texts = [
        "Hello, how are you today?",
        "你好，今天过得怎么样？",
        "Bonjour, comment allez-vous?",
        "Hola, ¿cómo estás?",
        "こんにちは、お元気ですか？",
        "订单编号：123456",
        "Fee Item: Service Charge",
        "费用项目：服务费",
        "Mixed text 混合文本",
        ""
    ]
    
    print("=== 语言检测演示 ===")
    for text in test_texts:
        print(f"\n文本: {text}")
        
        # 语言检测
        lang_result = detector.detect_language(text)
        print(f"语言: {lang_result['name']} ({lang_result['code']})")
        print(f"置信度: {lang_result['confidence']:.3f}")
        
        # 模式分析
        pattern = detector.analyze_text_patterns(text)
        if pattern:
            print(f"文本长度: {pattern['length']}")
            print(f"包含中文字符: {pattern['has_chinese_chars']}")
            print(f"包含英文字符: {pattern['has_english_chars']}")
            print(f"中文字符数: {pattern['chinese_char_count']}")
            print(f"英文字符数: {pattern['english_char_count']}")
        
        print("-" * 50)
    
    # DataFrame 示例
    print("\n=== DataFrame 语言检测示例 ===")
    
    data = {
        'fee_name': [
            "Service Charge",
            "服务费",
            "手续费",
            "Processing Fee",
            "平台使用费"
        ],
        'description': [
            "Standard service fee",
            "标准服务费用",
            "交易手续费",
            "Processing and handling fee",
            "平台使用和服务费"
        ]
    }
    
    df = pd.DataFrame(data)
    print("原始数据:")
    print(df)
    
    # 检测语言
    result_df = detector.detect_dataframe_languages(df, ['fee_name', 'description'])
    print("\n添加语言检测结果:")
    print(result_df)

if __name__ == "__main__":
    main() 