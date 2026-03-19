import os
import time
import threading
import chatwork
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 設定 ---
API_TOKEN = "d417c4819ad4b18a4a2c6bdbd84bb365"
# ChatworkのWebhook設定画面にある「署名」を入力してください。
# なければ None のままで検証をスキップするように調整します。
SECRET_TOKEN = None 

def continuous_send(room_id):
    # クラスをインスタンス化
    cw = chatwork.setup(room_id, API_TOKEN)
    print(f"Start loop for room: {room_id}")
    while True:
        try:
            cw.messagesend("a")
            # API制限(5分で300回)を考慮し、少し余裕を持たせるのが安全です
            time.sleep(1.2) 
        except Exception as e:
            print(f"Loop Error: {e}")
            break

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    # 署名検証
    signature = request.headers.get("X-ChatWorkWebhookSignature")
    # SECRET_TOKENがNoneの場合、chatwork.py側で検証をスルーする設計になっています
    if not chatwork.webhook_verify_signature(request.data, signature, SECRET_TOKEN):  # type: ignore
        return "invalid signature", 403

    data = request.json
    room_id = chatwork.webhook_get_roomid(data)
    
    if room_id:
        # 別スレッドで無限ループを開始
        thread = threading.Thread(target=continuous_send, args=(room_id,))
        thread.daemon = True
        thread.start()
        return jsonify({"status": "loop started"}), 200
    
    return jsonify({"status": "no room_id"}), 400

if __name__ == "__main__":
    # Railwayなどの環境では環境変数PORTが自動付与されます
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
