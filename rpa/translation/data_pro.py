import pandas as pd
import os
import datetime
import time


class FilterConfig:
    """筛选配置类 - 集中管理所有筛选相关的配置"""
    
    # 目标国家配置
    EU_COUNTRIES = ['英国', '德国', '法国', '比利时', '荷兰', 
                    '意大利', '西班牙', '瑞典', '爱尔兰', '土耳其']
    US_COUNTRIES = ['美国', '加拿大', '墨西哥']
    
    # 目标产品MSKU配置
    TARGET_MSKU = ["GL-BE3600", "GL-X2000"]
    
    # 必需的Excel列名
    REQUIRED_COLUMNS = ['国家', 'MSKU', '退货数量', '退货原因', '买家备注', '退货时间']
    
    # Sheet3的列名配置
    SHEET3_COLUMNS = ['來源', '產品', '平台', '負責部門', '問題總結', '需要注意?', '优先级', 
                      '重要性', '軟/硬件問題', '项目部跟进措施及进展', '評價原文', '退貨原因', 
                      '問題類型', '電商運營改善策略', '退貨地址', 'MAC地址', 'tracking No', 'Order Number', '获取数据日期']
    
    @classmethod
    def get_all_target_countries(cls):
        """获取所有目标国家列表"""
        return cls.EU_COUNTRIES + cls.US_COUNTRIES


def clean_and_preprocess_data(df):
    """
    数据清洗和预处理函数
    Args:
        df: 原始DataFrame
    Returns:
        df: 清洗后的DataFrame
    """
    print('\n=== 开始数据清洗和预处理 ===')
    
    # 验证必要列存在
    missing_cols = [col for col in FilterConfig.REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"缺失关键列: {missing_cols}，请检查Excel文件列名")
    
    # 只保留必要的列
    df = df[FilterConfig.REQUIRED_COLUMNS].copy()
    
    # 处理退货时间格式
    df['退货时间'] = pd.to_datetime(df['退货时间']).dt.date
    
    # 数据清洗与格式处理
    df['MSKU'] = df['MSKU'].astype(str).str.strip()
    
    # 加强国家列预处理 - 移除全半角空格
    df['国家'] = df['国家'].str.strip().str.replace(r'[\s\u3000]+', '', regex=True)
    
    # 添加平台列
    df['平台'] = ''
    df.loc[df['国家'].isin([s.strip() for s in FilterConfig.EU_COUNTRIES]), '平台'] = 'EU Amazon'
    df.loc[df['国家'].isin([s.strip() for s in FilterConfig.US_COUNTRIES]), '平台'] = 'US Amazon'
    
    print('数据清洗完成')
    return df


def print_data_analysis(df):
    """
    打印数据分析信息
    Args:
        df: 预处理后的DataFrame
    """
    print('\n=== 数据分析报告 ===')
    print(f'预处理后的国家值样例：{df["国家"].unique()}')
    print(f'目标国家列表：{FilterConfig.get_all_target_countries()}')
    print('平台分配情况：')
    platform_stats = df.groupby(['国家', '平台']).size().reset_index().rename(columns={0:'数量'})
    print(platform_stats.to_string(index=False))


