from pydantic import BaseModel
from typing import Optional


# 入力用スキーマ
class ProductCreate(BaseModel):
    code: str
    jan_code: str
    name: str
    price: int
    genre_large: Optional[str] = None
    genre_middle: Optional[str] = None
    genre_small: Optional[str] = None
    
# 出力用スキーマ
class ProductResponse(BaseModel):
    id: int
    code: str
    jan_code: str
    name: str
    price: int
    genre_large: Optional[str] = None
    genre_middle: Optional[str] = None
    genre_small: Optional[str] = None

    # SQLAlchemyのモデルから変換できるようにする
    class Config:
        orm_mode = True