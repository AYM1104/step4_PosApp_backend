from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from app.dependencies.db import get_db
from app.line.model_line_user import LineUser
from io import BytesIO
import qrcode

router = APIRouter()


""" LINE UID を埋め込んだ QRコードを生成するエンドポイント """
@router.get("/line/qr/{user_id}")
def generate_qr_for_line_user(user_id: str, db: Session = Depends(get_db)):
    # 指定されたLINE UIDのQRコードを生成して返す
    line_user = db.query(LineUser).filter(LineUser.line_uid == user_id).first()
    if not line_user:
        raise HTTPException(status_code=404, detail="LINEユーザーが見つかりません")

    qr_data = line_user.line_uid  # 直接UIDを埋め込む（今後はtokenに拡張も可能）
    qr = qrcode.make(qr_data)

    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")