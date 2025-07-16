def paginate(total: int, page: int, page_size: int) -> dict:
    """返回分页信息，包括offset等"""
    offset = (page - 1) * page_size
    return {
        'total': total,
        'page': page,
        'page_size': page_size,
        'offset': offset,
        'pages': (total + page_size - 1) // page_size
    } 