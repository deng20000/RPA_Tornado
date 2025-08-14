def check_status_code(response: dict, success_code=200) -> bool:
    """校验Json对象中的状态码"""
    return response.get('code') == success_code or response.get('status') == success_code 