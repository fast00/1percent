from totallib import *
from matplotlib import pyplot as plt
import pandas as pd


useppo = UsePPO('코스피200!')
useppo2 = UsePPO('코스닥150!')
# useoscillator = UseOSCILLATOR('코스피200!')
kospibasket = useppo.kospibasket
count = 0
daypercentcount = 0
daypercentsum = 0
graphcount = 0
garo = []
sero = []
for day in range(len(kospibasket)):
    if day < 1000:
        continue
    print(day)
    beforemonth = kospibasket[day - 30][0]  # 최초는 20일, 30일 86.5 %
    yesterday = kospibasket[day - 1][0]
    todaydate = kospibasket[day][0]
    stocklist = useppo.CheckStrogStock(beforemonth, yesterday, 2)
    stocklist2 = useppo2.CheckStrogStock(beforemonth, yesterday, 2)
    graphdate = str(int(kospibasket[day][0]))
    daypercent = useppo.MackoverlapPPO(day, 5, stocklist)
    daypercent2 = useppo2.MackoverlapPPO(day, 5, stocklist2)
    if daypercent ==1 and daypercent2 == 1:
        count+=1
        print(todaydate, count,useppo.generalcount+useppo2.generalcount, (useppo.particularcount+useppo2.particularcount)/(useppo.generalcount+useppo2.generalcount))
    # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
    # useoscillator.NegativeOS_Day(day, stocklist1)




# from strategy import *
# import matplotlib.pyplot as plt
# import math
# import numpy as np
# import pandas as pd
#
# useppo = UsePPO('코스닥150!')
# # useoscillator = UseOSCILLATOR('코스닥150!')
# kospibasket = useppo.kospibasket
# count = 0
# daypercentcount = 0
# daypercentsum = 0
# graphcount = 0
# garo = []
# sero = []
# garoserodic = {}
# daypercentcount2 = 0
# daypercentsum2 = 0
# graphcount2 = 0
# garo2 = []
# sero2 = []
# garolist = []
# garoserodic2 = {}
# for day in range(len(kospibasket)):
#     count += 1
#     if day < 1300:
#         continue
#     beforemonth = kospibasket[day - 30][0]  # 최초는 20일, 30일 86.5 %
#     yesterday = kospibasket[day - 1][0]
#     todaydate = kospibasket[day][0]
#     stocklist = useppo.CheckStrogStock(beforemonth, yesterday, 2)
#     graphdate = str(int(kospibasket[day][0]))[2:]
#     daypercent = useppo.MackoverlapPPO(day, 5, stocklist)
#     print(todaydate, count)
#     if daypercent != 1:
#
#         graphcount += 1
#         daypercentsum += daypercent
#         if graphcount % 1 == 0:
#             try:
#                 daypercentsum = daypercentsum / 1
#             except ZeroDivisionError:
#                 daypercentsum = 0
#             garo.append(graphdate)
#             sero.append(daypercentsum)
#             garoserodic[graphdate] = daypercentsum
#             result = sorted(garoserodic.items(), key=lambda x: x[1])
#             try:
#                 garolist = [result[i][0] for i in range(0, 6)]
#             except IndexError:
#                 garolist = [result[0][0]]
#             plt.scatter(garo, sero, s=10, color="red")
#             plt.plot(garo, sero, linestyle="solid", color="red")
#             daypercentsum = 0
#
#     beforemonth2 = kospibasket[day - 60][0]  # 최초는 20일, 30일 86.5 %
#     stocklist2 = useppo.CheckStrogStock(beforemonth2, yesterday, 2)
#     daypercent2 = useppo.MackoverlapPPO(day, 5, stocklist2)
#     print("60일-------", todaydate, count)
#     if count % 500 == 0:
#         plt.show()
#     if daypercent2 == 1:
#         continue
#     graphcount2 += 1
#     daypercentsum2 += daypercent2
#     if graphcount2 % 1 == 0:
#         try:
#             daypercentsum2 = daypercentsum2 / 1
#         except ZeroDivisionError:
#             daypercentsum2 = 0
#         garo2.append(graphdate)
#         sero2.append(daypercentsum2)
#         garoserodic2[graphdate] = daypercentsum2
#         result2 = sorted(garoserodic2.items(), key=lambda x: x[1])
#         try:
#             garolist2 = [result2[i][0] for i in range(0, 6)]
#         except IndexError:
#             garolist2 = [result2[0][0]]
#         plt.scatter(garo2, sero2, s=10, color="blue")
#         plt.plot(garo2, sero2, linestyle="solid", color="blue")
#         plt.xticks(garolist + garolist2, rotation=45)
#         daypercentsum2 = 0
#     # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
#     # useoscillator.NegativeOS_Day(day, stocklist1)
