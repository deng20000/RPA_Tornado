# routes.py
# 路由注册（自动收集装饰器方式）
routes = []

def route(path, methods=["GET"]):
    def decorator(cls):
        routes.append((path, cls))  # 只保留前两个参数，兼容Tornado
        return cls
    return decorator

# 确保所有handler被import，路由才能注册
from app.handlers.lingxing_auth import LingxingOrderHandler 