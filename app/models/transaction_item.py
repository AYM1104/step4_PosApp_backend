from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base
from sqlalchemy.orm import relationship

class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    jan_code = Column(String(13), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    product_code = Column(String(50), nullable=True)  # 商品一意コード（prd_id）
    tax_cd = Column(String(10), nullable=True)        # 消費税区分（例：10, 08, 非課税など）
    product_id = Column(Integer, ForeignKey("products.id"))

    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product")