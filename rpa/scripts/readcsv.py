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
import re
import os
import chardet
from typing import List, Union, Optional
from colorama import init, Fore, Style

# 初始化colorama用于彩色输出
init()

def main(args):
    # 设置正确的文件路径
    file_path = glv["g_downfile"]
    result = extract_rewards_data(file_path)
    
    # 美化输出结果
    # print(f"\n{Fore.CYAN}===== 数据提取结果 ====={Style.RESET_ALL}")
    metrics = ['Loyalty增量收入', '兑换者收入', '复购率', '复购客户数']
    for metric, value in zip(metrics, result):
        if value is not None:
            print(f"{Fore.GREEN}✓ {metric}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
    
            # print(f"{Fore.RED}✗ {metric}: 未找到数据{Style.RESET_ALL}")
    # print(f"{Fore.CYAN}======================{Style.RESET_ALL}\n")
    
    return result
def parse_currency_value(value_str):
    if pd.isna(value_str):
        return None
    # 转换为字符串并移除空格
    value_str = str(value_str).strip()
    
    # 检查是否为百分比格式
    if value_str.endswith('%'):
        try:
            # 保持百分比格式，包括%符号
            return value_str
        except ValueError:
            return None
    
    # 移除货币符号和千位分隔符
    value_str = value_str.replace('$', '').replace(',', '')
    
    # 检查是否为带括号的负数
    if value_str.startswith('(') and value_str.endswith(')'):
        value_str = '-' + value_str[1:-1]
        
    try:
        return float(value_str)
    except ValueError:
        return None

def detect_file_encoding(file_path: str) -> str:
    """检测文件编码"""
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def extract_rewards_data(file_path: str) -> List[Optional[Union[float, str]]]:
    """提取奖励数据
    
    Args:
        file_path: CSV文件路径
        
    Returns:
        包含四个指标的列表：[loyalty_revenue, redeemer_revenue, repeat_rate, repeat_customers]
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        # print(f"{Fore.RED}错误: 文件 '{file_path}' 不存在{Style.RESET_ALL}")
        return [None, None, None, None]
    
    # 检测文件编码
    try:
        encoding = detect_file_encoding(file_path)
        # print(f"{Fore.BLUE}文件编码: {encoding}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}检测文件编码时出错: {e}{Style.RESET_ALL}")
        encoding = 'utf-8'  # 使用默认编码
        
    # 读取CSV文件
    try:
        # 读取CSV文件，跳过前两行（标题行），指定列名
        df = pd.read_csv(file_path, 
                        skiprows=2, 
                        names=['Metric', 'Category', 'Value'],
                        encoding=encoding)
        
        # 数据清理
        df = df.dropna(how='all')  # 删除全空行
        df = df.fillna('')  # 将NA值替换为空字符串
        df = df.reset_index(drop=True)  # 重置索引
        
        # 清理字符串列中的空白字符
        df['Metric'] = df['Metric'].str.strip()
        df['Category'] = df['Category'].str.strip()
    except Exception as e:
        print(f"读取CSV文件时出错: {e}")
        return [None, None, None, None]
    
    # 提取所需数据
    try:
        # 打印DataFrame的前几行，使用更美观的格式
        # print(f"\n{Fore.CYAN}=== 数据预览（前5行）==={Style.RESET_ALL}")
        # print(df.head().to_string())
        # print(f"{Fore.CYAN}======================{Style.RESET_ALL}\n")
        
        # 使用更严格的数据提取逻辑
        def extract_value(metric_name, sub_category):
            try:
                # 使用列名来访问数据，添加更多的错误检查
                if 'Metric' not in df.columns or 'Category' not in df.columns or 'Value' not in df.columns:
                    print(f"{Fore.RED}错误: CSV文件格式不正确，缺少必要的列{Style.RESET_ALL}")
                    return None
                    
                row = df[(df['Metric'] == metric_name) & (df['Category'] == sub_category)]
                if not row.empty:
                    value = parse_currency_value(row.iloc[0]['Value'])
                    if value is not None:
                        print(f"{Fore.GREEN}找到 {metric_name} ({sub_category}): {Fore.YELLOW}{value}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}警告: {metric_name} ({sub_category}) 的值无法解析{Style.RESET_ALL}")
                    return value
                else:
                    print(f"{Fore.RED}未找到匹配的数据: {metric_name} ({sub_category}){Style.RESET_ALL}")
                return None
            except Exception as e:
                print(f"{Fore.RED}提取 {metric_name} ({sub_category}) 时出错: {e}{Style.RESET_ALL}")
                return None

        loyalty_revenue = extract_value('Loyalty incremental revenue', 'Total')
        redeemer_revenue = extract_value('Redeemer revenue', 'Total')
        repeat_rate = extract_value('Repeat purchase rate', 'Rate')
        repeat_customers = extract_value('Repeat purchase rate', 'Repeat customers')
        
        if loyalty_revenue is None:
            print("警告: 未找到Loyalty incremental revenue数据")
        if redeemer_revenue is None:
            print("警告: 未找到Redeemer revenue数据")
        if repeat_rate is None:
            print("警告: 未找到Repeat purchase rate (Rate)数据")
        if repeat_customers is None:
            print("警告: 未找到Repeat purchase rate (Repeat customers)数据")

        # 返回结果列表
        return [
            redeemer_revenue,
            loyalty_revenue,
            repeat_rate,
            repeat_customers
        ]
    except Exception as e:
        print(f"处理数据时出错: {e}")
        return [None, None, None, None]