def apply_business_filters(df):
    """
    应用业务筛选逻辑
    Args:
        df: 预处理后的DataFrame
    Returns:
        filtered_df: 筛选后的DataFrame
    """
    print('\n=== 开始应用业务筛选条件 ===')
    
    # 获取上周日期范围
    start_date, end_date, _ = get_last_week_dates()
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    
    print(f'筛选时间范围：{start_date} 到 {end_date}')
    
    # 筛选条件验证和统计
    target_countries = FilterConfig.get_all_target_countries()
    
    msku_matched = df[df["MSKU"].str.contains('|'.join(FilterConfig.TARGET_MSKU), na=False, regex=True)]
    country_matched = df[df['国家'].isin([s.strip() for s in target_countries])]
    comment_valid = df[(df['买家备注'].notna()) & (df['买家备注'].str.strip() != '')]
    date_in_range = df[(df['退货时间'] >= start_date) & (df['退货时间'] <= end_date)]
    
    print(f'MSKU匹配数量：{len(msku_matched)}')
    print(f'国家匹配数量：{len(country_matched)}')
    print(f'有效买家备注数量：{len(comment_valid)}')
    print(f'时间范围内数量：{len(date_in_range)}')
    
    # 应用所有筛选条件
    filtered_df = df[
        df["MSKU"].str.contains('|'.join(FilterConfig.TARGET_MSKU), na=False, regex=True) & 
        (df['国家'].isin([s.strip() for s in target_countries])) &
        (df['买家备注'].notna()) & 
        (df['买家备注'].str.strip() != '') &
        (df['退货时间'] >= start_date) &
        (df['退货时间'] <= end_date)
    ]
    
    print(f'最终筛选结果数量：{len(filtered_df)}')
    
    # 空数据验证
    if filtered_df.empty:
        print('\n⚠️ 警告：未找到匹配数据，请检查：')
        print('1. MSKU列值是否包含目标产品型号')
        print('2. 国家列值是否与目标国家列表完全一致')
        print('3. 数据是否包含空白或特殊字符')
        print('4. 退货时间是否在指定范围内')
        print(f'\n目标国家列表：{target_countries}')
        print(f'实际存在的国家值：{df["国家"].unique()}')
    
    return filtered_df


def create_sheet3_data(filtered_df):
    """
    创建客户问题分析数据结构
    Args:
        filtered_df: 筛选后的DataFrame
    Returns:
        sheet3_df: 客户问题分析格式的DataFrame
    """
    print('\n=== 创建客户问题分析数据结构 ===')
    
    # 获取当天日期，格式为YYYY-MM-DD
    today_date = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # 创建新的DataFrame用于Sheet3
    sheet3_df = pd.DataFrame(columns=FilterConfig.SHEET3_COLUMNS)
    
    # 填充数据
    for idx, row in filtered_df.iterrows():
        new_row = {col: '' for col in FilterConfig.SHEET3_COLUMNS}  # 初始化所有列为空
        new_row['來源'] = '退貨'  # 默认为退货
        new_row['產品'] = row['MSKU']  # 复制MSKU列
        new_row['平台'] = row['平台']  # 复制平台列
        new_row['問題總結'] = row['买家备注']  # 问题总结直接使用原始买家备注
        new_row['評價原文'] = row['买家备注']  # 评价原文为买家备注
        new_row['退貨原因'] = row['退货原因']  # 复制退货原因
        new_row['获取数据日期'] = today_date  # 设置当天日期
        sheet3_df = pd.concat([sheet3_df, pd.DataFrame([new_row])], ignore_index=True)
    
    print(f'客户问题分析数据创建完成，共{len(sheet3_df)}行')
    print(f'获取数据日期设置为: {today_date}')
    return sheet3_df


