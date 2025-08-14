# 限流器模块
# 实现API请求的限流功能，防止接口被恶意调用

import time
from typing import Dict, Optional
from threading import Lock


class TokenBucket:
    """令牌桶算法实现"""
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        初始化令牌桶
        
        Args:
            capacity: 桶容量
            refill_rate: 令牌补充速率（每秒补充的令牌数）
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        """
        消费令牌
        
        Args:
            tokens: 需要消费的令牌数
            
        Returns:
            bool: 是否成功消费令牌
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def _refill(self):
        """补充令牌"""
        now = time.time()
        time_passed = now - self.last_refill
        tokens_to_add = time_passed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now


class RateLimiter:
    """限流器"""
    
    def __init__(self):
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = Lock()
    
    def is_allowed(
        self, 
        key: str, 
        capacity: int = 10, 
        refill_rate: float = 1.0, 
        tokens: int = 1
    ) -> bool:
        """
        检查是否允许请求
        
        Args:
            key: 限流键（通常是IP地址或用户ID）
            capacity: 桶容量
            refill_rate: 令牌补充速率
            tokens: 需要消费的令牌数
            
        Returns:
            bool: 是否允许请求
        """
        with self.lock:
            if key not in self.buckets:
                self.buckets[key] = TokenBucket(capacity, refill_rate)
            
            return self.buckets[key].consume(tokens)
    
    def get_bucket_status(self, key: str) -> Optional[Dict[str, float]]:
        """
        获取桶状态
        
        Args:
            key: 限流键
            
        Returns:
            Dict: 桶状态信息
        """
        if key in self.buckets:
            bucket = self.buckets[key]
            with bucket.lock:
                bucket._refill()
                return {
                    'capacity': bucket.capacity,
                    'tokens': bucket.tokens,
                    'refill_rate': bucket.refill_rate
                }
        return None
    
    def clear_bucket(self, key: str):
        """清除指定的桶"""
        with self.lock:
            if key in self.buckets:
                del self.buckets[key]
    
    def clear_all_buckets(self):
        """清除所有桶"""
        with self.lock:
            self.buckets.clear()


# 全局限流器实例
rate_limiter = RateLimiter()