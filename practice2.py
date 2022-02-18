from strategy import *
from matplotlib import pyplot as plt
useppo = UsePPO()
useoscillator = UseOSCILLATOR()
kospibasket = useoscillator.kospibasket
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
    stocklist1 = useoscillator.CheckStrogStock(beforemonth, yesterday, 2)
    graphdate = str(kospibasket[day][0])
    print(todaydate, count)
    garo.append(graphdate)
    sero.append(useppo.MackoverlapPPO(day, 5, stocklist1))  # 여기에 할당해서 밑에 대입해야함
    plt.plot(garo, sero)


    # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
    # useoscillator.NegativeOS_Day(day, stocklist1)

    if graphcount % 100 == 0:
        plt.show()

