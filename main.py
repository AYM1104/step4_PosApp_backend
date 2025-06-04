from fastapi import FastAPI
from app.api import product
from app.api import transactions
from app.line import api_line_webhook
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 🔍 環境変数の確認ログ（デプロイ時のみ出力される）
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
print("[DEBUG] LINE_CHANNEL_SECRET:", LINE_CHANNEL_SECRET)


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





