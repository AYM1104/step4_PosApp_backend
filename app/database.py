import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.product import Base

# envファイルを読み込む
load_dotenv()

# envファイルからDB設定を取得
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# SQLAlchemy用のMySQL接続URLを作成
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# エンジン作成 （DB接続の入口）
engine = create_engine(DATABASE_URL, echo=True)

# セッション (DB操作時に使用)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)