from app.database import engine
from app.models import Base

# テーブル作成
Base.metadata.create_all(bind=engine)
print("✅ テーブル作成完了")


