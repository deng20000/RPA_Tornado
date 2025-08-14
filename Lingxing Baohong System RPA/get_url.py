# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
import json
import os
import urllib.parse

def main(args):
    # json_data = args
    result = extract_order_info(args)
    if result is False:
        print("\n无法提取链接，请检查上述错误信息")
    elif isinstance(result, list) and result:
        print("\n提取结果:")
        print(f"共找到 {len(result)} 个链接")
        for i, link in enumerate(result):
            print(f"链接 {i+1}: {link}")
    else:
        print("\n未找到有效的链接")
    return result



def generate_order_links(order_number, wo_number):
    """
    根据order_number和wo_number生成链接列表
    
    参数:
        order_number (str): 订单号
        wo_number (str): 工单号
    
    返回:
        list: 包含生成的链接的列表
    """
    # 基础URL模板
    base_url = "https://erp.lingxing.com/erp/mmulti/mpOrderDetail"
    
    # 固定参数
    fixed_params = {
        "detailType": "showDetail",
        "route": "/mpOrderManagement",
        "tag_name": "mpOrderDetail",
        "orderType": "",
        "activeType": "undelivered"
    }
    
    # 生成链接列表
    links = []
    
    # 只生成包含两个参数的链接（第一种链接）
    if order_number != 'N/A' and wo_number != 'N/A':
        params = fixed_params.copy()
        params["orderSn"] = order_number
        params["wo_number"] = wo_number
        query_string = urllib.parse.urlencode(params)
        links.append(f"{base_url}?{query_string}")
    
    return links

