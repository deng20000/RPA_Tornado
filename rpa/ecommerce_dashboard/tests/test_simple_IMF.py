import json
import re
from datetime import datetime, timedelta
import ast
from jsonpath_ng.ext import parse

# 模块描述：
# 1. 从原始XHR日志中提取所有请求体，并保存为新的JSON文件
# 2. 从新的JSON文件中提取指定产品的销售数据
# 3. 根据钉钉多维表位置数据结构，返回指定产品的销售数据


# 步骤1：从原始XHR日志中提取所有请求体，并保存为新的JSON文件
def extract_xhr_bodies_to_file(json_path, output_path="test.json"):
    """
    从原始XHR日志中提取所有请求体，并保存为新的JSON文件
    :param json_path: 原始XHR日志文件路径
    :param output_path: 输出文件路径
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        # 提取所有body并解析
        bodies = []
        for entry in logs:
            if entry.get('type') == 'XHR' and 'body' in entry:
                try:
                    body = json.loads(entry['body'])
                    bodies.append(body)
                except json.JSONDecodeError:
                    continue
        
        # 保存解析后的body到新文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(bodies, f, ensure_ascii=False, indent=2)
        
        return len(bodies)
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")
        return 0


def is_date_string(s):
    # 判断是否为日期格式 YYYY/MM/DD
    return bool(re.match(r"^\d{4}/\d{2}/\d{2}$", s))

def extract_sales_data_from_json(json_path,product_key, date_str=None):
    """从XHR日志中提取销售数据
    
    Args:
        json_path (str): 日志文件路径
        date_str (str, optional): 指定日期，默认为昨天，支持 YYYY-MM-DD 或 YYYY/MM/DD 格式
    
    Returns:
        dict: {store_name: sales_count, ...}
    """
    # 设置日期格式
    if not date_str:
        date_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif '/' in date_str:
        y, m, d = date_str.split('/')
        date_str = f"{y}-{m}-{d}"
                
    sales_data = {}
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
            print(f"读取到的数据长度: {len(logs)}")
            
        if not isinstance(logs, list):
            logs = [logs]
            
        for entry in logs:
            # 检查数据结构
            if isinstance(entry, dict) and 'data' in entry and 'statisticsList' in entry['data']:
                data = entry['data']
                # 直接使用 jsonpath 提取键值对
                jsonpath_expr = parse('$.statisticsList[*]')
                matches = jsonpath_expr.find(data)
                
                for match in matches:
                    store_name = match.value.get('storeName', [None])[0]
                    date_collect = match.value.get('dateCollect', {})
                    sales_count = date_collect.get(date_str)
                    
                    print(f"找到店铺: {store_name}, 日期: {date_str}, 销量: {sales_count}")
                    
                    if store_name and sales_count:
                        sales_data[store_name] = str(int(sales_count))
            else:
                print("数据结构不符合预期")
                    
    except Exception as e:
        print(f"处理数据出错: {str(e)}")
        
    return {product_key:sales_data}
   
def replace_sales_data_to_position_dict(sales_data, position_dict):
    """
    只对输入产品的编号做有销量过滤，其它产品保持原样，返回完整结构。
    """
    import copy
    updated_position_dict = copy.deepcopy(position_dict)
    for product_key, sales_info in sales_data.items():
        position_key = f"RPA{product_key}"
        if position_key in updated_position_dict:
            # 只保留有销量的编号
            new_dict = {}
            for region, sales_count in sales_info.items():
                for pos_num, pos_name in position_dict[position_key].items():
                    if pos_name == region:
                        new_dict[pos_num] = sales_count
                        break
            updated_position_dict[position_key] = new_dict
    return updated_position_dict


# 测试函数
if __name__ == "__main__":
    try:
        # print("开始处理XHR日志文件...")
        # # 首先提取所有请求体到test.json
        # bodies_count = extract_xhr_bodies_to_file("raw_data.json", "test.json")
        # print(f"已提取 {bodies_count} 条请求体到 test.json")
        
        # # 直接提取销售数据
        # sales_data = extract_sales_data_from_json("raw_data.json")
        # print("\n提取的销售数据 (店铺:销量):")
        # import pprint
        # pprint.pprint(sales_data)
        sales_data = {'GL.iNet_NA-CA': '10', 'GL.iNet EU': '1', 'MIC-US-MX': '9', 'GL Tech TH': '70', 'GL.iNet_EU&UK-BE': '80', 'GL.iNet_EU&UK-DE': '1', 'Lafaer': '2', 'GL.iNet_NA-MX': '3', 'GL.iNet_EU&UK-PL': '4', 'GL.iNet_JP-JP': '1', 'GL.iNet UK': '1', 'MIC-DE-UK': '23', 'GL.iNet CA': '1', 'GL.iNet US': '1', 'GL.iNet_NA-US': '1', 'MIC-US-US': '12', 'GL.iNet_AU-AU': '1', 'GL Tech AliExpress': '1', 'GL.iNet APAC': '1', 'GL.iNet_EU&UK-IT': '2', 'GL.iNet_EU&UK-UK': '3', 'GL Tech Walmart': '1'}
        site_result = {'RPAGL-BE3600': {'1': '2025/08/01', '3': 'GL Tech AliExpress', '5': 'GL-iNet Overseas Store Store', '7': 'GL.iNet_AU-AU', '8': 'GL.iNet_EU&UK-BE', '9': 'GL.iNet_EU&UK-DE', '10': 'GL.iNet_EU&UK-ES', '11': 'GL.iNet_EU&UK-FR', '12': 'GL.iNet_EU&UK-IE', '13': 'GL.iNet_EU&UK-IT', '14': 'GL.iNet_EU&UK-NL', '15': 'GL.iNet_EU&UK-PL', '16': 'GL.iNet_EU&UK-UK', '17': 'GL.iNet_JP-JP', '18': 'GL.iNet_NA-CA', '19': 'GL.iNet_NA-MX', '20': 'GL.iNet_NA-US', '22': 'GL Tech MY', '23': 'GL Tech PH', '24': 'GL Tech SG', '25': 'GL Tech TH', '27': 'GL.iNet CA', '28': 'GL.iNet EU', '29': 'GL.iNet UK', '30': 'GL.iNet US', '31': 'GL.iNet APAC', '33': 'GL Tech Walmart'}, 'RPAGL-MT6000': {'1': '2025/08/01', '3': 'GL Tech AliExpress', '5': 'GL-iNet Overseas Store Store', '7': 'GL.iNet_AU-AU', '8': 'GL.iNet_EU&UK-BE', '9': 'GL.iNet_EU&UK-DE', '10': 'GL.iNet_EU&UK-ES', '11': 'GL.iNet_EU&UK-FR', '12': 'GL.iNet_EU&UK-IE', '13': 'GL.iNet_EU&UK-IT', '14': 'GL.iNet_EU&UK-NL', '15': 'GL.iNet_EU&UK-PL', '16': 'GL.iNet_EU&UK-UK', '17': 'GL.iNet_JP-JP', '18': 'GL.iNet_NA-CA', '19': 'GL.iNet_NA-MX', '20': 'GL.iNet_NA-US', '22': 'GL Tech MY', '23': 'GL Tech PH', '24': 'GL Tech SG', '25': 'GL Tech TH', '27': 'GL.iNet CA', '28': 'GL.iNet EU', '29': 'GL.iNet UK', '30': 'GL.iNet US', '31': 'GL.iNet APAC'}, 'RPAGL-MT3000': {'1': '2025/08/01', '3': 'GL Tech AliExpress', '5': 'GL-iNet Overseas Store Store', '7': 'GL.iNet_AU-AU', '8': 'GL.iNet_EU&UK-BE', '9': 'GL.iNet_EU&UK-DE', '10': 'GL.iNet_EU&UK-ES', '11': 'GL.iNet_EU&UK-FR', '12': 'GL.iNet_EU&UK-IE', '13': 'GL.iNet_EU&UK-IT', '14': 'GL.iNet_EU&UK-NL', '15': 'GL.iNet_EU&UK-PL', '16': 'GL.iNet_EU&UK-UK', '17': 'GL.iNet_JP-JP', '18': 'GL.iNet_NA-CA', '19': 'GL.iNet_NA-MX', '20': 'GL.iNet_NA-US', '22': 'GL Tech MY', '23': 'GL Tech PH', '24': 'GL Tech SG', '25': 'GL Tech TH', '27': 'GL.iNet CA', '28': 'GL.iNet EU', '29': 'GL.iNet UK', '30': 'GL.iNet US', '31': 'GL.iNet APAC', '33': 'TEMU-US', '35': 'GL Tech Walmart'}, 'RPAGL-BE9300': {'1': '2025/08/01', '3': 'GL.iNet CA', '4': 'GL.iNet EU', '5': 'GL.iNet UK', '6': 'GL.iNet US', '7': 'GL.iNet APAC', '9': 'GL Tech AliExpress', '11': 'GL.iNet_AU-AU'}, 'RPAGL-RM1': {'1': '2025/08/01', '3': 'MIC-DE-BE', '4': 'MIC-DE-DE', '5': 'MIC-DE-ES', '6': 'MIC-DE-FR', '7': 'MIC-DE-IT', '8': 'MIC-DE-NL', '9': 'MIC-DE-PL', '10': 'MIC-DE-SE', '11': 'MIC-DE-UK', '12': 'MIC-US-CA', '13': 'MIC-US-MX', '14': 'MIC-US-US', '16': 'GL.iNet CA', '17': 'GL.iNet EU', '18': 'GL.iNet UK', '19': 'GL.iNet US', '20': 'GL.iNet APAC', '22': 'GL Tech AliExpress'}}
        
        position_dict = replace_sales_data_to_position_dict(sales_data, site_result)
        print("\n更新后的位置字典:", position_dict)
                
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")


