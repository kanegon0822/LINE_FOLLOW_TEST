from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
import linebot
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
from linebot.models.events import FollowEvent
import os


app=Flask(__name__)


linebot_api=LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])

handler=WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route("/callback",methods=['POST'])
def callback():
    signature=request.headers["X-Line-Signature"]
    body=request.get_data(as_text=True)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    message=profile.user_id
    linebot_api.reply_message(event.reply_token,TextSendMessage(text=message))

@handler.add(FollowEvent)
def handle_follow(event):
    linebot_api.reply_message(event.reply_token,TextSendMessage(text=
        'はじめまして！登録ありがとうございます。このチャンネルでは毎朝天気予報をお知らせします。'
    ))
    profile=linebot_api.get_profile(event.source.user_id)


if __name__=='__main__':
    app.run()

