# app/line/send_line_message.py

import os
import httpx

LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# ✅ 画像を返信する（既存の処理）
async def reply_image_message(reply_token: str, image_url: str):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    body = {
        "replyToken": reply_token,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": image_url,
                "previewImageUrl": image_url,
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        await client.post(LINE_REPLY_ENDPOINT, headers=headers, json=body)

# ✅ UID宛にテキストをプッシュ送信する（新規追加）
async def push_text_message(to: str, text: str):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    body = {
        "to": to,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(LINE_PUSH_ENDPOINT, headers=headers, json=body)
        if response.status_code != 200:
            raise Exception(f"❌ LINE push error: {response.text}")