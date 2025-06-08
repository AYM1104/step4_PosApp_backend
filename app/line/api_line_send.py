from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.line.send_line_message import push_text_message  # 👈 必要な関数を使う
import logging

router = APIRouter()

@router.post("/line/send")
async def send_purchase_to_line(payload: dict):
    user_id = payload.get("user_id")
    cart_items = payload.get("cart_items", [])

    if not user_id or not cart_items:
        return JSONResponse(status_code=400, content={"error": "Missing user_id or cart_items"})

    # メッセージを組み立て
    lines = [
        f"{item['name']} × {item['quantity']}：¥{item['price'] * item['quantity']}"
        for item in cart_items
    ]
    message = "🧾 ご購入ありがとうございます！\n" + "\n".join(lines)

    # LINEにプッシュ送信
    try:
        await push_text_message(user_id, message)
        return {"status": "ok"}
    except Exception as e:
        logging.exception("LINE送信エラー")
        return JSONResponse(status_code=500, content={"error": str(e)})