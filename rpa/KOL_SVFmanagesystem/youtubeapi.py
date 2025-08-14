from googleapiclient.discovery import build
from datetime import datetime
import time
import random
import concurrent.futures
import json


g_已发布视频汇总未更新_data = [
    {'Review Link': 'https://youtu.be/example1', 'Title': '视频1'},
    {'Review Link': 'https://youtu.be/example2', 'Title': '视频2'}
]

def main(args):
    # API密钥
    API_KEY = 'AIzaSyBpDtGKQarw7EhfmATCyQgDqSlhbhJDMTA'
    try:
        updated_data = verify_data(API_KEY)
        print("完成更新后数据为:", updated_data)
        # 将更新后的数据保存到文件
        with open('updated_video_data.json', 'w', encoding='utf-8') as f:
            json.dump({
                'status': 'success',
                'last_updated': datetime.now().isoformat(),
                'data': updated_data
            }, f, indent=4, ensure_ascii=False)
        print("数据已成功保存到updated_video_data.json")
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")
    


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
                return {"Views": "", "Likes": "", "Comments": "", "Subscribers": ""}
                
            return {
                "Views": str(stats.get('viewCount', '')),
                "Likes": str(stats.get('likeCount', '')),
                "Comments": str(stats.get('commentCount', '')),
                "Subscribers": str(channel_response['items'][0]['statistics'].get('subscriberCount', ''))
            }
            
        except Exception as e:
            print(f"API请求出错: {str(e)}")
            return {"Views": "", "Likes": "", "Comments": "", "Subscribers": ""}
            
    except Exception as e:
        print(f"处理过程出错: {str(e)}")
        return {"Views": "", "Likes": "", "Comments": "", "Subscribers": ""}

def verify_data(api_key):
    # 定义线程处理函数 
    def _process_single_row(row): 
        try: 
            # 从数据中获取视频链接 
            url = row.get('Review Link') 
            if url: 
                result = get_video_info(url, api_key) 
                if result: 
                    print(f"成功获取视频信息: {result}")
                    # 更新原始数据
                    row.update({
                        'Views': result['Views'],
                        'Likes': result['Likes'],
                        'Comments': result['Comments'],
                        'Subscribers': result['Subscribers']
                    })
                else: 
                    print("未获取到视频信息")
            else:
                print("未找到视频链接:", row) 

        except Exception as e: 
            print(f"处理单条数据时出错: {str(e)}") 
 
    data_list = g_已发布视频汇总未更新_data
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(_process_single_row, row) for row in data_list]
        for future in concurrent.futures.as_completed(futures): 
            try:
                future.result() 
            except Exception as e:
                print(f"线程执行出错: {str(e)}")
    return data_list

main("")
