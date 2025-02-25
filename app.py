from flask import Flask, request, abort, render_template, redirect

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from liffpy import (
    LineFrontendFramework as LIFF,
    ErrorResponse
)

#======這裡是呼叫的檔案內容=====
from message import *
from new import *
from Function import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import  os
import time
#======python的函數庫==========


app = Flask(__name__,template_folder='templates')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

liff_api = LIFF('mjKgiMMUswlG883lNPxJOGpi3gNVRJ8khLOGkgC8NzXZrUI9OoAglY14rNOe1C+uBKMpS6n1NPKoXfjDjSp2CKSxTDC7N/iaTdGxKRuXW2v8ZQzcfL99S+uyltX1WzddbQQR0S87YkfPOYk+1BGv0QdB04t89/1O/w1cDnyilFU=')
line_bot_api = LineBotApi('mjKgiMMUswlG883lNPxJOGpi3gNVRJ8khLOGkgC8NzXZrUI9OoAglY14rNOe1C+uBKMpS6n1NPKoXfjDjSp2CKSxTDC7N/iaTdGxKRuXW2v8ZQzcfL99S+uyltX1WzddbQQR0S87YkfPOYk+1BGv0QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('843fa1bfa2bfea8a7b34d25900c77b59')

# try:
#     now_LIFF_APP_number = len(liff_api.get())
# except:
#     now_LIFF_APP_number = 0

target_LIFF_APP_number = 10
# print(target_LIFF_APP_number,now_LIFF_APP_number)
# if now_LIFF_APP_number < target_LIFF_APP_number:
#     for i in range(target_LIFF_APP_number - now_LIFF_APP_number):
#         liff_api.add(view_type="full",view_url="https://www.google.com")

@app.route("/")
def index():
    return redirect("https://toiletclient-553f078e32d3.herokuapp.com")

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)

    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    if event.postback.data == 'Maso的鑄鐵坊':
        message = TextSendMessage(text="Maso的鑄鐵坊，目前施工中...")
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
