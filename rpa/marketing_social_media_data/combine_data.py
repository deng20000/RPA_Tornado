import json
from datetime import datetime

def load_json_file(filename):
    """加载JSON文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到 {filename} 文件")
        return None
    except json.JSONDecodeError:
        print(f"错误: {filename} 文件格式不正确")
        return None

def create_optimized_structure():
    """创建优化的数据结构"""
    # 加载两个JSON文件
    extracted_data = load_json_file('extracted_data_update.json')
    allfields_data = load_json_file('allfields_extracted_update.json')
    
    if not extracted_data or not allfields_data:
        return None
    
    # 获取数据
    records_data = extracted_data.get('data', {})
    fields_data = allfields_data.get('data', {})
    
    # 创建优化的数据结构
    optimized_structure = {
        "metadata": {
            "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "yesterday_date": extracted_data.get('yesterday_date', ''),
            "total_records": len(records_data),
            "total_fields": len(fields_data),
            "description": "优化的数据结构，结合记录ID和字段映射"
        },
        "records": {},
        "fields_mapping": fields_data,
        "quick_access": {
            "record_ids": list(records_data.keys()),
            "field_ids": list(fields_data.keys()),
            "field_names": list(fields_data.values())
        }
    }
    
    # 为每个记录创建详细结构
    for record_id, record_value in records_data.items():
        # 解析记录值（格式：时间name+社媒账号+渠道name）
        parts = record_value.split('+')
        if len(parts) >= 3:
            time_name, social_account, channel_name = parts[0], parts[1], parts[2]
        else:
            time_name, social_account, channel_name = record_value, '', ''
        
        optimized_structure["records"][record_id] = {
            "basic_info": {
                "time": time_name,
                "social_account": social_account,
                "channel": channel_name,
                "raw_value": record_value
            },
            "available_fields": fields_data,  # 该记录可用的所有字段
            "field_access": {
                "field_ids": list(fields_data.keys()),
                "field_names": list(fields_data.values())
            }
        }
    
    return optimized_structure

def save_optimized_structure(data):
    """保存优化的数据结构"""
    output_file = 'optimized_data_structure_update.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"优化的数据结构已保存到: {output_file}")
    print(f"包含 {len(data['records'])} 条记录")
    print(f"包含 {len(data['fields_mapping'])} 个字段")

def create_usage_examples():
    """创建使用示例"""
    examples = {
        "usage_examples": {
            "获取所有记录ID": "data['quick_access']['record_ids']",
            "获取所有字段ID": "data['quick_access']['field_ids']", 
            "获取所有字段名称": "data['quick_access']['field_names']",
            "获取特定记录信息": "data['records']['7Gtfo83ZWU']['basic_info']",
            "获取特定记录可用字段": "data['records']['7Gtfo83ZWU']['available_fields']",
            "通过字段ID获取字段名称": "data['fields_mapping']['9XFXz5d']",
            "检查字段是否存在": "'9XFXz5d' in data['fields_mapping']",
            "获取记录数量": "len(data['records'])",
            "获取字段数量": "len(data['fields_mapping'])"
        }
    }
    
    with open('usage_examples.json', 'w', encoding='utf-8') as f:
        json.dump(examples, f, ensure_ascii=False, indent=2)
    
    print("使用示例已保存到: usage_examples.json")

def main():
    """主函数"""
    try:
        # 创建优化的数据结构
        optimized_data = create_optimized_structure()
        
        if optimized_data:
            # 保存优化的数据结构
            save_optimized_structure(optimized_data)
            
            # 创建使用示例
            create_usage_examples()
            
            # 打印示例信息
            print("\n=== 数据结构说明 ===")
            print("1. records: 包含所有记录ID及其详细信息")
            print("2. fields_mapping: 字段ID到字段名称的映射")
            print("3. quick_access: 快速访问常用数据的索引")
            print("4. metadata: 数据集的元信息")
            
            print("\n=== 使用示例 ===")
            print("获取所有记录ID:", len(optimized_data['quick_access']['record_ids']))
            print("获取所有字段:", len(optimized_data['quick_access']['field_names']))
            print("示例记录ID:", list(optimized_data['records'].keys())[:3])
            print("示例字段:", list(optimized_data['fields_mapping'].values())[:5])
            
        else:
            print("创建优化数据结构失败")
            
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main() 