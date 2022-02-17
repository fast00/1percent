from dd import *
from docx import Document
from tqdm import tqdm
import numpy as np

filelist = ['코스닥150','코스피100','코스피1000일', '코스닥1000일', '코스피결과-220114', '코스닥결과-220114']

def GetDaylist(filename, marketkind):
    Connect()
    marketinfo = MaketInfo()
    codelist = marketinfo.GetClearStockInfoByMarket(marketkind)
    codelistinfile = []
    file = CallFromFile()
    kospibasket1 = file.DayList(filename, marketkind)
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

    for code in codelist:
        try:
            basket1 = file.DayList(filename, code)
            remaindaylist[code] = []
            basket2[code] = []
            for i in range(0, len(basket1)):  # 720일까지만 하기 basket2를 이용
                if basket1[i][0] < date:
                    basket2[code] += [basket1[i]]
                elif basket1[i][0] >= date:
                    remaindaylist[code] += [basket1[i]]
            # PP0 = indicators.MakePPOFromFile(5,basket2)
        except (FileNotFoundError, IndexError):
            continue

    return codelistinfile, kospibasket2, basket2, kospiremaindaylist, remaindaylist

def GetDaylist2(filename, marketkind):
    codelist = ['A005930', 'A000660', 'A005935', 'A207940', 'A035420', 'A051910', 'A005380', 'A006400', 'A035720', 'A000270', 'A005490', 'A105560', 'A096770', 'A012330', 'A066570', 'A068270', 'A323410', 'A028260', 'A055550', 'A377300', 'A034730', 'A259960', 'A302440', 'A051900', 'A009150', 'A086790', 'A015760', 'A032830', 'A003550', 'A036570', 'A011200', 'A017670', 'A352820', 'A018260', 'A316140', 'A033780', 'A361610', 'A010950', 'A034020', 'A000810', 'A010130', 'A003670', 'A003490', 'A251270', 'A329180', 'A011070', 'A090430', 'A034220', 'A402340', 'A030200', 'A024110', 'A009830', 'A011170', 'A326030', 'A383220', 'A138040', 'A009540', 'A018880', 'A086280', 'A004020', 'A011790', 'A032640', 'A097950', 'A069500', 'A088980', 'A000060', 'A006800', 'A035250', 'A021240', 'A011780', 'A020150', 'A137310', 'A000720', 'A010140', 'A161390', 'A028050', 'A005830', 'A071050', 'A008560', 'A000100', 'A267250', 'A271560', 'A241560', 'A003410', 'A139480', 'A180640', 'A016360', 'A005387', 'A000990', 'A307950', 'A078930', 'A006360', 'A029780', 'A005940', 'A047810', 'A036460', 'A002790', 'A008930', 'A002380', 'A272210', 'A371460', 'A010620', 'A128940', 'A007070', 'A008770', 'A004990', 'A014680', 'A026960', 'A052690', 'A138930', 'A028670', 'A000120', 'A088350', 'A047050', 'A012750', 'A204320', 'A042660', 'A336260', 'A012450', 'A039490', 'A112610', 'A030000', 'A285130', 'A336370', 'A051915', 'A282330', 'A047040', 'A375500', 'A064350', 'A005385', 'A023530', 'A000880', 'A298050', 'A006280', 'A004170', 'A001040', 'A001450', 'A093370', 'A298020', 'A010060', 'A252670', 'A278540', 'A000080', 'A102110', 'A111770', 'A011210', 'A009240', 'A081660', 'A012510', 'A003090']
    codelistinfile = []
    file = CallFromFile()
    kospibasket1 = file.DayList(filename, marketkind)
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

    for code in codelist:
        try:
            basket1 = file.DayList(filename, code)
            remaindaylist[code] = []
            basket2[code] = []
            for i in range(0, len(basket1)):  # 720일까지만 하기 basket2를 이용
                if basket1[i][0] < date:
                    basket2[code] += [basket1[i]]
                elif basket1[i][0] >= date:
                    remaindaylist[code] += [basket1[i]]
            # PP0 = indicators.MakePPOFromFile(5,basket2)
        except (FileNotFoundError, IndexError):
            continue

    return codelistinfile, kospibasket2, basket2, kospiremaindaylist, remaindaylist

result = GetDaylist2('코스피1000일', 'KOSPI')
k = []
for MAdayrange in range(5,6):
    total = 0
    count = 0
    totalpercent = 0
    kospicodelist = result[0]  #리스트
    kospibasket = result[1]   #리스트
    stockbasket = result[2]  #코드 : 바스켓
    kospiremaindaylist = result[3] #리스트
    remaindaylist = result[4]  #코드 : 바스켓
    middleresult = {}
    print(MAdayrange)

    percent = 0
    for day in range(len(remaindaylist)):
        generalcount = 0
        particularcount = 0
################################################
        indicators = Indicators('kospi')
        kospiPPO = indicators.MakePPOFromFile(MAdayrange, kospibasket)
        kospiresult = MARKETResultFromFile(kospiPPO, -1)
