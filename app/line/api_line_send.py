# app/line/api_line_send.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from app.line.send_line_message import push_text_message
import logging

router = APIRouter()


# 🔧 Pydanticモデルを使ってバリデーション
class CartItem(BaseModel):
    jan_code: str
    name: str
    price: int
    quantity: int

class LineSendPayload(BaseModel):
    user_id: str
    cart_items: List[CartItem]


@router.post("/line/send")
async def send_purchase_to_line(payload: LineSendPayload):
    user_id = payload.user_id
    cart_items = payload.cart_items

    lines = [
        f"{item.name} × {item.quantity}：¥{item.price * item.quantity}"
        for item in cart_items
    ]
    message = "🧾 ご購入ありがとうございます！\n" + "\n".join(lines)

    try:
        await push_text_message(user_id, message)
        return {"status": "ok"}
    except Exception as e:
        logging.exception("LINE送信エラー")
        return JSONResponse(status_code=500, content={"error": str(e)})