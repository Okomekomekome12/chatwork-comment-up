import os
import time
import chatwork
from flask import Flask, request, jsonify
app = Flask(__name__)
API_TOKEN = "YOUR_API_TOKEN"
SECRET_TOKEN = None
@app.route("/", methods=["GET"])
def health():
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN):  # type: ignore
        return "invalid signature", 403
    data = request.json
    room_id    = chatwork.webhook_get_roomid(data) 
    body       = chatwork.webhook_get_message(data)
    account_id = chatwork.webhook_get_account_id(data) 
    message_id = chatwork.webhook_get_message_id(data)

    #ーーーーーーーーーーーーーーーーーーーーーーーーーーーメインコードーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー
    cw = chatwork.setup(room_id, API_TOKEN)
    def startcomment():
        cw.messagesend("a")
        time.sleep(0.7)
    while True:
        if body == "/start":
            cw.messagesend("botを開始します")
            startcomment()
        elif body == "/stop":
            cw.messagesend("botを停止します")
            break
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)