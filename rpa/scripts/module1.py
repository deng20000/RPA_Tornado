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

import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any

def extract_data_from_html_string(html_content: str) -> Optional[Dict[str, str]]:
    """
    Extract specified fields from HTML-like string content.
    
    Args:
        html_content: HTML-like string content
        
    Returns:
        Dictionary with extracted fields or None if parsing fails
    """
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tables in the HTML content
    tables = soup.find_all('table')
    
    if not tables:
        return None
    
    # Fields to extract
    fields = ["Your Name","Job title","Business Email","Phone","Company Name","Company Website","How did you first learn about GL.INet","Select the solution you are most interested in...","Tell us more about your company/the project you're working on to help us understand your needs...","Schedule a meeting/phone call","I want to receive any promotion offers or industry news","Unique ID"]
    
    # Alternative field names that might appear
    field_alternatives = {
        "Company Name": ["Company Name / Website"],
        "Company Website": ["Company Name / Website"],
        "Select the solution you are most interested in...": [
            "Which solution are you interested in？",
            "Which product are you interested in?",
            "Why are you interested in partnering with GL.iNet?"
        ],
        "Tell us more about your company/the project you're working on to help us understand your needs...": [
            "Anything you want to tell us in advan",
            "What specific GL.iNet products or solutions are you most interested in?",
            "Do you have any specific collaboration ideas or projects in mind?",
            "Are there any additional details you'd like to share?"
        ],
        "I want to receive any promotion offers or industry news": [
            "I don't want to receive any promotion offers or industry news",
            "I'd like to receive newsletters from GL.iNet about new product release, industry insights and other commercial messages.",
            "I agree to GL.iNet's term of service."
        ]
    }
    
    # Extract data from each table and keep the most complete one
    all_data = []
    
    for table in tables:
        data = {}
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                field = cols[0].get_text().strip()
                value = cols[2].get_text().strip()
                
                # Check if field is in our target fields
                if field in fields:
                    data[field] = value
                else:
                    # Check alternative field names
                    for original_field, alternatives in field_alternatives.items():
                        if field in alternatives:
                            data[original_field] = value
                            # 处理需要反转值的字段
                            if field == "I don't want to receive any promotion offers or industry news":
                                if value.lower() == "true":
                                    data[original_field] = "false"
                                elif value.lower() == "false":
                                    data[original_field] = "true"
                            # 注意：对于其他替代字段，可能需要根据实际情况进行特殊处理
                            # 这里我们保持原值，但在实际应用中可能需要根据字段含义进行调整
        
        if data:
            all_data.append(data)
    
    # If we have multiple tables with data, choose the most complete one
    if not all_data:
        return None
    
    # Sort by number of keys (most complete data first)
    all_data.sort(key=lambda x: len(x), reverse=True)
    
    # Get the most complete data
    most_complete_data = all_data[0]
    
    # Attempt to fill any missing fields from other tables
    for field in fields:
        if field not in most_complete_data or not most_complete_data[field]:
            for data in all_data[1:]:
                if field in data and data[field]:
                    most_complete_data[field] = data[field]
                    break
    
    # Initialize all fields with empty strings if they don't exist
    for field in fields:
        if field not in most_complete_data:
            most_complete_data[field] = ""
    
    return most_complete_data

def process_html_strings(html_strings: List[str]) -> List[Dict[str, str]]:
    """
    Process multiple HTML strings and extract data while avoiding duplicates.
    
    Args:
        html_strings: List of HTML-like string content
        
    Returns:
        List of dictionaries with extracted data from each unique submission
    """
    all_extracted_data = []
    seen_unique_ids = set()
    
    for html_content in html_strings:
        data = extract_data_from_html_string(html_content)
        
        if data and "Unique ID" in data and data["Unique ID"]:
            unique_id = data["Unique ID"]
            
            # Check if this submission has already been processed
            if unique_id not in seen_unique_ids:
                seen_unique_ids.add(unique_id)
                all_extracted_data.append(data)
        elif data:
            # No Unique ID, so check for duplication based on email and name
            is_duplicate = False
            for existing_data in all_extracted_data:
                if (data.get("Business Email", "") == existing_data.get("Business Email", "") and 
                    data.get("Your Name", "") == existing_data.get("Your Name", "") and
                    data.get("Business Email", "") and data.get("Your Name", "")):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                all_extracted_data.append(data)
    
    return all_extracted_data

