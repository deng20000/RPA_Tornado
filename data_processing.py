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
from datetime import datetime
import os

def main(args):
    # 调用函数处理数据
    source_file = 'mailchimp.xlsx'
    new_file = process_mailchimp_data(source_file)
    if new_file:
        print(f"\n处理完成！新文件已保存为：{new_file}")


def process_mailchimp_data(source_file):
    """
    处理Mailchimp数据，创建新的Excel文件
    
    Args:
        source_file (str): 源Excel文件路径
    
    Returns:
        str: 新创建的文件名
    """
    try:
        # 获取用户下载目录路径
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        # 构建完整的源文件路径
        source_file_path = os.path.join(downloads_path, source_file)

        # 读取原始Excel数据文件
        df_growth = pd.read_excel(source_file_path, sheet_name='eDM - Growth')
        df_performance = pd.read_excel(source_file_path, sheet_name='eDM performance')

        # 筛选Status为Active的记录
        active_df = df_growth[df_growth['Status'] == 'Active']

        # 生成新文件名（格式：YYYY年MM月DD日Mailchimp数据查看.xlsx）
        current_date = datetime.now()
        new_filename = current_date.strftime('%Y年%m月%d日Mailchimp数据查看.xlsx')
        # 构建新文件的完整路径（保存到下载目录）
        new_file_path = os.path.join(downloads_path, new_filename)

        # 将筛选后的数据写入新的Excel文件
        with pd.ExcelWriter(new_file_path, engine='openpyxl') as writer:
            # 写入Active数据到指定sheet页
            active_df.to_excel(writer, sheet_name='eDM - Growth-Active', index=False)
            # 写入performance数据到新sheet页
            df_performance.to_excel(writer, sheet_name='eDM performance', index=False)

        print(f"数据已成功写入到新文件：{new_file_path}")
        print(f"已创建以下sheet页：")
        print(f"1. eDM - Growth-Active (共 {len(active_df)} 条记录)")
        print(f"2. eDM performance (共 {len(df_performance)} 条记录)")
        print("\neDM - Growth-Active 前5行数据预览:")
        print(active_df.head())
        glv["g_downloadfile"] = new_file_path
        # return new_file_path
        return "处理成功"
    except Exception as e:
        # print(f"处理过程中发生错误：{str(e)}")
        return f"处理过程中发生错误：{str(e)}"
        # return None