"""
scheme_line_user.py

LINEユーザーに関するPydanticスキーマ定義。
主にAPIの入出力時に使われるバリデーション・整形用。
"""

from pydantic import BaseModel
from datetime import datetime


class LineUserBase(BaseModel):
    line_uid: str


class LineUserCreate(LineUserBase):
    pass


class LineUserResponse(LineUserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True