##################################################
        checktoday = CheckToday()
        basket = []
        for keys, val in tqdm(stockbasket.items()):
            if len(val) >= MAdayrange:
                indicators = Indicators(keys)
                stockPPO = indicators.MakePPOFromFile(MAdayrange, val)
                lastdayresult = MakeTotalResult(stockPPO, 1)
                middleresult[keys] = lastdayresult
    #############하루 지남#################
        kospibasket += [kospiremaindaylist[day]]
        for keys,val in remaindaylist.items():
            stockbasket[keys] += [val[day]]
    ###################################
        for i in range(0,MAdayrange):
            basket.append(kospibasket[-MAdayrange+i])
        todayPPO = list(checktoday.MakePPOFromFile(MAdayrange,basket).values())[0]
        todayresult = checktoday.CheckTodayMarketFromFile(kospiresult, todayPPO)
        if todayresult != 1:
#######################################################
            for keys, val in tqdm(stockbasket.items()):
                if len(val) >= MAdayrange+1:
                    checktoday = CheckToday()
                    basket = []
                    for i in range(0, MAdayrange):
                        basket.append(val[-MAdayrange + i])
                    todayPPO = list(checktoday.MakePPOFromFile(MAdayrange, basket).values())[0]
                    if len(middleresult[keys]) != 0:
                        todayresult = checktoday.CheckTodayStockFromFile(middleresult[keys], todayPPO)
                        if todayresult == 1:
                            generalcount += 1
                            if val[-2][-1] >= 1:
                                particularcount += 1
            if generalcount == 0:
                continue
            try:
                percent = particularcount / generalcount * 100
                print('전체: ',generalcount,'성공: ', particularcount)
                if percent <= 50:
                    print(day)
                count += 1
            except ZeroDivisionError:
                percent = 0
                count += 1
                print('전체: ',generalcount,'성공: ', particularcount)
            print(day + 1, "일")
            print(round(percent,2))
        else:
            print('안삼')
    k.append(round(percent,2))
    print(k)
print(k)

