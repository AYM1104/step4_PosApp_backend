"""
model_line_token.py

LINEユーザーに紐づく一時的な識別用トークンを管理するSQLAlchemyモデル。
QRコード等に埋め込んでユーザー識別・連携に使用される。
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base  # 既存の Base クラスを継承

class LineToken(Base):
    """
    LINEトークン管理用テーブル定義。

    ・token: 一意の識別子（UUIDなど）
    ・line_user_id: 発行元のLINEユーザー（line_users.id）とのリレーション
    ・is_used: すでに使用されたかどうかのフラグ
    ・expires_at: 有効期限（任意設定）
    """
    __tablename__ = "line_tokens"

    token = Column(String(255), primary_key=True, index=True)  # UUIDなどを想定
    line_user_id = Column(Integer, ForeignKey("line_users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=True)

    # 関連ユーザー（多対1）
    line_user = relationship("LineUser", back_populates="tokens")