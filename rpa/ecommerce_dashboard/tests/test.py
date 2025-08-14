def replace_sales_data_to_position_dict(sales_data, position_dict):
    """
    将产品销售额数据替换到产品销量位置字典中
    
    Args:
        sales_data: 产品销售额数据字典
        position_dict: 产品销量位置字典
    
    Returns:
        tuple: (替换后的位置字典, 未替换数据的结构)
    """
    # 创建替换后的位置字典副本
    updated_position_dict = {}
    # 创建未替换数据的结构
    unreplaced_structure = {}
    
    for product_key, sales_info in sales_data.items():
        # 构造对应的位置字典键名
        position_key = f"RPA{product_key}"
        
        if position_key in position_dict:
            # 复制位置字典
            updated_position_dict[position_key] = position_dict[position_key].copy()
            unreplaced_structure[product_key] = {}
            
            # 遍历销售额数据，替换对应的位置
            for region, sales_count in sales_info.items():
                # 在位置字典中查找对应的位置编号
                for pos_num, pos_name in position_dict[position_key].items():
                    if pos_name == region:
                        # 替换销售额数据
                        updated_position_dict[position_key][pos_num] = sales_count
                        unreplaced_structure[product_key][region] = sales_count
                        break
        else:
            # 如果找不到对应的位置字典，保持原样
            updated_position_dict[position_key] = position_dict.get(position_key, {})
            unreplaced_structure[product_key] = sales_info.copy()
    
    return updated_position_dict, unreplaced_structure

# 测试数据
# sales_data = {
#     'GL-BE3600': {
#         'GL.iNet_EU&UK-IT': 0, 'GL.iNet_EU&UK-IE': 0, 'GL.iNet_EU&UK-NL': 1, 
#         'GL.iNet_EU&UK-PL': 1, 'GL.iNet_NA-MX': 2, 'GL.iNet_EU&UK-FR': 2, 
#         'GL.iNet_EU&UK-ES': 3, 'GL.iNet_JP-JP': 5, 'GL.iNet_AU-AU': 7, 
#         'GL.iNet_NA-CA': 8, 'GL.iNet_EU&UK-UK': 9, 'GL.iNet_EU&UK-DE': 13, 
#         'GL.iNet_NA-US': 76
#     },
#     'GL-MT6000': {
#         'GL.iNet_NA-MX': 1, 'GL.iNet_EU&UK-BE': 1, 'GL.iNet_EU&UK-PL': 2, 
#         'GL.iNet_JP-JP': 3, 'GL.iNet_NA-CA': 5, 'GL.iNet_EU&UK-FR': 5, 
#         'GL.iNet_EU&UK-IT': 6, 'GL.iNet_EU&UK-ES': 7, 'GL.iNet_AU-AU': 9, 
#         'GL.iNet_EU&UK-DE': 12, 'GL.iNet_EU&UK-UK': 14, 'GL.iNet_NA-US': 104
#     },
#     'GL-MT3000': {
#         'GL.iNet_EU&UK-IT': 0, 'GL.iNet_EU&UK-IE': 0, 'GL.iNet_EU&UK-NL': 1, 
#         'GL.iNet_EU&UK-PL': 1, 'GL.iNet_EU&UK-BE': 1, 'GL.iNet_JP-JP': 1, 
#         'GL.iNet_NA-MX': 4, 'GL.iNet_AU-AU': 8, 'GL.iNet_EU&UK-FR': 9, 
#         'GL.iNet_EU&UK-ES': 9, 'GL.iNet_EU&UK-UK': 12, 'GL.iNet_EU&UK-DE': 15, 
#         'GL.iNet_NA-CA': 16, 'GL.iNet_NA-US': 114
#     },
#     'GL-BE9300': {
#         'GL.iNet_AU-AU': 3
#     },
#     'GL-RM1': {
#         'MIC-DE-IT': 3, 'MIC-DE-DE': 9, 'MIC-DE-ES': 0, 'MIC-DE-NL': 0, 
#         'MIC-DE-BE': 0, 'MIC-US-US': 109, 'MIC-DE-PL': 1, 'MIC-DE-FR': 2, 
#         'MIC-US-CA': 5, 'MIC-DE-UK': 9
#     }
# }

