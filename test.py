from totallib import *

class Getbasket:
    def __init__(self, market,first,second):
        self.file = FileMethods()
        self.indicators = Indicators()
        self.codelist = self.file.GetStockList(market)
        self.marketbasket = self.file.MarketDayList(market)
        self.codedaybasket = {}
        self.positivegeneralcount = 0
        self.positiveparticularcount = 0
        self.ocillatorlist = {}  # 날짜,다음날고가증감률, 오실레이터,오늘증감률
        self.checkplus = {}
        self.fistminuscount = {}
        self.MackCodeDayBasket(market)
        self.MackMacdOscillator(market, first, second)

    def DicInitialization(self):
        for keys, val in self.codedaybasket.items():
            self.checkplus[keys] = 0
            self.fistminuscount[keys] = 0
        return True

    def MackMacdOscillator(self, market, first, second):  # 꼭 따로 선언해서 만들어줘야함
        self.MackCodeDayBasket(market)
        self.DicInitialization()
        for keys, val in self.codedaybasket.items():
            if len(val) >= 26:
                MA12 = self.indicators.MakeEMA(first, "D", val)
                MA26 = self.indicators.MakeEMA(second, "D", val)
                ocillator = self.indicators.MakeMACDoscillator("D", MA12, MA26)
                self.ocillatorlist[keys] = ocillator
        return True


    def MackCodeDayBasket(self, market):
        for code in self.codelist:
            self.codedaybasket[code] = []
            basket = self.file.StockDayList(market, code)
            for i in range(len(basket)):
                self.codedaybasket[code] += [basket[i]]
        return True

    def CheckStrogStock(self, startdate, enddate, startpecent):
        fitcount = {}
        for keys, val in self.codedaybasket.items():
            fitcount[keys] = 0
        for keys, val in self.codedaybasket.items():
            for i in range(len(val)):
                if startdate < val[i][0] <= enddate and val[i][7] >= startpecent:
                    fitcount[keys] += 1
        sortlist = sorted(fitcount.items(), key=lambda x: x[1], reverse=True)
        stocklist = []
        for i in range(0, 11):
            stocklist.append(sortlist[i][0])
        return stocklist

    def PositiveOS_Day(self, day, codelist):  # 양, 음수 모두 코스피 바스켓 안에 넣어서 이용해야함
        todaydate = self.marketbasket[day][0]
        if day > 40:  # 이정도 날짜부터 가중치가 거의 정확함
            for keys, val in self.ocillatorlist.items():
                for i in range(len(val) - 1):
                    if todaydate == val[i][0] and i > 40 and keys in codelist:
                        if val[i][2] < 0:
                            self.fistminuscount[keys] += 1
                            self.checkplus[keys] = 0
                        elif val[i][2] >= 0 and self.fistminuscount[keys] > 1:
                            self.checkplus[keys] += 1  # 첫번째 양수 오실래이터가 나온 날
                            if self.checkplus[keys] == 1:  # 양수인 첫날 오실레이터 음수에서 양수로 가는 날임 몇배 할지 생각해보기
                                if val[i][3] - val[i][4] >= 0:  # 다음날이 양수이고 양봉일때 , 이때 이격도 기울기가 전날보다 음수면 패스할것
                                    self.positivegeneralcount += 1
                                    print("- to +", keys)
                                    if val[i][1] >= 1:
                                        print(keys, "----")
                                        self.positiveparticularcount += 1
                            #     if val[i][3] - val[i][4] >= 0 and val[i + 1][2] >= val[i][2] and val[i + 1][3] - \
                            #             val[i + 1][
                            #                 4] > 0:  # 다음날이 양수이고 양봉일때 , 이때 이격도 기울기가 전날보다 음수면 패스할것
                            #         self.positivegeneralcount += 1
                            #         print("- to +", keys)
                            #         if val[i + 1][1] >= 0.8:
                            #             print(keys, "----")
                            #             self.positiveparticularcount += 1
                            #     if val[i + 1][3] - val[i + 1][4] > 0 and val[i + 2][2] >= val[i + 1][2] and val[i + 2][3] - \
                            #             val[i + 2][
                            #                 4] > 0:  # 다음날이 양수이고 양봉일때 , 이때 이격도 기울기가 전날보다 음수면 패스할것
                            #         self.positivegeneralcount += 1
                            #         print("- to +", keys)
                            #         if val[i + 2][1] >= 0.6:
                            #             print(keys, "----")
                            #             self.positiveparticularcount += 1
                            # if self.checkplus[keys] > 1:  # 보충하기
                            #     if val[i - 1][2] > 0 and val[i][2] > 0 and val[i + 1][2] > 0 and (
                            #             val[i][2] - val[i - 1][2]) / (i - (i - 1)) < 0 and (  # 수정해야함 기울기 안맞음
                            #             val[i][2] - val[i + 1][2]) / (i - (i + 1)) > 0:
                            #         self.positivegeneralcount += 1
                            #         print(keys, (val[i][2] - val[i + 1][2]) / (i - (i + 1)), val[i + 1][1])
                            #         if val[i + 1][1] >= 1:
                            #             print(keys, "----", (val[i][2] - val[i + 1][2]) / (i - (i + 1)))
                            #             self.positiveparticularcount += 1
                        break
            try:
                return round(self.positiveparticularcount / self.positivegeneralcount * 100, 2)
                print("양수 전체: ", self.positivegeneralcount, " 증가: ", self.positiveparticularcount, " total: ",
                      round(self.positiveparticularcount / self.positivegeneralcount * 100, 2), "%")
            except ZeroDivisionError:
                pass
        return 0

