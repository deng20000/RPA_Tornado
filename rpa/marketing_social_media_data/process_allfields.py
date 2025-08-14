import json
from datetime import datetime

def process_allfields_data():
    """处理allfields.json文件，提取除了指定字段外的所有字段"""
    # 读取allfields.json文件
    with open('allfields.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 需要排除的字段名称
    excluded_fields = ["父記錄", "社媒账号", "渠道", "时间"]
    
    # 提取符合条件的字段
    extracted_fields = []
    
    for field in data:
        field_name = field.get('name', '')
        field_id = field.get('id', '')
        
        # 检查字段是否在排除列表中
        if field_name not in excluded_fields:
            extracted_fields.append({
                "id": field_id,
                "name": field_name,
                "type": field.get('type', '')
            })
    
    return extracted_fields

def save_results(data):
    """保存结果到JSON文件"""
    output_file = 'allfields_extracted_update.json'
    
    # 将数据转换为字典格式，id为key，name为value
    data_dict = {}
    for field in data:
        data_dict[field['id']] = field['name']
    
    result = {
        "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "excluded_fields": ["父記錄", "社媒账号", "渠道", "时间"],
        "total_fields": len(data),
        "data": data_dict
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {output_file}")
    print(f"共提取 {len(data)} 个字段")

def main():
    """主函数"""
    try:
        # 处理数据
        extracted_fields = process_allfields_data()
        
        # 保存结果
        save_results(extracted_fields)
        
        # 打印前几条记录作为示例
        if extracted_fields:
            print("\n前10个字段示例:")
            for i, field in enumerate(extracted_fields[:10]):
                print(f"{i+1}. ID: {field['id']}, Name: {field['name']}, Type: {field['type']}")
        else:
            print("未找到符合条件的字段")
            
    except FileNotFoundError:
        print("错误: 找不到 allfields.json 文件")
    except json.JSONDecodeError:
        print("错误: allfields.json 文件格式不正确")
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main() 