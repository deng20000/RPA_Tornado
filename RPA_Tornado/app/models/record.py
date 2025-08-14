# record.py
# 用于定义数据模型 
from pydantic import BaseModel
from typing import List, Optional, Any

class StockAgeItem(BaseModel):
    name: str
    qty: int

class OrderRecord(BaseModel):
    wid: int
    product_id: int
    sku: str
    seller_id: str
    fnsku: str
    product_total: int
    product_valid_num: int
    product_bad_num: int
    product_qc_num: int
    product_lock_num: int
    good_lock_num: int
    bad_lock_num: int
    stock_cost_total: str
    quantity_receive: str
    stock_cost: str
    product_onway: int
    transit_head_cost: str
    average_age: int
    third_inventory: List[Any]  # 结构未知，保留 Any
    stock_age_list: List[StockAgeItem]
    available_inventory_box_qty: Optional[str]  # 有时为数字，有时为字符串

class OrderListResponse(BaseModel):
    code: int
    message: str
    data: Optional[List[OrderRecord]] = None 