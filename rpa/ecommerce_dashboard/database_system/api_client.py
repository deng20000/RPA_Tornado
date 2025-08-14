import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self, base_url: str = "http://192.168.17.123"):
        self.base_url = base_url
        
    def get_seller_list(self, offset: int = 0, length: int = 200) -> Optional[Dict[str, Any]]:
        """获取销售商列表"""
        try:
            url = f"{self.base_url}/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list"
            headers = {
                "Content-Type": "application/json"
            }
            payload = {
                "offset": offset,
                "length": length,
                "is_sync": 1,
                "status": 1
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # 检查HTTP错误
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"API请求失败: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"处理API响应时出错: {str(e)}")
            return None