#
# from creonlib import *
# from docx import Document
# from tqdm import tqdm
# import numpy as np
#
# filelist = ['코스닥150','코스피100','코스피1000일', '코스닥1000일', '코스피결과-220114', '코스닥결과-220114']
#
# def GetDaylist(filename, marketkind):
#     Connect()
#     marketinfo = MaketInfo()
#     codelist = marketinfo.GetClearStockInfoByMarket(marketkind)
#     codelistinfile = []
#     file = CallFromFile()
#     kospibasket1 = file.DayList(filename, marketkind)
#     kospibasket2 = []
#     basket2 = {}
#     remaindaylist = {}
#     kospiremaindaylist = []
#     date = 0
#     for i in range(0, len(kospibasket1)):
#         if i < 720:
#             kospibasket2.append(kospibasket1[i])
#         elif i == 720:
#             date = kospibasket1[i][0]
#             kospiremaindaylist.append(kospibasket1[i])
#         else:
#             kospiremaindaylist.append(kospibasket1[i])
#
#     for code in codelist:
#         try:
#             basket1 = file.DayList(filename, code)
#             remaindaylist[code] = []
#             basket2[code] = []
#             for i in range(0, len(basket1)):  # 720일까지만 하기 basket2를 이용
#                 if basket1[i][0] < date:
#                     basket2[code] += [basket1[i]]
#                 elif basket1[i][0] >= date:
#                     remaindaylist[code] += [basket1[i]]
#             # PP0 = indicators.MakePPOFromFile(5,basket2)
#         except (FileNotFoundError, IndexError):
#             continue
#
#     return codelistinfile, kospibasket2, basket2, kospiremaindaylist, remaindaylist
#
# def GetDaylist2(filename, marketkind):
#     codelist = ['A005930', 'A000660', 'A005935', 'A207940', 'A035420', 'A051910', 'A005380', 'A006400', 'A035720', 'A000270', 'A005490', 'A105560', 'A096770', 'A012330', 'A066570', 'A068270', 'A323410', 'A028260', 'A055550', 'A377300', 'A034730', 'A259960', 'A302440', 'A051900', 'A009150', 'A086790', 'A015760', 'A032830', 'A003550', 'A036570', 'A011200', 'A017670', 'A352820', 'A018260', 'A316140', 'A033780', 'A361610', 'A010950', 'A034020', 'A000810', 'A010130', 'A003670', 'A003490', 'A251270', 'A329180', 'A011070', 'A090430', 'A034220', 'A402340', 'A030200', 'A024110', 'A009830', 'A011170', 'A326030', 'A383220', 'A138040', 'A009540', 'A018880', 'A086280', 'A004020', 'A011790', 'A032640', 'A097950', 'A069500', 'A088980', 'A000060', 'A006800', 'A035250', 'A021240', 'A011780', 'A020150', 'A137310', 'A000720', 'A010140', 'A161390', 'A028050', 'A005830', 'A071050', 'A008560', 'A000100', 'A267250', 'A271560', 'A241560', 'A003410', 'A139480', 'A180640', 'A016360', 'A005387', 'A000990', 'A307950', 'A078930', 'A006360', 'A029780', 'A005940', 'A047810', 'A036460', 'A002790', 'A008930', 'A002380', 'A272210', 'A371460', 'A010620', 'A128940', 'A007070', 'A008770', 'A004990', 'A014680', 'A026960', 'A052690', 'A138930', 'A028670', 'A000120', 'A088350', 'A047050', 'A012750', 'A204320', 'A042660', 'A336260', 'A012450', 'A039490', 'A112610', 'A030000', 'A285130', 'A336370', 'A051915', 'A282330', 'A047040', 'A375500', 'A064350', 'A005385', 'A023530', 'A000880', 'A298050', 'A006280', 'A004170', 'A001040', 'A001450', 'A093370', 'A298020', 'A010060', 'A252670', 'A278540', 'A000080', 'A102110', 'A111770', 'A011210', 'A009240', 'A081660', 'A012510', 'A003090']
#     codelistinfile = []
#     file = CallFromFile()
#     kospibasket1 = file.DayList(filename, marketkind)
#     kospibasket2 = []
#     basket2 = {}
#     remaindaylist = {}
#     kospiremaindaylist = []
#     date = 0
#     for i in range(0, len(kospibasket1)):
#         if i < 720:
#             kospibasket2.append(kospibasket1[i])
#         elif i == 720:
#             date = kospibasket1[i][0]
#             kospiremaindaylist.append(kospibasket1[i])
#         else:
#             kospiremaindaylist.append(kospibasket1[i])
#
#     for code in codelist:
#         try:
#             basket1 = file.DayList(filename, code)
#             remaindaylist[code] = []
#             basket2[code] = []
#             for i in range(0, len(basket1)):  # 720일까지만 하기 basket2를 이용
#                 if basket1[i][0] < date:
#                     basket2[code] += [basket1[i]]
#                 elif basket1[i][0] >= date:
#                     remaindaylist[code] += [basket1[i]]
#             # PP0 = indicators.MakePPOFromFile(5,basket2)
#         except (FileNotFoundError, IndexError):
#             continue
#
#     return codelistinfile, kospibasket2, basket2, kospiremaindaylist, remaindaylist
#
# result = GetDaylist2('코스피1000일', 'KOSPI')
# k = []
# for MAdayrange in range(3,30):
#     total = 0
#     count = 0
#     totalpercent = 0
#     kospicodelist = result[0]  #리스트
#     kospibasket = result[1]   #리스트
#     stockbasket = result[2]  #코드 : 바스켓
#     kospiremaindaylist = result[3] #리스트
#     remaindaylist = result[4]  #코드 : 바스켓
#     middleresult = {}
#     print(MAdayrange)
#     for day in range(30):
#         generalcount = 0
#         particularcount = 0
# ################################################
#         indicators = Indicators('kospi')
#         kospiPPO = indicators.MakePPOFromFile(MAdayrange, kospibasket)
#         kospiresult = MARKETResultFromFile(kospiPPO, -1)
# ##################################################
#         checktoday = CheckToday()
#         basket = []
#         for keys, val in tqdm(stockbasket.items()):
#             if len(val) >= MAdayrange:
#                 indicators = Indicators(keys)
#                 stockPPO = indicators.MakePPOFromFile(MAdayrange, val)
#                 lastdayresult = MakeTotalResult(stockPPO, 1)
#                 middleresult[keys] = lastdayresult
#     #############하루 지남#################
#         kospibasket += [kospiremaindaylist[day]]
#         for keys,val in remaindaylist.items():
#             stockbasket[keys] += [val[day]]
#     ###################################
#         for i in tqdm(range(0,MAdayrange)):
#             basket.append(kospibasket[-MAdayrange+i])
#         todayPPO = list(checktoday.MakePPOFromFile(MAdayrange,basket).values())[0]
#         todayresult = checktoday.CheckTodayMarketFromFile(kospiresult, todayPPO)
#         if todayresult != 1:
# #######################################################
#             for keys, val in tqdm(stockbasket.items()):
#                 if len(val) >= MAdayrange+1:
#                     checktoday = CheckToday()
#                     basket = []
#                     for i in range(0, MAdayrange):
#                         basket.append(val[-MAdayrange + i])
#                     todayPPO = list(checktoday.MakePPOFromFile(MAdayrange, basket).values())[0]
#                     if len(middleresult[keys]) != 0:
#                         todayresult = checktoday.CheckTodayStockFromFile(middleresult[keys], todayPPO)
#                         if todayresult == 1:
#                             generalcount += 1
#                             if val[-2][-1] >= 1:
#                                 particularcount += 1
#             if generalcount == 0:
#                 continue
#             try:
#                 percent = particularcount / generalcount * 100
#                 print('전체: ',generalcount,'성공: ', particularcount)
#                 count += 1
#             except ZeroDivisionError:
#                 percent = 0
#                 count += 1
#                 print('전체: ',generalcount,'성공: ', particularcount)
#             total += percent
#             totalpercent = total / count
#             print(day + 1, "일")
#             print(round(totalpercent,2), round(percent,2))
#         else:
#             print('안삼')
#     k.append(round(totalpercent,2))
#     print(k)
# print(k)