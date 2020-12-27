import os
import json

import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory

from helper import LineAPI, webhook_parser
from fsm import TocMachine


load_dotenv()
app = Flask(__name__, static_url_path='')
machines = {}


# Handle State Trigger
def handleTrigger(state, reply_token, user_id, text):
    print("Server Handling State : %s" % state)
    if state == "init":
        machines[user_id].start(reply_token, text)
    elif state == "functionList":
        if text=="1":
            machines[user_id].Function1(reply_token, text)
        elif text=="2":
            machines[user_id].Function2(reply_token, text)
        elif text=="3" :
            machines[user_id].Function3(reply_token, text)
        else :
            machines[user_id].is_going_to_Error(reply_token, text)
    elif state == "anime":
        if text=="戀愛" or text=="溫馨" or text=="奇幻冒險" or text=="科幻未來" or text=="幽默搞笑" :
            machines[user_id].search(reply_token, text)
        elif text=="靈異鬼怪" or text=="推理懸疑" or text=="料理美食" or text=="社會寫實" or text=="運動競技" :
            machines[user_id].search(reply_token, text)
        elif text=="歷史傳記" or text=="青春校園" or text=="其他" or text=="電影版" or text=="OVA":
            machines[user_id].search(reply_token, text)
        else :
            machines[user_id].is_going_to_Error(reply_token, text)     
    elif state=="animeRank" :
        if text=="所有動畫" or text=="戀愛" or text=="溫馨" or text=="奇幻冒險" or text=="科幻未來" or text=="幽默搞笑" :
            machines[user_id].searchRank(reply_token, text)
        elif text=="靈異鬼怪" or text=="推理懸疑" or text=="料理美食" or text=="社會寫實" or text=="運動競技" :
            machines[user_id].searchRank(reply_token, text)
        elif text=="歷史傳記" or text=="青春校園" or text=="其他" or text=="電影版" or text=="OVA":
            machines[user_id].searchRank(reply_token, text)
        else :
            machines[user_id].is_going_to_Error(reply_token, text)
    elif state =="kind" :
        if text =='0':
            machines[user_id].restart(reply_token, text) 
        elif text=="下一頁" or text=="上一頁": 
            machines[user_id].loop(reply_token, text)
        elif text=="1" :
            machines[user_id].goback(reply_token, text)
    elif state =="Rank" :
        if text =='0':
            machines[user_id].restart_r(reply_token, text) 
        elif text=="1" :
            machines[user_id].goback_r(reply_token, text)
    


@app.route('/', methods=['POST'])
def receive():
    webhook = json.loads(request.data.decode("utf-8"))
    reply_token, user_id, message = webhook_parser(webhook)
    print(reply_token, user_id, message)

    if user_id not in machines:
        machines[user_id] = TocMachine()

    handleTrigger(machines[user_id].state, reply_token, user_id, message)
    return jsonify({})

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host = '0.0.0.0', port = port)