def format_data_output(data_list: List[Dict[str, str]]) -> str:
    """
    Format the extracted data into a readable string.
    
    Args:
        data_list: List of dictionaries containing extracted data
        
    Returns:
        Formatted string with the extracted data
    """
    output = ""
    fields = ["Your Name","Job title","Business Email","Phone","Company Name","Company Website","How did you first learn about GL.INet","Select the solution you are most interested in...","Tell us more about your company/the project you're working on to help us understand your needs...","Schedule a meeting/phone call","I want to receive any promotion offers or industry news","Unique ID"]
    
    for i, data in enumerate(data_list, 1):
        output += f"Record {i}:\n"
        for field in fields:
            output += f"  {field}: {data.get(field, '')}\n"
        output += "\n"
    
    return output

def extract_from_strings(html_strings: List[str]) -> List[List[str]]:
    """
    Main function to extract data from HTML-like strings and return a 2D list.
    
    Args:
        html_strings: List of HTML-like string content
        
    Returns:
        2D list where each row is a record and each column is a field value in the same order as fields
    """
    # The fields to extract in the defined order
    fields = ["Your Name","Job title","Business Email","Phone","Company Name","Company Website","How did you first learn about GL.INet","Select the solution you are most interested in...","Tell us more about your company/the project you're working on to help us understand your needs...","Schedule a meeting/phone call","I want to receive any promotion offers or industry news","Unique ID"]
    
    # Get the dictionary data first
    dict_data = process_html_strings(html_strings)
    
    # Convert to 2D list with ordered fields
    result_list = []
    for data in dict_data:
        row = [data.get(field, "") for field in fields]
        result_list.append(row)
    
    return result_list

# import datetime
from datetime import datetime
def process_data_for_output(data_list: List[List[str]], date: str = None) -> List[List[str]]:
    gemail = glv["g_线索人邮箱"]
    """
    Process the extracted data list by:
    1. Adding date at the first position of each row
    2. Adding "线索名称" with same value as "Company Name" (position 4) at the end
    3. Adding "国外官网" field as the second additional field (empty string)
    4. Adding "0" at the end
    
    Args:
        data_list: List of lists containing the extracted data
        date: Optional custom date string in YYYY-MM-DD format. If None, current date is used.
        
    Returns:
        Processed data list with additional fields
    """
    # Get date in YYYY-MM-DD format (use provided date or today's date)
    if date is None:
        today = datetime.now().strftime("%Y-%m-%d")
    else:
        today = date
    
    processed_data = []
    
    # Process each data row
    for row in data_list:
        # 在原始数据中，Company Name是第5个字段（索引4）
        company_name = row[4]
        
        # Create new row with date at first position
        processed_row = [today]
        
        # Add the original data
        processed_row.extend(row)
        
        # Add the three additional fields at the end
        processed_row.append(company_name)  # 线索名称，与Company Name相同
        processed_row.append("国外官网")  # 国外官网，空字符串
        processed_row.append("0")  # 末尾添加0
        processed_row.append(gemail) # 添加邮箱
        processed_data.append(processed_row)
    
    return processed_data

def filter_array(data):
    """
    筛选二维列表中符合条件的行：
    - 第二项(索引1)不为空
    - 第四项(索引3)不为空
    - 第六项(索引5)不为空
    - 最后一项为0
    
    Args:
        data: 二维列表
        
    Returns:
        tuple: (筛选后的结果列表, 行号列表)
        行号 = 索引 + 2
    """
    filtered_data = []
    row_numbers = []
    
    for i, row in enumerate(data):
        # 确保行有足够的元素
        if len(row) >= 15:
            # 检查条件：第二项、第四项、第六项不为空，最后一项为0
            if (row[1] and row[3] and row[5] and 
                row[-1] == 0):
                filtered_data.append(row)
                # 行号 = 索引 + 2
                row_numbers.append(i + 2)
    
    return filtered_data, row_numbers