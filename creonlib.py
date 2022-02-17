import time

import numpy as np
import win32com.client

KOSPI = 1
KOSDAQ = 2


def MakeRusultFromMain():
    Connect()
    marketinfo = MaketInfo()
    codelist = marketinfo.GetClearStockInfoByMarket(1)
    for code in codelist:
        print(code)
        result = []
        indicators = Indicators(code)
        PPO = indicators.MakePPO(5, 1000)
        if PPO == 1:
            continue
        method = PPOMethod()
        for rateofchange in range(-30, 30):
            method.Condition_Setting(PPO, rateofchange, 1)
            result += method.Get_result()
        print(result)
        if len(result) == 0:
            continue


def MARKETResult(MARKETCODE):
    # # 종합주가지수 : U001
    # # KP200 : U180
    # # 코스닥 종합 : U201
    # # KQ150 : U390
    indicators = Indicators(MARKETCODE)
    PPO = indicators.MakePPO(5, 1000)
    iter = np.arange(-10, 10, 0.5)
    method = PPOMethod()
    result = []
    for rateofchange in iter:
        rateofchange = round(rateofchange, 1)
        method.Condition_Setting_forMarket(PPO, rateofchange, 0)
        result += method.Get_result_forMarket()
    return result  # [이격도, 종가가 얼마나 등락해야하는지]


def MakeTotalResult(PPO, increasepercent):
    result = []
    for rateofchange in range(-30, 30):
        ppomethod = PPOMethod()
        ppomethod.Condition_Setting(PPO, rateofchange, increasepercent)
        middleresult = ppomethod.Get_result()
        if len(middleresult) != 0:  # 비어있는 middleresult가 [] 1개임
            result += middleresult
    return result  # [이격도, 종가가 얼마나 등락해야하는지]


def MARKETResultFromFile(PPO, increaserate):
    # # 종합주가지수 : U001
    # # KP200 : U180
    # # 코스닥 종합 : U201
    # # KQ150 : U390
    iter = np.arange(-10, 10, 0.5)
    method = PPOMethod()
    result = []
    for rateofchange in iter:
        rateofchange = round(rateofchange, 1)
        method.Condition_Setting_forMarket(PPO, rateofchange, increaserate)
        result += method.Get_result_forMarket()
    return result  # [이격도, 종가가 얼마나 등락해야하는지]


def Connect():
    objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
    b_connect = objCpCybos.IsConnect
    if b_connect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        exit()
    print('정상 연결')


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


def GetLimitTime():
    cptime = CpTimeChecker(1).checkRemainTime()
    if cptime[1] == 1 and cptime[0] != 0:
        while True:
            if CpTimeChecker(1).checkRemainTime()[0] == 0:
                time.sleep(0.5)
                break


class MaketInfo:
    def __init__(self):
        self.g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        self.objRq = win32com.client.Dispatch("CpSysDib.MarketEye")

    def GetMarketStartTime(self):
        """
         장 시작시간을 알려줍니다
         :param:
         :return: 시간
         """
        return self.g_objCodeMgr.GetMarketStartTime()

    def GetMarketEndTime(self):
        """
         장 마감시간을 알려줍니다
         :param:
         :return: 시간
         """
        return self.g_objCodeMgr.GetMarketEndTime()

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

    def GetStockInfoWithCodelist(self, codelist):
        """
         여러 코드별 재무를 한번에 가져와줌
        :param codelist : 코드 리스트
         :return: result
         """
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


class StockParticularInfo:
    def __init__(self, code):
        self.objStockOpenSb = win32com.client.Dispatch("Dscbo1.StockMst")
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.code = code
        self.todaydate = 0
        self.todaystartprice = 0
        self.todayhighprice = 0
        self.todaylowprice = 0
        self.todaycloseprice = 0
        self.volume = 0
        self.todaypercent = 0
        self.nextdayhighpercent = 0
        self.periodbasket = []

    def GetstockPeriodInfo(self, period):
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

    def GetPeriodBasket(self, period):
        basket = self.GetstockPeriodInfo(period)
        if basket == 1:
            return 1
        return self.periodbasket


