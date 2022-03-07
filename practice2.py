from strategy import *
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
def refresh():
    Connect()
    file = FileMethods2()
    file.save_Info(1000)  # 매일 실행
    return True
# refresh()
useppo = UsePPO("코스피200!")
useppo2 = UsePPO("코스닥150!")
kospibasket = useppo.kospibasket
count = 0
graphcount = 0
garo = []
sero = []
for day in range(len(kospibasket)):
    if day < 400:
        continue
    beforemonth = kospibasket[day - 30][0]
    yesterday = kospibasket[day - 1][0]
    todaydate = kospibasket[day][0]
    print(todaydate)
    stocklist = useppo.CheckStrogStock(beforemonth, yesterday, 2)
    stocklist2 = useppo2.CheckStrogStock(beforemonth, yesterday, 2)
    qospi = useppo.MackoverlapPPO(day, 5, stocklist)  # 여기에 할당해서 밑에 대입해야함
    qosdaq = useppo2.MackoverlapPPO(day, 5, stocklist2)  # 여기에 할당해서 밑에 대입해야함
    print(qosdaq,qospi)

