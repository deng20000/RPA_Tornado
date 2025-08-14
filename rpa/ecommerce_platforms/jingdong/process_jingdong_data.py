import pandas as pd
import re
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

# 只保留你关心的费用项
FEE_WHITELIST = [
    "货款", "交易服务费", "佣金", "商品保险服务费", "短信服务费", "京豆", "代收配送费", "京东代付全球售消费税", "京东代收全球售消费税"
]

def extract_fee_items_and_amounts(cell):
    """
    从单元格内容中提取所有（费用项, 金额）对
    """
    result = []
    if isinstance(cell, str):
        # 以\n分割，找出所有 费用项+金额 对
        lines = [l.strip() for l in cell.split('\n') if l.strip()]
        i = 0
        while i < len(lines) - 1:
            fee_name = lines[i]
            amount_str = lines[i+1]
            if re.match(r'^[+-]?\d+(\.\d+)?$', amount_str):
                try:
                    amount = float(amount_str)
                    result.append((fee_name, amount))
                except Exception:
                    pass
                i += 2
            else:
                i += 1
    return result

def is_fee_name(name):
    # 只保留白名单内的费用项
    return name in FEE_WHITELIST

def deduplicate_columns(columns):
    """
    对列名进行去重，重复的列名会加上 _1, _2 等后缀
    """
    seen = {}
    new_columns = []
    for col in columns:
        original_col = str(col) # 确保列名是字符串，避免AttributeError
        counter = seen.get(original_col, 0)
        if counter > 0:
            col_name = f"{original_col}_{counter}"
        else:
            col_name = original_col

        while col_name in new_columns: # 确保生成的名称也唯一，以防原始数据就是 col_1 这种
            counter += 1
            col_name = f"{original_col}_{counter}"
        seen[original_col] = counter + 1 # Update next counter for original_col
        new_columns.append(col_name)
    return new_columns

def is_original_column_to_exclude_from_final_merge(col_name, fee_whitelist):
    """
    判断原始DataFrame的列名是否是需要被排除在最终合并结果之外的列。
    这包括原始的费用项列（将被fee_df替换）、以及其他不规则的费用相关列。
    """
    col_name_str = str(col_name).strip()

    print(f"DEBUG: 正在检查列名 '{col_name_str}' (repr: {repr(col_name_str)}) (类型: {type(col_name)}) ")

    # Rule 1: Explicitly keep '资金动账备注' and '货款' (they are special descriptive columns)
    if col_name_str == '资金动账备注' or col_name_str == '货款':
        print(f"DEBUG: 列 '{col_name_str}' 明确保留 (特殊描述列)。")
        return False

    # Rule 2: Exclude if it's a clean fee name from FEE_WHITELIST (it will be provided by fee_df)
    # This now applies to all fee_whitelist items *except* '货款', which is handled by Rule 1.
    if col_name_str in fee_whitelist:
        print(f"DEBUG: 列 '{col_name_str}' 是白名单费用项，排除（将被fee_df替换）。")
        return True

    # Rule 3: Exclude if it's a number-like column name (e.g., '348', '+10374.00', '348.1')
    if re.fullmatch(r'[+-]?\d+(\.\d+)?', col_name_str):
        print(f"DEBUG: 列 '{col_name_str}' 看起来像数字，排除。")
        return True

    # Rule 4: Exclude if it contains newline and a fee item (complex, concatenated fee info)
    if '\n' in col_name_str and any(fee_item in col_name_str for fee_item in fee_whitelist):
        print(f"DEBUG: 列 '{col_name_str}' 包含换行符和费用项，排除。")
        return True

    # Rule 5: Exclude if it's a fee name with a numeric suffix (e.g., '佣金.1', '货款_1', '佣金 4')
    # Use f-string directly with manual escaping for '.', '_', '\s+'
    for fee_item in fee_whitelist:
        # Ensure fee_item itself is escaped for regex special characters
        escaped_fee_item = re.escape(fee_item)

        if re.fullmatch(f"{escaped_fee_item}\\.\\d+", col_name_str) or \
           re.fullmatch(f"{escaped_fee_item}_\\d+", col_name_str) or \
           re.fullmatch(f"{escaped_fee_item}\\s+\\d+", col_name_str):
            print(f"DEBUG: 列 '{col_name_str}' 是带后缀的费用项 '{fee_item}'，排除。")
            return True

    # Rule 6: If it passes all exclusion rules, keep it (it's a valid descriptive column)
    print(f"DEBUG: 列 '{col_name_str}' 保留。")
    return False

