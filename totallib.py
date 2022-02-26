from pykrx import stock
import win32com.client
from datetime import datetime
import os
import shutil
import time
import numpy as np


# 코스피 200 (180), 코스피지수 'U001'
# 코스닥 150 (390), 코스닥지수 'U201'

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


class Account:
    def __init__(self):
        self.objTrade = win32com.client.Dispatch("CpTrade.CpTdUtil")  # 함수안에서 전역변수로 써야함함
        self.initCheck = self.objTrade.TradeInit(0)
        if self.initCheck != 0:
            print("주문 초기화 실패")
            exit()
        else:
            self.acc = self.objTrade.AccountNumber[0]
            self.accFlag = self.objTrade.GoodsList(self.acc, 1)
            print(self.acc, self.accFlag[0], "계좌 주문 초기화 완료")
        self.objStockOrder = win32com.client.Dispatch("CpTrade.CpTd0311")

    def buyorder(self, code, amount, price):

        self.objStockOrder.SetInputValue(0, "2")  # 2: 매수
        self.objStockOrder.SetInputValue(1, self.acc)  # 계좌번호
        self.objStockOrder.SetInputValue(2, self.accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
        self.objStockOrder.SetInputValue(3, code)  # 종목코드 - 필요한 종목으로 변경 필요
        self.objStockOrder.SetInputValue(4, amount)  # 매수수량 - 요청 수량으로 변경 필요
        self.objStockOrder.SetInputValue(5, price)  # 주문단가 - 필요한 가격으로 변경 필요
        self.objStockOrder.SetInputValue(7, "0")  # 주문 조건 구분 코드, 0: 기본 1: IOC 2:FOK
        self.objStockOrder.SetInputValue(8, "01")  # 주문호가 구분코드 - 01: 보통
        nRet = self.objStockOrder.BlockRequest()
        if nRet != 0:
            print("주문요청 오류", nRet)
            # 0: 정상,  그 외 오류, 4: 주문요청제한 개수 초과
            exit()
        rqStatus = self.objStockOrder.GetDibStatus()
        errMsg = self.objStockOrder.GetDibMsg1()
        if rqStatus != 0:
            print("주문 실패: ", rqStatus, errMsg)
            exit()
        elif nRet == 0 and rqStatus == 0:
            print(code, "매수 성공")
        return True

    def sellorder(self, code, amount, price):
        self.objStockOrder.SetInputValue(0, "1")  # 2: 매도
        self.objStockOrder.SetInputValue(1, self.acc)  # 계좌번호
        self.objStockOrder.SetInputValue(2, self.accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
        self.objStockOrder.SetInputValue(3, code)  # 종목코드 - 필요한 종목으로 변경 필요
        self.objStockOrder.SetInputValue(4, amount)  # 매수수량 - 요청 수량으로 변경 필요
        self.objStockOrder.SetInputValue(5, price)  # 주문단가 - 필요한 가격으로 변경 필요
        self.objStockOrder.SetInputValue(7, "0")  # 주문 조건 구분 코드, 0: 기본 1: IOC 2:FOK
        self.objStockOrder.SetInputValue(8, "01")  # 주문호가 구분코드 - 01: 보통
        nRet = self.objStockOrder.BlockRequest()
        if nRet != 0:
            print("주문요청 오류", nRet)
            # 0: 정상,  그 외 오류, 4: 주문요청제한 개수 초과
            exit()
        rqStatus = self.objStockOrder.GetDibStatus()
        errMsg = self.objStockOrder.GetDibMsg1()
        if rqStatus != 0:
            print("주문 실패: ", rqStatus, errMsg)
            exit()
        elif nRet == 0 and rqStatus == 0:
            print(code, "매도 성공")
        return True

    def deposit(self):
        CpTdNew = win32com.client.Dispatch("CpTrade.CpTdNew5331A")
        CpTdNew.SetInputValue(0, self.acc)
        CpTdNew.SetInputValue(1, self.accFlag[0])
        CpTdNew.SetInputValue(6, ord("1"))
        CpTdNew.BlockRequest()
        money = CpTdNew.GetHeaderValue(9)
        print(money)
        return money


class MarketInfo:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    def Get_Market_Indexlist(self):
        todaydate = datetime.today().strftime("%Y%m%d")
        qospi = []
        qosdaq = []
        for ticker in stock.get_index_ticker_list(todaydate):
            if "코스피 200" == stock.get_index_ticker_name(ticker):
                qospi = stock.get_index_portfolio_deposit_file(ticker)
        for ticker in stock.get_index_ticker_list(todaydate, market='KOSDAQ'):
            if "코스닥 150" == stock.get_index_ticker_name(ticker):
                qosdaq = stock.get_index_portfolio_deposit_file(ticker)
        return qospi, qosdaq

    def GetstockPeriodInfo(self, period, code):  # 3일치를 부르면, 오늘 제외하고 2일치가 옴.
        """
         일별 ["날짜", "시가", "고가", "저가", "오늘종가", "오늘증가율", "고가증가율"]
         :param code, period: 코드, 기간(일)
         :return: 기간 별 정보
         """
        self.objStockChart.SetInputValue(0, str(code))  # 종목 코드
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
                                print(keys)
                                generalcount += 1
                                self.generalcount += 1
                                if todaystockbasket[-1][-1] >= 1:
                                    print(keys, "--")
                                    particularcount += 1
                                    self.particularcount += 1
                        break
            if generalcount != 0:
                try:
                    percent = round(particularcount / generalcount * 100, 2)
                    print(self.market, "전체: ", self.generalcount, "오늘 전체: ", generalcount, "오늘 증가: ", particularcount,
                          " total: ",
                          round(self.particularcount / self.generalcount * 100, 1), "%")
                except ZeroDivisionError:
                    percent = 0
                    print("0%")
            else:
                return 1
        return percent

    def MackoverlapPPO2(self, day, MAdayrange, stocklist):  # MackCodeDayBasket() 꼭 먼저 실행해줘야함
        if day > 500:  # 1년 데이터 축적
            try:
                print("전체: ", self.generalcount, " 증가: ", self.particularcount, " total: ",
                      round(self.particularcount / self.generalcount * 100, 2), "%")
            except ZeroDivisionError:
                print("0%")
                pass
            todaydate = self.kospibasket[day][0]
            for keys, val in self.codedaybasket.items():
                todaystockbasket = []
                for j in range(len(val)):
                    if val[j][0] == todaydate and keys in stocklist:
                        try:
                            CCI = self.indicators.MakeCCI(20, val)
                        except ZeroDivisionError:
                            print(keys, todaydate, "ZeroDivisionErrorZeroDivisionErrorZeroDivisionError")
                            continue  # 오류 수정해야함
                        newval = [val[i] for i in range(j)]  # 다음날것을 미리 반영해서 확률에 넣어버림 그래서 뺌
                        if len(newval) >= MAdayrange:
                            stockPPO = self.indicators.MakePPOFromFile(MAdayrange, newval)
                            stockoverlapppolist = self.totalresult.StockOverlapppoListFromFile(stockPPO, 1)
                            self.overlapppo[keys] = stockoverlapppolist
                            for i in range(0, MAdayrange):
                                todaystockbasket.append(val[j + 1 - MAdayrange + i])
                            if len(newval) % 500 != 0:
                                newval = [newval[-i] for i in range(1, 501)]
                                newval.reverse()  # 500일 데이터 기반으로 작동함. 500일씩 이동함
                            todayPPO = self.checktoday.MakePPOFromFile(MAdayrange, todaystockbasket)[0]
                            todayresult = self.checktoday.CheckTodayStockFromFile(self.overlapppo[keys], todayPPO)
                            if todayresult == 1 and CCI[val[j - 1][0]] < CCI[val[j][0]]:
                                print(todaydate)
                                print(keys)
                                self.generalcount += 1
                                if todaystockbasket[-1][-1] >= 1:
                                    print(keys, "--")
                                    self.particularcount += 1
                        break
        return True


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


class TotalResult:

    def StockOverlapppoListFromFile(self, PPO, increaserate):
        result = []
        ppomethod = PPOMethod()
        ppomethod.Condition_Setting(PPO, increaserate)
        middleresult = ppomethod.Get_result()
        if len(middleresult) != 0:  # 비어있는 middleresult가 [] 1개임
            result += middleresult
        return result  # [이격도]


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


class FileMethods:

    def clearfile(self):
        dir_path = "C:\\주가정보\\코스피200"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs("C:\\주가정보\\코스피200", exist_ok=True)
        dir_path = "C:\\주가정보\\코스닥150"
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs("C:\\주가정보\\코스닥150", exist_ok=True)
        return True

    def save_Info(self):
        self.clearfile()
        marketinfo = MarketInfo()
        qospi = marketinfo.Get_Market_Indexlist()[0]
        qosdaq = marketinfo.Get_Market_Indexlist()[1]
        for code in qospi:
            basket = marketinfo.GetstockPeriodInfo(505, code)
            f = open(f"C:\\주가정보\\코스피200\\{code}.txt", 'w', encoding='utf-8')
            f.write(str(basket))
            f.close()
        f = open(f"C:\\주가정보\\코스피200\\codelist.txt", 'w', encoding='utf-8')
        f.write(str(qospi))
        f.close()
        f = open(f"C:\\주가정보\\코스피200\\코스피200.txt", 'w', encoding='utf-8')
        f.write(str(marketinfo.GetstockPeriodInfo(505, 'U001')))
        f.close()
        for code in qosdaq:
            basket = marketinfo.GetstockPeriodInfo(505, code)
            f = open(f"C:\\주가정보\\코스닥150\\{code}.txt", 'w', encoding='utf-8')
            f.write(str(basket))
            f.close()
        f = open(f"C:\\주가정보\\코스닥150\\codelist.txt", 'w', encoding='utf-8')
        f.write(str(qosdaq))
        f.close()
        f = open(f"C:\\주가정보\\코스닥150\\코스닥150.txt", 'w', encoding='utf-8')
        f.write(str(marketinfo.GetstockPeriodInfo(505, 'U201')))
        f.close()

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
