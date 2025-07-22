from .statistics_routes import statistics_routes
from .base_data_routes import base_data_routes
from .multi_platform_routes import multi_platform_routes

routes = statistics_routes + base_data_routes + multi_platform_routes 