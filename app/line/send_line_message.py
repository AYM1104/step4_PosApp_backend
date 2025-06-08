# app/line/send_line_message.py

import os
import httpx

LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

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