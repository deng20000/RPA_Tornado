# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
import os
from datetime import datetime

def check_input_files():
    """检查输入文件是否都存在"""
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    current_date = datetime.now().strftime('%Y年%m月%d日')
    
    # 店铺与文件名的映射
    shop_files = {
        'gl-inet': f'{current_date}gl-inet店铺名称.xlsx',
        'GL.iNet UK': f'{current_date}GL.iNet UK店铺名称.xlsx',
        'GL.iNet CA': f'{current_date}GL.iNet CA店铺名称.xlsx',
        'GL.iNet US': f'{current_date}GL.iNet US店铺名称.xlsx',
        'GL.iNet EU': f'{current_date}GL.iNet EU店铺名称.xlsx'
    }
    
    missing_shops = []
    for shop, filename in shop_files.items():
        file_path = os.path.join(downloads_path, filename)
        if not os.path.exists(file_path):
            missing_shops.append(shop)
            print(f"缺少文件: {filename}")
    
    return len(missing_shops) == 0, missing_shops

def check_output_files():
    """检查输出文件是否已存在"""
    output_dir = glv["g_floder"]
    current_date = datetime.now().strftime('%Y年%m月%d日')
    
    # 输出文件与对应店铺的映射
    output_files = {
        'annyang': ['gl-inet', 'GL.iNet UK', 'GL.iNet CA'],
        'pingyangsong': ['GL.iNet US'],
        'cecilejiang': ['GL.iNet EU']
    }
    
    missing_outputs = []
    for output_name, shops in output_files.items():
        file_path = os.path.join(output_dir, f'{current_date}{output_name}.xlsx')
        if not os.path.exists(file_path):
            missing_outputs.extend(shops)
    
    return len(missing_outputs) == 0, missing_outputs

def main(args):
    input_files_ok, missing_input_shops = check_input_files()
    output_files_exist, missing_output_shops = check_output_files()
    
    if input_files_ok:
        print("✓ 所有输入文件都存在")
    else:
        print("✗ 缺少以下店铺的输入文件:")
        for shop in missing_input_shops:
            print(f"  - {shop}")
    
    if output_files_exist:
        print("✓ 所有输出文件已存在")
    else:
        print("✗ 缺少以下店铺的输出文件:")
        for shop in missing_output_shops:
            print(f"  - {shop}")
    
    return (input_files_ok, missing_input_shops, output_files_exist, missing_output_shops)

a =main("")
print(a)