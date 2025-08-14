# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
import json
import os
import ast

def main(args):
    pass

def batch_extract_from_tjson(tjson_path):
    """
    批量读取t.json并提取内容，返回所有提取结果的列表
    """
    with open(tjson_path, 'r', encoding='utf-8') as f:
        data_list = ast.literal_eval(f.read())
    results = []
    for item in data_list:
        if 'body' in item and item['body']:
            body_dict = json.loads(item['body'])
            result = extract_data_from_lingxin_json(body_dict)
            results.append(result)
    print(results)
    for i, res in enumerate(results, 1):
        print(f'--- 记录 {i} ---')
        for k, v in res.items():
            print(f'{k}: {v}')
        print() 
    return results

def extract_data_from_lingxin_json(input_data):
    """
    从lingxin.json文件或字典中提取所需数据
    
    参数:
        input_data: 可以是JSON文件路径(字符串)或已加载的字典对象
    """
    try:
        # 判断输入类型并获取数据
        if isinstance(input_data, str):
            # 输入是文件路径，读取JSON文件
            with open(input_data, 'r', encoding='utf-8') as file:
                data = json.load(file)
        elif isinstance(input_data, dict):
            # 输入已经是字典
            data = input_data
        else:
            raise ValueError("输入必须是JSON文件路径或字典对象")
        
        # 提取基本信息
        result = {}
        
        # 提取必填字段
        if 'data' in data:
            data_obj = data['data']
            
            # 收件人国家
            result['收件人国家'] = data_obj.get('receiver_country_code', '')
            
            # 报关单币制
            currency_symbol = data_obj.get('icon', '$')
            result['报关单币制'] = get_currency_code(currency_symbol)
            
            # 收件人信息
            if 'receive_info' in data_obj:
                receive_info = data_obj['receive_info']
                result['收件人姓名'] = receive_info.get('receiver_name', '')  # 收件人姓名
                result['收件人电话'] = receive_info.get('receiver_mobile', '')  # 收件人电话
                result['收件人州/区域'] = receive_info.get('state_or_region', '')  # 收件人州/区域
                result['收件人城市'] = receive_info.get('city', '')  # 收件人城市
                result['收件人地址1'] = receive_info.get('address_line1', '')  # 收件人地址1
                result['收件人地址2'] = receive_info.get('address_line2', '')  # 收件人地址2
                result['收件人公司名'] = receive_info.get('receiver_company_name', '')  # 收件人公司名
                result['收件人邮政编码'] = receive_info.get('postal_code', '1')  # 邮政编码


            # 买家信息
            if 'buyer_info' in data_obj:
                buyer_info = data_obj['buyer_info']
                result['收件人电子邮件'] = buyer_info.get('buyer_email', '')  # 收件人电子邮件
                result['备注'] = buyer_info.get('buyer_note', '')  # 备注
            
            # PCCC备注
            result['PCCC备注'] = data_obj.get('remark', '')
            
            # 平台订单号和交易订单号
            if 'order_item_info' in data_obj and len(data_obj['order_item_info']) > 0:
                # 平台订单号
                result['平台订单号'] = data_obj['order_item_info'][0].get('platform_order_name', '')
                # 交易订单号 (使用相同字段，因为用户要求中两个字段名称相同)
                result['交易订单号'] = data_obj['order_item_info'][0].get('platform_order_name', '')
            
            # 商品信息
            if 'order_item_info' in data_obj:
                items = []
                for item in data_obj['order_item_info']:
                    unitprice = item.get('unit_price_amount', '')
                    if unitprice=="" or int(unitprice) == 0:
                        unitprice = "1.00"
                    item_info = {
                        '产品SKU': item.get('local_sku', ''),  # 产品SKU
                        '数量': item.get('quantity', ''),  # 数量
                        '目的海关申报单价(USD)': unitprice,  # 目的海关申报单价(USD)
                        '订单销售单价': unitprice # 订单销售单价
                        # item.get('sales_revenue_amount', '')  
                    }
                    items.append(item_info)
                result['商品信息'] = items
        
        return result
    except Exception as e:
        print(f"提取数据时出错: {e}")
        return {}

