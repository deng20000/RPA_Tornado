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
import re
from datetime import datetime, timedelta

glv["g_floder"] = os.path.join(os.path.expanduser('~'), 'Downloads')
file_pairs = glv["g_dict"]
def main(args):
    glv["g_floder"] = os.path.join(os.path.expanduser('~'), 'Downloads')
    file_pairs = glv["g_dict"]
    # file_pairs = {
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日4PX-美国洛杉矶1仓库存明细.xlsx': 
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日GL.iNet US店铺名称.xlsx',
        
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日4PX-德国法兰克福仓库存明细.xlsx': 
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日GL.iNet EU店铺名称.xlsx',
        
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日4PX-英国路腾仓库存明细.xlsx': 
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日GL.iNet UK店铺名称.xlsx',
        
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日4PX-加拿大温哥华仓库存明细.xlsx': 
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日GL.iNet CA店铺名称.xlsx',
        
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日电商仓库库存明细.xlsx': 
    #     'C:\\Users\\gl-02251756\\Desktop\\数据查看数据处理\\2025年03月28日gl-inet店铺名称.xlsx'
    # }
    if not file_pairs:
        print("错误: 文件对字典为空")
        return {}
    
    result_dict = process_files(file_pairs)
    if result_dict:  # 添加对返回值的检查
        print(result_dict)
        for email, file_path in result_dict.items():
            print(f"- {email}: {file_path}")
            # 验证文件是否存在
            if os.path.exists(file_path):
                print(f"✓ 已生成文件: {file_path}")
            else:
                print(f"✗ 文件未生成: {file_path}")
    # merged_data = merge_result_files()
    # if merged_data is not None:
    #     print("合并后的文件路径:", merged_data,len(merged_data))
    # else:
    #     print("未找到合并后的文件")
    return result_dict or {}  # 确保返回值始终是字典
    
# 从店铺数据中提取实际存在的日期列
def get_actual_date_columns(shop_df):
    # 匹配中文日期格式列名（YYYY-MM-DD 使用量）
    return [col for col in shop_df.columns if re.match(r'\d{4}-\d{2}-\d{2} 使用量', str(col))]

# 生成需要处理的日期列
def generate_date_columns():
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    first_day = today.replace(day=1)
    date_list = []
    current_date = today - timedelta(days=1)
    while current_date >= first_day:
        date_list.append(current_date)
        current_date -= timedelta(days=1)
    if today.day == 1:
        last_month = today - timedelta(days=1)
        first_day_last_month = last_month.replace(day=1)
        current_date = last_month
        while current_date >= first_day_last_month:
            date_list.append(current_date)
            current_date -= timedelta(days=1)
    return [f"{d.strftime('%Y-%m-%d')} 使用量" for d in reversed(date_list)]

