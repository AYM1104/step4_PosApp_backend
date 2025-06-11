from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.models.transaction import Transaction
from app.models.transaction_item import TransactionItem
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone
from app.models.product import Product

router = APIRouter()

TAX_RATE = 0.1  # 消費税率（10%）
JST = timezone(timedelta(hours=9))  # 日本時間のタイムゾーン定義


# transactions テーブルに1件の「取引」を作成し、transaction_items テーブルにその取引に紐づく「商品明細」を複数登録する
@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(transaction_data: TransactionCreate, db: Session = Depends(get_db)):
    # 税抜金額の合計
    total_excluding_tax = sum(item.price * item.quantity for item in transaction_data.items)
    # 税額
    total_tax = int(total_excluding_tax * TAX_RATE)
    # 税込金額
    total_amount = total_excluding_tax + total_tax
    # 商品点数（合計数量）
    total_items = sum(item.quantity for item in transaction_data.items)
    # 日本時間で登録
    transaction_time=datetime.now(JST)  

    # トランザクション（親）を作成
    transaction = Transaction(
        register_user_code=transaction_data.register_user_code or "9999999999", 
        store_code="30", 
        pos_id="90",  
        total_excluding_tax=total_excluding_tax,
        total_tax=total_tax,
        total_amount=total_amount,
        total_items=total_items,
        transaction_time=transaction_time
    )
    db.add(transaction)
    db.flush()  # transaction.id を確定させるため

    # 子アイテムを追加
    for item in transaction_data.items:
        # ✅ 商品マスタから prd_id, tax_cd を取得
        product = db.query(Product).filter(Product.jan_code == item.jan_code).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"JANコード {item.jan_code} の商品が見つかりません")
        
        db_item = TransactionItem(
            transaction_id=transaction.id,
            jan_code=item.jan_code,
            name=item.name,
            price=item.price,
            quantity=item.quantity,
            product_code=product.product_code, 
            tax_cd="10",
            product_id=product.id
        )
        db.add(db_item)

    db.commit()
    # ✅ items を含めて返す
    transaction_with_items = db.query(Transaction).options(joinedload(Transaction.items)).get(transaction.id)
    # ✅ 各明細アイテムの中身を確認するログ（ここに入れる！）
    for item in transaction_with_items.items:
        print("🧾 item:", vars(item))
    return transaction_with_items

# 全ての取引とその商品明細を一覧で取得
@router.get("/transactions", response_model=list[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).options(joinedload(Transaction.items)).all()
    return transactions