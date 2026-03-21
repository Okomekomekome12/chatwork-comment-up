import time
import chatwork


API_TOKEN = "ca8a3ef60488030d8e0f9485ec6db3e6"
SECOND_API_TOKEN = "6dcdee09b6d09eb2709ea7ffe17a953e"
print("初期化を開始します、、5分待てやゴラァ((")
time.sleep(300)
print("初期化完了☆")
cw = chatwork.setup(426121900,API_TOKEN)
cw2 = chatwork.setup(426121900,SECOND_API_TOKEN)

while True:
    cw2.messagesend("a")
    cw.messagesend("a")
    time.sleep(1.2)