def save_results_to_excel(file_path, filtered_df, sheet3_df, sales_data=None):
    """
    保存结果到Excel文件
    Args:
        file_path: Excel文件路径
        filtered_df: 筛选后的数据
        sheet3_df: 客户问题分析格式的数据
        sales_data: 可选的销量数据字典
    
    工作表说明:
        - "周度销量数据": 包含地区/平台、MSKU、销量、退货数量、退货率、退货开始日期、退货结束日期
          按MSKU和地区/平台分组合计退货数量，并计算退货率（退货数量/销量*100%）
        - "客户问题分析": 包含來源、產品、平台、問題總結、評價原文、退貨原因等分析数据
    """
    print('\n=== 保存结果到Excel ===')
    
    try:
        # 获取上周日期范围（不跨月）
        last_week_dates = get_last_week_dates()
        start_date = last_week_dates[0]  # 上周开始日期
        end_date = last_week_dates[1]    # 上周结束日期
        
        # 创建Sheet2数据结构 - 按MSKU和地区/平台分组合计
        print('\n=== 创建周度销量数据统计 ===')
        
        # 按MSKU和平台分组，合计退货数量
        grouped_df = filtered_df.groupby(['MSKU', '平台']).agg({
            '退货数量': 'sum'  # 合计退货数量
        }).reset_index()
        
        print(f'分组后数据行数: {len(grouped_df)}')
        
        # 确保所有销量数据中的SKU+平台组合都出现在最终结果中
        if sales_data:
            # 获取现有退货数据中的组合
            existing_combinations = set()
            for _, row in grouped_df.iterrows():
                existing_combinations.add((row['MSKU'], row['平台']))
            
            # 添加所有销量数据中存在但退货数据中不存在的组合
            missing_rows = []
            
            # 遍历所有销量数据中的SKU+平台组合
            for msku in sales_data.keys():
                for platform in sales_data[msku].keys():
                    if (msku, platform) not in existing_combinations:
                        # 添加缺失的组合，退货数量默认为0
                        missing_rows.append({
                            'MSKU': msku,
                            '平台': platform,
                            '退货数量': 0  # 默认退货数量为0
                        })
            
            # 将缺失的行添加到分组数据中
            if missing_rows:
                missing_df = pd.DataFrame(missing_rows)
                grouped_df = pd.concat([grouped_df, missing_df], ignore_index=True)
                print(f'添加缺失的销量数据组合后行数: {len(grouped_df)}')
                print(f'添加的组合数量: {len(missing_rows)}')
        
        # 添加地区/平台列（复制平台列的值）
        grouped_df['地区/平台'] = grouped_df['平台']
        
        # 添加销量列
        if sales_data:
            # 根据MSKU和平台直接匹配销量数据（不进行平台名称映射）
            def get_sales_quantity(row):
                msku = row['MSKU']
                platform = row['平台']
                
                # 直接匹配平台名称
                if msku in sales_data and platform in sales_data[msku]:
                    return sales_data[msku][platform]
                
                return 0
            
            grouped_df['销量'] = grouped_df.apply(get_sales_quantity, axis=1)
        else:
            grouped_df['销量'] = 0  # 如果没有销量数据，默认为0
        
        # 不再计算退货率（已删除退货率列）
        
        # 添加退货开始日期和结束日期（默认为上周时间范围）
        grouped_df['退货开始日期'] = start_date
        grouped_df['退货结束日期'] = end_date
        
        # 定义Sheet2的列顺序（删除退货原因列和退货率列）
        sheet2_columns = [
            '地区/平台', 
            'MSKU', 
            '销量', 
            '退货数量',
            '退货开始日期', 
            '退货结束日期'
        ]
        
        # 使用分组后的数据
        sheet2_df = grouped_df
        
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            # 保存周度销量数据 - 按照新的格式
            sheet2_df[sheet2_columns].to_excel(writer, sheet_name='周度销量数据', index=False)
            print(f'✅ 数据已成功写入到 {file_path} 的"周度销量数据"工作表')
            print(f'   - 退货开始日期: {start_date}')
            print(f'   - 退货结束日期: {end_date}')
            print(f'   - 包含销量数据: {"是" if sales_data else "否"}')
            
            # 保存客户问题分析
            sheet3_df.to_excel(writer, sheet_name='客户问题分析', index=False)
            print(f'✅ 数据已成功写入到 {file_path} 的"客户问题分析"工作表')
            
    except PermissionError:
        print(f'❌ 错误：文件 {file_path} 被其他程序占用，请关闭后重试')
        raise
    except Exception as e:
        print(f'❌ 保存文件时发生错误: {e}')
        raise


