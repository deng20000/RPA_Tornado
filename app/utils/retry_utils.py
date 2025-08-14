import asyncio
import time
from functools import wraps
from .log_utils import log_exception

def sync_retry(func, times=3, delay=2):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(times):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_exception(e)
                if attempt == times - 1:
                    raise
                time.sleep(delay)
    return wrapper

def async_retry(func, times=3, delay=2):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        for attempt in range(times):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log_exception(e)
                if attempt == times - 1:
                    raise
                await asyncio.sleep(delay)
    return wrapper 