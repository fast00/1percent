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
for day in range(len(kospibasket)):
    count += 1
    if day < 300:
        continue
    beforemonth = kospibasket[day - 20][0]
    yesterday = kospibasket[day - 1][0]
    todaydate = kospibasket[day][0]
    stocklist1 = useppo.CheckStrogStock(beforemonth, yesterday, 4)
    graphdate = str(int(kospibasket[day][0]))
    daypercent = useppo.MackoverlapPPO(day, 5, stocklist1)
    print(todaydate, count)
    if count % 1000 == 0:
        plt.show()
    if daypercent == 1:
        continue
    graphcount += 1
    daypercentsum += daypercent
    if graphcount % 10 == 0:
        try:
            daypercentsum = daypercentsum / 10
        except ZeroDivisionError:
            daypercentsum = 0
        garo.append(graphdate)
        sero.append(daypercentsum)
        df = pd.DataFrame({
            'DATE': garo,
            'AMOUNT': sero
        })
        xs = df['DATE'].to_list()
        xlabels = df['DATE'].apply(lambda x: x[2:]).to_list()
        ys = df['AMOUNT'].to_list()
        plt.plot(xs, ys)
        plt.xticks(ticks=xs, labels=xlabels, rotation=45)
        plt.locator_params(axis='x', nbins=int(len(xlabels) / 10))
        daypercentsum = 0

    # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
    # useoscillator.NegativeOS_Day(day, stocklist1)