class Indicators:
    def __init__(self, code):
        self.code = code
        self.basket = []  # ["날짜", "시가", "고가", "저가", "오늘종가", "거래량", "오늘증가율", "다음날고가증가율"]
        self.Madayrange = 0
        self.MA = {}  # {날짜 : MA , 오늘증감률, 다음날고가증감률}
        self.PPO = {}  # {날짜 : 이격도 , 오늘증감률, 다음날고가증감률}
        self.CCI = {}  # {날짜 : CCI}

    def MakeMA(self, MAdayrange, datevolume):
        MA = 0
        result = {}
        self.Madayrange = MAdayrange
        stockParticularInfo = StockParticularInfo(self.code)
        self.basket = stockParticularInfo.GetPeriodBasket(MAdayrange + datevolume - 1)  # 몇일선을 만들건지 + 몇일 가져올건지
        if self.basket == 1:
            return 1
        for i in range(len(self.basket)):
            if i >= MAdayrange - 1:
                for k in range(0, MAdayrange):
                    MA += self.basket[i - k][4]
                MA = MA / MAdayrange
                result[self.basket[i][0]] = [round(MA, 3), self.basket[i][6], self.basket[i][7]]
                MA = 0
        self.MA = result
        return result

    def MakePPO(self, MAdayrange, datevolume):
        MA = self.MakeMA(MAdayrange, datevolume)
        if MA == 1:
            return 1
        result = {}
        for i in range(len(self.basket)):
            for keys, val in self.MA.items():
                if self.basket[i][0] == keys:
                    PPO = self.basket[i][4] / val[0] * 100
                    result[self.basket[i][0]] = [round(PPO, 3), self.basket[i][6], self.basket[i][7]]
        self.PPO = result
        return result  # {날짜 : [이격도 , 오늘증감률, 고가증감률]}

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

    def MakeMAFromFile(self, MAdayrange, basket):
        MA = 0
        result = {}
        self.Madayrange = MAdayrange
        self.basket = basket
        for i in range(len(self.basket)):
            if i >= MAdayrange - 1:
                for k in range(0, MAdayrange):
                    MA += self.basket[i - k][4]
                MA = MA / MAdayrange
                result[self.basket[i][0]] = [round(MA, 3), self.basket[i][6], self.basket[i][7]]
                MA = 0
        self.MA = result
        return result

    def MakePPOFromFile(self, MAdayrange, basket):
        self.MakeMAFromFile(MAdayrange, basket)
        result = {}
        for i in range(len(self.basket)):
            for keys, val in self.MA.items():
                if self.basket[i][0] == keys:
                    PPO = self.basket[i][4] / val[0] * 100
                    result[self.basket[i][0]] = [round(PPO, 3), self.basket[i][6], self.basket[i][7]]
        self.PPO = result
        return result  # {날짜 : [이격도 , 오늘증감률, 고가증감률]}


class PPOMethod:
    def __init__(self):
        self.rateofchange = 0
        self.PPOrange = []
        self.PPOrangecount = {}
        self.PPOrangePaticularcount = {}
        self.PPOrangePercent = {}
        self.daylist = {}

    def SortList(self, dic):
        result = []
        for keys, val in dic.items():
            result.append(val[0])
        result.sort()
        return result

    def DicInitialize(self, PPO):
        self.PPOrange = self.SortList(PPO)  # [PPO만 리스트에 저장해서 정렬함]
        for i in range(round(self.PPOrange[-1] - self.PPOrange[0])):
            self.PPOrangecount[self.PPOrange[0] + i] = 0
            self.PPOrangePaticularcount[self.PPOrange[0] + i] = 0
            self.PPOrangePercent[self.PPOrange[0] + i] = 0
            self.daylist[self.PPOrange[0] + i] = []

    def DicInitialize_forMarket(self, PPO):
        self.PPOrange = self.SortList(PPO)  # [PPO만 리스트에 저장해서 정렬함]
        iter = np.arange(0, self.PPOrange[-1] - self.PPOrange[0], 0.1)
        for i in iter:
            i = round(i, 1)
            self.PPOrangecount[self.PPOrange[0] + i] = 0
            self.PPOrangePaticularcount[self.PPOrange[0] + i] = 0
            self.PPOrangePercent[self.PPOrange[0] + i] = 0
            self.daylist[self.PPOrange[0] + i] = []

    def Condition_Setting(self, PPO, rateofchange, increasepersent):
        self.rateofchange = rateofchange
        self.DicInitialize(PPO)
        for i in range(round(self.PPOrange[-1] - self.PPOrange[0])):
            for keys, val in PPO.items():
                if self.PPOrange[0] + i <= val[0] < self.PPOrange[0] + i + 1 and int(val[1]) == self.rateofchange:
                    self.PPOrangecount[self.PPOrange[0] + i] += 1
                    self.daylist[self.PPOrange[0] + i] += [keys]
                    if val[2] >= increasepersent:
                        self.PPOrangePaticularcount[self.PPOrange[0] + i] += 1
        for i in range(round(self.PPOrange[-1] - self.PPOrange[0])):  # 최종확률구하기
            try:
                self.PPOrangePercent[self.PPOrange[0] + i] = round(
                    self.PPOrangePaticularcount[self.PPOrange[0] + i] / self.PPOrangecount[self.PPOrange[0] + i] * 100,
                    2)
            except ZeroDivisionError:
                self.PPOrangePercent[self.PPOrange[0] + i] = 0
        return True

    def Get_result(self):
        result = []
        for i in range(round(self.PPOrange[-1] - self.PPOrange[0])):
            if self.PPOrangePaticularcount[self.PPOrange[0] + i] >= 5 and \
                    self.PPOrangePercent[self.PPOrange[0] + i] >= 85:
                # print(self.rateofchange,"\n",round(self.PPOrange[0] + i,2),self.PPOrangePercent[self.PPOrange[0] + i],"\n", self.daylist[self.PPOrange[0] + i])
                result.append(round(self.PPOrange[0] + i, 2))
                result.append(self.rateofchange)
        return result  # [이격도, 종가가 얼마나 등락해야하는지]

    def Condition_Setting_forMarket(self, PPO, rateofchange, increasepersent):
        self.rateofchange = rateofchange
        self.DicInitialize_forMarket(PPO)
        iter = np.arange(0, self.PPOrange[-1] - self.PPOrange[0], 0.1)
        for i in iter:
            i = round(i, 1)
            for keys, val in PPO.items():
                if self.PPOrange[0] + i <= val[0] < self.PPOrange[0] + i + 0.1 and str(self.rateofchange) <= format(
                        val[1], ".1f") < str(self.rateofchange + 0.5):
                    self.PPOrangecount[self.PPOrange[0] + i] += 1
                    self.daylist[self.PPOrange[0] + i] += [keys]
                    if val[2] <= increasepersent:
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
        iter = np.arange(0, self.PPOrange[-1] - self.PPOrange[0], 0.1)
        for i in iter:
            i = round(i, 1)
            if self.PPOrangePaticularcount[self.PPOrange[0] + i] >= 3 and \
                    self.PPOrangePercent[self.PPOrange[0] + i] >= 80:
                # print(self.rateofchange, "\n", round(self.PPOrange[0] + i, 2),
                #       self.PPOrangePercent[self.PPOrange[0] + i], "\n", len(self.daylist[self.PPOrange[0] + i]), '\n',
                #       self.daylist[self.PPOrange[0] + i])
                result.append(self.PPOrange[0] + i)
                result.append(self.rateofchange)
        return result


