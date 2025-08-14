# 调试GL-BE9300的数据匹配
sales_data = {'GL-BE9300': {'GL.iNet_AU-AU': 3}}

position_dict = {
    'RPAGL-BE9300': {
        '1': '2025/07/29', '3': 'GL.iNet CA', '4': 'GL.iNet EU', '5': 'GL.iNet UK', 
        '6': 'GL.iNet US', '7': 'GL.iNet APAC', '9': 'GL Tech AliExpress'
    }
}

print("销售额数据中的区域:")
for region in sales_data['GL-BE9300'].keys():
    print(f"  {region}")

print("\n位置字典中的区域:")
for pos_num, pos_name in position_dict['RPAGL-BE9300'].items():
    print(f"  {pos_num}: {pos_name}")

print("\n匹配检查:")
for region in sales_data['GL-BE9300'].keys():
    found = False
    for pos_num, pos_name in position_dict['RPAGL-BE9300'].items():
        if pos_name == region:
            print(f"  ✓ {region} 匹配位置 {pos_num}")
            found = True
            break
    if not found:
        print(f"  ✗ {region} 未找到匹配") 