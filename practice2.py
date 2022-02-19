from strategy import *
from matplotlib import pyplot as plt
import pandas as pd


useppo = UsePPO()
# useoscillator = UseOSCILLATOR()
kospibasket = useppo.kospibasket
count = 0
graphcount = 0
garo = []
sero = []
for day in range(len(kospibasket)):
    count += 1
    graphcount += 1
    if day < 400:
        continue
    beforemonth = kospibasket[day - 20][0]
    yesterday = kospibasket[day - 1][0]
    todaydate = kospibasket[day][0]
    stocklist1 = useppo.CheckStrogStock(beforemonth, yesterday, 2)
    graphdate = str(int(kospibasket[day][0]))
    print(todaydate, count)
    garo.append(graphdate)
    sero.append(useppo.MackoverlapPPO(day, 5, stocklist1))  # 여기에 할당해서 밑에 대입해야함
    df = pd.DataFrame({
        'DATE': garo,
        'AMOUNT': sero
    })
    xs = df['DATE'].to_list()
    xlabels = df['DATE'].apply(lambda x: x[2:]).to_list()
    ys = df['AMOUNT'].to_list()
    plt.plot(xs, ys)
    plt.xticks(ticks=xs, labels=xlabels, rotation=45)
    plt.locator_params(axis='x', nbins=int(len(xlabels) / 30))
    # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
    # useoscillator.NegativeOS_Day(day, stocklist1)

    if graphcount % 100 == 0:
        plt.show()

