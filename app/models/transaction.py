from sqlalchemy import Column, Integer, String, DateTime
from app.models.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    register_user_code = Column(String(20), nullable=False, default="9999999999")
    store_code = Column(String(10), nullable=False, default="30")
    pos_id = Column(String(10), nullable=False, default="90") 
    total_excluding_tax = Column(Integer, nullable=False)
    total_tax = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable=False) 
    total_items = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Transaction → TransactionItem の1対多リレーション
    items = relationship("TransactionItem", back_populates="transaction")