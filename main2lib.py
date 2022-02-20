import time
import numpy as np
import win32com.client

KOSPI = 1
KOSDAQ = 2


# # 종합주가지수 : U001
# # KP200 : U180
# # 코스닥 종합 : U201
# # KQ150 : U390
class Account:
    def __init__(self, money):
        self.money = money
        self.stockcount = 0
        self.stockmoney = 0

    def buy(self, buyprice):
        if buyprice < self.money:
            for count in range(int(self.money / buyprice)):
                if 0 <= self.money - count * buyprice - (count * buyprice * 0.00015):
                    self.stockcount = count  # 가지고 있는 주식수
            if self.stockcount == 0:
                return 1
            self.stockmoney = self.stockcount * buyprice
            fees = self.stockmoney * 0.00015
            self.money = self.money - self.stockmoney - fees
        else:
            return 1
        return 0

    def sell(self, sellprice):
        fees = (sellprice * self.stockcount * 0.00015) + (sellprice * self.stockcount * 0.0023)
        self.stockmoney = sellprice * self.stockcount - fees
        self.money = self.stockmoney + self.money
        return True


def Connect():
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    b_connect = objCpCybos.IsConnect
    if b_connect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
    print('정상 연결')
    return True


def GetLimitTime():
    cptime = CpTimeChecker(1).checkRemainTime()
    if cptime[1] == 1 and cptime[0] != 0:
        while True:
            if CpTimeChecker(1).checkRemainTime()[0] == 0:
                time.sleep(0.5)
                break
    return True


class CpTimeChecker:
    def __init__(self, checkType):
        self.g_objCpStatus = win32com.client.Dispatch("CpUtil.CpCybos")
        self.chekcType = checkType  # 0: 주문 관련 1: 시세 요청 관련 2: 실시간 요청 관련

    def checkRemainTime(self):
        # 연속 요청 가능 여부 체크
        remainTime = self.g_objCpStatus.LimitRequestRemainTime
        remainCount = self.g_objCpStatus.GetLimitRemainCount(self.chekcType)  # 시세 제한
        if remainCount <= 0:
            while remainCount <= 0:
                # pythoncom.PumpWaitingMessages()
                time.sleep(remainTime / 1000)
                remainCount = self.g_objCpStatus.GetLimitRemainCount(1)  # 시세 제한
                remainTime = self.g_objCpStatus.LimitRequestRemainTime  #
                print(remainCount, remainTime)
            print("시간 지연 !!!!!!!!!!!!!")
        return remainTime, remainCount


class Codelist:
    def __init__(self):
        self.g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        self.objRq = win32com.client.Dispatch("CpSysDib.MarketEye")

    def GetStockListByMarket(self, cpe_market_kind):  # 거래소
        """
        코드 리스트를 가져옵니다
        NULL = 0,
        KOSPI = 1,
        KOSDAQ = 2,
        FREEBOARD = 3,
        KRX = 4,
        KONEX = 5,
        :param cpe_market_kind: 업종
        :return: 코드 리스트
        """
        generalcodelist = self.g_objCodeMgr.GetStockListByMarket(cpe_market_kind)
        particalcodelist = []
        for code in generalcodelist:
            if self.g_objCodeMgr.GetStockSectionKind(code) == 1 and self.g_objCodeMgr.GetStockSupervisionKind(
                    code) == 0 and self.g_objCodeMgr.GetStockStatusKind(code) == 0:
                particalcodelist.append(code)
        return particalcodelist

    def GetClearStockInfoByMarket(self, marketkind):
        """
         여러 코드별 재무를 한번에 가져와줌
        :param marketkind : 코드 리스트
         :return: result
         """
        codelist = []
        if marketkind == 'KOSPI':
            codelist = self.GetStockListByMarket(KOSPI)
        elif marketkind == 'KOSDAQ':
            codelist = self.GetStockListByMarket(KOSDAQ)
        elif marketkind == 'ALL':
            codelist = self.GetStockListByMarket(KOSPI) + self.GetStockListByMarket(KOSDAQ)
        codes = []
        result = []
        for i in codelist:
            codes.append(i)
            if len(codes) == 200 or (len(codelist) - codelist.index(i) < 200 and len(codelist) % 200 == len(codes)):
                rqField = [0, 109]  # 코드, 분기 유보율
                self.objRq.SetInputValue(0, rqField)  # 요청 필드
                self.objRq.SetInputValue(1, codes)  # 종목코드 or 종목코드 리스트
                self.objRq.BlockRequest()
                GetLimitTime()
                cnt = self.objRq.GetHeaderValue(2)  # 종목 개수
                for k in range(cnt):
                    code = self.objRq.GetDataValue(0, k)  # 코드
                    reserveratio = self.objRq.GetDataValue(1, k)  # 분기 유보율
                    if reserveratio > 0:
                        result.append(code)
                codes = []
        return result


