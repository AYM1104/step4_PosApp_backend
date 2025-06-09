from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
# from app.line import model_line_user
from datetime import datetime

import qrcode
from io import BytesIO
import base64
from app.line.send_line_message import reply_text_message
from app.line.model_line_user import LineUser

import os
from dotenv import load_dotenv
load_dotenv()

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

router = APIRouter()

""" DBにLINEUIDを登録する関数 """
def register_line_user(user_id: str, db: Session):
    # 重複を確認
    existing = db.query(LineUser).filter(LineUser.line_uid == user_id).first()
    if existing:
        return
    # 重複がなければ新規登録
    new_user = LineUser(line_uid=user_id, created_at=datetime.utcnow())
    db.add(new_user)
    db.commit()



""" LINEの友達追加イベントを受け取り、DBにユーザーを登録するエンドポイント """
@router.post("/line/webhook")
async def line_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    print("📨 Webhook受信:", body)
    signature = request.headers.get("x-line-signature")

    # セキュリティチェック
    # hash = hmac.new(LINE_CHANNEL_SECRET.encode('utf-8'), body, hashlib.sha256).digest()
    # computed_signature = base64.b64encode(hash).decode('utf-8')
    # if signature != computed_signature:
    #     raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    for event in data.get("events", []):
        event_type = event.get("type")
        user_id = event["source"]["userId"]

        # 1. 友だち追加イベント：ユーザー登録
        if event_type == "follow":
            register_line_user(user_id, db)

        # 2. 「QRコード」メッセージに反応してその場で画像生成→返信
        elif event_type == "message" and event["message"]["type"] == "text":
            text = event["message"]["text"].strip().lower()
            if text in ["qrコード", "qr", "qr code"]:
                # DBにユーザーが存在するか確認（念のため）
                user = db.query(LineUser).filter(LineUser.line_uid == user_id).first()
                if not user:
                    register_line_user(user_id, db)

                # ✅ QRコード表示ページのURLを生成して送信
                qr_page_url = f"{FRONTEND_BASE_URL}/line/qr?user_id={user_id}"
                await reply_text_message(
                    reply_token=event["replyToken"],
                    text=f"こちらがあなた専用のQRコードです！\n{qr_page_url}"
                )

    return JSONResponse(content={"status": "ok"})