from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.line_user import LineUser
from datetime import datetime
import os
import hmac
import hashlib
import base64

router = APIRouter()

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")  # 必須：.env や GitHub Secretsで定義

def register_line_user(user_id: str, db: Session):
    """LINEユーザーをDBに登録（重複は無視）"""
    existing = db.query(LineUser).filter(LineUser.line_uid == user_id).first()
    if existing:
        return
    new_user = LineUser(line_uid=user_id, created_at=datetime.utcnow())
    db.add(new_user)
    db.commit()

# LINEの友達追加イベントを受け取り、ユーザー登録する
@router.post("/line/webhook")
async def line_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    print("📨 Webhook受信:", body)
    signature = request.headers.get("x-line-signature")

    # セキュリティチェック
    hash = hmac.new(LINE_CHANNEL_SECRET.encode('utf-8'), body, hashlib.sha256).digest()
    computed_signature = base64.b64encode(hash).decode('utf-8')
    if signature != computed_signature:
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    for event in data.get("events", []):
        if event.get("type") == "follow":
            user_id = event["source"]["userId"]
            register_line_user(user_id, db)

    return JSONResponse(content={"status": "ok"})



# ーーーーー仮で実装
import requests

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@router.post("/line/send-receipt")
def send_receipt_to_user(user_id: str, db: Session = Depends(get_db)):
    # 仮の買い物履歴
    message = {
        "type": "text",
        "text": "🧾 ご購入ありがとうございます！\n\n- ペン × 2本\n- ノート × 1冊\n\n合計: ¥880（税込）"
    }

    # LINEに送信
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }

    body = {
        "to": user_id,
        "messages": [message]
    }

    res = requests.post("https://api.line.me/v2/bot/message/push", json=body, headers=headers)

    if res.status_code != 200:
        print("❌ LINE送信失敗:", res.text)
        raise HTTPException(status_code=500, detail="LINE送信に失敗しました")

    return {"status": "sent"}