def convert_sales_data_format(sales_data):
    """
    转换销量数据格式
    Args:
        sales_data: 可以是字典格式或列表格式
                   列表格式: [{'SKU': 'GL-X2000', '平台': '美亚', '数量': '29'}, ...]
                   字典格式: {"GL-X2000": {"美亚": 29}, ...}
    Returns:
        dict: 统一的字典格式 {"SKU": {"平台": 数量}}
    """
    if sales_data is None:
        return None
    
    # 如果已经是字典格式，直接返回
    if isinstance(sales_data, dict):
        return sales_data
    
    # 如果是列表格式，转换为字典格式
    if isinstance(sales_data, list):
        converted_data = {}
        for item in sales_data:
            if not isinstance(item, dict):
                continue
            
            # 获取字段值，支持不同的字段名
            sku = item.get('SKU') or item.get('MSKU') or item.get('sku') or item.get('msku')
            platform = item.get('平台') or item.get('platform') or item.get('Platform')
            quantity = item.get('数量') or item.get('quantity') or item.get('Quantity') or item.get('销量')
            
            if sku and platform and quantity is not None:
                # 确保数量是数字类型
                try:
                    quantity = int(quantity) if isinstance(quantity, str) else quantity
                except (ValueError, TypeError):
                    quantity = 0
                
                # 构建嵌套字典结构
                if sku not in converted_data:
                    converted_data[sku] = {}
                converted_data[sku][platform] = quantity
        
        return converted_data
    
    return None


def process_fba_returns(file_path, sales_data=None):
    """
    处理FBA退货订单数据的主函数
    Args:
        file_path: Excel文件路径
        sales_data: 可选的销量数据，支持两种格式：
                   1. 字典格式: {"SKU": {"平台": 数量}}
                   2. 列表格式: [{'SKU': 'GL-X2000', '平台': '美亚', '数量': '29'}, ...]
    """
    try:
        # 参数类型检查
        if not isinstance(file_path, str):
            raise TypeError(f"file_path必须是字符串类型，当前类型: {type(file_path)}")
        
        if sales_data is not None and not isinstance(sales_data, (dict, list)):
            raise TypeError(f"sales_data必须是字典类型、列表类型或None，当前类型: {type(sales_data)}")
        
        # 转换销量数据格式为统一的字典格式
        sales_data = convert_sales_data_format(sales_data)
        
        # 1. 读取Excel文件
        print('\n=== 开始处理FBA退货订单数据 ===')
        print(f'文件路径: {file_path}')
        if sales_data:
            print(f'销量数据: {sales_data}')
        
        df = pd.read_excel(file_path, engine='openpyxl', sheet_name=0)
        
        # 2. 数据预览
        print('\n=== 数据加载摘要 ===')
        print(f'总行数: {len(df)}')
        print('\n前3行数据样例:')
        print(df.head(3))
        print('\n列名清单:', df.columns.tolist())
        
        # 3. 数据清洗和预处理
        df_cleaned = clean_and_preprocess_data(df)
        
        # 4. 打印数据分析信息
        print_data_analysis(df_cleaned)
        
        # 5. 应用业务筛选逻辑
        filtered_df = apply_business_filters(df_cleaned)
        
        # 6. 设置显示格式并打印结果
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 20)
        
        print('\n=== 筛选后的退货订单数据 ===')
        if not filtered_df.empty:
            print(filtered_df.to_string(index=False))
        else:
            print('无符合条件的数据')
        
        # 7. 创建客户问题分析数据结构
        sheet3_df = create_sheet3_data(filtered_df)
        
        # 8. 保存结果到Excel
        save_results_to_excel(file_path, filtered_df, sheet3_df, sales_data)
        
        print('\n=== 数据处理完成 ===')
        
    except FileNotFoundError:
        print(f"❌ 错误：文件 {file_path} 未找到")
        raise
    except KeyError as e:
        print(f"❌ 列不存在: {e}，请检查列名匹配")
        raise
    except Exception as e:
        print(f"❌ 处理时发生错误: {e}")
        raise