class MarketInfo:
    def __init__(self, code):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.code = code

    def GetstockPeriodInfo(self, period):  # 3일치를 부르면, 오늘 제외하고 2일치가 옴.
        """
         일별 ["날짜", "시가", "고가", "저가", "오늘종가", "오늘증가율", "고가증가율"]
         :param code, period: 코드, 기간(일)
         :return: 기간 별 정보
         """
        self.objStockChart.SetInputValue(0, str(self.code))  # 종목 코드
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
        self.objStockChart.SetInputValue(4, period + 1)  # 최근 100일 치
        self.objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 날짜,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('D'))  # '차트 주가 - 일간 차트 요청
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()
        GetLimitTime()
        len1 = self.objStockChart.GetHeaderValue(3)
        condition = self.objStockChart.GetHeaderValue(17)
        if chr(condition) != '0':  # 정상이 아닌 종목
            return 1
        basket = []
        for i in range(len1):
            day = self.objStockChart.GetDataValue(0, i)
            open = self.objStockChart.GetDataValue(1, i)
            high = self.objStockChart.GetDataValue(2, i)
            low = self.objStockChart.GetDataValue(3, i)
            todayclose = self.objStockChart.GetDataValue(4, i)
            volume = self.objStockChart.GetDataValue(5, i)
            basket.append([day, open, high, low, todayclose, volume])  # "날짜", "시가", "고가", "저가", "오늘종가", "거래량"
        basket.reverse()
        for i in range(len(basket)):
            if 0 < i:
                try:
                    todaypercent = round((basket[i][4] - basket[i - 1][4]) / basket[i - 1][4] * 100, 2)
                except ZeroDivisionError:
                    todaypercent = 0
                basket[i] = basket[i] + [todaypercent]
                if i < len(basket) - 1:
                    try:
                        nextdayhighpercent = round((basket[i + 1][2] - basket[i][4]) / basket[i][4] * 100, 2)
                    except ZeroDivisionError:
                        nextdayhighpercent = 0
                    basket[i] = basket[i] + [nextdayhighpercent]
        del basket[0]
        self.todaydate = basket[-1][0]
        self.todaystartprice = basket[-1][1]
        self.todayhighprice = basket[-1][2]
        self.todaylowprice = basket[-1][3]
        self.todaycloseprice = basket[-1][4]
        self.volume = basket[-1][5]
        self.todaypercent = basket[-1][6]
        self.periodbasket = basket
        del basket[-1]  # 다음날고가증가율을 포함하기 때문에 마지막날은 없어야함
        return basket  # ["날짜", "시가", "고가", "저가", "오늘종가", "거래량", "오늘증가율", "다음날고가증가율"]

    def GetstockMinutePeriodInfo(self):  # 3일치를 부르면, 오늘 제외하고 2일치가 옴.
        """
         일별 ["날짜", "시가", "고가", "저가", "오늘종가", "오늘증가율", "고가증가율"]
         :param: code, period: 코드, 기간(일)
         :return: 기간 별 정보
         """
        self.objStockChart.SetInputValue(0, str(self.code))  # 종목 코드
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
        self.objStockChart.SetInputValue(4, 402)  # 최근 100일 치 1561
        self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 날짜,시간,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('m'))  # '차트 주기 - 분/틱
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()
        GetLimitTime()
        len1 = self.objStockChart.GetHeaderValue(3)
        basket = []
        for i in range(len1):
            day = self.objStockChart.GetDataValue(0, i)
            time = self.objStockChart.GetDataValue(1, i)
            open = self.objStockChart.GetDataValue(2, i)
            high = self.objStockChart.GetDataValue(3, i)
            low = self.objStockChart.GetDataValue(4, i)
            todayclose = self.objStockChart.GetDataValue(5, i)
            volume = self.objStockChart.GetDataValue(6, i)
            basket.append([day, time - 1, open, high, low, todayclose, volume])  # 날짜,시간,시가,고가,저가,종가,거래량
        basket.reverse()
        return basket  # [날짜,시간,시가,고가,저가,종가,거래량]


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
        return ocillator

    def MakeMAFromFile(self, MAdayrange, basket):
        MA = 0
        result = []
        self.Madayrange = MAdayrange
        self.basket = basket
        for i in range(len(self.basket)):
            if i >= MAdayrange - 1:
                for k in range(0, MAdayrange):
                    MA += self.basket[i - k][4]
                MA = MA / MAdayrange
                result.append(
                    [self.basket[i][0], round(MA, 3), self.basket[i][4], self.basket[i][6], self.basket[i][7]])
                MA = 0
        self.MA = result
        return result  # [날짜, 평균, 오늘종가, 오늘증감률, 다음날고가증감률]

    def MakePPOFromFile(self, MAdayrange, basket):
        self.MakeMAFromFile(MAdayrange, basket)
        result = []
        for i in range(len(self.MA)):
            PPO = self.MA[i][2] / self.MA[i][1] * 100
            result.append([self.MA[i][0], round(PPO, 3), self.MA[i][3], self.MA[i][4]])
        self.PPO = result
        return result  # {날짜 : [이격도 , 오늘증감률, 다음날고가증감률]}

    def MakeCCI(self, MAdayrange, basket):
        self.basket = basket
        Mlist = []
        for i in range(len(basket)):
            M = (self.basket[i][2] + self.basket[i][3] + self.basket[i][4]) / 3
            Mlist.append([self.basket[i][0], M])
        for i in range(len(Mlist)):
            m = 0
            d = 0
            if i >= MAdayrange - 1:
                for k in range(0, MAdayrange):
                    m += Mlist[i - k][1]
                m = m / MAdayrange
                for k in range(0, MAdayrange):
                    d += abs(Mlist[i - k][1] - m)
                d = d / MAdayrange
                self.CCI[Mlist[i][0]] = round((Mlist[i][1] - m) / (d * 0.015), 3)
        return self.CCI


