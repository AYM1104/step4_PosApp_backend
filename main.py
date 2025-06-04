from fastapi import FastAPI
from app.api import product
from app.api import transactions
from app.line import api_line_webhook
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔍 環境変数の確認ログ（デプロイ時のみ出力される）ーーーーーー
import os

try:
    print("[DEBUG] LINE_CHANNEL_SECRET:", os.getenv("LINE_CHANNEL_SECRET"))
except Exception as e:
    print("[ERROR] SECRET読み込みで例外:", e)

# ーーーーーーーーーーーーーーーーーーーーーーーーーーーー  

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://app-step4-25.azurewebsites.net"
    ],  # Next.js devサーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターを登録
app.include_router(product.router)
app.include_router(transactions.router)
app.include_router(api_line_webhook.router)