try:
    from forex_python.converter import CurrencyCodes
    # 初始化CurrencyCodes对象
    currency_codes = CurrencyCodes()
    
    def get_currency_code(currency_symbol):
        """
        使用forex-python库根据货币符号返回对应的货币代码
        """
        # 常见货币符号到代码的映射（用于forex-python不支持的符号）
        fallback_map = {
            "$": "USD",  # 美元
            "€": "EUR",  # 欧元
            "£": "GBP",  # 英镑
            "¥": "JPY",  # 日元
            "₩": "KRW",  # 韩元
            "₹": "INR",  # 印度卢比
            "₽": "RUB",  # 俄罗斯卢布
            "₴": "UAH",  # 乌克兰格里夫纳
            "₿": "BTC",  # 比特币
            "￥": "CNY",  # 人民币
            "A$": "AUD",  # 澳元
            "C$": "CAD",  # 加元
            "HK$": "HKD",  # 港币
            "S$": "SGD",  # 新加坡元
            "Fr": "CHF",  # 瑞士法郎
            "R$": "BRL",  # 巴西雷亚尔
            "R": "ZAR",   # 南非兰特
            "kr": "SEK",  # 瑞典克朗
            "฿": "THB",   # 泰铢
        }
        
        # 对于常见的货币符号，直接使用映射表
        if currency_symbol in fallback_map:
            return fallback_map[currency_symbol]
            
        # 如果不在映射表中，尝试使用forex-python库
        # 注意：这种方法不是很可靠，因为forex-python没有直接提供从符号到代码的转换
        # 但我们可以尝试一些常见的货币代码
        common_codes = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'AUD', 'CAD', 'CHF', 'HKD', 'SGD']
        for code in common_codes:
            if currency_symbol == currency_codes.get_symbol(code):
                return code
        
        # 如果无法识别，默认返回USD
        return "USD"
        
except ImportError:
    # 如果forex-python库不可用，使用静态映射
    def get_currency_code(currency_symbol):
        """
        根据货币符号返回对应的货币代码
        """
        currency_map = {
            "$": "USD",  # 美元
            "€": "EUR",  # 欧元
            "£": "GBP",  # 英镑
            "¥": "JPY",  # 日元
            "₩": "KRW",  # 韩元
            "₹": "INR",  # 印度卢比
            "₽": "RUB",  # 俄罗斯卢布
            "₴": "UAH",  # 乌克兰格里夫纳
            "₿": "BTC",  # 比特币
            "￥": "CNY",  # 人民币
            "A$": "AUD",  # 澳元
            "C$": "CAD",  # 加元
            "HK$": "HKD",  # 港币
            "S$": "SGD",  # 新加坡元
            "Fr": "CHF",  # 瑞士法郎
            "R$": "BRL",  # 巴西雷亚尔
            "R": "ZAR",   # 南非兰特
            "kr": "SEK",  # 瑞典克朗
            "฿": "THB",   # 泰铢
        }
        
        return currency_map.get(currency_symbol, "USD")  # 默认返回USD


# test unittest
# def main():
#     # 获取当前脚本所在目录
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     json_file_path = os.path.join(current_dir, 'lingxin.json')
    
#     # 示例1：从文件路径提取数据
#     print("\n示例1：从文件路径提取数据")
#     extracted_data_from_file = extract_data_from_lingxin_json(json_file_path)
#     print("提取的数据（从文件路径）:")
#     for key, value in extracted_data_from_file.items():
#         if key == "商品信息":
#             print(f"{key}:")
#             for i, item in enumerate(value, 1):
#                 print(f"  商品 {i}:")
#                 for item_key, item_value in item.items():
#                     print(f"    {item_key}: {item_value}")
#         else:
#             print(f"{key}: {value}")
    
#     # 示例2：从字典提取数据
#     print("\n示例2：从字典提取数据")
#     # 先读取JSON文件获取字典
#     with open(json_file_path, 'r', encoding='utf-8') as file:
#         json_dict = json.load(file)
#     # 然后从字典提取数据
#     extracted_data_from_dict = extract_data_from_lingxin_json(json_dict)
#     print("提取的数据（从字典）:")
#     for key, value in extracted_data_from_dict.items():
#         if key == "商品信息":
#             print(f"{key}:")
#             for i, item in enumerate(value, 1):
#                 print(f"  商品 {i}:")
#                 for item_key, item_value in item.items():
#                     print(f"    {item_key}: {item_value}")
#         else:
#             print(f"{key}: {value}")
    
#     return extracted_data_from_file