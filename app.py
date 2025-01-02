from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

line_bot_api = LineBotApi(config=os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(config=os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "開門":
        open_door()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='門已開啟'))
    elif event.message.text == "顯示":
        display_message(event.message.text)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='文字已顯示'))
    elif event.message.text == "警報":
        trigger_alarm()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='警報已觸發'))

def open_door():
    # 實作開門邏輯
    pass

def display_message(message):
    # 實作顯示文字邏輯
    pass

def trigger_alarm():
    # 實作觸發警報邏輯
    pass

if __name__ == "__main__":
    app.run(port=5000)