def extract_order_info(json_file_path_or_data):
    """
    从JSON文件、字典或字典列表中提取order_number和wo_number
    
    参数:
        json_file_path_or_data (str或dict或list): JSON文件的路径、直接传入的字典数据或字典列表
    
    返回:
        list或False: 包含链接的列表，如果body为空则返回False
    """
    try:
        # 检查传入的是文件路径、字典还是字典列表
        if isinstance(json_file_path_or_data, list):
            # 处理字典列表
            print("使用传入的字典列表数据")
            for item in json_file_path_or_data:
                if isinstance(item, dict) and 'body' in item and item['body']:
                    print(f"在列表中找到包含有效body字段的字典")
                    # 递归调用自身处理这个字典
                    result = extract_order_info(item)
                    if result is not False:  # 如果成功提取到信息
                        return result
            # 如果遍历完列表都没有找到有效的body，返回False
            print("列表中没有找到包含有效body字段的字典")
            return False
        elif isinstance(json_file_path_or_data, dict):
            data = json_file_path_or_data
            print("使用传入的字典数据")
        else:
            # 处理文件路径
            json_file_path = json_file_path_or_data
            # 检查文件是否存在
            if not os.path.exists(json_file_path):
                print(f"错误: 找不到文件 {json_file_path}")
                print(f"当前工作目录: {os.getcwd()}")
                return None, None
                
            # 获取文件大小
            file_size = os.path.getsize(json_file_path)
            print(f"文件大小: {file_size} 字节")
            
            # 读取JSON文件
            print(f"正在读取文件: {json_file_path}")
            try:
                with open(json_file_path, 'r', encoding='utf-8') as file:
                    # 先读取文件内容
                    content = file.read()
                    print(f"成功读取文件内容，长度: {len(content)} 字符")
                    
                    # 尝试解析JSON
                    try:
                        data = json.loads(content)
                        print("JSON解析成功")
                    except json.JSONDecodeError as json_err:
                        print(f"JSON解析错误: {str(json_err)}")
                        # 显示错误位置附近的内容
                        pos = json_err.pos
                        start = max(0, pos - 50)
                        end = min(len(content), pos + 50)
                        print(f"错误位置附近的内容: ...{content[start:end]}...")
                        return None, None
            except UnicodeDecodeError as ude:
                print(f"Unicode解码错误: {str(ude)}")
                print("尝试使用不同的编码...")
                # 尝试其他编码
                for encoding in ['latin-1', 'gbk', 'cp1252']:
                    try:
                        with open(json_file_path, 'r', encoding=encoding) as file:
                            content = file.read()
                            data = json.loads(content)
                            print(f"使用 {encoding} 编码成功解析JSON")
                            break
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        continue
                else:
                    print("所有尝试的编码都失败了")
                    return None, None
        
        # 检查是否存在body字段
        if 'body' in data:
            body = data['body']
            # 检查body是否为空
            if not body:
                print("'body'字段为空")
                return False
                
            print("找到'body'字段")
            
            # 检查body的类型
            if isinstance(body, dict):
                # 提取order_number和wo_number
                order_number = body.get('order_number', 'N/A')
                wo_number = body.get('wo_number', 'N/A')
                
                print(f"提取的字段: order_number={order_number}, wo_number={wo_number}")
                # 生成链接列表
                links = generate_order_links(order_number, wo_number)
                return links if links else False
            else:
                print(f"错误: 'body'字段不是字典类型，而是 {type(body)}")
                # 如果body是字符串，可能需要再次解析
                if isinstance(body, str):
                    try:
                        print("尝试解析body字符串为JSON...")
                        body_data = json.loads(body)
                        if isinstance(body_data, dict):
                            print("成功将body字符串解析为字典")
                            # 打印body_data的所有键，帮助调试
                            print(f"body_data中的键: {list(body_data.keys())}")
                            
                            order_number = body_data.get('order_number', 'N/A')
                            wo_number = body_data.get('wo_number', 'N/A')
                            
                            # 如果没有找到这些键，尝试在嵌套结构中查找
                            if order_number == 'N/A' or wo_number == 'N/A':
                                print("在顶级未找到所需字段，尝试在嵌套结构中查找...")
                                
                                # 检查是否有list字段，订单信息可能在列表中
                                links_list = []
                                if 'list' in body_data and isinstance(body_data['list'], list) and body_data['list']:
                                    print(f"找到'list'字段，包含 {len(body_data['list'])} 个项目")
                                    
                                    # 遍历所有列表项
                                    for index, item in enumerate(body_data['list']):
                                        if isinstance(item, dict):
                                            if index == 0:
                                                print(f"第一个列表项的键: {list(item.keys())}")
                                            
                                            # 尝试从列表项中提取
                                            item_order = item.get('order_number')
                                            item_wo = item.get('wo_number')
                                            
                                            # 也尝试其他可能的键名
                                            if not item_order:
                                                item_order = item.get('orderNumber') or item.get('order_id') or item.get('orderId')
                                            if not item_wo:
                                                item_wo = item.get('woNumber') or item.get('wo_id') or item.get('woId')
                                            
                                            if item_order or item_wo:
                                                # 使用默认值'N/A'确保即使只找到一个字段也能返回完整的元组
                                                item_order = item_order or 'N/A'
                                                item_wo = item_wo or 'N/A'
                                                # 生成链接并添加到列表
                                                item_links = generate_order_links(item_order, item_wo)
                                                if item_links:
                                                    links_list.extend(item_links)
                                                print(f"项目 {index+1}: order_number={item_order}, wo_number={item_wo}")
                                    
                                    # 如果找到了链接，返回链接列表
                                    if links_list:
                                        print(f"共生成 {len(links_list)} 个链接")
                                        return links_list
                                    return False
                                
                                # 遍历所有可能的嵌套字典
                                for key, value in body_data.items():
                                    if isinstance(value, dict):
                                        temp_order = value.get('order_number')
                                        temp_wo = value.get('wo_number')
                                        if temp_order:
                                            order_number = temp_order
                                            print(f"在嵌套字典 '{key}' 中找到 order_number: {order_number}")
                                        if temp_wo:
                                            wo_number = temp_wo
                                            print(f"在嵌套字典 '{key}' 中找到 wo_number: {wo_number}")
                            
                            print(f"从字符串解析的body中提取: order_number={order_number}, wo_number={wo_number}")
                            # 生成链接列表
                            links = generate_order_links(order_number, wo_number)
                            return links if links else False
                    except json.JSONDecodeError as e:
                        print(f"无法将body字符串解析为JSON: {str(e)}")
                        # 尝试提取部分字符串进行分析
                        print(f"body字符串前100个字符: {body[:100]}...")
                return False
        else:
            print("错误: JSON文件中没有'body'字段")
            # 打印顶级键
            print(f"文件中的顶级键: {list(data.keys()) if isinstance(data, dict) else '不是字典类型'}")
            return False
    
    except json.JSONDecodeError as e:
        print(f"错误: 无法解析JSON文件: {str(e)}")
        return False
    except FileNotFoundError:
        print(f"错误: 找不到文件 {json_file_path_or_data}")
        return False
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
