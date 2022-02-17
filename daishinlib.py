import time

import win32com.client

NULL = 0
KOSPI = 1
KOSDAQ = 2
FREEBOARD = 3
KRX = 4
KONEX = 5


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


class DaishinMgr:
    def __init__(self):
        self.g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        # self.objRq = win32com.client.Dispatch("CpSysDib.CpSvr7049")
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.objRq = win32com.client.Dispatch("CpSysDib.MarketEye")
        self.objStockOpenSb = win32com.client.Dispatch("Dscbo1.StockMst")

    def GetTime(self):
        cptime = CpTimeChecker(1).checkRemainTime()
        if cptime[1] == 1 and cptime[0] != 0:
            while True:
                if CpTimeChecker(1).checkRemainTime()[0] == 0:
                    time.sleep(0.5)
                    break

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
        sum = 0
        for i in codelist:
            codes.append(i)
            if len(codes) == 200 or (len(codelist) - codelist.index(i) < 200 and len(codelist) % 200 == len(codes)):
                rqField = [0, 109]  # 코드, 분기 유보율
                self.objRq.SetInputValue(0, rqField)  # 요청 필드
                self.objRq.SetInputValue(1, codes)  # 종목코드 or 종목코드 리스트
                self.objRq.BlockRequest()
                self.GetTime()
                cnt = self.objRq.GetHeaderValue(2)  # 종목 개수
                for k in range(cnt):
                    code = self.objRq.GetDataValue(0, k)  # 코드
                    reserveratio = self.objRq.GetDataValue(1, k)  # 분기 유보율
                    if reserveratio > 0:
                        result.append(code)
                codes = []
        return result

    def GetStockManagement(self, code):
        self.objStockOpenSb.SetInputValue(0, code)
        self.objStockOpenSb.BlockRequest()
        self.GetTime()
        for i in range(66,70):
            manage = chr(self.objStockOpenSb.GetHeaderValue(i))
            if manage == 'Y':  # 거래정지, 관리종목
                return 1
            if i == 67 and manage != '1':  # 투자경고
                return 1
            if i == 69 and manage != '0':  # 불성실공시
                return 1
        return 0

    def GetstockPeriodayInfo(self, code, period):
        """
         일별 ["날짜", "시가", "고가", "저가", "종가", "대비", "퍼센트"]
         :param code, period: 코드, 기간(일)
         :return: 기간 별 정보
         """
        self.objStockChart.SetInputValue(0, str(code))  # 종목 코드 - 삼성전자
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
        self.objStockChart.SetInputValue(4, period+1)  # 최근 100일 치
        self.objStockChart.SetInputValue(5, [0, 2, 3, 4, 5])  # 날짜,시가,고가,저가,종가
        self.objStockChart.SetInputValue(6, ord('D'))  # '차트 주가 - 일간 차트 요청
        self.objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
        self.objStockChart.BlockRequest()
        self.GetTime()
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
            basket.append([day, open, high, low, todayclose])  # "날짜", "시가", "고가", "저가", "오늘종가"
        basket.reverse()
        for i in range(len(basket)):
            if i>0:
                try:
                    todaypercent = round((basket[i][4] - basket[i-1][4])/basket[i-1][4]*100,2)
                except ZeroDivisionError:
                    todaypercent = 0
                try:
                    highpercent = round((basket[i][2] - basket[i-1][4])/basket[i-1][4]*100,2)
                except ZeroDivisionError:
                    highpercent = 0
                basket[i] = basket[i] + [todaypercent, highpercent]
        del basket[0]
        return basket  # ["날짜", "시가", "고가", "저가", "오늘종가", "오늘증가율", "고가증가율"]

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

    def InquireStock(self, code, fromday, today):
        self.objStockChart.SetInputValue(0,code)
        self.objStockChart.SetInputValue(1, ord('1'))
        self.objStockChart.SetInputValue(2, today)
        self.objStockChart.SetInputValue(3, fromday)
        self.objStockChart.SetInputValue(5, [0,3,5,6,8])  #날짜 고가 종가 전일종가대비 거래량
        self.objStockChart.BlockRequest()
        self.GetTime()
        len = self.objStockChart.GetHeaderValue(3)
        result = []
        for i in range(len):
            day = self.objStockChart.GetDataValue(0, i)
            high = self.objStockChart.GetDataValue(1, i)
            todayclose = self.objStockChart.GetDataValue(2, i)
            diff = self.objStockChart.GetDataValue(3, i)
            yesterdayclose = todayclose - diff
            volume = self.objStockChart.GetDataValue(4, i)
            percent = round((high-yesterdayclose)/yesterdayclose*100,2)
            result.append(day)
            result.append(f'고가 : {percent}%')
            result.append(f'거래량 : {volume}')
        return f'{code} : {result}'

    def CheckPredict(self, codedic, percent):
        codes = []
        particalcode = []
        for keys,val in codedic.items():
            codes.append(keys)
        rqField = [0, 6, 23]  # 코드, 고가, 전일종가
        self.objRq.SetInputValue(0, rqField)  # 요청 필드
        self.objRq.SetInputValue(1, codes)  # 종목코드 or 종목코드 리스트
        self.objRq.BlockRequest()
        self.GetTime()
        cnt = self.objRq.GetHeaderValue(2)  # 종목 개수
        generalcount = len(codes)
        particalcount = 0
        for k in range(cnt):
            try:
                code = self.objRq.GetDataValue(0, k)  # 코드
                high = self.objRq.GetDataValue(1, k)  # 고가
                yesterdayclose = self.objRq.GetDataValue(2, k)  # 전일종가
                calpercent = round((high-yesterdayclose)/yesterdayclose*100,2)
            except ZeroDivisionError:
                continue
            if calpercent >= percent:
                particalcount += 1
                particalcode.append(code)
        try:
            totalpercent = round(particalcount/generalcount*100,2)
        except ZeroDivisionError:
            totalpercent = 0
        return f'{totalpercent}%', particalcode

