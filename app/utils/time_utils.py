from datetime import datetime
from typing import Tuple

def parse_time(time_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """解析时间字符串为datetime对象，支持自定义格式"""
    return datetime.strptime(time_str, fmt)

def get_time_range(start_time: str, end_time: str, fmt: str = "%Y-%m-%d") -> Tuple[datetime, datetime]:
    """返回起止时间的datetime对象，支持自定义格式"""
    return parse_time(start_time, fmt), parse_time(end_time, fmt) 