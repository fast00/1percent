# # 381 1524
#
#
# from main2lib import *
# from tqdm import tqdm
# # Connect()
# #양수 부분
# file = FileMethods()
# indicators = Indicators()
# codelist = file.GetStockList('코스피150')
# kospibasket = file.MarketDayList('코스피150')
# codebasket = {}
# ocillatorlist = {}
# generalpluscount = {}
# particularpluscount = {}
# for code in codelist:
#     codebasket[code] = []
#     basket = file.StockDayList('코스피150', code)
#     for i in range(len(basket)):
#         codebasket[code] += [basket[i]]
#
# for keys, val in codebasket.items():
#     if len(val) >= 26:
#         MA12 = indicators.MakeEMA(12, "D", val)
#         MA26 = indicators.MakeEMA(26, "D", val)
#         ocillator = indicators.MakeMACDoscillator("D",MA12, MA26)
#         ocillatorlist[keys] = ocillator
#         generalpluscount[keys] = 0
#         particularpluscount[keys] = 0
#
# percent = 0
# highcount = 0
# highpercent = 0
# count = 0
# totalpercent = []
# totalincome = []
# gihaaverage = []
# for day in range(len(kospibasket)):
#     generalcount = 0
#     particularcount = 0
#     todaydate = kospibasket[day][0]
#     if day <= 400:  # 이정도 날짜부터 가중치가 거의 정확함
#         continue
#     print(todaydate, "일")
#     for keys, val in ocillatorlist.items():
#         for i in range(len(val)):
#             if todaydate == val[i][0] and i > 400:
#                 if val[i][2] >= 0:
#                     generalpluscount[keys] += 1
#                     if generalpluscount[keys] == 1 and val[i][3] - val[i][4] > 0:  # 첫날 0보다 크고 양봉
#                         particularpluscount[keys] += 1
#                     if generalpluscount[keys] == 2 and val[i][3] - val[i][4] > 0:  # 둘째날 0보다 크고 양봉
#                         particularpluscount[keys] += 1
#                 elif val[i][2] < 0:
#                     generalpluscount[keys] = 0
#                     particularpluscount[keys] = 0
#                 if particularpluscount[keys] == 2:
#                     print(keys,val[i][2],val[i][1])
#                     generalcount += 1
#                     highpercent = val[i][1]
#                     gihaaverage.append(highpercent)
#                     if val[i][1] >= 1:
#                         particularcount += 1
#                 break
#     try:
#         if generalcount != 0:
#             count+=1
#             percent += round(particularcount / generalcount * 100, 2)
#             print("전체: ",generalcount," 증가: ",particularcount,"총이익:",sum(gihaaverage)/count," total: ",percent/count ,"%")
#     except ZeroDivisionError:
#         continue
#                 #["날짜", "시가", "고가", "저가", "오늘종가", "거래량", "오늘증가율", "다음날고가증가율"]
#                 # [날짜,시간,시가,고가,저가,종가,거래량]
#
# for i in range(len(gihaaverage)):
#     gihaaverage[i] = gihaaverage[i]+1
# gob = 1
# for i in range(len(gihaaverage)):
#     gob = gob * gihaaverage[i]
#
# print(gob**0.5-1)
#
# # 381 1524
#
# ###############################카톡 확인해서 조건만 바꾸기(음수)
#
from main2lib import *
from tqdm import tqdm
file = FileMethods()
indicators = Indicators()
checktoday = CheckToday()
totalresult = TotalResult()
codelist = file.GetStockList('코스피150')
kospibasket = file.MarketDayList('코스피150')
codebasket = {}
ocillatorlist = {}
generalpluscount = {}
minuslist= {}
particularpluscount = {}
for code in codelist:
    codebasket[code] = []
    basket = file.StockDayList('코스피150', code)
    for i in range(len(basket)):
        codebasket[code] += [basket[i]]

for keys, val in codebasket.items():
    if len(val) >= 26:
        MA12 = indicators.MakeEMA(12, "D", val)
        MA26 = indicators.MakeEMA(26, "D", val)
        ocillator = indicators.MakeMACDoscillator("D",MA12, MA26)
        ocillatorlist[keys] = ocillator
        generalpluscount[keys] = 0
        particularpluscount[keys] = 0
        minuslist[keys] = []
g =0
p =0
average = {}
hap = 0

