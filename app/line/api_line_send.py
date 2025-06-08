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

    if not user_id or not cart_items:
        return JSONResponse(status_code=400, content={"error": "Missing user_id or cart_items"})

    # 🧾 各商品を1行ずつ整形（ドット記法に修正）
    lines = [
        f"{item.name} × {item.quantity}：¥{item.price * item.quantity}"
        for item in cart_items
    ]

    # ✅ 合計金額を計算
    total = sum(item.price * item.quantity for item in cart_items)

    # ✨ メッセージに合計を追加
    message = (
        "🧾 ご購入ありがとうございます！\n"
        + "\n".join(lines)
        + f"\n\n🧮 合計：¥{total}"
    )

    try:
        await push_text_message(user_id, message)
        return {"status": "ok"}
    except Exception as e:
        logging.exception("LINE送信エラー")
        return JSONResponse(status_code=500, content={"error": str(e)})