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
import psutil
from datetime import datetime

def close_wps_process():
    # 关闭所有WPS进程
    for proc in psutil.process_iter():
        try:
            if "wps" in proc.name().lower():
                proc.kill()
                print("已关闭WPS进程")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Define regions dictionary at module level
regions = {
    'US': {
        'region': 'US',
        'shopify_channel': 'Shopify',
        'amazon_channel': 'Amazon',
        'shopify_site': 'US',
        'amazon_site': 'Amazon US',
        'shopify_store_name': 'shopfiy-US买家退货',
        'amazon_store_name': '亚马逊-买家退货-US',
        'shopify_sheet_name': 'shopify-US买家退货',
        'amazon_sheet_name': '亚马逊-买家退货-US',
        'amazon_remove_sheet_name': '亚马逊移除-US',
        'removal_store_name': 'Heison NA-US',
        'amazon_remove_columns': [
            '表中来源数据', '店铺',
            'Amazon系統建移出單日期', 'Amazon移出單號',
            '移出日期', '型號', 'Amazon FUSKU',
            '產品狀態', '數量', '物流公司',
            '跟蹤號', '移除命令類型'
        ]
    },
    'UK': {
        'region': 'UK',
        'shopify_channel': 'Shopify',
        'amazon_channel': 'Amazon',
        'shopify_site': 'UK',
        'amazon_site': 'Amazon UK',
        'shopify_store_name': 'shopfiy-UK买家退货',
        'amazon_store_name': '亚马逊-买家退货-UK',
        'shopify_sheet_name': 'shopify-UK买家退货',
        'amazon_sheet_name': '亚马逊-买家退货-UK',
        'amazon_remove_sheet_name': '亚马逊移除-UK',
        'removal_store_name': 'Heison NA-UK',
        'amazon_remove_columns': [
            '表中来源数据', '店铺',
            'Amazon系統建移出單日期', 'Amazon移出單號',
            '移出日期', '型號', 'Amazon FUSKU',
            '產品狀態', '數量', '物流公司',
            '跟蹤號', '移除命令類型'
        ]
    },
    'EU': {
        'region': 'EU',
        'shopify_channel': 'Shopify',
        'amazon_channel': 'Amazon',
        'shopify_site': 'EU',
        'amazon_site': 'Amazon EU',
        'amazon_sites': ['Amazon IT', 'Amazon DE', 'Amazon FR', 'Amazon ES',
                        'Amazon NL', 'Amazon SE', 'Amazon TR', 'Amazon PL',
                        'Amazon BE', 'Amazon IE'],
        'shopify_store_name': 'shopfiy-EU买家退货',
        'amazon_store_name': '亚马逊-买家退货-EU',
        'shopify_sheet_name': 'shopify-EU买家退货',
        'amazon_sheet_name': '亚马逊-买家退货-EU',
        'amazon_remove_sheet_name': '亚马逊移除-EU',
        'removal_store_name': 'Heison NA-EU',
        'amazon_remove_columns': [
            '表中来源数据', '店铺',
            'Amazon系統建移出單日期', 'Amazon移出單號',
            '移出日期', '型號', 'Amazon FUSKU',
            '產品狀態', '數量', '物流公司',
            '跟蹤號', '移除命令類型'
        ]
    }
}