# 主处理函数
def process_files(file_pairs=None):
    # 定义仓库-文件映射关系
    WAREHOUSE_MAPPING = {
        'annyang': ['gl-inet', 'GL.iNet UK', 'GL.iNet CA'],
        'pingyangsong': ['GL.iNet US'],
        'cecilejiang': ['GL.iNet EU']
    }

    # 定义仓库与4PX仓库的对应关系
    WAREHOUSE_4PX_MAPPING = {
        'GL.iNet US': '4PX-美国洛杉矶1',
        'GL.iNet EU': '4PX-德国法兰克福',
        'GL.iNet UK': '4PX-英国路腾',
        'GL.iNet CA': '4PX-加拿大温哥华',
        'gl-inet': '电商仓库'
    }

    try:
        # 初始化数据存储
        inventory_data = {}
        shop_data = {}
        
        # 设置输出目录
        output_dir = glv["g_floder"]
        # output_dir = os.path.dirname(__file__)
        
        if file_pairs is None:
            # 检查输入目录是否存在
            input_dir = os.path.dirname(__file__)
            if not os.path.exists(input_dir):
                print("错误: 输入目录不存在")
                return

            # 检查目录中是否有Excel文件
            excel_files = [f for f in os.listdir(input_dir) if f.endswith('.xlsx') and '~$' not in f]
            if not excel_files:
                print("错误: 目录中没有找到Excel文件")
                return

            # 获取当前日期部分，用于匹配文件
            date_pattern = re.compile(r'(\d{4})年(\d{2})月(\d{2})日')
            current_date_prefix = None
            
            # 首先确定当前日期前缀
            for file in excel_files:
                match = date_pattern.search(file)
                if match:
                    current_date_prefix = match.group(0)
                    break
            
            if not current_date_prefix:
                print("错误: 无法确定当前日期前缀，请确保文件名包含正确的日期格式（例如：2024年03月21日）")
                return

            # 读取所有文件
            files_processed = 0
            for file in excel_files:
                if current_date_prefix in file:
                    file_path = os.path.join(input_dir, file)
                    try:
                        # 识别店铺文件
                        if '店铺名称' in file:
                            for wh_key in WAREHOUSE_MAPPING.values():
                                for wh in wh_key:
                                    if wh in file:
                                        shop_data[wh] = pd.read_excel(file_path)
                                        print(f"✓ 成功读取店铺文件: {file} -> {wh}")
                                        files_processed += 1
                        
                        # 识别库存文件
                        elif '库存明细' in file:
                            for wh, warehouse_4px in WAREHOUSE_4PX_MAPPING.items():
                                if warehouse_4px in file:
                                    inventory_data[wh] = pd.read_excel(file_path)
                                    print(f"✓ 成功读取库存文件: {file} -> {wh}")
                                    files_processed += 1
                    
                    except Exception as e:
                        print(f"⚠ 警告: 读取文件 {file} 时出错: {str(e)}")

            if files_processed == 0:
                print("错误: 没有成功读取任何文件，请检查文件名格式是否正确")
                return

        # 处理传入的文件对
        files_processed = 0
        for inventory_path, shop_path in file_pairs.items():
            try:
                # 处理库存文件
                for wh, warehouse_4px in WAREHOUSE_4PX_MAPPING.items():
                    if warehouse_4px in inventory_path:
                        inventory_data[wh] = pd.read_excel(inventory_path)
                        print(f"✓ 成功读取库存文件: {os.path.basename(inventory_path)} -> {wh}")
                        files_processed += 1
                        
                        # 处理对应的店铺文件
                        if wh in WAREHOUSE_4PX_MAPPING:
                            shop_data[wh] = pd.read_excel(shop_path)
                            print(f"✓ 成功读取店铺文件: {os.path.basename(shop_path)} -> {wh}")
                            files_processed += 1
                        break
                        
            except Exception as e:
                print(f"⚠ 警告: 读取文件对时出错: {str(e)}")
                continue

            if files_processed == 0:
                print("错误: 没有成功读取任何文件，请检查文件名格式是否正确")
                return

        # 创建日期列
        date_columns = generate_date_columns()
        
        # 获取当前日期作为文件名前缀
        current_date = datetime.now().strftime('%Y年%m月%d日')
        
        # 处理每个输出分组
        for output_name, warehouses in WAREHOUSE_MAPPING.items():
            output_file = os.path.join(output_dir, f'{current_date}{output_name}.xlsx')
            print(f"处理输出文件: {output_file}")
            
            # 检查文件是否被占用
            if os.path.exists(output_file):
                try:
                    # 尝试打开文件
                    with open(output_file, 'a+b') as f:
                        pass
                except PermissionError:
                    print(f"错误: {output_file} 已被其他程序打开，请关闭后重试")
                    continue
            
            try:
                with pd.ExcelWriter(output_file) as writer:
                    sheets_added = 0
                    for wh in warehouses:
                        if wh in inventory_data and wh in shop_data:
                            print(f"  处理仓库: {wh}")
                            # 合并库存数据和店铺数据
                            inventory = inventory_data[wh]
                            shop = shop_data[wh]
                            
                            # 确保两个数据框都有SKU列
                            if 'SKU' not in inventory.columns or 'SKU' not in shop.columns:
                                print(f"  警告: {wh} 的数据缺少SKU列，跳过处理")
                                continue
                            
                            # 合并并计算使用量
                            try:
                                # 保留库存原始数据（SKU、可用量和型号）
                                inventory_sku = inventory[['SKU', '型号', '可用量']].copy()
                                
                                # 预处理SKU：去除特殊字符、空格并统一大写
                                inventory_sku['SKU'] = inventory_sku['SKU'].str.replace('[^A-Za-z0-9-]', '').str.strip().str.upper()
                                
                                # 处理店铺数据
                                shop_filtered = shop.copy()
                                shop_filtered['SKU'] = shop_filtered['SKU'].str.replace('[^A-Za-z0-9-]', '').str.strip().str.upper()
                                
                                # 生成日期列
                                date_columns = generate_date_columns()
                                
                                # 初始化结果DataFrame
                                result = inventory_sku.copy()
                                # 重命名型号列为产品名称
                                result = result.rename(columns={'型号': '产品名称'})
                                # 添加店铺名称列并设置为当前sheet页名称
                                result.insert(0, '店铺名称', wh)
                                # 添加更新时间列，设置为当前日期 - 改为中文日期格式
                                current_date_ymd = datetime.now().strftime('%Y年%m月%d日')
                                result.insert(2, '更新时间', current_date_ymd)
                                # 调整列顺序，确保列顺序正确
                                result = result[['店铺名称', '产品名称', '更新时间', 'SKU', '可用量']]
                                result['总使用量'] = 0
                                
                                # 为每个日期创建使用量列并初始化为0
                                for date_col in date_columns:
                                    result[date_col] = 0
                                
                                # 处理店铺数据中的销量
                                if '时间' in shop_filtered.columns and 'SKU' in shop_filtered.columns and '销量' in shop_filtered.columns:
                                    # 确保时间列是datetime类型
                                    shop_filtered['时间'] = pd.to_datetime(shop_filtered['时间'])
                                    
                                    # 按SKU和时间分组，计算销量总和
                                    sales_grouped = shop_filtered.groupby(['SKU', '时间'])['销量'].sum().reset_index()
                                    
                                    # 更新每个日期的使用量
                                    for _, row in sales_grouped.iterrows():
                                        date_col = row['时间'].strftime('%Y-%m-%d') + ' 使用量'
                                        if date_col in date_columns:
                                            sku_mask = result['SKU'] == row['SKU']
                                            if any(sku_mask):
                                                result.loc[sku_mask, date_col] += row['销量']
                                                result.loc[sku_mask, '总使用量'] += row['销量']
                                
                                # 确保所有数值列为整数类型
                                numeric_columns = ['可用量', '总使用量'] + date_columns
                                result[numeric_columns] = result[numeric_columns].fillna(0).astype(int)
                                
                                # 保存到对应sheet
                                result.to_excel(writer, sheet_name=wh, index=False)
                                sheets_added += 1
                                print(f"  成功保存 {wh} 的数据到 {output_name}.xlsx")
                            except Exception as e:
                                print(f"  处理 {wh} 时出错: {str(e)}")
                        else:
                            missing = []
                            if wh not in inventory_data:
                                missing.append("库存数据")
                            if wh not in shop_data:
                                missing.append("店铺数据")
                            print(f"  警告: {wh} 缺少 {', '.join(missing)}，跳过处理")
                    
                    # 添加默认工作表当没有数据时
                    if sheets_added == 0:
                        pd.DataFrame(['当前分组无有效数据']).to_excel(writer, sheet_name='无数据', index=False)
                        
            except PermissionError as e:
                print(f"错误: 无法写入文件 {output_file}，请确保文件未被占用且有写入权限")
                print(f"详细错误: {str(e)}")
            except Exception as e:
                print(f"处理文件 {output_file} 时发生错误: {str(e)}")

        # 处理完成后的统计信息
        print("\n处理完成统计:")
        print(f"- 成功处理文件数: {files_processed}")
        print(f"- 处理的仓库数: {len(inventory_data)}")
        print("- 生成的输出文件:")
        
        # 收集生成的输出文件路径
        output_files = {
            'ann.yang@gl-inet.com': os.path.join(output_dir, f'{current_date}annyang.xlsx'),
            'pingyang.song@gl-inet.com': os.path.join(output_dir, f'{current_date}pingyangsong.xlsx'),
            'cecile.jiang@gl-inet.com': os.path.join(output_dir, f'{current_date}cecilejiang.xlsx')
        }
        
        # 验证文件是否存在
        for email, file_path in output_files.items():
            if os.path.exists(file_path):
                print(f"✓ 已生成文件: {file_path}")
            else:
                print(f"✗ 文件未生成: {file_path}")
        
        return output_files

    except Exception as e:
        print(f"\n程序执行出错: {str(e)}")
        print("请检查以下可能的问题:")
        print("1. 确保所有Excel文件都已关闭")
        print("2. 确保文件名格式正确（包含日期、仓库信息等）")
        print("3. 确保文件内容格式正确（包含必要的列如SKU、时间、销量等）")
        print("4. 确保有足够的磁盘空间和写入权限")
        return {}  # 发生错误时返回空字典
   

