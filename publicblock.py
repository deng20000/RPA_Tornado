import datetime
import os

def add_date_time_to_sublists(input_list):
    """
    title: 子列表添加日期和时间
    description: 获取%当前日期%并将其添加到%每个子列表%的头部，同时在尾部添加%当前录入时间%。
    inputs: 
        - input_list (list): 包含子列表的列表，eg: "[[1,2,3], ['a','b']]"
    outputs: 
        - result_list (list): 处理后列表，eg: "[[日期,1,2,3,时间], [日期,'a','b',时间]]"
    """
    
    # 1. 检查输入有效性
    if not isinstance(input_list, list):
        raise ValueError("输入必须是列表类型")
    
    # 2. 获取当前日期和时间
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 3. 为每个子项添加日期和时间
   
    for sublist in input_list:
        if not isinstance(sublist, list):
            input_list.insert(0,current_date)
            input_list.append(current_time)
            break
        else:
            sublist.insert(0,current_date)
            sublist.append(current_time)

def delete_file_if_exists(file_path):
    """
    title: 检验并删除文件
    description: 检查指定路径的文件是否存在，如果存在则删除该文件，返回操作结果。
    inputs: 
        - file_path (str): 文件路径，eg: "C:/temp/test.txt"
    outputs: 
        - result (str): 操作结果，eg: "文件已删除"
    """
    
    # 检查输入有效性
    if not isinstance(file_path, str):
        return "错误：文件路径必须是字符串类型"
    
    # 检查文件是否存在
    if os.path.isfile(file_path):
        try:
            # 删除文件
            os.remove(file_path)
            return f"文件 '{file_path}' 已成功删除"
        except Exception as e:
            return f"删除文件时出错: {str(e)}"
    else:
        return f"文件 '{file_path}' 不存在，无需删除"

def convert_to_2d_array(nested_list):
    # 初始化一个空列表来存储二维数组
    result = []
    
    # 遍历嵌套列表中的每个子列表
    for sublist in nested_list:
        # 遍历子列表中的每个项目
        for item in sublist:
            # 将每个项目添加到结果列表中
            result.append(item)
    
    return result