from .statistics_routes import statistics_routes
from .base_data_routes import base_data_routes
from .multi_platform_routes import multi_platform_routes
from .product_routes import product_routes
from .amazon_table_routes import amazon_table_routes
from .dashboard_routes import dashboard_routes

routes = statistics_routes + base_data_routes + multi_platform_routes + product_routes + amazon_table_routes + dashboard_routes