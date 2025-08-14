import json

def extract_youtube_records(json_file):
    """提取Platforms name为Youtube的记录"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    youtube_records = []
    for record in data:
        if 'fields' in record and 'Platforms' in record['fields']:
            for platform in record['fields']['Platforms']:
                if platform.get('name') == 'Youtube':
                    link = record.get('fields', {}).get('Review Link', '-1')
                    if link == '-1':
                        print(f"Record ID {record['id']} has no Review Link.")
                        continue
                    else:
                        if record.get('fields', {}).get('Review Link', {}).get('link') == '-1':
                            print(f"Record ID {record['id']} has no valid Review Link.")
                            continue
                        else:
                            link = record['fields']['Review Link']['link']
                            youtube_record = {
                                record['id']: {
                                    'Views': record.get('fields', {}).get('Views', '-1'),
                                    'Likes': record.get('fields', {}).get('Likes', '-1'),
                                    'Comments': record.get('fields', {}).get('Comments', '-1'),
                                    'Subscribers': record.get('fields', {}).get('Subscribers', '-1'),
                                    'link': record.get('link', '-1')  # 新增的link字段
                                },"Review Link": link
                            }
                            print(f"Record ID {record['id']} has Review Link: {link}")
                    youtube_records.append(youtube_record)
                    break
    
    return youtube_records
def extract_youtube_info(data):
    # 假设youtube_data是一个包含条目信息的字典
    # 例如：youtube_data = {'id': '12345', 'title': 'Example Video', 'subscribers': 1000, 'views': 5000, 'comments': 20, 'likes': 300}
    
    youtube_records = []
    for record in data:
        if 'fields' in record and 'Platforms' in record['fields']:
            for platform in record['fields']['Platforms']:
                if platform.get('name') == 'Youtube':
                    youtube_records.append({record.get('id'): record})
                    break
    # 初始化一个空字典来存储提取的信息
    extracted_info = {}
    
    # 定义需要提取的键
    keys_to_extract = ['subscribers', 'views', 'comments', 'likes']
    
    return youtube_records

def get_record_by_id(json_file, record_id):
    """根据ID获取特定记录内容"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for record in data:
        if record.get('id') == record_id:
            return record
    
    return None

def export_to_json(data, output_file):
    """将数据导出到JSON文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"数据已成功导出到 {output_file}")
# 示例用法
youtube_data = {
    'id': '12345',
    'title': 'Example Video',
    'subscribers': 1000,
    'views': 5000,
    'comments': 20,
    'likes': 300
}

if __name__ == '__main__':
    # 提取所有Youtube记录
    records = extract_youtube_records('text.json')
    print(f"找到 {len(records)} 条Youtube记录:")
    for i, rec in enumerate(records, 1):
        print(f"{i}. ID={list(rec.keys())[0]}")  # 由于rec是一个字典，其键为ID
    
    # 用户输入ID
    selected_id = input("\n请输入要导出的记录ID: ")
    record = get_record_by_id('text.json', selected_id)
    
    if record:
        export_to_json(record, 'onetest.json')
    else:
        print("未找到该ID对应的记录")