import requests
from typing import Dict, Any
from .retry_utils import sync_retry

@sync_retry
def get_exchange_rate(from_currency: str, to_currency: str, start_date: str, end_date: str, api_key: str) -> Dict[str, Any]:
    """
    获取指定时间段内的货币汇率数据。
    :param from_currency: 源货币代码，如 'CNY'
    :param to_currency: 目标货币代码，如 'USD'
    :param start_date: 开始日期，格式 'YYYY-MM-DD'
    :param end_date: 结束日期，格式 'YYYY-MM-DD'
    :param api_key: fastforex API key
    :return: 汇率数据的字典
    """
    url = f"https://api.fastforex.io/time-series?from={from_currency}&to={to_currency}&start={start_date}&end={end_date}&api_key={api_key}"
    headers = {"accept": "application/json"}
    print("[DEBUG] 汇率请求URL:", url)
    print("[DEBUG] API KEY:", api_key)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json() 
