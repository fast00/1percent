from totallib import *
import telepot
import schedule
import time


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


def job1():
    Connect()
    todaydate = int(datetime.today().strftime("%Y%m%d"))
    file = FileMethods()
    file.save_Info_from_marketeye(todaydate)
    account = Account()
    strategy = Strategy()
    qospilist = strategy.ppostrategy("코스피200", todaydate)
    qosdaqlist = strategy.ppostrategy("코스닥150", todaydate)
    msg = account.buy(qosdaqlist, qospilist)
    stockdeposit = account.stockdeposit()
    deposit = account.deposit()
    if msg == 1:
        textbox(0, msg, deposit)
    else:
        textbox(1, msg, deposit)
    if len(stockdeposit[1]) != 0:
        for key, val in stockdeposit[1].items():
            if key in qospilist:
                upprice = account.qospi_sellPrice_Quotation(val[1])
                msg = account.reservation_sellorder(key, val[0], upprice)
                textbox(2, msg, deposit)
            else:
                upprice = account.qosdaq_sellPrice_Quotation(val[1])
                msg = account.reservation_sellorder(key, val[0], upprice)
                textbox(2, msg, deposit)
    return True


def job3():  # 전 주문 취소
    Connect()
    account = Account()
    account.reservation_cencelorder()
    msg = account.secondsell()
    deposit = account.deposit()
    textbox(3, msg, deposit)


def HedGe():  # 30초마다 실행
    Connect()
    deposit = 0
    account = Account()
    Hedge = account.hedge()
    if Hedge[0] == 4:
        textbox(4, Hedge[1], deposit)


def shut_down():
    todaystock = []
    deposit = 0
    textbox(5, todaystock, deposit)

refresh()
job1()
schedule.every().day.at("15:19:50").do(job1)
schedule.every().day.at("15:10").do(refresh)
schedule.every().day.at("11:30").do(job3)
schedule.every().day.at("22:00").do(shut_down)

while True:
    schedule.run_pending()
    nowtime = int(datetime.today().strftime("%H%M%S"))
    if nowtime <= 91050 or 113040 <= nowtime < 150954 or 151300 <= nowtime <= 151850:
        Connect()
        time.sleep(5)
    elif 91100 <= nowtime <= 112940:
        HedGe()
        time.sleep(3)
