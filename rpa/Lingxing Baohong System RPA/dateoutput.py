# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
import pandas as pd
import os
from datetime import datetime

def main(args):
    # 假设你的数据叫 data
    data = glv['g_orderresult']

    rows = []
    for order_list in data:
        for order in order_list:
            order_info = order.copy()
            products = order_info.pop('商品信息')
            for product in products:
                row = order_info.copy()
                row.update(product)
                rows.append(row)

    # 获取当前日期
    date_prefix = datetime.now().strftime("%Y%m%d")
    # 获取用户Downloads目录
    downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    # 拼接完整文件名
    file_path = os.path.join(downloads_dir, f"{date_prefix}_orders.xlsx")

    df = pd.DataFrame(rows)
    df.to_excel(file_path, index=False)
    print(f"文件已保存到: {file_path}")
    return file_path
