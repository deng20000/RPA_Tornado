# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
from googleapiclient.discovery import build
from datetime import datetime
import time
import random
def main(args):
    # API密钥
    API_KEY = 'AIzaSyBpDtGKQarw7EhfmATCyQgDqSlhbhJDMTA'

    # 测试数据
    # data = [['https://youtu.be/Qq9e9U6KhiU?feature=shared', 'Youtube', 'MT3000', '2025-01-03', 
    #         'The Uncast Show', 'KOL-MIcro 5k-50k', '6630', '18057', '42', '766', '', 
    #         'UGC', 'US', 'FALSE', '', 'FALSE', 'FALSE', '', '', '', '', '', '']]

    glv["g_datalist"] = verify_data(glv["g_datalist"], API_KEY)
    # for row in updated_data:
    #     print(row)
 
    # glv["g_datalist"] = verify_data(glv["g_datalist"])

    # for row in glv["g_datalist"]:
    #     print(row)  # 打印更新后的数据
#   updated_data = verify_data(args[0])
#   for row in args[0]:
#     print(row)  # 打印更新后的数据

def get_video_info(video_url, api_key):
    try:
        # 更健壮的视频ID提取
        video_id = None
        if not video_url:  # 增加空URL检查
            print("URL为空")
            return {"views": "", "likes": "", "comments": "", "subscribers": ""}
            
        if 'youtu.be' in video_url:
            try:
                video_id = video_url.split('youtu.be/')[1].split('?')[0].strip()
            except:
                pass
        elif 'youtube.com' in video_url:
            try:
                if 'v=' in video_url:
                    video_id = video_url.split('v=')[1].split('&')[0].strip()
            except:
                pass
        
        if not video_id:
            print(f"无法从URL提取视频ID: {video_url}")
            return {"views": "", "likes": "", "comments": "", "subscribers": ""}
            
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        try:
            # 一次性获取所有需要的信息
            video_response = youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                print(f"未找到视频信息: {video_url}")
                return {"views": "", "likes": "", "comments": "", "subscribers": ""}
            
            video_item = video_response['items'][0]
            stats = video_item['statistics']
            channel_id = video_item['snippet']['channelId']
            
            # 获取频道信息
            channel_response = youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                print(f"未找到频道信息: {channel_id}")
                return {"views": "", "likes": "", "comments": "", "subscribers": ""}
                
            return {
                "views": str(stats.get('viewCount', '')),
                "likes": str(stats.get('likeCount', '')),
                "comments": str(stats.get('commentCount', '')),
                "subscribers": str(channel_response['items'][0]['statistics'].get('subscriberCount', ''))
            }
            
        except Exception as e:
            print(f"API请求出错: {str(e)}")
            return {"views": "", "likes": "", "comments": "", "subscribers": ""}
            
    except Exception as e:
        print(f"处理过程出错: {str(e)}")
        return {"views": "", "likes": "", "comments": "", "subscribers": ""}

def verify_data(data_list, api_key):
    for row in data_list:
        url = row[0]
        result = get_video_info(url, api_key)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if all(result.values()):
            # 更新数据
            row[6] = result['subscribers']
            row[7] = result['views']
            row[8] = result['comments']
            row[9] = result['likes']
            row[16] = f"获取成功_{current_time}"
            
            print("数据已更新：")
            print(f"更新时间: {current_time}")
            print(f"订阅者数: {result['subscribers']}")
            print(f"观看数: {result['views']}")
            print(f"评论数: {result['comments']}")
            print(f"点赞数: {result['likes']}")
        else:
            row[16] = f"获取失败_{current_time}"
            print(f"获取数据失败，保持原有数据不变 (时间: {current_time})")
        
        # 添加随机延时避免频繁请求
        time.sleep(random.uniform(1, 3))
        
    return data_list
main("")