class CheckToday:
    def __init__(self):
        self.basket = []
        self.Madayrange = 0
        self.MA = {}
        self.PPO = {}

    def MakeMAFromFile(self, MAdayrange, basket):
        MA = 0
        result = {}
        self.Madayrange = MAdayrange
        self.basket = basket
        for i in range(len(self.basket)):
            if i >= MAdayrange - 1:
                for k in range(0, MAdayrange):
                    MA += self.basket[i - k][4]
                MA = MA / MAdayrange
                result[self.basket[i][0]] = [round(MA, 3), self.basket[i][6], self.basket[i][7]]  # {날짜 : MA , 고가증감률}
                MA = 0
        self.MA = result
        return result

    def MakePPOFromFile(self, MAdayrange, basket):
        self.MakeMAFromFile(MAdayrange, basket)
        result = {}
        for i in range(len(self.basket)):
            for keys, val in self.MA.items():
                if self.basket[i][0] == keys:
                    PPO = self.basket[i][4] / val[0] * 100
                    result[self.basket[i][0]] = [round(PPO, 3), self.basket[i][6], self.basket[i][7]]
        self.PPO = result
        return result  # {날짜 : [이격도 , 오늘증감률, 고가증감률]}

    def CheckTodayStockFromFile(self, middleresult, todayPPO):  # [이격도 , 오늘증감률, 내일고가증감률]
        for i in range(int(len(middleresult) / 2)):
            if middleresult[2 * i] <= todayPPO[0] < middleresult[2 * i] + 1 and int(todayPPO[1]) == middleresult[
                2 * i + 1]:
                return 1

        return 0

    def CheckTodayMarketFromFile(self, middleresult, todayPPO):  # [이격도 , 오늘증감률, 고가증감률]
        for i in range(int(len(middleresult) / 2)):
            if middleresult[2 * i] <= todayPPO[0] < middleresult[2 * i] + 0.1 and format(todayPPO[1], ".1f") == str(
                    middleresult[2 * i + 1]):
                return 1
        return 0


class CallFromFile:
    def DayList(self, filename, code):
        f = open(f"C:\\Users\\82104\\Desktop\\{filename}\\{code}.txt", 'r', encoding='utf-8')
        txt = f.read()
        result = self.ChangeDayList(txt)
        f.close()
        return result

    def ResultList(self, filename, code):
        f = open(f"C:\\Users\\82104\\Desktop\\{filename}\\{code}.txt", 'r', encoding='utf-8')
        txt = f.read()
        result = self.ChangeResultList(txt)
        f.close()
        return result

    def ChangeResultList(self, txt):
        txt = txt.replace('[', '').replace(']', '').replace(' ', '').replace('\r', '')
        list1 = txt.split(",")
        list2 = []
        result = []
        count = 0
        for i in list1:
            count += 1
            list2.append(float(i))
            if count == 2:
                result.append(list2)
                list2 = []
                count = 0
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
