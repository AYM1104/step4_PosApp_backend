from fastapi import FastAPI
from app.api import product, transactions, line_webhook
from fastapi.middleware.cors import CORSMiddleware
from app.api.line_uid_qrcode import router as line_uid_qrcode_router

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

# ルーターを登録
app.include_router(product.router)
app.include_router(transactions.router)
app.include_router(line_webhook.router)
app.include_router(line_uid_qrcode_router)



