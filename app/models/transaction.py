from sqlalchemy import Column, Integer, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    total_excluding_tax = Column(Integer, nullable=False)
    total_tax = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False) 
    total_items = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Transaction → TransactionItem の1対多リレーション
    items = relationship("TransactionItem", back_populates="transaction")