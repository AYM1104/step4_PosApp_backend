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

    transaction = relationship("Transaction", back_populates="items")