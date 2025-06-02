import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# 🔽 モデル読み込み（Base.metadata を利用）
from app.models.base import Base
from app.models import product, transaction, transaction_item

# 🔽 .env を読み込んで環境変数を取得
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# この Alembic Config オブジェクトで ini 設定ファイルの値にアクセスできる
config = context.config

# ログ設定を ini ファイルから読み込む
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# モデルの MetaData（自動マイグレーションに必要）
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """offline モードでマイグレーション実行（DB に接続しない）"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """online モードでマイグレーション実行（実際に DB に接続）"""
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# 実行モードに応じて分岐
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()