for day in range(len(kospibasket)):
    generalcount = 0
    particularcount = 0

    todaydate = kospibasket[day][0]
    if day <= 400:  # 이정도 날짜부터 가중치가 거의 정확함
        continue
    for keys, val in ocillatorlist.items():
        for i in range(len(val)-1):
            if todaydate == val[i][0] and i > 400:
                if val[i][2] >= 0:
                    generalpluscount[keys] += 1
                    particularpluscount[keys] = 0
                if val[i][2] < 0:
                    if generalpluscount[keys] >= 1:
                        particularpluscount[keys] += 1
                        if particularpluscount[keys] == 1:
                            minuslist[keys].append(val[i][2])
                        if val[i+1][2] >= 0:
                            minuslist[keys].append(val[i][2])
                break
                #["날짜", "시가", "고가", "저가", "오늘종가", "거래량", "오늘증가율", "다음날고가증가율"]
                # [날짜,시간,시가,고가,저가,종가,거래량]

    if day <= 700:
        continue
    print(todaydate, "일")
    for key, val in minuslist.items():
        if len(val) == 0:
            continue
        average[key] = round(sum(val)/len(val),2)

    for keys, val in ocillatorlist.items():
        for i in range(len(val)-1):
            if todaydate == val[i][0] and i > 700:
                if (val[i][2] - val[i-1][2]) / (i - (i-1)) > 0 and val[i][3] - val[i][4] > 0:
                    if average[keys]*1/3 > val[i][2] >= average[keys]*1/2:
                        print(keys)
                        generalcount += 1
                        g +=1
                        if val[i][1] + val[i+1][1] >= 1:
                            hap += val[i][1]
                            print("----",keys)
                            particularcount += 1
                            p+=1
    try:
        print(round(particularcount/generalcount*100,2),"%","전체: ",generalcount,"성공: ",particularcount)
    except ZeroDivisionError:
        continue
print(p/g*100)
print(hap/p)
#
#
# from main2lib import *
# from tqdm import tqdm
# # Connect()
# #양수 부분
# file = FileMethods()
# indicators = Indicators()
# checktoday = CheckToday()
# totalresult = TotalResult()
# codelist = file.GetStockList('코스피150')
# kospibasket = file.MarketDayList('코스피150')
# codebasket = {}
# ocillatorlist = {}
# generalpluscount = {}
# generalminuscount = {}
# particularpluscount = {}
# for code in codelist:
#     codebasket[code] = []
#     basket = file.StockDayList('코스피150', code)
#     for i in range(len(basket)):
#         codebasket[code] += [basket[i]]
#
# for keys, val in codebasket.items():
#     if len(val) >= 26:
#         MA12 = indicators.MakeEMA(12, "D", val)
#         MA26 = indicators.MakeEMA(26, "D", val)
#         ocillator = indicators.MakeMACDoscillator("D",MA12, MA26)
#         ocillatorlist[keys] = ocillator
#         generalpluscount[keys] = 0
#         generalminuscount[keys] = 0
#         particularpluscount[keys] = 0
#
# percent = 0
# percent1 = 0
# highcount = 0
# highpercent = 0
# signal = 0
# count = 0
# totalpercent = []
# totalincome = []
# gihaaverage = []
# generalcount = 0
# particularcount = 0
# for day in range(len(kospibasket)):
#
#     todaydate = kospibasket[day][0]
#     if day <= 400:  # 이정도 날짜부터 가중치가 거의 정확함
#         continue
#     print(todaydate, "일")
#     for keys, val in ocillatorlist.items():
#         for i in range(len(val)-1):
#             if todaydate == val[i][0] and i > 400:
#                 if val[i][2] < 0:
#                     signal = 0
#                     generalminuscount[keys] += 1
#                     generalpluscount[keys] = 0
#                 if val[i][2] >= 0:
#                     if generalminuscount[keys] > 1:
#                         generalpluscount[keys] += 1
#                     if generalpluscount[keys] > 1:
#                         if (val[i][2] - val[i-1][2]) / i - (i-1) < 0:
#                             signal = 1
#                             generalcount += 1
#                             if val[i][1] >= 1:
#                                 particularcount += 1
# try:
#     percent = particularcount / generalcount
#     percent1 += percent
#     count += 1
#     print("전체: ",generalcount,"성공: ",particularcount,round(percent*100,2),"%")
# except ZeroDivisionError:
#     pass
#
# print(percent1 / count *100)
# ##########################################################################
# # generalcount = 0
# # particularcount = 0
# # a = {}
# # for keys, val in codebasket.items():
# #     a[keys] = 0
# # for day in tqdm(range(len(kospibasket))):
# #     todaydate = kospibasket[day][0]
# # for keys, val in codebasket.items():
# #     for i in range(len(val)):
# #         if 20210730 < val[i][0]<=20211030:
# #             generalcount+=1
# #             if 11>val[i][7]>=4:
# #                 particularcount+=1
# #                 a[keys]+=1
# # ##############상찍기 전 3개월정도 확인해보기
# # print(particularcount/generalcount*100,"\n",particularcount)
# #
# # a=sorted(a.items(), key=lambda x: x[1], reverse=True)
# # print(a)
# # b=[]
# # for i in range(0,10):
# #     b.append(a[i][0])
# # print(b)