import json

def safe_json_load(file_path):
    """更安全地加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # 尝试逐行读取处理
            data = []
            f.seek(0)
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return data

# 目标国家列表
target_countries = ['IT', 'DE', 'FR', 'ES', 'NL', 'SE', 'TR', 'PL', 'BE']
for _ in range(len(target_countries)):
    target_countries[_] = "Amazon "+target_countries[_]

# 读取原始数据
data = safe_json_load('test.json')

# 过滤数据
filtered_data = []
for item in data:
    if not isinstance(item, dict):
        continue
        
    fields = item.get('fields', {})
    shopify_site = fields.get('shopify站点', [{}])
    if shopify_site and isinstance(shopify_site, list):
        shopify_site = shopify_site[0].get('name', '')
    else:
        shopify_site = ''
        
    purchase_channel = fields.get('购买渠道', {})
    if isinstance(purchase_channel, dict):
        purchase_channel = purchase_channel.get('name', '')
    else:
        purchase_channel = ''
        
    return_point = fields.get('退货点', '')
    
    # 检查条件：Shopify站点包含Amazon，购买渠道是Amazon，退货点在目标国家中
    if 'Amazon' in shopify_site and purchase_channel == 'Amazon' and any(country in return_point for country in target_countries):
        filtered_data.append(item)

# 写入新文件
with open('filtered_data.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"已过滤出{len(filtered_data)}条符合条件的记录，保存到filtered_data.json")