def process_excel_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    print(f"成功读取Excel文件，共{len(df)}行数据")

    # 打印原始表头信息 (Keep this for debugging)
    print("原始表头:")
    for i, col in enumerate(df.columns):
        print(f"列{i}: {col}")

    # 在所有操作前，先对原始DataFrame的列名进行去重
    df.columns = deduplicate_columns(df.columns)

    # 1. 逐行提取费用项和金额，只保留白名单
    fee_rows = []
    for row in df.itertuples(index=False):
        fee_dict = {name: 0 for name in FEE_WHITELIST}
        for cell in row:
            if isinstance(cell, str):
                lines = [l.strip() for l in cell.splitlines() if l.strip()]
                for i in range(0, len(lines)-1, 2):
                    fee_name = lines[i].strip() # 确保费用项名称干净
                    try:
                        amount = float(lines[i+1])
                        if fee_name in fee_dict:
                            fee_dict[fee_name] += amount
                    except Exception:
                        continue
        fee_rows.append(fee_dict)
    fee_df = pd.DataFrame(fee_rows, columns=FEE_WHITELIST)

    # 2. 确定要保留的原始列（非费用项的列，且不是旧的、不规范的费用项列）
    original_cols_to_keep = []
    for col in df.columns:
        if not is_original_column_to_exclude_from_final_merge(col, FEE_WHITELIST):
            original_cols_to_keep.append(col)
    print(f"DEBUG: 最终保留的原始列：{original_cols_to_keep}")

    # 3. 合并：原始非费用列 + 新生成的费用列
    result_df = pd.concat([df[original_cols_to_keep].reset_index(drop=True), fee_df], axis=1)

    # 4. 再次对合并后的result_df列名去重，以防万一
    result_df.columns = deduplicate_columns(result_df.columns)

    # 5. 合计并打印
    summary = fee_df.sum(axis=0)
    print("各费用项合计：")
    print(summary)

    # 6. 添加合计行
    summary_row = {col: "" for col in result_df.columns}
    # 优先将'费用汇总'放到'地区'列下，如果'地区'列不存在，则找第一个非费用项列
    if '地区' in result_df.columns:
        summary_row['地区'] = "费用汇总"
    else:
        first_non_fee_col_found = False
        for col_name in result_df.columns:
            if col_name not in FEE_WHITELIST:
                summary_row[col_name] = "费用汇总"
                first_non_fee_col_found = True
                break
        if not first_non_fee_col_found and result_df.columns.any(): # 如果都是费用项列，就用第一个列
            summary_row[result_df.columns[0]] = "费用汇总"

    for fee_name in FEE_WHITELIST:
        if fee_name in summary: # 确保费用项存在于汇总中
            summary_row[fee_name] = summary[fee_name]

        result_df = pd.concat([result_df, pd.DataFrame([summary_row])], ignore_index=True)
        
    # 7. 保存
    with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                result_df.to_excel(writer, sheet_name='统计后', index=False)
    print(f"处理后的数据已保存到{file_path}的'统计后'表中")

    # 8. 返回结果字典
    return {
        "fee_summary": summary.to_dict(),
        "summary_row_data": summary_row
    }

if __name__ == "__main__":
    excel_file = "c:\\Users\\gl-02251756\\Desktop\\rpa\\jingdong\\2025年05月31日京东数据明细.xlsx"
    print(process_excel_data(excel_file))