class Indicators:
    def __init__(self):
        self.MA = []
        self.EMA = []
        self.Madayrange = 0
        self.EMAbasket = []
        self.basket = []
        self.CCI = {}

    def MakeEMA(self, MAdayrange, type, basket):
        self.Madayrange = MAdayrange
        self.basket = basket
        MA1 = 0
        EMA1 = 0
        k = 2 / (MAdayrange + 1)
        result = []
        if type == "M":
            for i in range(len(self.basket)):
                if i == MAdayrange - 1:
                    for j in range(0, MAdayrange):
                        MA1 += self.basket[i - j][5]
                    MA1 = MA1 / MAdayrange

                if i == MAdayrange:
                    EMA1 = ((self.basket[i][5] - MA1) * k) + MA1

                if i > MAdayrange:
                    EMA1 = ((self.basket[i][5] - EMA1) * k) + EMA1
                    result.append([self.basket[i][0], self.basket[i][1], EMA1, self.basket[i][5]])
                    # [날짜,시간, 평균,종가]
        if type == "D":
            for i in range(len(self.basket)):
                if i == MAdayrange - 1:
                    for j in range(0, MAdayrange):
                        MA1 += self.basket[i - j][4]
                    MA1 = MA1 / MAdayrange

                if i == MAdayrange:
                    EMA1 = ((self.basket[i][4] - MA1) * k) + MA1

                if i > MAdayrange:
                    EMA1 = ((self.basket[i][4] - EMA1) * k) + EMA1
                    result.append([self.basket[i][0], self.basket[i][7], EMA1, self.basket[i][4], self.basket[i][1]])
                    # [날짜,다음날고가증감률, 평균,종가,오늘시가]
        self.EMA = result
        return result

    def MakeEMAsignal(self, EMAdayrange, EMAbasket):
        MA1 = 0
        EMA1 = 0
        k = 2 / (EMAdayrange + 1)
        result = []
        for i in range(len(EMAbasket)):
            if i == EMAdayrange - 1:
                for j in range(0, EMAdayrange):
                    MA1 += EMAbasket[i - j][2]
                MA1 = MA1 / EMAdayrange

            if i == EMAdayrange:
                EMA1 = ((EMAbasket[i][2] - MA1) * k) + MA1

            if i > EMAdayrange:
                EMA1 = ((EMAbasket[i][2] - EMA1) * k) + EMA1
                result.append([EMAbasket[i][0], EMAbasket[i][1], EMA1, EMAbasket[i][3]])
        return result  # m [날짜,시간, EMA, 종가], d [날짜,다음날고가증감률, EMA,오늘증감률]

    def MakeMACDoscillator(self, type, MA1, MA2):
        MACDbasket = []
        MACDoscillator = []
        comparerange = []
        if type == "M":
            for i in range(len(MA1)):
                for k in range(len(MA2)):
                    if MA1[i][0] == MA2[k][0] and MA1[i][1] == MA2[k][1]:
                        MACDbasket.append([MA1[i][0], MA1[i][1], MA1[i][2] - MA2[k][2], MA1[i][3]])
                        break
            signalbasket = self.MakeEMAsignal(9, MACDbasket)
            for i in range(len(MACDbasket)):
                for k in range(len(signalbasket)):
                    if MACDbasket[i][0] == signalbasket[k][0] and MACDbasket[i][1] == signalbasket[k][1]:
                        MACDoscillator.append(
                            [MACDbasket[i][0], MACDbasket[i][1], float(round(MACDbasket[i][2] - signalbasket[k][2], 2)),
                             MACDbasket[i][3]])
                        # 날짜, 시간, 오실레이터, 종가 | 날짜,다음날고가증감률, 오실레이터,오늘증감률
                        comparerange.append(int(MACDbasket[i][2] - signalbasket[k][2]))
                        break
        if type == "D":
            for i in range(len(MA1)):
                for k in range(len(MA2)):
                    if MA1[i][0] == MA2[k][0]:
                        MACDbasket.append([MA1[i][0], MA1[i][1], MA1[i][2] - MA2[k][2], MA1[i][3], MA1[i][4]])
                        break
            signalbasket = self.MakeEMAsignal(9, MACDbasket)
            for i in range(len(MACDbasket)):
                for k in range(len(signalbasket)):
                    if MACDbasket[i][0] == signalbasket[k][0]:
                        MACDoscillator.append(
                            [MACDbasket[i][0], MACDbasket[i][1], float(round(MACDbasket[i][2] - signalbasket[k][2], 2)),
                             MACDbasket[i][3], MACDbasket[i][4]])
                        # 날짜, 시간, 오실레이터, 종가 | 날짜,다음날고가증감률, 오실레이터,종가,시가
                        comparerange.append(int(MACDbasket[i][2] - signalbasket[k][2]))
                        break
        ocillator = MACDoscillator
        return ocillator  # 날짜, 다음날고가증감률, 오실레이터, 종가, 시가