def read_processed_file_content(file_path):
    """
    读取处理完成后的Excel文件内容（只读取处理后的结果数据，不包含原始数据）
    Args:
        file_path: Excel文件路径
    Returns:
        dict: 包含处理后的sheet页内容的字典
              {
                  '周度销量数据': [{'列名1': '值1', '列名2': '值2', ...}, ...],
                  '客户问题分析': [{'列名1': '值1', '列名2': '值2', ...}, ...]
              }
    """
    try:
        print(f'\n=== 开始读取处理完成的文件内容 ===')
        print(f'文件路径: {file_path}')
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        result = {
            '周度销量数据': [],
            '客户问题分析': []
        }
        
        # 读取周度销量数据sheet页
        try:
            df_sheet2 = pd.read_excel(file_path, engine='openpyxl', sheet_name='周度销量数据')
            print(f'周度销量数据 行数: {len(df_sheet2)}')
            print(f'周度销量数据 列名: {df_sheet2.columns.tolist()}')
            
            # 将DataFrame转换为字典列表，空值转换为空字符串
            for _, row in df_sheet2.iterrows():
                row_dict = {}
                for col in df_sheet2.columns:
                    value = row[col]
                    # 处理空值，转换为空字符串
                    if pd.isna(value) or value is None:
                        row_dict[col] = ""
                    else:
                        row_dict[col] = str(value)
                result['周度销量数据'].append(row_dict)
                
        except Exception as e:
            print(f'读取周度销量数据时发生错误: {e}')
            result['周度销量数据'] = []
        
        # 读取客户问题分析sheet页
        try:
            df_sheet3 = pd.read_excel(file_path, engine='openpyxl', sheet_name='客户问题分析')
            print(f'客户问题分析 行数: {len(df_sheet3)}')
            print(f'客户问题分析 列名: {df_sheet3.columns.tolist()}')
            
            # 将DataFrame转换为字典列表，空值转换为空字符串
            for _, row in df_sheet3.iterrows():
                row_dict = {}
                for col in df_sheet3.columns:
                    value = row[col]
                    # 处理空值，转换为空字符串
                    if pd.isna(value) or value is None:
                        row_dict[col] = ""
                    else:
                        row_dict[col] = str(value)
                result['客户问题分析'].append(row_dict)
                
        except Exception as e:
            print(f'读取客户问题分析时发生错误: {e}')
            result['客户问题分析'] = []
        
        print(f'\n=== 文件内容读取完成 ===')
        print(f'周度销量数据 条数: {len(result["周度销量数据"])}')
        print(f'客户问题分析 条数: {len(result["客户问题分析"])}')
        
        # 打印前几条数据作为示例
        if result['周度销量数据']:
            print(f'\n周度销量数据 第一条数据示例:')
            print(result['周度销量数据'][0])
        
        if result['客户问题分析']:
            print(f'\n客户问题分析 第一条数据示例:')
            print(result['客户问题分析'][0])
        
        return result
        
    except FileNotFoundError:
        print(f"❌ 错误：文件 {file_path} 未找到")
        raise
    except Exception as e:
        print(f"❌ 读取文件内容时发生错误: {e}")
        raise

