routes = []

def route(path):
    def decorator(cls):
        routes.append((path, cls))
        return cls
    return decorator

from app.ecommerce_dashboard.handlers.stat_handler import SaleStatHandler

# 注册统一路由
route("/api/ecommerce/sale_stat")(SaleStatHandler) 