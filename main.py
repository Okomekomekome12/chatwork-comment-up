import time
import chatwork

API_TOKEN = "ca8a3ef60488030d8e0f9485ec6db3e6"
time.sleep(300)
cw = chatwork.setup(426121900,API_TOKEN)
while True:
    cw.messagesend("a")
    time.sleep(0.7)