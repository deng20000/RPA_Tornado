"""
测试脚本
验证数据处理器的各项功能
"""

import json
import os
from main_data_process import DataProcessor
from facebook_processor import FacebookProcessor
from platform_config import get_platform_fields, get_field_mapping

def test_platform_config():
    """测试平台配置功能"""
    print("=== 测试平台配置功能 ===")
    
    # 测试获取平台字段
    fb_fields = get_platform_fields("FaceBook")
    print(f"Facebook字段: {fb_fields}")
    
    yt_fields = get_platform_fields("Youtube")
    print(f"Youtube字段: {yt_fields}")
    
    # 测试获取字段映射
    fb_mapping = get_field_mapping("facebook")
    print(f"Facebook映射: {fb_mapping}")
    
    print("平台配置测试完成\n")

def test_facebook_processor():
    """测试Facebook处理器"""
    print("=== 测试Facebook处理器 ===")
    
    processor = FacebookProcessor()
    
    # 测试前缀匹配
    test_data = {
        "fb-fans-123": {"count": 100},
        "fb-fans-456": {"count": 200},
        "fb-post-published": {"count": 10},
        "other-data": {"count": 999}
    }
    
    matched_keys = processor.find_keys_by_prefix(test_data, "fb-fans")
    print(f"匹配的键: {matched_keys}")
    
    # 测试值提取
    values = processor.extract_value_by_jsonpath(test_data, matched_keys)
    print(f"提取的值: {values}")
    
    # 测试字段映射
    mapped_data = processor.map_facebook_fields(test_data)
    print(f"映射结果: {mapped_data}")
    
    # 测试统计信息
    stats = processor.get_mapping_statistics(mapped_data)
    print(f"统计信息: {stats}")
    
    print("Facebook处理器测试完成\n")

def test_data_processor():
    """测试数据处理器"""
    print("=== 测试数据处理器 ===")
    
    processor = DataProcessor()
    
    # 测试文件检查
    files_exist = processor.check_input_files()
    print(f"输入文件检查: {files_exist}")
    
    # 测试日期获取
    yesterday = processor.get_yesterday_date()
    print(f"昨天日期: {yesterday}")
    
    # 测试源文件获取
    source_files = processor.get_source_files()
    print(f"源文件列表: {source_files}")
    
    print("数据处理器测试完成\n")

def check_input_files():
    """检查input文件夹中的输入文件是否存在"""
    print("=== 检查input文件夹中的输入文件 ===")
    
    required_files = [
        "dingding_fields.json",
        "dingding_allfields.json"
    ]
    
    missing_files = []
    for file in required_files:
        input_path = os.path.join("input", file)
        if not os.path.exists(input_path):
            missing_files.append(file)
    
    if missing_files:
        print(f"缺少必要的输入文件: {missing_files}")
        print("请确保以下文件存在于input文件夹中:")
        for file in required_files:
            print(f"  - input/{file}")
        return False
    else:
        print("所有必要的输入文件都存在")
        return True

def run_full_test():
    """运行完整测试"""
    print("开始运行完整测试...\n")
    
    # 检查输入文件
    if not check_input_files():
        print("测试终止：缺少必要的输入文件")
        return
    
    # 测试各个组件
    test_platform_config()
    test_facebook_processor()
    test_data_processor()
    
    # 运行主程序
    print("=== 运行主程序 ===")
    processor = DataProcessor()
    processor.main()
    
    print("完整测试完成！")

if __name__ == "__main__":
    run_full_test() 