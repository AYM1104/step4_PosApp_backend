from app.database import engine, SessionLocal
from app.models.product import Base, Product  # あなたのモデルに合わせて変更

# テーブル作成
Base.metadata.create_all(bind=engine)
print("✅ テーブル作成完了")


