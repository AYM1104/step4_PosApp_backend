from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# 入力用スキーマ（1つの商品）
class TransactionItemCreate(BaseModel):
    jan_code: str
    name: str
    price: int
    quantity: int

# 入力用スキーマ（取引全体）
class TransactionCreate(BaseModel):
    register_user_code: Optional[str] = None
    items: List[TransactionItemCreate]
    
# 出力用スキーマ（1つの商品）
class TransactionItemResponse(BaseModel):
    id: int
    transaction_id: int
    jan_code: str
    name: str
    price: int
    quantity: int
    product_code: Optional[str] = None
    tax_cd: Optional[str] = None

    class Config:
        orm_mode = True


# 出力用スキーマ（取引全体）
class TransactionResponse(BaseModel):
    id: int
    transaction_time: datetime
    register_user_code: str     
    store_code: str             
    pos_id: str
    total_excluding_tax: int 
    total_tax: int
    total_amount: int
    total_items: int
    items: List[TransactionItemResponse]

    class Config:
        orm_mode = True