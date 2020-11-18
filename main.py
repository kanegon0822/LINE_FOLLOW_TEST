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
    profile=linebot_api.get_profile(event.source.user_id)
    if event.message.text=='登録':
        os.environ[profile.user_id]=profile.user_id
        linebot_api.reply_message(event.reply_token,TextSendMessage(text='USER_ID「'+os.environ[profile.user_id]+'」を登録します'))

    elif event.message.text=='削除':
        if os.environ.get(profile.user_id)==None:
            pass
        else:
            del os.environ[profile.user_id]
            linebot_api.reply_message(event.reply_token,TextSendMessage(text='USER_IDを削除しました'))
    
    elif event.message.text=='確認':
        linebot_api.reply_message(event.reply_token,TextSendMessage(text=os.environ.get(profile.user_id)))
    
    else:
        linebot_api.reply_message(event.reply_token,TextSendMessage(text=
            'USER_IDを登録する場合は「登録」を\n削除する場合は「削除」を\n入力してください。'
        ))

@handler.add(FollowEvent)
def handle_follow(event):
    linebot_api.reply_message(event.reply_token,TextSendMessage(text=
        '登録ありがとうございます！！\nUSER_IDを登録する場合は「登録」を\n削除する場合は「削除」を\n入力してください。'
    ))


if __name__=='__main__':
    app.run()

