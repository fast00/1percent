from strategy import *
from matplotlib import pyplot as plt
useppo = UsePPO()
useoscillator = UseOSCILLATOR()
kospibasket = useoscillator.kospibasket
count = 0
count2 = 0
garo = []
sero = []
for day in range(len(kospibasket)):
    count += 1
    count2 += 1
    if day < 400:
        continue
    beforemonth = kospibasket[day - 20][0]
    yesterday = kospibasket[day - 1][0]
    todaydate = kospibasket[day][0]
    todaydate2 = str(kospibasket[day][0])
    print(todaydate, count)
    stocklist1 = useoscillator.CheckStrogStock(beforemonth, yesterday, 2)
    # useoscillator.PositiveOS_Day(day, yesterday, stocklist1)
    # useoscillator.NegativeOS_Day(day, stocklist1)
    garo.append(todaydate2)
    sero.append(useppo.MackoverlapPPO(day, 5, stocklist1))  # 여기에 할당해서 밑에 대입해야함
    plt.plot(garo, sero)
    if count2 % 100 == 0:
        plt.show()




