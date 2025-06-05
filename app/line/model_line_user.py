"""
model_line_user.py

LINE連携ユーザー情報を管理するSQLAlchemyモデル。
LINE UID（line_uid）を一意に記録し、関連するトークントラッキングに使用される。
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base  # 既存の Base クラスを継承
from app.line.model_line_token import LineToken

class LineUser(Base):
    """
    LINEユーザーを管理するテーブル定義。
    1ユーザーに対して複数のトークン（QRコードなど）を発行可能。
    """
    __tablename__ = "line_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    line_uid = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 関連するトークン（1対多の関係）
    tokens = relationship(LineToken, back_populates="line_user")