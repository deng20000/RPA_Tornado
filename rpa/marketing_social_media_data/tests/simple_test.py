"""
简单测试脚本
用于验证真实数据处理功能
"""

import os
import json
from main_data_process import DataProcessor

def check_files():
    """检查input文件夹中的文件是否存在"""
    print("=== 检查input文件夹中的输入文件 ===")
    
    required_files = [
        "dingding_fields.json",
        "dingding_allfields.json"
    ]
    
    optional_files = [
        "fb_fetch_inf.json",
        "youtube_fetch_inf.json",
        "instagram_fetch_inf.json",
        "linkedin_fetch_inf.json",
        "x_fetch_inf.json"
    ]
    
    print("必要文件:")
    for file in required_files:
        input_path = os.path.join("input", file)
        exists = os.path.exists(input_path)
        status = "✅" if exists else "❌"
        print(f"  {status} input/{file}")
    
    print("\n可选文件:")
    for file in optional_files:
        input_path = os.path.join("input", file)
        exists = os.path.exists(input_path)
        status = "✅" if exists else "❌"
        print(f"  {status} input/{file}")
    
    # 检查input文件夹
    if not os.path.exists("input"):
        print("\n创建input文件夹...")
        os.makedirs("input")
        print("✅ input文件夹已创建")
    else:
        print("\n✅ input文件夹已存在")
    
    # 检查output文件夹
    if not os.path.exists("output"):
        print("\n创建output文件夹...")
        os.makedirs("output")
        print("✅ output文件夹已创建")
    else:
        print("\n✅ output文件夹已存在")
    
    return all(os.path.exists(os.path.join("input", f)) for f in required_files)

def run_processor():
    """运行数据处理器"""
    print("\n=== 运行数据处理器 ===")
    
    processor = DataProcessor()
    processor.main()
    
    print("\n=== 检查输出文件 ===")
    output_files = [
        "optimized_data_structure_update.json",
        "mapping_report.json",
        "fb_fetch_inf_update.json"
    ]
    
    for file in output_files:
        output_path = os.path.join("output", file)
        if os.path.exists(output_path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")

def main():
    """主函数"""
    print("数据处理系统测试")
    print("=" * 50)
    
    # 检查文件
    if not check_files():
        print("\n❌ 缺少必要的输入文件，请确保以下文件存在于input文件夹中:")
        print("  - input/dingding_fields.json")
        print("  - input/dingding_allfields.json")
        return
    
    # 运行处理器
    run_processor()
    
    print("\n✅ 测试完成！")

if __name__ == "__main__":
    main() 