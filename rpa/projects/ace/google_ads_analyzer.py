#!/usr/bin/env python3
"""
谷歌账户数据查看
查看广告数据（CPC、ROAS、CPM、花费等）
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Dict, List, Optional
import sys

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent.parent))

from config import get_config
from utils.logger import LoggerMixin, log_execution_time

class GoogleAdsAnalyzer(LoggerMixin):
    """谷歌广告数据分析器"""
    
    def __init__(self):
        self.config = get_config()
        self.output_dir = self.config.OUTPUT_DIR / "ace"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 目标地区
        self.target_regions = ['US', 'EU', 'CA', 'GL', 'UK']
        
        # 结果列
        self.result_columns = [
            '地区', '费用', '展示次数', '点击次数', '转化率', 
            '转化价值', '单位费用转化价值', '转化次数', 
            '平均每次点击费用', '点击率'
        ]
    
    def extract_region(self, ad_series: str) -> Optional[str]:
        """从广告系列名称中精确提取地区代码"""
        if pd.isna(ad_series):
            return None
        
        ad_str = str(ad_series).upper()
        
        # 正则匹配独立的大写地区代码（避免误匹配）
        for region in self.target_regions:
            if re.search(rf'\b{region}\b', ad_str):
                return region
        
        return None
    
    def compute_statistics(self, group: pd.DataFrame) -> List:
        """计算分组统计指标"""
        # 基础数值型总和
        total_cost = group['费用'].sum()
        total_imp = group['展示次数'].sum()
        total_clicks = group['点击次数'].sum()
        total_convs = group['转化次数'].sum()
        total_conv_value = group['转化价值'].sum()
        
        # 防除零处理
        def safe_division(a, b):
            return a / b if b > 0 else 0.0
        
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
    
    @log_execution_time
    def analyze_google_ads_data(self, file_path: str) -> str:
        """
        分析谷歌广告数据
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            输出文件路径
        """
        self.logger.info(f"开始分析谷歌广告数据: {file_path}")
        
        try:
            # 数据读取与预处理
            df = pd.read_excel(file_path, header=2)
            self.logger.info(f"成功读取数据，共 {len(df)} 条记录")
        except Exception as e:
            self.logger.error(f"读取文件失败: {e}")
            raise
        
        # 检查必要列
        required_columns = [
            '广告系列', '费用', '展示次数', '点击次数', '转化率', 
            '转化价值', '单位费用转化价值', '转化次数', 
            '平均每次点击费用', '点击率'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"缺少必要列: {', '.join(missing_columns)}")
        
        # 筛选需要的列
        df = df[required_columns].copy()
        
        # 提取地区并过滤
        df['地区'] = df['广告系列'].apply(self.extract_region)
        df = df[df['地区'].isin(self.target_regions)]
        
        self.logger.info(f"过滤后数据，共 {len(df)} 条记录")
        
        # 按地区聚合统计
        statistics = []
        for region in self.target_regions:
            region_group = df[df['地区'] == region]
            if not region_group.empty:
                stats = self.compute_statistics(region_group)
                statistics.append(stats)
                self.logger.info(f"{region} 地区统计完成")
        
        # 生成结果表
        result_df = pd.DataFrame(statistics, columns=self.result_columns)
        
        # 生成输出文件
        output_file = self._generate_output(result_df)
        
        self.logger.info(f"数据分析完成，输出文件: {output_file}")
        return output_file
    
    def _generate_output(self, result_df: pd.DataFrame) -> str:
        """生成输出文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"谷歌广告数据分析_{timestamp}.xlsx"
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # 主要结果
            result_df.to_excel(writer, sheet_name='地区汇总', index=False)
            
            # 添加统计信息
            summary_data = {
                '总费用': result_df['费用'].sum(),
                '总展示次数': result_df['展示次数'].sum(),
                '总点击次数': result_df['点击次数'].sum(),
                '总转化次数': result_df['转化次数'].sum(),
                '总转化价值': result_df['转化价值'].sum(),
                '平均转化率': result_df['转化率'].mean(),
                '平均点击率': result_df['点击率'].mean(),
                '平均CPC': result_df['平均每次点击费用'].mean(),
                '平均ROAS': result_df['单位费用转化价值'].mean(),
            }
            
            summary_df = pd.DataFrame([summary_data])
            summary_df.to_excel(writer, sheet_name='总体统计', index=False)
        
        return str(output_file)
    
    def generate_report(self, result_df: pd.DataFrame) -> str:
        """生成分析报告"""
        report_lines = []
        report_lines.append("=" * 50)
        report_lines.append("谷歌广告数据分析报告")
        report_lines.append("=" * 50)
        report_lines.append("")
        
        # 总体统计
        total_cost = result_df['费用'].sum()
        total_imp = result_df['展示次数'].sum()
        total_clicks = result_df['点击次数'].sum()
        total_convs = result_df['转化次数'].sum()
        total_conv_value = result_df['转化价值'].sum()
        
        report_lines.append("📊 总体统计:")
        report_lines.append(f"  总费用: ${total_cost:,.2f}")
        report_lines.append(f"  总展示次数: {total_imp:,}")
        report_lines.append(f"  总点击次数: {total_clicks:,}")
        report_lines.append(f"  总转化次数: {total_convs:,}")
        report_lines.append(f"  总转化价值: ${total_conv_value:,.2f}")
        report_lines.append(f"  平均转化率: {result_df['转化率'].mean():.2%}")
        report_lines.append(f"  平均点击率: {result_df['点击率'].mean():.2%}")
        report_lines.append(f"  平均CPC: ${result_df['平均每次点击费用'].mean():.2f}")
        report_lines.append(f"  平均ROAS: {result_df['单位费用转化价值'].mean():.2f}")
        report_lines.append("")
        
        # 地区明细
        report_lines.append("🌍 地区明细:")
        for _, row in result_df.iterrows():
            report_lines.append(f"  {row['地区']}:")
            report_lines.append(f"    费用: ${row['费用']:,.2f}")
            report_lines.append(f"    转化率: {row['转化率']:.2%}")
            report_lines.append(f"    ROAS: {row['单位费用转化价值']:.2f}")
            report_lines.append("")
        
        return "\n".join(report_lines)

def main():
    """主函数"""
    analyzer = GoogleAdsAnalyzer()
    
    # 示例用法
    file_path = input("请输入谷歌广告数据文件路径: ").strip()
    
    try:
        output_file = analyzer.analyze_google_ads_data(file_path)
        print(f"✅ 分析完成！输出文件: {output_file}")
        
        # 读取结果并生成报告
        result_df = pd.read_excel(output_file, sheet_name='地区汇总')
        report = analyzer.generate_report(result_df)
        print("\n" + report)
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 