class PPOMethod:
    def __init__(self):
        self.rateofchange = 0
        self.PPOrange = []
        self.PPOrangecount = {}
        self.PPOrangePaticularcount = {}
        self.PPOrangePercent = {}
        self.daylist = {}

    def SortList(self, PPO):
        result = []
        for i in range(len(PPO)):
            result.append(PPO[i][1])
        result = [min(result), max(result)]
        return result

    def DicInitialize(self, PPO):
        self.PPOrange = self.SortList(PPO)  # [PPO만 리스트에 저장해서 정렬함]
        for i in range(round(self.PPOrange[-1] + 1 - self.PPOrange[0])):
            self.PPOrangecount[self.PPOrange[0] + i] = 0
            self.PPOrangePaticularcount[self.PPOrange[0] + i] = 0
            self.PPOrangePercent[self.PPOrange[0] + i] = 0
            self.daylist[self.PPOrange[0] + i] = []

    def DicInitialize_forMarket(self, PPO):
        self.PPOrange = self.SortList(PPO)  # [PPO만 리스트에 저장해서 정렬함]
        iter = np.arange(0, self.PPOrange[-1] + 0.1 - self.PPOrange[0], 0.1)
        for i in iter:
            i = round(i, 1)
            self.PPOrangecount[self.PPOrange[0] + i] = 0
            self.PPOrangePaticularcount[self.PPOrange[0] + i] = 0
            self.PPOrangePercent[self.PPOrange[0] + i] = 0
            self.daylist[self.PPOrange[0] + i] = []
        return True

    def Condition_Setting(self, PPO, increaserate):
        self.DicInitialize(PPO)
        for i in range(round(self.PPOrange[-1] + 1 - self.PPOrange[0])):
            for k in range(len(PPO)):
                if self.PPOrange[0] + i <= PPO[k][1] < self.PPOrange[0] + i + 1:
                    self.PPOrangecount[self.PPOrange[0] + i] += 1
                    self.daylist[self.PPOrange[0] + i] += [PPO[k][0]]
                    if PPO[k][3] >= increaserate:
                        self.PPOrangePaticularcount[self.PPOrange[0] + i] += 1
        for i in range(round(self.PPOrange[-1] + 1 - self.PPOrange[0])):  # 최종확률구하기
            try:
                self.PPOrangePercent[self.PPOrange[0] + i] = round(
                    self.PPOrangePaticularcount[self.PPOrange[0] + i] / self.PPOrangecount[self.PPOrange[0] + i] * 100,
                    2)
            except ZeroDivisionError:
                self.PPOrangePercent[self.PPOrange[0] + i] = 0
        return self.PPOrangePercent

    def Get_result(self):
        result = []
        for i in range(round(self.PPOrange[-1] + 1 - self.PPOrange[0])):
            if 2 <= self.PPOrangePaticularcount[self.PPOrange[0] + i] <= 9 and \
                    self.PPOrangePercent[self.PPOrange[0] + i] >= 85:
                result.append(round(self.PPOrange[0] + i, 2))
                # print(self.rateofchange,"\n",round(self.PPOrange[0] + i,2),self.PPOrangePercent[self.PPOrange[0] + i],"\n", self.daylist[self.PPOrange[0] + i])
        return result  # [이격도, 종가가 얼마나 등락해야하는지]

    def Condition_Setting_forMarket(self, PPO, increaserate):
        self.DicInitialize_forMarket(PPO)
        iter = np.arange(0, self.PPOrange[-1] + 0.1 - self.PPOrange[0], 0.1)
        for i in iter:
            i = round(i, 1)
            for k in range(len(PPO)):
                if self.PPOrange[0] + i <= PPO[k][1] < self.PPOrange[0] + i + 0.1:
                    self.PPOrangecount[self.PPOrange[0] + i] += 1
                    self.daylist[self.PPOrange[0] + i] += [PPO[k][0]]
                    if PPO[k][3] <= increaserate:
                        self.PPOrangePaticularcount[self.PPOrange[0] + i] += 1
        for i in iter:
            i = round(i, 1)  # 최종확률구하기
            try:
                self.PPOrangePercent[self.PPOrange[0] + i] = round(
                    self.PPOrangePaticularcount[self.PPOrange[0] + i] / self.PPOrangecount[self.PPOrange[0] + i] * 100,
                    2)
            except ZeroDivisionError:
                self.PPOrangePercent[self.PPOrange[0] + i] = 0
        return self.PPOrangePercent

    def Get_result_forMarket(self):
        result = []
        iter = np.arange(0, self.PPOrange[-1] + 0.1 - self.PPOrange[0], 0.1)
        for i in iter:
            i = round(i, 1)
            if self.PPOrangePaticularcount[self.PPOrange[0] + i] >= 5 and self.PPOrangePercent[
                self.PPOrange[0] + i] >= 85:
                result.append(self.PPOrange[0] + i)
                # print(self.rateofchange, "\n", round(self.PPOrange[0] + i, 2),
                #       self.PPOrangePercent[self.PPOrange[0] + i], "\n", len(self.daylist[self.PPOrange[0] + i]), '\n',
                #       self.daylist[self.PPOrange[0] + i])
        return result


