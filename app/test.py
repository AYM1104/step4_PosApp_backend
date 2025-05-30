import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.jancodelookup.com/"
APP_ID = os.getenv("JAN_API_KEY")
KEYWORD = "4969929260338"  # ← ここを商品名などに変更

params = {
    "appId": APP_ID,
    "query": KEYWORD,
    "hits": 5,         # 件数を増やせる（例：5件まで）
    "page": 1,
    "type": "keyword"  # ✅ キーワード検索
}

res = requests.get(API_URL, params=params)
data = res.json()

if res.status_code == 200 and data.get("product"):
    print("✅ 全体情報:")
    info = data.get("info", {})
    print(f"・検索数: {info.get('count')}")
    print(f"・ページ番号: {info.get('page')}")
    print(f"・開始順位: {info.get('first')}")
    print(f"・終了順位: {info.get('last')}")
    print(f"・返却件数: {info.get('hits')}")
    print(f"・総ページ数: {info.get('pageCount')}\n")

    print("✅ 商品一覧:")
    for product in data["product"]:
        print("-----")
        print(f"商品名       : {product.get('itemName')}")
        print(f"JANコード    : {product.get('codeNumber')}")
        print(f"コード種別   : {product.get('codeType')}")
        print(f"品番（型番） : {product.get('itemModel')}")
        print(f"ブランド名   : {product.get('brandName')}")
        print(f"メーカー名   : {product.get('makerName')}")
        print(f"メーカー名カナ : {product.get('makerNameKana')}")
        print(f"商品ページURL : {product.get('itemUrl')}")
        print(f"画像URL       : {product.get('itemImageUrl')}")
        print(f"追加情報       : {product.get('ProductDetails')}")
        print("-----\n")

else:
    print("❌ 商品が見つかりませんでした")