def merge_result_files():
    """
    读取3个结果文件并合并数据
    返回：包含表头和数据的二维列表
    """
    try:
        # 获取当前日期作为文件名前缀
        current_date = datetime.now().strftime('%Y年%m月%d日')
        
        # 定义要读取的文件
        files_to_read = [
            f'{current_date}annyang.xlsx',
            f'{current_date}pingyangsong.xlsx',
            f'{current_date}cecilejiang.xlsx'
        ]
        
        # 初始化结果列表
        all_data = []
        headers = None
        glv["g_floder"] = os.path.join(os.path.expanduser('~'), 'Downloads')
        # 读取每个文件
        for file_name in files_to_read:
            file_path = os.path.join(glv["g_floder"], file_name)
            if os.path.exists(file_path):
                # 读取所有sheet
                excel_data = pd.read_excel(file_path, sheet_name=None)
                
                # 处理每个sheet的数据
                for sheet_name, df in excel_data.items():
                    # 如果还没有表头，使用第一个数据框的列名
                    if headers is None:
                        headers = df.columns.tolist()
                        all_data.append(headers)
                    
                    # 添加数据行
                    for _, row in df.iterrows():
                        all_data.append(row.tolist())
            else:
                print(f"警告: 文件不存在 - {file_path}")
        
        return all_data
    
    except Exception as e:
        print(f"合并文件时出错: {str(e)}")
        return []

# main("")
