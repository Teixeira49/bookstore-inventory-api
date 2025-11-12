
import math

def api_response(data=None, detail="Success", status_code=200):
    return {
        "status_code": status_code,
        "detail": detail,
        "data": data,
    }

def api_response_paginated(data=None, detail="Success", status_code=200, page: int = 0, limit: int = 10, total_items: int = 0):
    return {
        "status_code": status_code,
        "detail": detail,
        "data": data,
        "limit": limit,
        "page_number": page + 1,
        "page_index": page,
        "page_size": len(data),
        "total_items": total_items,
        "total_pages": math.ceil(total_items / limit) if limit > 0 else 0,
        "is_first_page": page == 0,
        "is_last_page": page == math.ceil(total_items / limit) - 1
    }