from main2lib import *

class UseOSCILLATOR:
    def __init__(self, market):
        self.file = FileMethods()
        self.indicators = Indicators()
        self.codelist = self.file.GetStockList(market)
        self.kospibasket = self.file.MarketDayList(market)
        self.codedaybasket = {}
        self.ocillatorlist = {}  # 날짜,다음날고가증감률, 오실레이터,오늘증감률
        self.checkplus = {}
        self.checkminus = {}
        self.fistminuscount = {}
        self.fistpluscount = {}
        self.minusOS_list = {}
        self.minusOS_average = {}
        self.positivepercent = 0
        self.positivecount = 0
        self.positivegeneralcount = 0
        self.positiveparticularcount = 0
        self.negativepercent = 0
        self.negativecount = 0
        self.negativegeneralcount = 0
        self.negativeparticularcount = 0
        self.MackMacdOscillator(market)

    def DicInitialization(self):
        for keys, val in self.codedaybasket.items():
            self.checkplus[keys] = 0
            self.checkminus[keys] = 0
            self.fistminuscount[keys] = 0
            self.fistpluscount[keys] = 0
            self.minusOS_list[keys] = []

    def MackminusOS_average(self):
        for key, val in self.minusOS_list.items():
            if len(val) == 0:
                continue
            self.minusOS_average[key] = round(sum(val) / len(val), 2)

    def MackCodeDayBasket(self, market):
        for code in self.codelist:
            self.codedaybasket[code] = []
            basket = self.file.StockDayList(market, code)
            for i in range(len(basket)):
                self.codedaybasket[code] += [basket[i]]

    def MackMacdOscillator(self, market):  # 꼭 따로 선언해서 만들어줘야함
        self.MackCodeDayBasket(market)
        self.DicInitialization()
        for keys, val in self.codedaybasket.items():
            if len(val) >= 26:
                MA12 = self.indicators.MakeEMA(10, "D", val)
                MA26 = self.indicators.MakeEMA(2, "D", val)
                ocillator = self.indicators.MakeMACDoscillator("D", MA12, MA26)
                self.ocillatorlist[keys] = ocillator

    # ex)
    # useoscillator = UseOSCILLATOR()
    # useoscillator.MackMacdOscillator()
    # kospibasket = useoscillator.kospibasket
    # for day in range(len(kospibasket)):
    #     useoscillator.PositiveOS_Day(day)
    #     useoscillator.NegativeOS_Day(day)

    def PositiveOS_Day(self, day, startday, codelist):  # 양, 음수 모두 코스피 바스켓 안에 넣어서 이용해야함
        todaydate = self.kospibasket[day][0]
        if day > 40 and todaydate > float(startday):  # 이정도 날짜부터 가중치가 거의 정확함
            for keys, val in self.ocillatorlist.items():
                for i in range(len(val) - 1):
                    if todaydate == val[i][0] and i > 40 and keys in codelist:
                        # try:
                        #     CCI = self.indicators.MakeCCI(20, val)
                        # except ZeroDivisionError:
                        #     print(keys,todaydate,"ZeroDivisionErrorZeroDivisionErrorZeroDivisionError")
                        #     continue  # 오류 수정해야함
                        if val[i][2] < 0:
                            self.fistminuscount[keys] += 1
                            self.checkplus[keys] = 0
                        elif val[i][2] >= 0 and self.fistminuscount[keys] > 1:
                            self.checkplus[keys] += 1  # 첫번째 양수 오실래이터가 나온 날
                            if self.checkplus[keys] == 1:  # 양수인 첫날 오실레이터 음수에서 양수로 가는 날임 몇배 할지 생각해보기
                                if val[i][3] - val[i][4] >= 0:  # 다음날이 양수이고 양봉일때 , 이때 이격도 기울기가 전날보다 음수면 패스할것
                                    self.positivegeneralcount += 1
                                    print("- to +",keys)
                                    if val[i][1] >= 1:
                                        print(keys,"----")
                                        self.positiveparticularcount += 1
                                if val[i][3] - val[i][4] >= 0 and val[i + 1][2] >= val[i][2] and val[i + 1][3] - \
                                        val[i + 1][
                                            4] > 0:  # 다음날이 양수이고 양봉일때 , 이때 이격도 기울기가 전날보다 음수면 패스할것
                                    self.positivegeneralcount += 1
                                    print("- to +", keys)
                                    if val[i + 1][1] >= 0.8:
                                        print(keys, "----")
                                        self.positiveparticularcount += 1
                                if val[i+1][3] - val[i+1][4] > 0 and val[i + 2][2] >= val[i+1][2] and val[i + 2][3] - \
                                        val[i + 2][
                                            4] > 0:  # 다음날이 양수이고 양봉일때 , 이때 이격도 기울기가 전날보다 음수면 패스할것
                                    self.positivegeneralcount += 1
                                    print("- to +", keys)
                                    if val[i + 2][1] >= 0.6:
                                        print(keys, "----")
                                        self.positiveparticularcount += 1
                            if self.checkplus[keys] > 1:  # 보충하기
                                if val[i - 1][2] > 0 and val[i][2] > 0 and val[i + 1][2] > 0 and (val[i][2] - val[i - 1][2]) / (i - (i - 1)) < 0 and (   # 수정해야함 기울기 안맞음
                                        val[i][2] - val[i + 1][2]) / (i - (i + 1)) > 0:
                                    self.positivegeneralcount += 1
                                    print(keys,(val[i][2] - val[i + 1][2]) / (i - (i + 1)), val[i + 1][1])
                                    if val[i + 1][1] >= 1:
                                        print(keys,"----",(val[i][2] - val[i + 1][2]) / (i - (i + 1)))
                                        self.positiveparticularcount += 1
                        break
            try:
                print("양수 전체: ", self.positivegeneralcount, " 증가: ", self.positiveparticularcount, " total: ",
                      round(self.positiveparticularcount / self.positivegeneralcount * 100, 2), "%")
            except ZeroDivisionError:
                pass
        return True

    def NegativeOS_Day(self, day, codelist):
        todaydate = self.kospibasket[day][0]
        if day > 40:  # 이정도 날짜부터 가중치가 거의 정확함, # 음수 오실레이터 정보 수집
            for keys, val in self.ocillatorlist.items():
                for i in range(len(val) - 1):
                    if todaydate == val[i][0] and i > 40:
                        if val[i][2] >= 0:
                            self.fistpluscount[keys] += 1
                            self.checkminus[keys] = 0
                        if val[i][2] < 0:
                            if self.fistpluscount[keys] >= 1:
                                self.checkminus[keys] += 1
                                if self.checkminus[keys] == 1:  # 음수가 나온 첫째날
                                    self.minusOS_list[keys].append(val[i][2])
                                elif val[i + 1][2] >= 0:  # 다음날이 양수인경우(마지막 음수날)
                                    self.minusOS_list[keys].append(val[i][2])
                        break
        if day > 400:
            self.MackminusOS_average()
            for keys, val in self.ocillatorlist.items():
                for i in range(len(val) - 2):
                    if todaydate == val[i][0] and keys in self.minusOS_average:
                        if (val[i][2] - val[i - 1][2]) / (i - (i - 1)) > 0 and val[i][3] - val[i][
                            4] > 0:  # 캔들 양봉인지 음봉인지 해볼것
                            if self.minusOS_average[keys] * 1 / 3 > val[i][2] >= self.minusOS_average[keys] * 1 / 2:
                                print(keys)
                                self.negativegeneralcount += 1
                                if val[i][1] >= 1:
                                    print("---",keys)
                                    self.negativeparticularcount += 1
            try:
                print("음수 전체: ", self.negativegeneralcount, " 증가: ", self.negativeparticularcount, " total: ",
                      round(self.negativeparticularcount / self.negativegeneralcount * 100, 2), "%")
            except ZeroDivisionError:
                pass
        return True

