import os
import requests
from dotenv import load_dotenv

# envファイルの読み込み
load_dotenv()

# 検索に必要な情報を取得
RAKUTEN_APP_ID = os.getenv("RAKUTEN_APP_ID")
RAKUTEN_API_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"
JAN_CODE = "4901777431508"

# URLに追加するパラメーター
params = {
    "applicationId": RAKUTEN_APP_ID,
    "keyword": JAN_CODE,
    "format": "json"
}

res = requests.get(RAKUTEN_API_URL, params=params)
data = res.json()

if res.status_code == 200 and data.get("Items"):
    item = data["Items"][0]["Item"]
    print(f"商品名: {item['itemName']}")
    print(f"ジャンルID: {item['genreId']}")
    print(f"商品URL: {item['itemUrl']}")
    print(f"画像URL: {item['mediumImageUrls'][0]}")
else:
    print("商品が見つかりませんでした")
    print(res.url)         # 実際に送信されたURLを確認
    print(res.status_code) # ステータスコード
    print(data)       



RAKUTEN_GENRE_API_URL = "https://app.rakuten.co.jp/services/api/IchibaGenre/Search/20140222"

# 商品検索APIで取得したジャンルIDを使う
genre_id = item["genreId"]

genre_params = {
    "applicationId": RAKUTEN_APP_ID,
    "genreId": genre_id,
    "format": "json"
}

genre_res = requests.get(RAKUTEN_GENRE_API_URL, params=genre_params)
genre_data = genre_res.json()

if genre_res.status_code == 200 and "parents" in genre_data:
    # 階層を取得して " > " で連結
    hierarchy = " > ".join([p["parent"]["genreName"] for p in genre_data["parents"]])
    current = genre_data["current"]["genreName"]
    print(f"ジャンル階層: {hierarchy} > {current}")
else:
    print("ジャンル情報が取得できませんでした")
    print(genre_res.status_code)
    print(genre_data)