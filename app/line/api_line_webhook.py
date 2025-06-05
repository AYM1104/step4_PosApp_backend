from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.line import model_line_user
from datetime import datetime
import os
import hmac
import hashlib
import base64

router = APIRouter()

# LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")  # 必須：.env や GitHub Secretsで定義

""" DBにLINEUIDを登録する関数 """
def register_line_user(user_id: str, db: Session):
    # 重複を確認
    existing = db.query(model_line_user).filter(model_line_user.line_uid == user_id).first()
    if existing:
        return
    # 重複がなければ新規登録
    new_user = model_line_user(line_uid=user_id, created_at=datetime.utcnow())
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
        if event.get("type") == "follow":
            user_id = event["source"]["userId"]
            register_line_user(user_id, db)

    return JSONResponse(content={"status": "ok"})
