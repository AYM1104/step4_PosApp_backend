from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
# from app.line import model_line_user
from datetime import datetime

import qrcode
from io import BytesIO
import base64
from app.line.send_line_message import reply_image_message
from app.line.model_line_user import LineUser

router = APIRouter()

# LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")  # 必須：.env や GitHub Secretsで定義

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

                # ✅ QRコード生成
                qr = qrcode.make(user_id)
                buf = BytesIO()
                qr.save(buf, format="PNG")
                buf.seek(0)

                # ✅ Base64エンコードして Data URI に変換
                base64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
                # data_url = f"data:image/png;base64,{base64_image}"

                # ✅ LINEに画像として返信（Data URI は使えないので注意！）
                # → 必ず public URL or S3 にアップロードする必要あり
                # → ここでは fallback: 画像を「LINE側で表示できるURL」として仮に扱う
                image_hosting_url = f"https://1cc6-2400-2412-be0-b00-54df-ab0c-4ba-5e3e.ngrok-free.app/line/qr/{user_id}"

                await reply_image_message(
                    reply_token=event["replyToken"],
                    image_url=image_hosting_url  # ← StreamingResponseでこのURLから取得できるようにしておく
                )

    return JSONResponse(content={"status": "ok"})