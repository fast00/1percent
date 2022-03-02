from totallib import *
import telepot
import schedule
import time


# 30만원으로 시작!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def test():
    Connect()
    file = FileMethods()
    file.save_Info(501)
    strategy = Strategy()
    qospilist = strategy.ppostrategy("코스피200")
    qosdaqlist = strategy.ppostrategy("코스닥150")
    print(qospilist, qosdaqlist)


def textbox(numtype, codelist, deposit):
    token = "5141292184:AAENQEkjsmqVgRWUSS32e3K_LFWeRzbv3xI"
    bot = telepot.Bot(token)
    codelist = str(codelist).replace("[", "").replace("]", "")
    deposit = str(deposit)
    todaydate = str(datetime.today().strftime("%Y%m%d"))
    if numtype == 0:
        bot.sendMessage(1886738532, text="-------------"+todaydate+"--------------")
        bot.sendMessage(1886738532, text="오늘은 종목이 없습니다.")
        bot.sendMessage(1886738532, text="잔액: " + deposit)
    elif numtype == 1:
        bot.sendMessage(1886738532, text="-------------" + todaydate + "--------------")
        bot.sendMessage(1886738532, text=codelist + "종목을 매수하였습니다.")
        bot.sendMessage(1886738532, text="잔액: " + deposit)
    elif numtype == 2:
        bot.sendMessage(1886738532, text=codelist + "종목매도주문을 넣었습니다.")
    elif numtype == 3:
        bot.sendMessage(1886738532, text=codelist + "종목을 매도하였습니다.")
        bot.sendMessage(1886738532, text="잔액: " + deposit)
    elif numtype == 4:
        bot.sendMessage(1886738532, text=codelist + "프로그램을 종료해주세요.")


def job1():
    Connect()
    file = FileMethods()
    file.save_Info(501)
    account = Account()
    strategy = Strategy()
    qospilist = strategy.ppostrategy("코스피200")
    qosdaqlist = strategy.ppostrategy("코스닥150")
    todaystock = account.buy(qosdaqlist, qospilist)
    deposit = account.deposit()
    if todaystock == 0:
        textbox(0, todaystock, deposit)
    else:
        textbox(1, todaystock, deposit)
    return True


def job2():
    Connect()
    account = Account()
    todaystock = account.firstsell()  # 9:00시에 매도주문 걸어놓기
    deposit = account.deposit()
    textbox(2, todaystock, deposit)
    return True


def job3():
    Connect()
    account = Account()
    account.cancelorder()  # 전 주문 취소
    todaystock = account.secondsell()
    deposit = account.deposit()
    textbox(3, todaystock, deposit)
    return True


def job4():
    todaystock = []
    deposit = 0
    textbox(4, todaystock, deposit)
    return True

test()
# schedule.every().day.at("15:13").do(job1)
# schedule.every().day.at("09:00").do(job2)
# schedule.every().day.at("11:30").do(job3)
# schedule.every().day.at("22:00").do(job4)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

