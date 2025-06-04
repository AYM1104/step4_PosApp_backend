from fastapi import FastAPI
from app.api import product
from app.api import transactions
from app.line import api_line_webhook
from fastapi.middleware.cors import CORSMiddleware

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

import logging
import os

logger = logging.getLogger("uvicorn")

@app.get("/")
def root():
    secret = os.getenv("LINE_CHANNEL_SECRET")
    if secret:
        logger.info("✅ LINE_CHANNEL_SECRET (GET /): 設定されています（長さ: %d）", len(secret))
    else:
        logger.warning("❌ LINE_CHANNEL_SECRET (GET /): 未設定です")
    return {"message": "Azure MySQL Connected!"}




# ルーターを登録
app.include_router(product.router)
app.include_router(transactions.router)
app.include_router(api_line_webhook.router)