class UsePPO:
    def __init__(self, market):
        self.market = market
        self.file = FileMethods()
        self.indicators = Indicators()
        self.codelist = self.file.GetStockList(market)
        self.kospibasket = self.file.MarketDayList(market)
        self.checktoday = CheckToday()
        self.totalresult = TotalResult()
        self.codedaybasket = {}
        self.overlapppo = {}
        self.generalcount = 1
        self.particularcount = 1
        self.MackCodeDayBasket(market)

    def MackCodeDayBasket(self, market):
        for code in self.codelist:
            self.codedaybasket[code] = []
            basket = self.file.StockDayList(market, code)
            for i in range(len(basket)):
                self.codedaybasket[code] += [basket[i]]

    def CheckStrogStock(self, startdate, enddate, startpecent):
        generalcount = 0
        particularcount = 0
        fitcount = {}
        for keys, val in self.codedaybasket.items():
            fitcount[keys] = 0
        for keys, val in self.codedaybasket.items():
            for i in range(len(val)):
                if startdate < val[i][0] <= enddate:
                    generalcount += 1
                    if val[i][7] >= startpecent:
                        particularcount += 1
                        fitcount[keys] += 1
        sortlist = sorted(fitcount.items(), key=lambda x: x[1], reverse=True)
        stocklist = []
        for i in range(0, 10):
            stocklist.append(sortlist[i][0])
        return stocklist

    def MackoverlapPPO(self, day, MAdayrange, stocklist):  # 코스닥 500일기준 - 85.6 % , (코스피 600일 83.7 % 유동성이 낮음)
        percent = 0
        generalcount = 0
        particularcount = 0
        result = []
        if day > 500:  # 1년 데이터 축적
            todaydate = self.kospibasket[day][0]
            for keys, val in self.codedaybasket.items():
                todaystockbasket = []
                for j in range(len(val)):
                    if val[j][0] == todaydate and keys in stocklist:
                        newval = [val[i] for i in range(j)]  # 다음날것을 미리 반영해서 확률에 넣어버림 그래서 뺌
                        if len(newval) >= MAdayrange and len(newval) > 500:
                            if len(newval) % 500 != 0:
                                newval = [newval[-i] for i in range(1, 501)]
                                newval.reverse()  # 500일 데이터 기반으로 작동함. 500일씩 이동함
                            stockPPO = self.indicators.MakePPOFromFile(MAdayrange, newval)
                            stockoverlapppolist = self.totalresult.StockOverlapppoListFromFile(stockPPO, 1)
                            self.overlapppo[keys] = stockoverlapppolist
                            for i in range(0, MAdayrange):
                                todaystockbasket.append(val[j - MAdayrange + i + 1])
                            todayPPO = self.checktoday.MakePPOFromFile(MAdayrange, todaystockbasket)[0]
                            todayresult = self.checktoday.CheckTodayStockFromFile(self.overlapppo[keys], todayPPO)
                            if todayresult == 1:
                                result.append(keys)
                                print(keys)
                                generalcount += 1
                                self.generalcount += 1
                                if todaystockbasket[-1][-1] >= 1:
                                    print(keys, "--")
                                    particularcount += 1
                                    self.particularcount += 1
                        break
            try:
                percent = round(particularcount / generalcount * 100, 2)
                print(self.market, "전체: ", self.generalcount, " 증가: ", self.particularcount, " total: ",
                      round(self.particularcount / self.generalcount * 100, 2), "%")
            except ZeroDivisionError:
                pass
        return result

    # def MackoverlapPPO(self, day, MAdayrange, stocklist):  # MackCodeDayBasket() 꼭 먼저 실행해줘야함
    #     if day > 400:  # 1년 데이터 축적
    #         try:
    #             print("전체: ", self.generalcount, " 증가: ", self.particularcount, " total: ",
    #                   round(self.particularcount / self.generalcount * 100, 2), "%")
    #         except ZeroDivisionError:
    #             print("0%")
    #             pass
    #         todaydate = self.kospibasket[day][0]
    #         for keys, val in self.codedaybasket.items():
    #             todaystockbasket = []
    #             for j in range(len(val)):
    #                 if val[j][0] == todaydate and keys in stocklist:
    #                     try:
    #                         CCI = self.indicators.MakeCCI(20, val)
    #                     except ZeroDivisionError:
    #                         print(keys,todaydate,"ZeroDivisionErrorZeroDivisionErrorZeroDivisionError")
    #                         continue  # 오류 수정해야함
    #
    #                     newval = [val[i] for i in range(j)]  # 다음날것을 미리 반영해서 확률에 넣어버림 그래서 뺌
    #                     if len(newval) >= MAdayrange:
    #                         stockPPO = self.indicators.MakePPOFromFile(MAdayrange, newval)
    #                         stockoverlapppolist = self.totalresult.StockOverlapppoListFromFile(stockPPO, 1)
    #                         self.overlapppo[keys] = stockoverlapppolist
    #                         for i in range(0, MAdayrange):
    #                             todaystockbasket.append(val[j + 1 - MAdayrange + i])
    #                         todayPPO = self.checktoday.MakePPOFromFile(MAdayrange, todaystockbasket)[0]
    #                         todayresult = self.checktoday.CheckTodayStockFromFile(self.overlapppo[keys], todayPPO)
    #                         if todayresult == 1 and CCI[val[j - 1][0]] < CCI[val[j][0]]:
    #
    #                             print(todaydate)
    #                             print(keys)
    #                             self.generalcount += 1
    #                             if todaystockbasket[-1][-1] >= 1:
    #                                 print(keys,"--")
    #                                 self.particularcount += 1
    #                     break
    #     return True
