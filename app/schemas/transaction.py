from pydantic import BaseModel
from typing import List
from datetime import datetime


# 入力用スキーマ（1つの商品）
class TransactionItemCreate(BaseModel):
    jan_code: str
    name: str
    price: int
    quantity: int

# 入力用スキーマ（取引全体）
class TransactionCreate(BaseModel):
    items: List[TransactionItemCreate]
    
# 出力用スキーマ（1つの商品）
class TransactionItemResponse(BaseModel):
    id: int
    transaction_id: int
    jan_code: str
    name: str
    price: int
    quantity: int

    class Config:
        orm_mode = True


# 出力用スキーマ（取引全体）
class TransactionResponse(BaseModel):
    id: int
    created_at: datetime
    total_excluding_tax: int 
    total_tax: int
    total_amount: int
    items: List[TransactionItemResponse]

    class Config:
        orm_mode = True