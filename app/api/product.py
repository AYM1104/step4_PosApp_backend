from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.dependencies.db import get_db  # ← 共通の依存関数をインポート

router = APIRouter()

# 商品を登録するエンドポイント
@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # JANコードの重複チェック
    if product.jan_code:
        existing = db.query(Product).filter(Product.jan_code == product.jan_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="同じJANコードの商品がすでに存在します。")
    
    try:
        db_product = Product(**product.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# 全商品の商品情報を取得するエンドポイント
@router.get("/products", response_model=List[ProductResponse])
def read_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

# JANコードで商品情報を取得するエンドポイント
@router.get("/products/by-jan-code", response_model=ProductResponse)
def get_product_by_jan_code(
    jan_code: str = Query(..., description="JANコード"),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.jan_code == jan_code).first()
    if not product:
        raise HTTPException(status_code=404, detail="該当する商品が見つかりません")
    return product




# # 特定の商品を"商品コード"or"JANコード"で取得するエンドポイント
# @router.get("/products/search", response_model=ProductResponse)
# def search_product(
#     code: str = Query(None),
#     jan_code: str = Query(None),
#     db: Session = Depends(get_db)
# ):
#     if not code and not jan_code:
#         raise HTTPException(status_code=400, detail="商品コードまたはJANコードのいずれかを指定してください。")

#     query = db.query(Product)

#     if code:
#         query = query.filter(Product.code == code)
#     if jan_code:
#         query = query.filter(Product.jan_code == jan_code)

#     product = query.first()

#     if not product:
#         raise HTTPException(status_code=404, detail="該当する商品が見つかりませんでした。")

#     return product