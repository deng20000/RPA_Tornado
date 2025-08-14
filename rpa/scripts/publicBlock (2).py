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
import numpy as np

def main(args):
    pass


def update_subscribers_data(data,fake_data):
    pass
 


def get_excel_column_letter(index):
    """
    Convert a number to Excel-style column letter(s).
    1 -> A, 2 -> B, ..., 26 -> Z, 27 -> AA, 28 -> AB, etc.
    
    Args:
        index: The index to convert (1-based)
        
    Returns:
        Excel column letter(s)
    """
    result = ""
    while index > 0:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result

def get_excel_column_letter_plus(month_number):
    """
    Get the Excel-style letter for a month number with 3-row gaps:
    1 (January) -> B
    2 (February) -> E (B + 3)
    3 (March) -> H (E + 3)
    ...and so on
    
    Args:
        month_number: The month number (1-12)
        
    Returns:
        The corresponding Excel column letter with 3-row gaps
    """
    # January (1) is B (index 2)
    # February (2) is E (index 5)
    # So the formula is: base_index + (month_number - 1) * 3
    base_index = 2  # B is at index 2
    gap = 3  # 3-row gap between months
    
    excel_index = base_index + (month_number - 1) * gap
    return get_excel_column_letter(excel_index)

def get_month_column_new(month_number):
    """
    获取月份对应的Excel列字母：
    2月 -> B
    3月 -> F
    4月 -> G
    5月 -> H
    之后月份每+1，字母索引也+1
    
    Args:
        month_number: 月份数字 (1-12)
        
    Returns:
        对应的Excel列字母
    """
    if month_number <= 1:
        # 处理1月份的特殊情况
        return "A"
    elif month_number == 2:
        # 2月份返回B
        return "B"
    elif month_number == 3:
        # 3月份返回F
        return "F"
    else:
        # 6月份开始，每增加1个月，字母索引增加1
        # 5月是H (索引8)，所以6月是I (索引9)
        base_index = 6  # I 的索引是 9 (对应6月)
        month_offset = month_number - 3  # 从6月开始算起
        
        excel_index = base_index + month_offset
        return get_excel_column_letter(excel_index)

def get_month_letter():
    """
    Get the Excel-style letter for the current month.
    
    Returns:
        The corresponding Excel column letter
    """
    # Get current month (1-12)
    current_month = datetime.now().month
    
    # Since January (1) should be B (2), we add an offset of 1
    excel_index = current_month + 1
    return get_excel_column_letter(excel_index)

def get_month_letter_plus():
    """
    Get the Excel-style letter for the current month with 3-row gaps.
    
    Returns:
        The corresponding Excel column letter with 3-row gaps
    """
    # Get current month (1-12)
    current_month = datetime.now().month
    return get_excel_column_letter_plus(current_month)

def get_month_letter_new():
    """
    获取当前月份对应的Excel列字母
    
    Returns:
        当前月份对应的Excel列字母
    """
    current_month = datetime.now().month
    return get_month_column_new(current_month)

def calculate_differences(data):
    """
    计算嵌套列表中每对数据的差值，并在每项末尾添加差值
    
    Args:
        data: 四个子列表的列表，每个子列表包含5个数据对
        
    Returns:
        list: 包含差值的列表，保持原有格式和单位
    """
    result = []
    
    for sublist in data:
        differences = []
        for pair in sublist:
            # 处理不同类型的数据
            if '%' in pair[0]:  # 百分比数据
                val1 = float(pair[0].replace('%', ''))
                val2 = float(pair[1].replace('%', ''))
                diff = val1 - val2
                differences.append([pair[0], pair[1], f"{diff:.1f}%"])
            elif any(currency in pair[0] for currency in ['$', '€', '£']):  # 货币数据
                # 获取货币符号
                currency = '$' if '$' in pair[0] else '€' if '€' in pair[0] else '£'
                val1 = float(pair[0].replace(currency, ''))
                val2 = float(pair[1].replace(currency, ''))
                diff = val1 - val2
                differences.append([pair[0], pair[1], f"{currency}{diff:.0f}"])
            else:  # 普通数值
                val1 = float(pair[0])
                val2 = float(pair[1])
                diff = val1 - val2
                differences.append([pair[0], pair[1], f"{diff:.2f}"])
        
        result.append(differences)
    
    return result

