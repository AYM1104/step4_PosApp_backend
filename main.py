from fastapi import FastAPI
from app.api import product
from app.api import transactions
from app.line import api_line_webhook
from fastapi.middleware.cors import CORSMiddleware
import os

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

@app.get("/")
def root():
    return {"message": "Azure MySQL Connected!"}

# ルーターを登録
app.include_router(product.router)
app.include_router(transactions.router)
app.include_router(api_line_webhook.router)


@app.on_event("startup")
def log_line_env():
    secret = os.getenv("LINE_CHANNEL_SECRET")
    if secret:
        print("✅ LINE_CHANNEL_SECRET:", secret)
    else:
        print("❌ LINE_CHANNEL_SECRET が未設定です")


