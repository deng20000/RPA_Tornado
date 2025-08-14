# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
from bs4 import BeautifulSoup

def main(args):
    pass
    # result = []
    # for _ in args:
    #     temp = extract_info_from_html(_[0],_[1])
    #     result.append(temp)
    # print("处理后数据内容为：")
    # for _ in result:
    #     print(_)
    # return result

def extract_info_from_html(html_string, send_time=None):
    """
    从HTML字符串中提取信息并转换为格式化的文本
    
    参数:
        html_string (str): HTML格式的字符串
        send_time (str, optional): 发送时间，格式为 'YYYY-MM-DD HH:MM:SS'
    
    返回:
        str: 格式化的文本信息
    """
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # 提取表格数据
    tables = soup.find_all('table')
    table_data = []
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                key = cells[0].get_text().strip()
                value = cells[2].get_text().strip()
                table_data.append((key, value))
    
    # 提取其他文本内容
    text_content = []
    for div in soup.find_all('div'):
        text = div.get_text().strip()
        if text and text not in [item[0] for item in table_data] and text not in [item[1] for item in table_data]:
            text_content.append(text)
    
    # 移除重复的表格数据
    unique_table_data = []
    seen_keys = set()
    
    for key, value in table_data:
        if key not in seen_keys:
            unique_table_data.append((key, value))
            seen_keys.add(key)
    
    # 格式化输出
    output = []
    
    # 添加邮件头部信息
    header_found = False
    for text in text_content:
        if "Hi team" in text or "Best regards" in text:
            header_found = True
            lines = text.split('\n')
            for line in lines:
                if line.strip():
                    output.append(line.strip())
            output.append("")
    
    if not header_found and text_content:
        output.append(text_content[0])
        output.append("")
    
    # 添加表格数据
    output.append("申请信息:")
    output.append("-" * 40)
    for key, value in unique_table_data:
        output.append(f"{key}: {value}")
    output.append("-" * 40)
    output.append("")
    
    # 添加发送时间
    if send_time:
        output.append(f"发送时间: {send_time}")
    
    # 合并为格式化文本
    return "\n".join(output)