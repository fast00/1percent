################################################################연습봇#############################################################
# 테스트를 위한 연습봇입니다. 텔레그램에 '연습봇'을 검색해주세요./id = practice21bot'
import time
import telepot

token = "5141292184:AAENQEkjsmqVgRWUSS32e3K_LFWeRzbv3xI"
bot = telepot.Bot(token)
num = 0
def handle(msg):
    global num
    content_type, chat, user_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            print(user_id)
            bot.sendMessage(1886738532, text='안녕하세요. 오늘의 수익률을 알려드립니다.')
            bot.sendMessage(1886738532, text='오늘은 종목이 없습니다.')
while True:
    time.sleep(10)
    bot.sendMessage(1886738532, text='안녕하세요. 오늘의 수익률을 알려드립니다.')
