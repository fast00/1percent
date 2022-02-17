from main2lib import *
from tqdm import tqdm

info = FileMethods().GetDaylist('코스피150')
indicators = Indicators()
checktoday = CheckToday()
totalresult = TotalResult()
totalpercent = {}
generalcount = 0
particularcount = 0
for MAdayrange in range(5, 30):
    percent = 0

    stockcodelist = info[0]  # 리스트
    marketbasket = info[1]  # 리스트
    stockbasket = info[2]  # 코드 : 바스켓
    marketremaindaylist = info[3]  # 리스트
    stockremaindaylist = info[4]  # 코드 : 바스켓
    overlapppo = {}
    for day in range(len(marketremaindaylist)):
        todaymarketbasket = []
        marketbasket = [marketbasket[i] for i in range(len(marketbasket)-1)]  #다음날것을 미리 반영해서 확률에 넣어버림 그래서 뺌
        kospiPPO = indicators.MakePPOFromFile(MAdayrange, marketbasket)
        marketoverlapppolist = totalresult.MARKETOverlapppoListFromFile(kospiPPO, -1)
        for keys, val in stockbasket.items():
            val = [val[i] for i in range(len(val) - 1)]
            if len(val) >= MAdayrange:
                stockPPO = indicators.MakePPOFromFile(MAdayrange, val)
                stockoverlapppolist = totalresult.StockOverlapppoListFromFile(stockPPO, 1)
                overlapppo[keys] = stockoverlapppolist

        marketbasket += [marketremaindaylist[day]]  # 하루 추가
        todaydate = marketremaindaylist[day][0]
        for keys, val in stockremaindaylist.items():
            for i in range(len(val)):
                if todaydate == val[i][0]:
                    stockbasket[keys] += [val[i]]

        for i in range(0, MAdayrange):  # 오늘 시장 PPO계산을 위한 5일
            todaymarketbasket.append(marketbasket[-MAdayrange + i])
        todaymarketppo = checktoday.MakePPOFromFile(MAdayrange, todaymarketbasket)[0]
        todayresult = checktoday.CheckTodayMarketFromFile(marketoverlapppolist, todaymarketppo)
        if todayresult == 1:
            print('안삼')
            continue

        for keys, val in stockbasket.items():
            if len(val) >= MAdayrange + 2:  # overlapppo 만들때 하루 지나고 만들어서 4일차엔 없었는데 5일차에 생길수 있음 그래서 + 1 근데 위에서 마지막날
                # 제외를 하므로 +2
                todaystockbasket = []
                for i in range(0, MAdayrange):
                    todaystockbasket.append(val[-MAdayrange + i])
                todayPPO = checktoday.MakePPOFromFile(MAdayrange, todaystockbasket)[0]
                todayresult = checktoday.CheckTodayStockFromFile(overlapppo[keys], todayPPO)
                if todayresult == 1:
                    print(keys,todaydate)
                    generalcount += 1
                    if todaystockbasket[-1][-1] >= 1:
                        print(todaystockbasket[-1][0])
                        print(keys)
                        particularcount += 1
        try:
            percent = round(particularcount / generalcount * 100,2)
        except ZeroDivisionError:
            pass
        print(day+1,'일\n','전체: ', generalcount, '성공: ', particularcount,'total :',percent)

    totalpercent[MAdayrange] = percent
    print(totalpercent)

from main2lib import *
from chectheme import CheckTheme
from tqdm import tqdm

Connect()
info = FileMethods().GetDaylist('코스피150')
indicators = Indicators()
checktoday = CheckToday()
totalresult = TotalResult()
totalpercent = {}

for MAdayrange in range(5, 30):
    print(MAdayrange,"일선")
    percent = 0
    stockcodelist = info[0]  # 리스트
    marketbasket = info[1]  # 리스트
    stockbasket = info[2]  # 코드 : 바스켓
    marketremaindaylist = info[3]  # 리스트
    stockremaindaylist = info[4]  # 코드 : 바스켓
    overlapppo = {}
    for day in range(len(marketremaindaylist)):
        generalcount = 0
        particularcount = 0
        todaymarketbasket = []
        marketbasket = [marketbasket[i] for i in range(len(marketbasket)-1)]  #다음날것을 미리 반영해서 확률에 넣어버림 그래서 뺌
        kospiPPO = indicators.MakePPOFromFile(MAdayrange, marketbasket)
        marketoverlapppolist = totalresult.MARKETOverlapppoListFromFile(kospiPPO, -1)
        for keys, val in stockbasket.items():
            val = [val[i] for i in range(len(val) - 1)]
            if len(val) >= MAdayrange:
                stockPPO = indicators.MakePPOFromFile(MAdayrange, val)
                stockoverlapppolist = totalresult.StockOverlapppoListFromFile(stockPPO, 1)
                overlapppo[keys] = stockoverlapppolist

        marketbasket += [marketremaindaylist[day]]  # 하루 추가
        todaydate = marketremaindaylist[day][0]
        todayrate = marketremaindaylist[day][6]
        for keys, val in stockremaindaylist.items():
            for i in range(len(val)):
                if todaydate == val[i][0]:
                    stockbasket[keys] += [val[i]]

        for i in range(0, MAdayrange):  # 오늘 시장 PPO계산을 위한 5일
            todaymarketbasket.append(marketbasket[-MAdayrange + i])
        todaymarketppo = checktoday.MakePPOFromFile(MAdayrange, todaymarketbasket)[0]
        todayresult = checktoday.CheckTodayMarketFromFile(marketoverlapppolist, todaymarketppo)
        if todayresult == 1:
            print('안삼')
            continue
        result = []
        result2 = []
        for keys, val in stockbasket.items():
            if len(val) >= MAdayrange + 2:  # overlapppo 만들때 하루 지나고 만들어서 4일차엔 없었는데 5일차에 생길수 있음 그래서 + 1 근데 위에서 마지막날
                # 제외를 하므로 +2
                todaystockbasket = []
                for i in range(0, MAdayrange):
                    todaystockbasket.append(val[-MAdayrange + i])
                todayPPO = checktoday.MakePPOFromFile(MAdayrange, todaystockbasket)[0]
                todayresult = checktoday.CheckTodayStockFromFile(overlapppo[keys], todayPPO)
                if todayresult == 1:
                    result += [keys]
                    generalcount += 1
                    if todaystockbasket[-2][-1] >= 1:
                        result2 += [keys]
                        particularcount += 1
        try:
            percent = round(particularcount / generalcount * 100, 2)
            if percent <= 50:
                print(todaydate,todayrate,"%",'\n','전체: ',generalcount,result,'성공: ',particularcount,result2)
                for i in result:
                    if i in result2:
                        continue
                    else:
                        pass
                count = 0
        except ZeroDivisionError:
            pass
        try:
            percent = round(particularcount / generalcount * 100,2)
        except ZeroDivisionError:
            pass
        print(day+1,'일')
    totalpercent[MAdayrange] = percent