def get_month_letters_sub():
    """
    获取从上个月到当前月的所有字母表示（包括中间月份和间隔字母），以及当前月的下一个字母
    1月=D, 2月=F, 3月=H, 4月=J, 5月=L, 6月=N, 
    7月=P, 8月=R, 9月=T, 10月=V, 11月=X, 12月=Z
    
    Returns:
        list: 从上个月到当前月的字母列表（包括间隔字母）和当前月的下一个字母
    """
    from datetime import datetime, timedelta
    
    # 获取当前日期
    current_date = datetime.now()
    # 获取上个月的日期
    last_month = current_date - timedelta(days=current_date.day)
    
    # 月份到字母的映射（1月=D，每隔2个字母递增）
    month_to_letter = {
        1: 'D', 2: 'F', 3: 'H', 4: 'J', 5: 'L',
        6: 'N', 7: 'P', 8: 'R', 9: 'T',
        10: 'V', 11: 'X', 12: 'Z'
    }
    
    # 获取起始和结束字母的ASCII码
    start_letter = month_to_letter[last_month.month]
    end_letter = month_to_letter[current_date.month]
    start_ascii = ord(start_letter)
    end_ascii = ord(end_letter)
    
    # 生成所有字母（包括间隔字母）
    result = []
    if start_ascii <= end_ascii:
        # 正常情况
        for ascii_code in range(start_ascii, end_ascii + 1):
            result.append(chr(ascii_code))
    else:
        # 跨年情况
        # 从起始字母到Z
        for ascii_code in range(start_ascii, ord('Z') + 1):
            result.append(chr(ascii_code))
        # 从A到结束字母
        for ascii_code in range(ord('A'), end_ascii + 1):
            result.append(chr(ascii_code))
    
    # 添加当前月字母的下一个字母
    next_ascii = ord(end_letter) + 1
    if next_ascii <= ord('Z'):
        result.append(chr(next_ascii))
    else:
        # 如果当前月是Z，则下一个字母回到A
        result.append('A')
    
    return result

def transform_data():
    """
    将输入的三维列表数据转换为指定格式
    
    Args:
        data: 输入的三维列表，每个子列表包含2个子列表，每个子列表包含4个元素
        
    Returns:
        result: 转换后的三维列表，按列重组数据
    """
    # 首先将三维列表展平成二维列表
    data = glv['g_compareresult']
    flat_data = []
    for group in data:
        for item in group:
            flat_data.append(item)
    
    # 转换为numpy数组并确保是字符串类型
    data_array = np.array(flat_data, dtype=str)
    
    # 创建结果列表
    result = []
    
    # 处理每一列数据
    for col in range(4):
        # 获取当前列的所有数据
        column_data = data_array[:, col]
        
        # 创建配对列表
        paired_data = []
        for i in range(0, len(column_data), 2):
            val1 = str(column_data[i])  # 确保是普通字符串
            val2 = str(column_data[i+1])  # 确保是普通字符串
            paired_data.append([val1, val2])
        
        # 将配对数据添加到结果中
        result.append(paired_data)
    glv['g_compareresult'] = result
    print(glv['g_compareresult'])
    # return result

def subtract_subscriber_data(last_month_data, current_month_data):
    """
    对两个月份的数据进行相减操作
    
    Args:
        last_month_data: 上个月的数据，二维列表格式 [[''], [''], [''], [''], ['']]
        current_month_data: 当前月的数据，二维列表格式 [['12612'], ['66862'], ['34443'], ['49912'], ['6757']]
        
    Returns:
        list: 相减后的二维列表
    """
    # 1. 数据验证
    if not isinstance(last_month_data, list) or not isinstance(current_month_data, list):
        raise ValueError("输入数据必须是列表格式")
    
    if len(last_month_data) != len(current_month_data):
        raise ValueError("两个月份的数据长度不一致")
    
    # 2. 数据处理和相减
    result = []
    for i in range(len(current_month_data)):
        # 获取当前项的数据
        current_value = current_month_data[i][0] if current_month_data[i][0] else '0'
        last_value = last_month_data[i][0] if last_month_data[i][0] else '0'
        
        # 转换为数字进行计算
        try:
            current_num = int(current_value)
            last_num = int(last_value)
            diff = current_num - last_num
            # 保持返回格式一致
            result.append([str(diff)])
        except ValueError:
            # 如果转换失败，添加0
            result.append(['0'])
    
    return result

# [['3393.62', '7875.6', '', '', '859.09'], ['-150.0', '376.0', '', '', '-57.0'], ['1.22%', '1.82%', '2.47%', '3.8%', '3.9%'], ['1.0', '11.0', '6.0', '6.0', '3.0']]

def fix_data(data):
    """
    修复数据格式，将空字符串转换为0，并计算每行合计

    Args:
        data: 待修复的数据，二维列表格式

    Returns:
        list: 修复后的二维列表，每行包含合计
    """
    result = []
    for row in data:
        new_row = []
        row_sum = 0
        
        # 处理每行数据
        for value in row:
            # 处理空值
            if value == '':
                processed_value = '0'
            else:
                processed_value = value
                
            # 计算合计（排除百分比）
            try:
                if '%' not in processed_value:
                    row_sum += float(processed_value)
            except ValueError:
                pass
                
            # 转换为列表格式
            new_row.append([processed_value])
        
        # 添加合计到行尾
        if '%' in row[0]:  # 百分比行
            new_row.append([f"{sum([float(x[0].replace('%', '')) for x in new_row if x[0] != '0']):.2f}%"])
        else:  # 数值行
            new_row.append([f"{row_sum:.2f}"])
            
        result.append(new_row)
    
    return result


