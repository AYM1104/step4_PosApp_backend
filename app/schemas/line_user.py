from pydantic import BaseModel
from datetime import datetime

class LineUserCreate(BaseModel):
    line_uid: str

class LineUserResponse(BaseModel):
    line_uid: str
    created_at: datetime

    class Config:
        orm_mode = True