def process_returns_data_by_region(excel_path, sheet_name, region_config):
    """通用的退货数据处理函数"""
    # 先关闭WPS进程
    close_wps_process()

    # 读取Excel文件中的指定sheet
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    except FileNotFoundError:
        print(f"错误: 文件 '{excel_path}' 未找到.")
        return {}
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")
        return {}

    # 检查原始数据
    print(f"\n=== {region_config['region']}数据处理 ===")
    print("原始数据总行数:", len(df))

    # 检查必要列是否存在
    required_cols = ['购买渠道', 'shopify站点']  # 移除操作类型检查
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"错误: 原始数据缺少列: {', '.join(missing_cols)}")
        return {}

    # 检查购买渠道和站点的唯一值
    print("\n数据检查:")
    print("购买渠道的唯一值:", df['购买渠道'].unique())
    print("shopify站点的唯一值:", df['shopify站点'].unique())

    # 数据筛选（使用配置中的渠道名称）
    shopify_df = df[
        (df['购买渠道'] == region_config['shopify_channel']) &
        (df['shopify站点'] == region_config['shopify_site'])
    ].copy()

    # --- REMOVE regions dictionary definition from here ---

    # Modify the amazon_df filtering logic
    amazon_sites_list = region_config.get('amazon_sites', [region_config.get('amazon_site')])
    # Filter out None values in case amazon_site is missing and amazon_sites is used
    amazon_sites_list = [site for site in amazon_sites_list if site]
    if not amazon_sites_list:
         print(f"警告: {region_config['region']} 区域未配置有效的 Amazon 站点。")
         amazon_df = pd.DataFrame() # Create empty DataFrame
    else:
        amazon_df = df[
            (df['购买渠道'] == region_config['amazon_channel']) &
            (df['shopify站点'].isin(amazon_sites_list))
        ].copy()


    # --- ADD Amazon Remove filtering logic ---
    # --- 修改 Amazon Remove 处理逻辑 ---
    amazon_remove_df = pd.DataFrame(columns=region_config['amazon_remove_columns'])
    
    # 设置默认值
    amazon_remove_df.loc[0] = {
        '表中来源数据': '退货统计表',
        '店铺': region_config['amazon_store_name'],
        'Amazon系統建移出單日期': None,
        'Amazon移出單號': None,
        '移出日期': None,
        '型號': None,
        'Amazon FUSKU': None,
        '產品狀態': None,
        '數量': None,
        '物流公司': None,
        '跟蹤號': None,
        '移除命令类型': None
    }
    
    print(f"{region_config['amazon_remove_sheet_name']} 创建空表，包含示例行")
    
    # 直接使用创建的DataFrame
    amazon_remove_filtered = amazon_remove_df.copy()

    # Update print statement
    if 'amazon_sites' in region_config:
        sites = ', '.join(region_config['amazon_sites'])
    else:
        sites = region_config.get('amazon_site', 'N/A')
    print(f"Amazon条件: 购买渠道={region_config['amazon_channel']}, shopify站点={sites}")
    print(f"\n筛选结果:")
    print(f"{region_config['shopify_sheet_name']} 筛选出 {len(shopify_df)} 条数据")
    print(f"{region_config['amazon_sheet_name']} 筛选出 {len(amazon_df)} 条数据")
    # Print remove count if applicable
    if 'amazon_remove_sheet_name' in region_config:
        print(f"{region_config['amazon_remove_sheet_name']} 创建空表")


    # 添加新字段
    # Apply to shopify_df and amazon_df
    for current_df in [shopify_df, amazon_df]:
        if not current_df.empty:
            if '表中来源数据' not in current_df.columns:
                current_df.insert(0, '表中来源数据', '退货统计表')
            if '店铺' not in current_df.columns:
                current_df.insert(1, '店铺', None) # Initialize with None

    # Apply to amazon_remove_df if it exists and is not empty
    if not amazon_remove_df.empty:
         if '表中来源数据' not in amazon_remove_df.columns:
             amazon_remove_df.insert(0, '表中来源数据', '退货统计表')
         if '店铺' not in amazon_remove_df.columns:
             amazon_remove_df.insert(1, '店铺', None) # Initialize with None


    # 设置店铺信息
    if not shopify_df.empty:
        shopify_df['店铺'] = region_config['shopify_store_name']
    if not amazon_df.empty:
        amazon_df['店铺'] = region_config['amazon_store_name']
    if not amazon_remove_df.empty:
        amazon_remove_df['店铺'] = region_config['amazon_store_name'] # Use same store name for removal


    # 选择需要的列
    selected_columns_returns = [
        '表中来源数据', '店铺',
        '订单号', '产品型号', '数量', '购买渠道',
        '退货时间', '购买时间', '退货点',
        '客户是否寄回(寄回单号）'
    ]

    # 创建筛选后的DataFrame，不再添加默认值
    shopify_filtered = pd.DataFrame(columns=selected_columns_returns)
    if not shopify_df.empty:
        cols_to_select_s = [col for col in selected_columns_returns if col in shopify_df.columns]
        shopify_filtered = shopify_df[cols_to_select_s]

    amazon_filtered = pd.DataFrame(columns=selected_columns_returns)
    if not amazon_df.empty:
        cols_to_select_a = [col for col in selected_columns_returns if col in amazon_df.columns]
        amazon_filtered = amazon_df[cols_to_select_a]

    # 简化移除表创建逻辑，只保留列结构
    amazon_remove_filtered = pd.DataFrame(columns=region_config['amazon_remove_columns'])

    # 保存数据到Excel
    try:
        timestamp = datetime.now().strftime("%Y年%m月%d日")
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        output_file = os.path.join(downloads_dir, f'{timestamp}退货追踪{region_config["region"]}.xlsx')

        with pd.ExcelWriter(output_file) as writer:
            # Shopify数据 - 无论是否有数据都创建sheet
            shopify_filtered.to_excel(writer, sheet_name=region_config['shopify_sheet_name'], index=False)
            
            # Amazon数据 - 无论是否有数据都创建sheet
            amazon_filtered.to_excel(writer, sheet_name=region_config['amazon_sheet_name'], index=False)
            
            # 移除表 - 创建空表，只保留列结构
            if 'amazon_remove_sheet_name' in region_config:
                amazon_remove_filtered.to_excel(writer, sheet_name=region_config['amazon_remove_sheet_name'], index=False)

        print(f"\n {region_config['region']}数据已成功保存到: {output_file}")
        print("包含以下sheet页:")
        print(f"- {region_config['shopify_sheet_name']}")
        print(f"- {region_config['amazon_sheet_name']}")
        if 'amazon_remove_sheet_name' in region_config:
            print(f"- {region_config['amazon_remove_sheet_name']} (空表)")

    except Exception as e:
        print(f"\n保存{region_config['region']}数据时发生错误: {str(e)}")

    # --- Ensure return statement is correctly placed ---
    results_dict = {}
    if not shopify_filtered.empty:
        results_dict[f'shopify_{region_config["region"].lower()}'] = shopify_filtered
    if not amazon_filtered.empty:
        results_dict[f'amazon_{region_config["region"].lower()}'] = amazon_filtered
    if not amazon_remove_filtered.empty:
         results_dict[f'amazon_remove_{region_config["region"].lower()}'] = amazon_remove_filtered
    return results_dict


