import pandas as pd
import os

def process_excel_data(input_file, output_file):
    """
    处理Excel数据的主函数
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    print(f"开始处理Excel文件...")
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")

    try:
        # 1. 读取原始Excel文件的订单sheet
        print("\n1. 正在读取原始Excel文件...")
        df = pd.read_excel(input_file, sheet_name='订单')
        print(f"成功读取订单数据，共 {len(df)} 行")

        # 2. 保存到新的Excel文件
        print("\n2. 正在创建新的Excel文件...")
        df.to_excel(output_file, sheet_name='订单', index=False)
        print("新Excel文件创建成功")

        # 3. 读取新文件并进行条件筛选
        print("\n3. 正在进行数据筛选...")
        df = pd.read_excel(output_file, sheet_name='订单')

        # 筛选条件
        mask = (df['明细状态'] != '关闭')
        filtered_df = df[mask]
        print(f"筛选后数据行数: {len(filtered_df)}")

        # 4. 创建汇总sheet
        print("\n4. 正在创建汇总sheet...")
        summary_columns = ['发货时间', '订单号', '系统单号', '【线上】规格', '商品编码', 
                         '数量','运费','税额', '系统备注', '明细状态', 
                         '买家实付', '仓库名称','商品名称','折后单价','应收总计', 
                         '线上备注', '出库单号', '店铺名称']

        # 检查列是否存在
        available_columns = [col for col in summary_columns if col in df.columns]
        summary_df = filtered_df[available_columns].copy()
        
        # 读取国内平台销售料号维护表
        print("\n正在读取国内平台销售料号维护表...")
        product_table = pd.read_excel('国内平台销售料号维护表.xlsx', sheet_name='Sheet1')
        product_mapping = product_table.set_index('商品编码')['【线上】规格'].to_dict()
        
        # 匹配并填充【线上】规格
        # 匹配并填充【线上】规格
        original_count = len(summary_df[summary_df['【线上】规格'].notna()])
        summary_df['【线上】规格'] = summary_df['商品编码'].map(product_mapping).fillna(summary_df['【线上】规格'])
        new_count = len(summary_df[summary_df['【线上】规格'].notna()])
        print(f"成功填充【线上】规格字段: {new_count - original_count}条")
        
        # 格式化发货时间为YYYY/MM/DD
        summary_df['发货时间'] = pd.to_datetime(summary_df['发货时间']).dt.strftime('%Y/%m/%d')
        
        # 在"数量"列后插入"产品金额"列
        summary_df.insert(summary_df.columns.get_loc('数量')+1, '产品金额', summary_df['折后单价'] * summary_df['数量'])
        print("汇总sheet创建完成")

        # 5. 创建对公打款sheet
        print("\n5. 正在创建对公打款sheet...")
        # 获取所有包含"线下"或"对公"的系统备注
        target_values = summary_df[
            summary_df['系统备注'].str.contains('线下|对公', na=False)
        ]['系统备注'].unique()
        
        # 使用isin进行筛选
        public_payment_df = summary_df[summary_df['系统备注'].isin(target_values)]
        # 打印筛选后的系统备注
        print("\n对公打款sheet中的系统备注值:")
        print(public_payment_df['系统备注'].unique())
        print(f"对公打款数据行数: {len(public_payment_df)}")

        # 6. 创建售后sheet
        print("\n6. 正在创建售后sheet...")
        after_sale_df = summary_df[summary_df['系统备注'].str.contains('来自售后', na=False)]
        print(f"售后数据行数: {len(after_sale_df)}")

        # 7. 创建销售sheet
        print("\n7. 正在创建销售sheet...")
        # 销售数据 = 汇总 - 对公打款 - 售后
        sales_df = summary_df[
            ~summary_df.index.isin(public_payment_df.index) & 
            ~summary_df.index.isin(after_sale_df.index)
        ]
        print(f"销售数据行数: {len(sales_df)}")

        # 保存所有sheet
        print("\n8. 正在保存所有sheet到Excel文件...")
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, sheet_name='订单', index=False)
            summary_df.to_excel(writer, sheet_name='汇总', index=False)
            public_payment_df.to_excel(writer, sheet_name='对公打款', index=False)
            after_sale_df.to_excel(writer, sheet_name='售后', index=False)
            sales_df.to_excel(writer, sheet_name='销售', index=False)
        
        print("\n处理完成！")
        return True
        
    except Exception as e:
        print(f"\n错误: {str(e)}")
        return False

def main():
    # 定义输入和输出文件路径
    input_file = '输入文件\\2025年06月05日国内订单下载年月.xlsx'
    output_file = '2025年06月5号国内订单下载年月处理后.xlsx'
    
    # 执行处理
    success = process_excel_data(input_file, output_file)
    
    if success:
        print("程序执行成功！")
    else:
        print("程序执行失败！")

if __name__ == "__main__":
    main()