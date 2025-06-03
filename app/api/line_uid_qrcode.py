
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.utils.line_uid_qrcode_generator import generate_line_qr

router = APIRouter()

@router.get("/line/qr/{line_uid}")
def get_qr_code(line_uid: str):
    buf = generate_line_qr(line_uid)
    return StreamingResponse(buf, media_type="image/png")