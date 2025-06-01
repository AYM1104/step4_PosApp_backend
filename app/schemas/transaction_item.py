from pydantic import BaseModel

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

    class Config:
        orm_mode = True