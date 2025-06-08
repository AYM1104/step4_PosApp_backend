from fastapi import FastAPI
from app.api import product
from app.api import transactions
from app.line import api_line_webhook, api_line_qr, api_line_send
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv() 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://app-step4-25.azurewebsites.net"
    ],  # Next.js devサーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# import logging
# import os

# logger = logging.getLogger("uvicorn")

# @app.get("/debug/access-token")
# def check_access_token():
#     token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
#     if token:
#         logger.info("✅ LINE_CHANNEL_ACCESS_TOKEN: 設定されています（長さ: %d）", len(token))
#         return {"status": "ok", "length": len(token)}
#     else:
#         logger.warning("❌ LINE_CHANNEL_ACCESS_TOKEN: 未設定です")
#         return {"status": "missing"}




# ルーターを登録
app.include_router(product.router)
app.include_router(transactions.router)
app.include_router(api_line_webhook.router)
app.include_router(api_line_qr.router)
app.include_router(api_line_send.router)


