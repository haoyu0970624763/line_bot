import os

from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError


load_dotenv()

channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
FSM_GRAPH_URL = os.getenv("FSM_GRAPH_URL")

line_bot_api = LineBotApi(channel_access_token)

def webhook_parser(webhook):
    event = webhook["events"][0]
    reply_token = event["replyToken"]
    user_id = event["source"]["userId"]
    message = event["message"]["text"]

    return reply_token, user_id, message


class LineAPI:
    @staticmethod
    def send_reply_message(reply_token, reply_msg):
        try:
            line_bot_api.reply_message(reply_token, TextSendMessage(text=reply_msg))
        except LineBotApiError as e:
            print(e)

    def send_fsm_graph( self,reply_token):
        try:
            # for demo, hard coded image url, line api only support image over https
            line_bot_api.reply_message(reply_token, ImageSendMessage(original_content_url="https://12c907feb304.ngrok.io/show-fsm", preview_image_url='https://12c907feb304.ngrok.io/show-fsm'))
        except LineBotApiError as e:
            print(e)
