from googleapiclient.discovery import build
from datetime import datetime
import time
import random
import concurrent.futures
from datetime import datetime

def main(args):
    # API密钥
    API_KEY = 'AIzaSyBpDtGKQarw7EhfmATCyQgDqSlhbhJDMTA'
    glv["g_已发布视频汇总已更新数据"] = verify_data( API_KEY)
    glv["g_当天时间"] = datetime.now().strptime('%Y-%m-%d')
    print("完成更新后数据为:", glv["g_已发布视频汇总已更新数据"])


def get_video_info(video_url, Remark, api_key):
    # 修改逻辑
    # 1.URL为空、无法提取到视频ID/未找到视频信息、未找到频道信息、API请求异常、处理过程出错 不修改逻辑
    try:
        # 更健壮的视频ID提取
        video_id = None
        if not video_url:  # 增加空URL检查
            Remark = "URL为空"
            return {"Remark": Remark}
            
        if 'youtu.be' in video_url:
            try:
                video_id = video_url.split('youtu.be/')[1].split('?')[0].strip()
            except:
                Remark = "无法从youtu.be URL提取视频ID"
                return {"Remark": Remark}
        elif 'youtube.com' in video_url:
            try:
                if 'v=' in video_url:
                    video_id = video_url.split('v=')[1].split('&')[0].strip()
            except:
                Remark = "无法从youtube.com URL提取视频ID"
                return {"Remark": Remark}
        
        if not video_id:
            Remark = f"无法从URL提取视频ID: {video_url}"
            return {"Remark": Remark}
            
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        try:
            # 一次性获取所有需要的信息
            video_response = youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                Remark = f"未找到视频信息: {video_url}"
                return {"Remark": Remark}
            
            video_item = video_response['items'][0]
            stats = video_item['statistics']
            channel_id = video_item['snippet']['channelId']
            
            # 获取频道信息
            channel_response = youtube.channels().list(
                part='statistics',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                Remark = f"未找到频道信息: {channel_id}"
                return {"Remark": Remark}
                
            return {
                "Remark": Remark  # 保留原有备注
            }
            
        except Exception as e:
            Remark = f"API请求出错: {str(e)}"
            return {"Remark": Remark}
            
    except Exception as e:
        Remark = f"处理过程出错: {str(e)}"
        return {"Remark": Remark}

def verify_data(api_key):
    # 定义线程处理函数 
#     {'08pwHALj5Y': {'Views': '11457', 'Likes': '159', 'Comments': '39', 'Subscribers': '26700'}, 
# 'Review Link': 'https://youtu.be/PQiV9ovIWsY'}
    # 定义线程处理函数 
    def _process_single_row(row): 
        try: 
            # 从数据中获取视频链接 
            url = row.get('Review Link')
            Remark = row.get('备注', '')
            if url: 
                result = get_video_info(url, Remark, api_key)
                if result: 
                    if 'Remark' in result:
                        row['备注'] = result['Remark']
                    print(f"处理结果: {result}")
                else: 
                    row['备注'] = "未获取到视频信息"
            else:
                row['备注'] = "未提供视频URL"
        except Exception as e: 
            row['备注'] = f"处理异常: {str(e)}"
            print(f"处理单条数据时出错: {str(e)}")
 
    data_list = glv["g_已发布视频汇总未更新数据"] 
    # 创建线程池（建议5-10个线程）
    with concurrent.futures.ThreadPoolExecutor(max_workers=20)  as executor:
        futures = [executor.submit(_process_single_row, row) for row in data_list]
        for future in concurrent.futures.as_completed(futures): 
            try:
                future.result() 
            except Exception as e:
                print(f"线程执行出错: {str(e)}")
    return data_list
 
