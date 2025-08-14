import pytest
from app.services.multi_platform_service import MultiPlatformService
from app.middleware.auth import AccessTokenManager

@pytest.mark.asyncio
async def test_order_profit_msku_sign():
    access_token = await AccessTokenManager.get_token()
    service = MultiPlatformService()
    # 用你实际有权限的店铺ID
    params = {
        "offset": 0,
        "length": 1000,
        "sids": [113, 115],  # 这里必须用真实可用的sid
        "startDate": "2025-07-17",
        "endDate": "2025-07-17"
    }
    if not sids or not isinstance(sids, list) or not sids:
        raise ValueError("sids 必须为非空的店铺ID数组")
    result = await service.get_profit_report_msku(
        access_token=access_token,
        offset=params["offset"],
        length=params["length"],
        sids=params["sids"],
        startDate=params["startDate"],
        endDate=params["endDate"]
    )
    print(result)
    assert result["code"] in (0, 200), f"签名错误: {result}" 