#first 11 이상 second 10 다음 하기
# qospi = Getbasket("코스피200")
result = []
for first in range(6,24):
    for second in range(5,24):
        print(first,second,"--------------------------")
        qosdaq = Getbasket("코스피200",first,second)
        marketbasket = qosdaq.marketbasket
        for day in range(len(marketbasket)):
            todatdate = marketbasket[day][0]
            print(todatdate, day)
            if day > 40:
                beforemonth = marketbasket[day - 30][0]
                yesterday = marketbasket[day - 1][0]
                # stocklist = qospi.CheckStrogStock(beforemonth, yesterday, 2)
                # qospi.PositiveOS_Day(day, stocklist)
                stocklist = qosdaq.CheckStrogStock(beforemonth, yesterday, 2)
                qosdaq.PositiveOS_Day(day, stocklist)
                if day == 501:
                    try:
                        re = round(qosdaq.positiveparticularcount / qosdaq.positivegeneralcount * 100, 2)
                        result.append([f"{first} - {second}", qosdaq.positivegeneralcount, re])
                    except:
                        result.append(0)
        print(result)

# qosdaq = Getbasket("코스닥150",10,7)
# qospi = Getbasket("코스피200",11,20)
# marketbasket = qospi.marketbasket
# for day in range(len(marketbasket)):
#     todatdate = marketbasket[day][0]
#     print(todatdate, day)
#     if day > 40:
#         beforemonth = marketbasket[day - 30][0]
#         yesterday = marketbasket[day - 1][0]
#         stocklist = qospi.CheckStrogStock(beforemonth, yesterday, 5)
#         qospi.PositiveOS_Day(day, stocklist)
        # stocklist = qosdaq.CheckStrogStock(beforemonth, yesterday, 5)
        # qosdaq.PositiveOS_Day(day, stocklist)