# --- Keep only ONE definition of regions in the main block ---
def read_removal_report(file_path, region_config):
    """读取移除货件详情报告并写入指定Excel文件"""
    if not os.path.exists(file_path):
        print(f"错误：移除货件详情文件不存在: {file_path}")
        return None
        
    try:
        # 尝试使用不同的编码方式读取
        encodings = ['utf-8', 'gbk', 'latin1']
        df = None
        
        for encoding in encodings:
            try:
                # 使用制表符分隔符读取txt文件
                df = pd.read_csv(file_path, sep='\t', encoding=encoding)
                print(f"成功使用 {encoding} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue
            
        if df is None:
            print("无法使用支持的编码读取文件")
            return None

        # 创建新的DataFrame并设置列
        new_df = pd.DataFrame(columns=[
            '表中来源数据', '店铺',
            'Amazon系統建移出單日期', 'Amazon移出單號',
            '移出日期', '型號', 'Amazon FUSKU',
            '產品狀態', '數量', '物流公司',
            '跟蹤號', '移除命令類型'
        ])

        # 填充数据
        new_df['表中来源数据'] = '亚马逊移除'  # 固定值
        new_df['店铺'] = region_config['removal_store_name']  # 使用配置中的店铺名称
        new_df['Amazon系統建移出單日期'] = df['request-date']
        new_df['Amazon移出單號'] = df['order-id']
        new_df['移出日期'] = df['shipment-date']
        new_df['型號'] = df['sku']
        new_df['Amazon FUSKU'] = df['fnsku']
        new_df['產品狀態'] = df['disposition']  # 根据图片数据设置
        new_df['數量'] = df['shipped-quantity']  # 假设列名为'数量'
        new_df['物流公司'] = df['carrier']  # 假设列名为'物流公司'
        new_df['跟蹤號'] = df['tracking-number']  # 假设列名为'跟踪号'
        new_df['移除命令類型'] = df['removal-order-type']  # 根据图片数据设置
            
        # 获取目标Excel文件路径
        target_date = datetime.now().strftime("%Y年%m月%d日")
        target_file = os.path.join(os.path.expanduser('~'), 'Downloads', f'{target_date}退货追踪{region_config["region"]}.xlsx')
        
        try:
            # 读取现有Excel文件
            with pd.ExcelWriter(target_file, mode='a', if_sheet_exists='overlay') as writer:
                # 先写入所有数据
                new_df.to_excel(writer, sheet_name=region_config['amazon_remove_sheet_name'], index=False)
                
                # 读取写入的工作表
                workbook = writer.book
                worksheet = workbook[region_config['amazon_remove_sheet_name']]
                
                # 获取数据行数（不包括表头）
                row_count = len(new_df)
                
                # 对每一行数据进行处理
                for row in range(2, row_count + 2):  # 从第2行开始（跳过表头）
                    # 填充固定列的值
                    worksheet.cell(row=row, column=1, value='亚马逊移除')  # 表中来源数据列
                    worksheet.cell(row=row, column=2, value=region_config['removal_store_name'])  # 店铺列
                
            print(f"成功将移除报告数据写入到文件: {target_file}")
            
        except FileNotFoundError:
            print(f"目标Excel文件不存在: {target_file}")
            return None
        except Exception as e:
            print(f"写入Excel文件时发生错误: {str(e)}")
            return None
            
        return new_df
        
    except pd.errors.EmptyDataError:
        print(f"错误：文件为空: {file_path}")
        return None
    except Exception as e:
        print(f"处理移除货件详情文件时发生错误: {str(e)}")
        return None

def process_removal_reports(desktop_dir):
    """处理移除货件详情报告"""
    print("\n=== 处理移除货件详情报告 ===")
    output_files = []
    
    # 设置移除报告文件夹路径，使用当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")
    removal_reports_dir = os.path.join(desktop_dir, f"{current_date}移除报告报表")
    
    # 检查文件夹是否存在
    if not os.path.exists(removal_reports_dir):
        print(f"警告: 移除报告报表文件夹不存在: {removal_reports_dir}")
        return output_files
        
    # 遍历移除报告报表文件夹下的所有文件
    for file in os.listdir(removal_reports_dir):
        if not file.endswith('.txt') or not file.startswith('Heison'):
            continue

        # 确定区域
        region = None
        if 'Heison_NA-US' in file:
            region = 'US'
        elif 'Heison_EU&UK-UK' in file:
            region = 'UK'
        elif any(f'Heison_EU&UK-{country}' in file for country in 
                ['IT', 'DE', 'FR', 'ES', 'NL', 'SE', 'TR', 'PL', 'BE', 'IE']):
            region = 'EU'

        if region:
            print(f"\n处理{region}区域移除报告: {file}")
            removal_df = read_removal_report(
                os.path.join(removal_reports_dir, file),  # 使用移除报告文件夹的完整路径
                regions[region]
            )
            if removal_df is not None:
                print(f"{region}移除报告处理成功")
                
                # 获取输出文件路径
                timestamp = datetime.now().strftime("%Y年%m月%d日")
                output_file = os.path.join(os.path.expanduser('~'), 'Downloads', 
                                         f'{timestamp}退货追踪{region}.xlsx')
                if output_file not in output_files:
                    output_files.append(output_file)
    
    return output_files

def main(args):
   # 设置输入文件路径为用户桌面目录
    desktop_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    excel_path = os.path.join(desktop_dir, '退货追踪.xlsx')
    sheet_name = '2025退货统计表'

    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误: 请确保文件 '退货追踪.xlsx' 位于您的桌面: {desktop_dir}")
        return

    # 处理所有区域的数据
    all_results = {}
    output_files = []
    
    # 获取当前日期
    timestamp = datetime.now().strftime("%Y年%m月%d日")
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    for region, config in regions.items():
        # 处理每个区域的数据
        region_results = process_returns_data_by_region(
            excel_path,
            sheet_name,
            config
        )
        all_results.update(region_results)
        
        # 添加每个区域的输出文件路径
        output_file = os.path.join(downloads_dir, f'{timestamp}退货追踪{region}.xlsx')
        if os.path.exists(output_file):
            output_files.append(output_file)

    print("\n所有区域处理完成.")

    # 处理移除报告
    removal_files = process_removal_reports(desktop_dir)
    # 合并所有输出文件路径
    output_files.extend(removal_files)
    
    # 返回所有输出文件路径
    return ';'.join(output_files)

# if __name__ == '__main__':
#     print(main(None))