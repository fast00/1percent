import time

from totallib import *
import telepot
import schedule


# 40만원으로 시작!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def refresh():
    Connect()
    file = FileMethods()
    file.save_Info(501)  # 매일 실행
    return True


def textbox(numtype, msg, deposit):
    todaydate = str(datetime.today().strftime("%Y%m%d"))
    token = "5141292184:AAENQEkjsmqVgRWUSS32e3K_LFWeRzbv3xI"
    bot = telepot.Bot(token)
    deposit = str(deposit)
    if numtype == 0:
        bot.sendMessage(1886738532, text="오늘은 종목이 없습니다.")
        bot.sendMessage(1886738532, text="잔액: " + deposit)
    elif numtype == 1:
        bot.sendMessage(1886738532, text="----------------" + todaydate + "---------------")
        for i in msg:
            bot.sendMessage(1886738532, text=i)
        bot.sendMessage(1886738532, text="잔액: " + deposit)
    elif numtype == 2:
        bot.sendMessage(1886738532, text=msg)
    elif numtype == 3:
        for i in msg:
            bot.sendMessage(1886738532, text=i)
        bot.sendMessage(1886738532, text="잔액: " + deposit)
    elif numtype == 4:
        bot.sendMessage(1886738532, text="헷지 하였습니다.")
        bot.sendMessage(1886738532, text="-----------------------------")
        for i in msg:
            bot.sendMessage(1886738532, text=msg[i])
        bot.sendMessage(1886738532, text="-----------------------------")
    elif numtype == 5:
        bot.sendMessage(1886738532, text="프로그램을 종료해주세요.")


def Checktoday():
    Connect()
    todaydate = int(datetime.today().strftime("%Y%m%d"))
    file = FileMethods()
    file.save_Info_from_marketeye(todaydate)
    order = Account_and_Order()
    strategy = Strategy()
    qospilist = strategy.ppostrategy("코스피200", todaydate)
    qosdaqlist = strategy.ppostrategy("코스닥150", todaydate)
    msg = order.buy(qosdaqlist, qospilist)
    stockdeposit = order.stockdeposit()
    deposit = order.deposit()
    if msg == 1:
        textbox(0, msg, deposit)
    else:
        textbox(1, msg, deposit)
    if len(stockdeposit[1]) != 0:
        for key, val in stockdeposit[1].items():
            if key in qospilist:
                upprice = Cal_Price().qospi_sellPrice_Quotation(val[1])
                msg = order.reservation_sellorder(key, val[0], upprice)
                textbox(2, msg, deposit)
            else:
                upprice = Cal_Price().qosdaq_sellPrice_Quotation(val[1])
                msg = order.reservation_sellorder(key, val[0], upprice)
                textbox(2, msg, deposit)
    return True


def MarketpriceSell():  # 전 주문 취소
    Connect()
    order = Account_and_Order()
    order.reservation_cencelorder()
    msg = order.sellall()
    deposit = order.deposit()
    textbox(3, msg, deposit)


def HedGe():  # 30초마다 실행
    Connect()
    order = Account_and_Order()
    Hedge = order.hedge()
    GetLimitTime()
    if Hedge[0] == 4:
        deposit = order.deposit()
        textbox(4, Hedge[1], deposit)


def shut_down():
    todaystock = []
    deposit = 0
    textbox(5, todaystock, deposit)

ao = Account_and_Order()
ao.deposit()
schedule.every().day.at("15:19:50").do(Checktoday)
schedule.every().day.at("15:10").do(refresh)
schedule.every().day.at("11:30").do(MarketpriceSell)
schedule.every().day.at("22:00").do(shut_down)

while True:
    schedule.run_pending()
    nowtime = int(datetime.today().strftime("%H%M%S"))
    if nowtime <= 91050 or 113000 <= nowtime < 150952 or 151300 <= nowtime <= 151930:
        Connect()
        time.sleep(5)
    elif 91100 <= nowtime <= 112950:
        HedGe()
        time.sleep(3)