class CheckToday:
    def __init__(self):
        self.basket = []
        self.Madayrange = 0
        self.MA = {}
        self.PPO = {}

    def MakeMAFromFile(self, MAdayrange, basket):
        MA = 0
        result = []
        self.Madayrange = MAdayrange
        self.basket = basket
        for i in range(len(self.basket)):
            if i >= MAdayrange - 1:
                for k in range(0, MAdayrange):
                    MA += self.basket[i - k][4]
                MA = MA / MAdayrange
                result.append([self.basket[i][0], round(MA, 3), self.basket[i][4]])
                MA = 0
        self.MA = result
        return result  # [날짜, 평균, 오늘종가, 오늘증감률, 다음날고가증감률]

    def MakePPOFromFile(self, MAdayrange, basket):
        self.MakeMAFromFile(MAdayrange, basket)
        result = []
        for i in range(len(self.MA)):
            PPO = self.MA[i][2] / self.MA[i][1] * 100
            result.append([self.MA[i][0], round(PPO, 3)])
        self.PPO = result
        return result  # [날짜, 이격도 , 오늘증감률, 다음날고가증감률]

    def CheckTodayStockFromFile(self, middleresult, todayPPO):  # [날짜, 이격도 , 오늘증감률, 다음날고가증감률]
        for i in range(len(middleresult)):
            if middleresult[i] <= todayPPO[1] < middleresult[i] + 1:
                return 1
        return 0

    def CheckTodayMarketFromFile(self, middleresult, todayPPO):  # [이격도 , 오늘증감률, 고가증감률]
        for i in range(len(middleresult)):
            if middleresult[i] <= todayPPO[1] < middleresult[i] + 0.1:
                return 1
        return 0