position_dict = {
    'RPAGL-BE3600': {
        '1': '2025/07/29', '3': 'GL Tech AliExpress', '5': 'GL-iNet Overseas Store Store', 
        '7': 'GL.iNet_AU-AU', '8': 'GL.iNet_EU&UK-BE', '9': 'GL.iNet_EU&UK-DE', 
        '10': 'GL.iNet_EU&UK-ES', '11': 'GL.iNet_EU&UK-FR', '12': 'GL.iNet_EU&UK-IE', 
        '13': 'GL.iNet_EU&UK-IT', '14': 'GL.iNet_EU&UK-NL', '15': 'GL.iNet_EU&UK-PL', 
        '16': 'GL.iNet_EU&UK-UK', '17': 'GL.iNet_JP-JP', '18': 'GL.iNet_NA-CA', 
        '19': 'GL.iNet_NA-MX', '20': 'GL.iNet_NA-US', '22': 'GL Tech MY', 
        '23': 'GL Tech PH', '24': 'GL Tech SG', '25': 'GL Tech TH', '27': 'GL.iNet CA', 
        '28': 'GL.iNet EU', '29': 'GL.iNet UK', '30': 'GL.iNet US', '31': 'GL.iNet APAC', 
        '33': 'GL Tech Walmart'
    },
    'RPAGL-MT6000': {
        '1': '2025/07/29', '3': 'GL Tech AliExpress', '5': 'GL-iNet Overseas Store Store', 
        '7': 'GL.iNet_AU-AU', '8': 'GL.iNet_EU&UK-BE', '9': 'GL.iNet_EU&UK-DE', 
        '10': 'GL.iNet_EU&UK-ES', '11': 'GL.iNet_EU&UK-FR', '12': 'GL.iNet_EU&UK-IE', 
        '13': 'GL.iNet_EU&UK-IT', '14': 'GL.iNet_EU&UK-NL', '15': 'GL.iNet_EU&UK-PL', 
        '16': 'GL.iNet_EU&UK-UK', '17': 'GL.iNet_JP-JP', '18': 'GL.iNet_NA-CA', 
        '19': 'GL.iNet_NA-MX', '20': 'GL.iNet_NA-US', '22': 'GL Tech MY', 
        '23': 'GL Tech PH', '24': 'GL Tech SG', '25': 'GL Tech TH', '27': 'GL.iNet CA', 
        '28': 'GL.iNet EU', '29': 'GL.iNet UK', '30': 'GL.iNet US', '31': 'GL.iNet APAC'
    },
    'RPAGL-MT3000': {
        '1': '2025/07/29', '3': 'GL Tech AliExpress', '5': 'GL-iNet Overseas Store Store', 
        '7': 'GL.iNet_AU-AU', '8': 'GL.iNet_EU&UK-BE', '9': 'GL.iNet_EU&UK-DE', 
        '10': 'GL.iNet_EU&UK-ES', '11': 'GL.iNet_EU&UK-FR', '12': 'GL.iNet_EU&UK-IE', 
        '13': 'GL.iNet_EU&UK-IT', '14': 'GL.iNet_EU&UK-NL', '15': 'GL.iNet_EU&UK-PL', 
        '16': 'GL.iNet_EU&UK-UK', '17': 'GL.iNet_JP-JP', '18': 'GL.iNet_NA-CA', 
        '19': 'GL.iNet_NA-MX', '20': 'GL.iNet_NA-US', '22': 'GL Tech MY', 
        '23': 'GL Tech PH', '24': 'GL Tech SG', '25': 'GL Tech TH', '27': 'GL.iNet CA', 
        '28': 'GL.iNet EU', '29': 'GL.iNet UK', '30': 'GL.iNet US', '31': 'GL.iNet APAC', 
        '33': 'TEMU-US', '35': 'GL Tech Walmart'
    },
    'RPAGL-BE9300': {
        '1': '2025/07/29', '3': 'GL.iNet CA', '4': 'GL.iNet EU', '5': 'GL.iNet UK', 
        '6': 'GL.iNet US', '7': 'GL.iNet APAC', '9': 'GL Tech AliExpress'
    },
    'RPAGL-RM1': {
        '1': '2025/07/29', '3': 'MIC-DE-BE', '4': 'MIC-DE-DE', '5': 'MIC-DE-ES', 
        '6': 'MIC-DE-FR', '7': 'MIC-DE-IT', '8': 'MIC-DE-NL', '9': 'MIC-DE-PL', 
        '10': 'MIC-DE-SE', '11': 'MIC-DE-UK', '12': 'MIC-US-CA', '13': 'MIC-US-MX', 
        '14': 'MIC-US-US', '16': 'GL.iNet CA', '17': 'GL.iNet EU', '18': 'GL.iNet UK', 
        '19': 'GL.iNet US', '20': 'GL.iNet APAC', '22': 'GL Tech AliExpress'
    }
}

# 测试函数
if __name__ == "__main__":
    updated_positions, unreplaced_data = replace_sales_data_to_position_dict(sales_data, position_dict)
    
    print("替换后的位置字典:")
    for product, positions in updated_positions.items():
        print(f"\n{product}:")
        for pos_num, value in positions.items():
            print(f"  {pos_num}: {value}")
    
    print("\n\n未替换数据的结构:")
    for product, regions in unreplaced_data.items():
        print(f"\n{product}:")
        for region, count in regions.items():
            print(f"  {region}: {count}")