class Tool:
    def __init__(self, stockPeriodayInfo, pporange):
        self.stockPeriodayInfo = stockPeriodayInfo  # ["날짜", "시가", "고가", "저가", "오늘종가", "오늘증감율", "고가증감율"]
        self.pporange = pporange  # 몇일 이격 인지 입력
        self.ppolist = []  # [날짜 , 이격도 , 오늘증감률, 고가증감률]
        self.totalresult = {}  # 최종 결과
        self.percentandparticular = {}  # 전날 퍼센트 : 확률, 개수
        self.generalresult = {}  # 전체 확률 카운트
        self.particularresult = {}  # 부분 확률 카운트
        self.rangedayresult = {}  # 범위안에 들어가는 전체확률 일수
        self.rangeresult = {}  # 전체 범위안에 있는 이격도
        self.percent = 0

    def MakePPOList(self):
        """
         이격도를 만듭니다.
         :param: stockPeriodayInfo, pporange
         :return: ppolist, ppo
         """
        MA = 0  # 이동평균선
        for i in range(len(self.stockPeriodayInfo)):
            if i >= self.pporange-1:
                for k in range(0, 5):
                    MA += self.stockPeriodayInfo[i - k][4]
                MA = MA / self.pporange  # 이격도
                PPO = self.stockPeriodayInfo[i][4] / MA * 100  # 이격도
                self.ppolist.append(
                    [self.stockPeriodayInfo[i][0], round(PPO, 2), self.stockPeriodayInfo[i][5],
                     self.stockPeriodayInfo[i][6]])  # [날짜 , 이격도 , 오늘증감률, 고가증감률]
                MA = 0
        ppo = []  # 이격도 리스트
        for i in range(len(self.ppolist)):
            ppo.append((self.ppolist[i][1]))
        ppo.sort()
        return ppo

    def MackAverage(self, dic):
        valaverage = 0
        count = 0
        try:
            for keys, val in dic.items():
                if dic[keys] > 0:
                    count += 1
                    valaverage += dic[keys]
            valaverage /= count
        except ZeroDivisionError:
            valaverage = 0
        return valaverage

    def UsePPO(self, ppo, nextday, decreasepercent, increasepersent, percent):
        """
         이격도를 사용해서 계산합니다.
         :param: ppolist, ppo, nextday, increasepersent, decreasepercent
         :return: generalresult, particularresult, rangeresult
         """
        self.percent = percent
        for k in range(round(ppo[-1] - ppo[0])):
            self.generalresult[ppo[0] + k] = 0  # 범위안에 들어가는 횟수
            self.particularresult[ppo[0] + k] = 0  # 일정 퍼센트 이상 횟수
            self.rangedayresult[f"{ppo[0] + k}~{ppo[0] + k + 1}"] = []  # 최종 결과 초기화(날짜)
            self.rangeresult[f"{ppo[0] + k}~{ppo[0] + k + 1}"] = 0  # 최종 결과 초기화
        for k in range(round(ppo[-1] - ppo[0])):
            for i in range(len(self.ppolist) - nextday):
                if i > 0 and ppo[0] + k <= self.ppolist[i][1] < ppo[0] + k + 1 and int(self.ppolist[i][2]) == decreasepercent:  # 범위 내부 and 하락률 소수점 제거
                    self.generalresult[ppo[0] + k] += 1  # 범위안에 들어가는 횟수 추가
                    self.rangedayresult[f"{ppo[0] + k}~{ppo[0] + k + 1}"] += [self.ppolist[i],self.ppolist[i+1][-1]]  #  다음날 추가
                    if self.ppolist[i + nextday][3] >= increasepersent:
                        # print(self.ppolist[i])
                        self.particularresult[ppo[0] + k] += 1  # 일정 퍼센트 이상 횟수 추가

        return self.generalresult, self.particularresult, self.rangeresult, self.rangedayresult

    def FaildayResult(self, ppo, nextday, decreasepercent, increasepersent, percent):
        """
         이격도를 사용해서 계산합니다.
         :param: ppolist, ppo, nextday, increasepersent, decreasepercent
         :return: generalresult, particularresult, rangeresult
         """
        faillist = []
        self.percent = percent
        for k in range(round(ppo[-1] - ppo[0])):
            self.generalresult[ppo[0] + k] = 0  # 범위안에 들어가는 횟수
            self.particularresult[ppo[0] + k] = 0  # 일정 퍼센트 이상 횟수
            self.rangedayresult[f"{ppo[0] + k}"] = []  # 최종 결과 초기화(날짜)
            self.rangeresult[f"{ppo[0] + k}~{ppo[0] + k + 1}"] = 0  # 최종 결과 초기화
        for k in range(round(ppo[-1] - ppo[0])):
            for i in range(len(self.ppolist) - nextday):
                if i > 0 and ppo[0] + k <= self.ppolist[i][1] < ppo[0] + k + 1 and int(
                        self.ppolist[i][2]) == decreasepercent:  # 범위 내부 and 하락률 소수점 제거
                    self.generalresult[ppo[0] + k] += 1  # 범위안에 들어가는 횟수 추가
                    self.rangedayresult[f"{ppo[0] + k}"] += [self.ppolist[i][0]]  # 해당 날짜 추가
                    if self.ppolist[i + nextday][3] >= increasepersent:
                        # print(self.ppolist[i])
                        # self.rangedayresult[f"{ppo[0] + k}"] += [self.ppolist[i][0]]
                        self.rangedayresult[f"{ppo[0] + k}"][-1] = ''  # 해당 날짜 추가
                        self.particularresult[ppo[0] + k] += 1  # 일정 퍼센트 이상 횟수 추가

        generalaverage = self.MackAverage(self.generalresult)
        particularalaverage = self.MackAverage(self.particularresult)
        for i in range(round(ppo[-1] - ppo[0])):  # 최종 결과를 구함
            try:
                self.rangeresult[
                    f"{ppo[0] + i}~{ppo[0] + i + 1}"] = f"{round(self.particularresult[ppo[0] + i] / self.generalresult[ppo[0] + i] * 100, 2)}%"  # 최종 결과 {범위: 확률}
            except ZeroDivisionError:
                self.rangeresult[f"{ppo[0] + i}~{ppo[0] + i + 1}"] = "0%"

        for i in range(round(ppo[-1] - ppo[0])):  # -퍼센트 별로 확률을 구함
            if self.particularresult[ppo[0] + i] == 0:
                continue
            if self.generalresult[ppo[0] + i] >= generalaverage and self.particularresult[ppo[0] + i] >= particularalaverage and \
                    self.particularresult[ppo[0] + i] / self.generalresult[ppo[0] + i] * 100 >= self.percent and \
                    self.generalresult[ppo[0] + i] >= 5:  # 전체 평균보다 횟수가 많고 그 확률이 percent 이상
                faillist = self.rangedayresult[f"{ppo[0] + i}"]

        return faillist

    def MackRangePPO(self, code, ppo, decreasepercent):
        """
         이격도를 사용해서 계산합니다.
         :param: ppo, generalresult, particularresult, rangeresult
         :return: rangeresult
         """
        generalaverage = self.MackAverage(self.generalresult)
        particularalaverage = self.MackAverage(self.particularresult)
        result = []  # 이격도 범위, 증감률
        for i in range(round(ppo[-1] - ppo[0])):  # 최종 결과를 구함
            try:
                self.rangeresult[
                    f"{ppo[0] + i}~{ppo[0] + i + 1}"] = f"{round(self.particularresult[ppo[0] + i] / self.generalresult[ppo[0] + i] * 100, 2)}%"  # 최종 결과 {범위: 확률}
            except ZeroDivisionError:
                self.rangeresult[f"{ppo[0] + i}~{ppo[0] + i + 1}"] = "0%"

        for i in range(round(ppo[-1] - ppo[0])):  # -퍼센트 별로 확률을 구함
            if self.particularresult[ppo[0] + i] == 0:
                continue
            if self.generalresult[ppo[0] + i] >= generalaverage and self.particularresult[ppo[0] + i] >= particularalaverage and \
                    self.particularresult[ppo[0] + i] / self.generalresult[ppo[0] + i] * 100 >= self.percent and self.generalresult[ppo[0] + i] >= 5:  # 전체 평균보다 횟수가 많고 그 확률이 percent 이상
                result.append(ppo[0] + i)
                result.append(decreasepercent)
                self.percentandparticular[decreasepercent] = [self.rangeresult[f'{ppo[0] + i}~{ppo[0] + i + 1}'],
                                                              self.particularresult[ppo[0] + i]]  # 퍼센트랑 오른 개수 구함 최종값 산출할때 씀
                print(
                    f"{code}:{decreasepercent}\n"
                    f"({ppo[0] + i}~{ppo[0] + i + 1}): {self.rangeresult[f'{ppo[0] + i}~{ppo[0] + i + 1}']} \
                    당일 횟수: {self.generalresult[ppo[0] + i]} , 다음날 상승 횟수: {self.particularresult[ppo[0] + i]}\n"
                    f"{self.rangedayresult[f'{ppo[0] + i}~{ppo[0] + i + 1}']}")
        return self.rangeresult, result