def process_data(data):
    """
    处理数据，将空字符串转换为0，并计算每行合计
    规则与fix_data相同

    Args:
        data: 待处理的数据，二维列表格式

    Returns:
        list: 处理后的二维列表，每行包含合计
    """
    result = []
    for row in data:
        new_row = []
        row_sum = 0
        
        # 处理每行数据
        for value in row:
            # 处理特殊值和空值
            if value == '- $∅':
                processed_value = '0'
            else:
                processed_value = value.replace('+ ', '')  # 移除加号前缀
                
            # 转换为列表格式
            new_row.append([processed_value])
            
            # 计算合计
            try:
                if '%' in processed_value:
                    # 百分比值
                    num_value = float(processed_value.replace('%', ''))
                    row_sum += num_value
                elif any(currency in processed_value for currency in ['$', '€', '£']):
                    # 货币值
                    num_value = float(processed_value.replace('$', '').replace('€', '').replace('£', ''))
                    row_sum += num_value
                else:
                    # 普通数值
                    row_sum += float(processed_value)
            except ValueError:
                continue
        
        # 添加合计到行尾
        if '%' in row[0]:  # 百分比行
            new_row.append([f"{row_sum:.1f}%"])
        elif any(currency in row[0] for currency in ['$', '€', '£']):  # 货币行
            new_row.append([f"${row_sum:.0f}"])  # 使用美元符号作为默认货币
        else:  # 普通数值行
            new_row.append([f"{row_sum:.0f}"])
            
        result.append(new_row)
    
    return result

def process_nested_data(data):
    """
    处理数据，对第1和第2项进行累加，并将每项数据嵌套到列表中
    
    Args:
        data: 包含三个子列表的列表
        
    Returns:
        list: 处理后的列表，每项数据被嵌套，并包含累加结果
    """
    result = []
    
    for i, row in enumerate(data):
        processed_row = []
        row_sum = 0
        
        for value in row:
            # 移除千分位逗号
            clean_value = value.replace(',', '')
            
            # 将每个值嵌套到列表中
            if i == 1:  # 货币行
                # 获取货币符号
                currency = '$' if '$' in clean_value else '€' if '€' in clean_value else '£'
                num_value = float(clean_value.replace(currency, ''))
                processed_row.append([value])
                if i < 2:  # 只对前两行进行累加
                    row_sum += num_value
            else:  # 普通数值行
                num_value = float(clean_value)
                processed_row.append([value])
                if i < 2:  # 只对前两行进行累加
                    row_sum += num_value
        
        # 添加累加结果（只对前两行）
        if i < 2:
            if i == 1:  # 货币行
                processed_row.append([f"${row_sum:.0f}"])
            else:  # 普通数值行
                processed_row.append([f"{row_sum:.0f}"])
                
        result.append(processed_row)
    
    return result

def calculate_y_sum(data):
    """
    使用numpy对Y轴数据进行合计并添加到尾部
    
    Args:
        data: 二维列表数据
        
    Returns:
        list: 处理后的列表，包含Y轴合计
    """
    # import numpy as np
    
    # 转换为numpy数组
    arr = np.array(data, dtype=float)
    
    # 计算Y轴（列）的合计
    col_sums = np.sum(arr, axis=0)
    
    # 将合计转换为列表并格式化为整数字符串
    col_sums_list = [str(int(x)) for x in col_sums]
    
    # 将原数据和合计组合
    result = data + [col_sums_list]
    
    return result


def convert_to_nested_lists(data):
    """
    将每一项数据转换为嵌套列表格式
    
    Args:
        data: 二维列表数据
        
    Returns:
        list: 转换后的嵌套列表
    """
    result = []
    for row in data:
        # 将每一行的每个元素转换为单元素列表
        nested_row = [[item] for item in row]
        result.append(nested_row)
    
    return result

def extract_last_y_values(data):
    """
    使用numpy提取Y轴最后一个数据，并转换为嵌套列表格式
    
    Args:
        data: 包含Y轴数据的列表
        
    Returns:
        list: 转换后的二维列表
    """
    import numpy as np
    
    # 转换为numpy数组
    arr = np.array(data)
    
    # 提取最后一列数据
    last_column = arr[:, -1]
    
    # 将每个值转换为单元素列表，并组成二维列表
    result = [[str(value)] for value in last_column]
    
    return result
