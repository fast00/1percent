from pybithumb import Bithumb

# con_key = "d7805b704205efedbedabf6597a12f62"
# sec_key = "fb019a02a304b77e256940a7a8247213"
# bithumb = Bithumb(con_key, sec_key)
#
# print(bithumb.get_balance("BTC"))
#
# df = Bithumb.get_candlestick("BTC", chart_intervals="1m")
# df.tail(1500)
# basket = []
# for i in range(1,1500):
#     middlebasket = []
#     date = int(str(df.index[-i])[2:16].replace(" ","").replace(":","").replace("-",""))  #년월일시간분
#     middlebasket.append(date)
#     middlebasket += df.iloc[-i].tolist()
#     basket.append(middlebasket)
# basket.reverse()
# for i in range(len(basket)):
#     if 0 < i:
#         try:
#             todaypercent = round((basket[i][4] - basket[i - 1][4]) / basket[i - 1][4] * 100, 2)
#         except ZeroDivisionError:
#             todaypercent = 0
#         basket[i] = basket[i] + [todaypercent]
#         if i < len(basket) - 1:
#             try:
#                 nextdayhighpercent = round((basket[i + 1][2] - basket[i][4]) / basket[i][4] * 100, 2)
#             except ZeroDivisionError:
#                 nextdayhighpercent = 0
#             basket[i] = basket[i] + [nextdayhighpercent]
# del basket[0]
# f = open(f"C:\\주가정보\\비트코인\\2m.txt", 'w', encoding='utf-8')
# f.write(str(basket))
# f.close()
#
####################2분봉 따로 만들기
# df = Bithumb.get_candlestick("BTC", chart_intervals="1m")
# df.tail(1500)
# basket = []
# for i in range(1,1500):
#     middlebasket = []
#     date = int(str(df.index[-i])[2:16].replace(" ","").replace(":","").replace("-",""))  #년월일시간분
#     middlebasket.append(date)
#     middlebasket += df.iloc[-i].tolist()
#     basket.append(middlebasket)
# basket.reverse()
# token = 0
# newbasket = []
# for i in range(0,len(basket)):
#     token += 1
#     if token == 2:
#         if basket[i][3] >= basket[i-1][1]:
#             newbasket.append([basket[i-1][0], basket[i-1][1], basket[i][2], basket[i][3],
# for i in range(len(basket)):
#     if 0 < i:
#         try:
#             todaypercent = round((basket[i][4] - basket[i - 1][4]) / basket[i - 1][4] * 100, 2)
#         except ZeroDivisionError:
#             todaypercent = 0
#         basket[i] = basket[i] + [todaypercent]
#         if i < len(basket) - 1:
#             try:
#                 nextdayhighpercent = round((basket[i + 1][2] - basket[i][4]) / basket[i][4] * 100, 2)
#             except ZeroDivisionError:
#                 nextdayhighpercent = 0
#             basket[i] = basket[i] + [nextdayhighpercent]
# del basket[0]
# f = open(f"C:\\주가정보\\비트코인\\2m.txt", 'w', encoding='utf-8')
# f.write(str(basket))
# f.close()

from strategy import *

useppo = UsebitcoinPPO('비트코인')
useoscillator = UsebitcoinOSCILLATOR('비트코인')
kospibasket = useppo.codedaybasket["1m"]
count = 0
daypercentcount = 0
daypercentsum = 0
graphcount = 0
garo = []
sero = []
for day in range(len(kospibasket)):
    count += 1
    if day < 100:
        continue
    # beforemonth = day - 30  # 최초는 20일, 30일 86.5 %
    # yesterday = day - 1
    # stocklist = useppo.CheckStrogStock(beforemonth, yesterday, 2)
    stocklist = 0
    daypercent = useppo.MackoverlapPPO(day, 5, stocklist,200)
    useoscillator.PositiveOS_Day(day, stocklist)
    # useoscillator.NegativeOS_Day(day, stocklist)
    # if count % 3299 == 0: