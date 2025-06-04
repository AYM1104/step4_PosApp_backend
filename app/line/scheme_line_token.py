"""
scheme_line_token.py

LINEトークンに関するPydanticスキーマ定義。
QRコード認証やLINE送信連携に用いる。
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LineTokenCreate(BaseModel):
    line_user_id: int


class LineTokenResponse(BaseModel):
    token: str
    line_user_id: int
    created_at: datetime
    is_used: bool
    expires_at: Optional[datetime] = None

    class Config:
        orm_mode = True