
from main2lib import *
from tqdm import tqdm

# 381 1524
list = {}
Connect()
codelist = Codelist().GetClearStockInfoByMarket('KOSPI')
marketinfo = MarketInfo("A138040")
indicators = Indicators()
minutebasket = marketinfo.GetstockMinutePeriodInfo()

MA12 = indicators.MakeEMA(10, minutebasket)
MA26 = indicators.MakeEMA(1, minutebasket)
MACDbasket = []
for i in range(len(MA12)):
    for k in range(len(MA26)):
        if MA12[i][0] == MA26[k][0] and MA12[i][1] == MA26[k][1]:
            MACDbasket.append([MA12[i][0], MA12[i][1], round(MA12[i][2] - MA26[k][2], 2), MA12[i][3]])
signalbasket = indicators.MakeEMAsignal(9, MACDbasket)
# print(MACDbasket)
# print(signalbasket)
MACDoscillator = []
comparerange = []
for i in range(len(MACDbasket)):
    for k in range(len(signalbasket)):
        if MACDbasket[i][0] == signalbasket[k][0] and MACDbasket[i][1] == signalbasket[k][1]:
            MACDoscillator.append(
                [MACDbasket[i][0], MACDbasket[i][1], float(round(MACDbasket[i][2] - signalbasket[k][2], 2)),
                 MACDbasket[i][3]])
            # 날짜, 시간, 오실레이터, 종가
            comparerange.append(int(MACDbasket[i][2] - signalbasket[k][2]))
ocillator = MACDoscillator
print(ocillator)
# print(ocillator)
nowprice = 0
endprice = 0
incomlist = []
incomlist2 = []
ot = 0
buy = 0
pluscount = 0
fistX = 0
fistY = 0
secondX = 0
secondY = 0
slope = 0
slopelist = {}
for i in tqdm(range(len(ocillator))):
    if ocillator[i][2] > 0 and buy == 0:
        pluscount += 1
        if pluscount == 1:
            fistX = i
            fistY = ocillator[i][2]
            continue
        secondX = i
        secondY = ocillator[i][2]
        slope = (secondY - fistY) / (secondX - fistX)
        print(slope)
