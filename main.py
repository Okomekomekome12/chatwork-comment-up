import os
import time
import threading
import chatwork
from flask import Flask, request, jsonify

app = Flask(__name__)

API_TOKEN    = "ca8a3ef60488030d8e0f9485ec6db3e6"
SECRET_TOKEN = "uBHVYDNYAqV3zv9PxNtGnnAzHUbPZfWrf13cJGjEAD8="


def continuous_send(room_id):
    cw = chatwork.setup(room_id, API_TOKEN)
    while True:
        try:
            cw.messagesend("a")
        except:
            time.sleep(60)
            continue
        # 部屋単位の制限は全体より厳しい（約100回/5分）
        time.sleep(3)


@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    sig = request.headers.get("X-ChatWorkWebhookSignature")
    if not chatwork.webhook_verify_signature(request.data, sig, SECRET_TOKEN):
        return "", 403

    room_id = chatwork.webhook_get_roomid(request.json)
    if not room_id:
        return "", 400

    threading.Thread(target=continuous_send, args=(str(room_id),), daemon=True).start()
    return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))