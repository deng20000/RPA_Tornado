# -*- coding: utf-8 -*-
import xbot
from xbot import print, sleep
from . import package
from .package import variables as glv
import pandas as pd
from xbot import excel
import numpy as np
import re
from xbot.app import logging
def main(args):
    file_path = args
    logging.info(file_path)
    target_regions = ['US', 'EU', 'CA', 'GL', 'UK']  # 统一定义目标地区
    resultset = [['地区', '费用', '展示次数', '点击次数', 
                         '转化率', '转化价值', '单位费用转化价值',
                         '转化次数', '平均每次点击费用', '点击率']]
    try:
        # 数据读取与预处理
        df = pd.read_excel(file_path, header=2)
        required_columns = ['广告系列', '费用', '展示次数', '点击次数', 
                        '转化率', '转化价值', '单位费用转化价值', 
                        '转化次数', '平均每次点击费用', '点击率']
        df = df[required_columns].copy()
        # 提取地区并过滤
        df['地区'] = df['广告系列'].apply(extract_region)
        df = df[df['地区'].isin(target_regions)]       
        # 按地区聚合统计
        statistics = []
        for region in target_regions:
            region_group = df[df['地区'] == region]
            if not region_group.empty:
                stats = compute_statistics(region_group)
                statistics.append(stats)
            
            # 生成结果表
        result_cols = ['地区', '费用', '展示次数', '点击次数', 
                    '转化率', '转化价值', '单位费用转化价值',
                    '转化次数', '平均每次点击费用', '点击率']
        result_df = pd.DataFrame(statistics, columns=result_cols)
        logging.info(result_df)
        resultset.append(result_df.values.tolist())
        logging.info(resultset)
        return resultset
    except Exception as e:
        print(f"处理文件 {file_path} 失败: {str(e)}")
    print(resultset)
    return resultset

def extract_region(ad_series):
    """从广告系列名称中精确提取地区代码"""
    if pd.isna(ad_series):
        return None
    ad_str = str(ad_series).upper()
    # 正则匹配独立的大写地区代码（避免误匹配）
    for region in ['US', 'EU', 'CA', 'GL', 'UK']:
        if re.search(rf'\b{region}\b', ad_str):
            return region
    return None

def compute_statistics(group):
    """计算分组统计指标"""
    # 基础数值型总和
    total_cost = group['费用'].sum()
    total_imp = group['展示次数'].sum()
    total_clicks = group['点击次数'].sum()
    total_convs = group['转化次数'].sum()
    total_conv_value = group['转化价值'].sum()
    
    # 防除零处理
    safe_division = lambda a, b: a / b if b > 0 else 0.0
    
    # 比率指标计算
    conversion_rate = safe_division(total_convs, total_clicks)
    ctr = safe_division(total_clicks, total_imp)
    avg_cpc = safe_division(total_cost, total_clicks)
    roas = safe_division(total_conv_value, total_cost)
    
    return [
        group['地区'].iloc[0],  # 地区名称
        total_cost,            # 总费用
        total_imp,             # 总展示
        total_clicks,          # 总点击
        conversion_rate,       # 转化率
        total_conv_value,      # 总转化价值
        roas,                  # 单位费用转化价值
        total_convs,           # 总转化次数
        avg_cpc,               # 平均点击成本
        ctr                    # 点击率
    ]

if __name__ == "__main__":
    main("")