class StockPredict(Tool):
    def __init__(self, code, stockPeriodayInfo, pporange):
        super().__init__(stockPeriodayInfo, pporange)
        self.code = code
        self.ppo = 0

    def TodayPPO(self):
        MA = 0  # 이동평균선
        for i in range(self.pporange+1):
            if i != 0:
                MA += self.stockPeriodayInfo[-i][-3]
        MA = MA / self.pporange
        self.ppo = round(self.stockPeriodayInfo[-1][-3] / MA * 100, 2)  # 이격도
        return self.ppo  # checktodaystock에 넘겨줌

    def CheckTodayStock(self, totalresult):  # [코드 : 이격도 범위, 증감률]
        total = {}
        for keys, val in totalresult.items():
            if keys == self.code and val != '[]':
                for i in range(int(len(val) / 2)):
                    if val[2 * i] <= self.ppo < val[2 * i] + 1 and int(self.stockPeriodayInfo[-1][-2]) == val[
                        2 * i + 1]:
                        total[self.code] = self.percentandparticular[int(self.stockPeriodayInfo[-1][-2])]
        if len(total) == 0 or DaishinMgr().GetStockManagement(self.code) == 1:
            return 1
        return self.code, self.percentandparticular[int(self.stockPeriodayInfo[-1][-2])]

class CheckResult:
    def CheckOnePercent(self):
        f = open("C:\\Users\\82104\\Desktop\\1%.txt", 'r', encoding='utf-8')
        lines = f.readlines()
        codedic = eval(lines[-1])
        manager = DaishinMgr()
        result = manager.CheckPredict(codedic,1)
        f.close()
        print(result)

    def CheckTwoPercent(self):
        f = open("C:\\Users\\82104\\Desktop\\2%.txt", 'r', encoding='utf-8')
        lines = f.readlines()
        codedic = eval(lines[-1])
        manager = DaishinMgr()
        result = manager.CheckPredict(codedic,2)
        f.close()
        print(result)