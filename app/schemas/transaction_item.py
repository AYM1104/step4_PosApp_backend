from pydantic import BaseModel
from typing import Optional

# 入力用スキーマ（会計時に送る各アイテム）
class TransactionItemCreate(BaseModel):
    jan_code: str
    name: str
    price: int
    quantity: int

# 出力用スキーマ（取引内容を取得するとき用）
class TransactionItemResponse(TransactionItemCreate):
    id: int
    transaction_id: int
    product_code: Optional[str]  # ✅ 商品一意コード
    tax_cd: Optional[str]        # ✅ 消費税区分
    product_id: Optional[int]

    class Config:
        orm_mode = True