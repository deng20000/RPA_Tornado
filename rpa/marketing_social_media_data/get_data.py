import json
from datetime import datetime, timedelta
import os

def get_yesterday_date():
    """获取昨天的日期，格式为YYYY.MM"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y.%m")

def process_fields_data():
    """处理fields.json文件，提取昨天的数据"""
    # 读取fields.json文件
    with open('fields.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取昨天的日期
    yesterday_date = get_yesterday_date()
    print(f"筛选日期: {yesterday_date}")
    
    # 筛选昨天的数据
    filtered_data = []
    
    for item in data:
        if 'fields' in item and '时间' in item['fields']:
            time_field = item['fields']['时间']
            if isinstance(time_field, dict) and 'name' in time_field:
                time_name = time_field['name']
                
                # 检查时间是否为昨天
                if time_name == yesterday_date:
                    # 提取所需字段
                    record_id = item.get('id', '')
                    social_account = item['fields'].get('社媒账号', '')
                    channel_name = ''
                    
                    # 获取渠道名称
                    if '渠道' in item['fields']:
                        channel = item['fields']['渠道']
                        if isinstance(channel, dict) and 'name' in channel:
                            channel_name = channel['name']
                    
                    # 构建返回格式：时间name+社媒账号+渠道name（不包含id）
                    result_format = f"{time_name}+{social_account}+{channel_name}"
                    
                    filtered_data.append({
                        "id": record_id,
                        "time_name": time_name,
                        "social_account": social_account,
                        "channel_name": channel_name,
                        "formatted_result": result_format
                    })
    
    return filtered_data

def save_results(data):
    """保存结果到JSON文件"""
    output_file = 'extracted_data_update.json'
    
    # 将数据转换为字典格式，id为key，拼接字符串为value
    data_dict = {}
    for item in data:
        data_dict[item['id']] = item['formatted_result']
    
    result = {
        "extraction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "yesterday_date": get_yesterday_date(),
        "total_records": len(data),
        "data": data_dict
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {output_file}")
    print(f"共找到 {len(data)} 条昨天的记录")

def main():
    """主函数"""
    try:
        # 处理数据
        filtered_data = process_fields_data()
        
        # 保存结果
        save_results(filtered_data)
        
        # 打印前几条记录作为示例
        if filtered_data:
            print("\n前5条记录示例:")
            for i, record in enumerate(filtered_data[:5]):
                print(f"{i+1}. {record['formatted_result']}")
        else:
            print("未找到昨天的数据")
            
    except FileNotFoundError:
        print("错误: 找不到 fields.json 文件")
    except json.JSONDecodeError:
        print("错误: fields.json 文件格式不正确")
    except Exception as e:
        print(f"处理过程中出现错误: {e}")

if __name__ == "__main__":
    main()










