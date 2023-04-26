from fastapi import FastAPI, Request
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv; load_dotenv()
import uvicorn
import os

CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET') or 'CHANNEL_SECRET'
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN') or 'CHANNEL_ACCESS_TOKEN'

app = FastAPI()

line_bot_api = LineBotApi(channel_access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=CHANNEL_SECRET)

logger = logging.getLogger(__name__)

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    
    body = await request.body()
    logger.info("Request body:" + body.decode())
    
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        logger.warning("Invalid signature")
        return "Invalid signature"
    
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level='info')