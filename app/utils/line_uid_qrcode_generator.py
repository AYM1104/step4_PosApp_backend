# QRコードを生成する関数

import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
import os

def generate_line_qr(line_uid: str):
    # QRに埋め込む内容（例: LINE UID付きのURL）
    qr_url = f"{os.getenv('FRONTEND_BASE_URL')}/receipt?uid={line_uid}"

    qr = qrcode.make(qr_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)
    return buf