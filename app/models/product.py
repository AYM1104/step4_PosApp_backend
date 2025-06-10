from sqlalchemy import Column, Integer, String
from app.models.base import Base


# 商品テーブルを作成
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)  # 商品ID
    product_code = Column(String(25), nullable=True)              # 商品コード
    jan_code = Column(String(13), unique=True)          # JANコード
    name = Column(String(50), nullable=False)           # 商品名
    price = Column(Integer, nullable=False)             # 商品価格（税抜）
    genre_large = Column(String(50))
    genre_middle = Column(String(50))
    genre_small = Column(String(50))