class TotalResult:

    def MARKETOverlapppoListFromFile(self, PPO, increaserate):
        method = PPOMethod()
        result = []
        method.Condition_Setting_forMarket(PPO, increaserate)
        result += method.Get_result_forMarket()
        return result  # [이격도]

    def StockOverlapppoListFromFile(self, PPO, increaserate):
        result = []
        ppomethod = PPOMethod()
        ppomethod.Condition_Setting(PPO, increaserate)
        middleresult = ppomethod.Get_result()
        if len(middleresult) != 0:  # 비어있는 middleresult가 [] 1개임
            result += middleresult
        return result  # [이격도]


class FileMethods:

    def GetDaylist(self, filename):
        codelistinfile = self.GetStockList(filename)
        kospibasket1 = self.MarketDayList(filename)
        kospibasket2 = []
        basket2 = {}
        remaindaylist = {}
        kospiremaindaylist = []
        date = 0
        for i in range(0, len(kospibasket1)):
            if i < 720:
                kospibasket2.append(kospibasket1[i])
            elif i == 720:
                date = kospibasket1[i][0]
                kospiremaindaylist.append(kospibasket1[i])
            else:
                kospiremaindaylist.append(kospibasket1[i])
        for code in codelistinfile:
            basket1 = self.StockDayList(filename, code)
            remaindaylist[code] = []
            basket2[code] = []
            for i in range(0, len(basket1)):  # 720일까지만 하기 basket2를 이용
                if basket1[i][0] < date:
                    basket2[code] += [basket1[i]]
                elif basket1[i][0] >= date:
                    remaindaylist[code] += [basket1[i]]
        return codelistinfile, kospibasket2, basket2, kospiremaindaylist, remaindaylist

    def GetDaylist2(self, filename):
        codelistinfile = self.GetStockList(filename)
        kospibasket1 = self.MarketDayList(filename)
        kospibasket2 = []
        basket2 = {}
        for i in range(0, len(kospibasket1)):
            kospibasket2.append(kospibasket1[i])
        for code in codelistinfile:
            basket1 = self.StockDayList(filename, code)
            basket2[code] = []
            for i in range(0, len(basket1)):  # 720일까지만 하기 basket2를 이용
                basket2[code] += [basket1[i]]
        return codelistinfile, kospibasket2, basket2

    def StockDayList(self, filename, code):
        f = open(f"C:\\주가정보\\{filename}\\{code}.txt", 'r', encoding='utf-8')
        txt = f.read()
        result = self.ChangeDayList(txt)
        f.close()
        return result

    def MarketDayList(self, filename):
        f = open(f"C:\\주가정보\\{filename}\\{filename}.txt", 'r', encoding='utf-8')
        txt = f.read()
        result = self.ChangeDayList(txt)
        f.close()
        return result

    def ChangeDayList(self, txt):
        txt = txt.replace('[', '').replace(']', '').replace(' ', '').replace('\r', '')
        list1 = txt.split(",")
        list2 = []
        result = []
        count = 0
        for i in list1:
            count += 1
            list2.append(float(i))
            if count == 8:
                result.append(list2)
                list2 = []
                count = 0
        return result

    def GetStockList(self, filename):
        f = open(f"C:\\주가정보\\{filename}\\codelist.txt", 'r', encoding='utf-8')
        txt = f.read()
        txt = txt.replace('[', '').replace(']', '').replace(' ', '').replace('\r', '').replace('\'', '')
        result = txt.split(",")
        return result