def get_last_week_dates():
    """
    title: 获取上一周日期范围
    description: 获取上一周的周一和周日日期，以及该月第几周，格式为YYYY-MM-DD。如果日期范围跨月，则默认从当月1号开始。
    inputs: 
        - None
    outputs: 
        - result (list): 上周信息列表，eg: ["2023-05-01", "2023-05-07", 3]
    """
    
    # 获取当前日期
    today = datetime.datetime.now().date()
    
    # 计算上一周的周一
    days_since_monday = today.weekday()
    last_monday = today - datetime.timedelta(days=days_since_monday + 7)
    
    # 计算上一周的周日
    last_sunday = last_monday + datetime.timedelta(days=6)
    
    # 检查是否跨月
    if last_monday.month != today.month:
        # 如果跨月，则从当月1号开始
        last_monday = datetime.date(today.year, today.month, 1)
        # 重新计算周日（从当月1号算起的第一周的周日）
        last_sunday = last_monday + datetime.timedelta(days=6 - last_monday.weekday())
    
    # 计算该月第几周
    first_day_of_month = datetime.date(last_monday.year, last_monday.month, 1)
    
    # 计算月初第一周的结束日期
    first_week_end = first_day_of_month
    while first_week_end.weekday() < 6:  # 直到找到第一个周日
        first_week_end += datetime.timedelta(days=1)
    
    # 计算上周的周一与月初第一周结束日期之间相差多少周
    days_since_first_week = (last_monday - (first_week_end + datetime.timedelta(days=1))).days
    weeks_since_first_week = max(0, days_since_first_week // 7)
    
    # 月初第一周(不管是否满一周)算第一周，之后每过一周加1
    month_week_number = weeks_since_first_week + 2  # 加2是因为月初一周算1，然后再加上后续的周数
    
    # 特殊情况：如果last_monday刚好在月初第一周内
    if last_monday <= first_week_end:
        month_week_number = 1
    
    # 返回周一日期、周日日期和该月第几周
    result = [
        last_monday.strftime("%Y-%m-%d"),
        last_sunday.strftime("%Y-%m-%d"),
        month_week_number
    ]
    
    return result

def main(file_path, sales_data=None):
    """
    主函数：处理FBA退货订单数据
    Args:
        file_path: Excel文件的完整路径（必需参数）
        sales_data: 可选的销量数据，支持两种格式：
                   1. 字典格式: {"SKU": {"平台": 数量}}
                   2. 列表格式: [{'SKU': 'GL-X2000', '平台': '美亚', '数量': '29'}, ...]
    """
    # 参数验证
    if file_path is None:
        raise ValueError("file_path 参数不能为 None，必须提供有效的文件路径")
    
    if not isinstance(file_path, str):
        raise TypeError(f"file_path 必须是字符串类型，当前类型: {type(file_path)}")
    
    if sales_data is not None and not isinstance(sales_data, (dict, list)):
        raise TypeError(f"sales_data 必须是字典类型、列表类型或 None，当前类型: {type(sales_data)}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    print(f"开始处理文件：{file_path}")
    
    # 调用处理函数
    try:
        process_fba_returns(file_path, sales_data)
        print(f"\n✅ 文件 {file_path} 处理完成")
        return True
    except Exception as e:
        print(f"\n❌ 处理文件时发生错误：{e}")
        import traceback
        traceback.print_exc()
        raise

# 如果直接运行此脚本，则处理指定的文件
if __name__ == "__main__":
    # Mock销量数据 - 直接使用与退货数据一致的平台名称
    sale_data = [
        # US Amazon 销量数据
        {'SKU': 'GL-X2000', '平台': 'US Amazon', '数量': '29'}, 
        {'SKU': 'GL-BE3600', '平台': 'US Amazon', '数量': '581'}, 
        {'SKU': 'GL-RM1', '平台': 'US Amazon', '数量': '502'}, 
        
        # EU Amazon 销量数据
        {'SKU': 'GL-X2000', '平台': 'EU Amazon', '数量': '14'}, 
        {'SKU': 'GL-BE3600', '平台': 'EU Amazon', '数量': '150'}, 
        {'SKU': 'GL-RM1', '平台': 'EU Amazon', '数量': '133'}, 
        
        # 其他平台销量数据
        {'SKU': 'GL-X2000', '平台': 'Shopee', '数量': '0'}, 
        {'SKU': 'GL-BE3600', '平台': 'Shopee', '数量': '13'}, 
        {'SKU': 'GL-X2000', '平台': 'Walmart', '数量': '0'}, 
        {'SKU': 'GL-BE3600', '平台': 'Walmart', '数量': '0'},
        
        # 添加更多真实的销量数据示例
        {'SKU': 'GL-RM1', '平台': 'Shopee', '数量': '25'},
        {'SKU': 'GL-RM1', '平台': 'Walmart', '数量': '8'}
    ] 
    
    # 构建完整的文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, '2025年08月11日退货订单.xlsx')
    
    # 处理Excel文件
    # main(file_path, sale_data)
    result = read_processed_file_content(file_path)
    print(result.keys())