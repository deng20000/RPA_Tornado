from app.auth.openapi import OpenApiBase
from app.config import settings
from app.utils.retry_utils import async_retry

@async_retry
async def api_request(route_name: str, query_data: dict):
    api = OpenApiBase(settings.LLX_API_HOST, settings.LLX_APP_ID, settings.LLX_APP_SECRET)
    token = await api.generate_access_token()
    resp = await api.request(
        access_token=token.access_token,
        route_name=route_name,
        method="POST",
        req_body=query_data
    )
    return resp.model_dump() 