from strategy import *
from matplotlib import pyplot as plt
import pandas as pd


useppo = UsePPO('코스닥150!')
# useoscillator = UseOSCILLATOR('코스닥150!')
kospibasket = useppo.kospibasket
count = 0
daypercentcount = 0
daypercentsum = 0
graphcount = 0
garo = []
sero = []
dic = {}
for count1 in range(3, 15):
    useppo = UsePPO('코스닥150!')
    kospibasket = useppo.kospibasket
    for day in range(len(kospibasket)):
        count += 1
        if day < 300 or day > 1500:
            continue
        beforemonth = kospibasket[day - 20][0]
        yesterday = kospibasket[day - 1][0]
        todaydate = kospibasket[day][0]
        stocklist1 = useppo.CheckStrogStock(beforemonth, yesterday, 2)
        graphdate = str(int(kospibasket[day][0]))
        daypercent = useppo.MackoverlapPPO(day, 5, stocklist1, count1)
        print(todaydate, count)
    count = 0
    try:
        dic[count1] = round(useppo.particularcount / useppo.generalcount,4)
    except ZeroDivisionError:
        pass
    print(dic)
        # if daypercent == 1:
        #     continue
        # graphcount += 1
        # daypercentsum += daypercent
        # if graphcount % 10 == 0:
        #     try:
        #         daypercent = round(daypercentsum / 10)
        #     except ZeroDivisionError:
        #         daypercent = 0
        #     garo.append(graphdate)
        #     sero.append(daypercent)
        #     df = pd.DataFrame({
        #         'DATE': garo,
        #         'AMOUNT': sero
        #     })
        #     xs = df['DATE'].to_list()
        #     xlabels = df['DATE'].apply(lambda x: x[2:]).to_list()
        #     ys = df['AMOUNT'].to_list()
        #     plt.plot(xs, ys)
        #     plt.xticks(ticks=xs, labels=xlabels, rotation=45)
        #     plt.locator_params(axis='x', nbins=int(len(xlabels) / 10))
        #     daypercentsum = 0
        #
         # 여기에 할당해서 밑에 대입해야함
        # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
        # useoscillator.NegativeOS_Day(day, stocklist1)

        # if count % 1000 == 0:
        #     plt.show()

