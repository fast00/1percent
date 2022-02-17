from matplotlib import pyplot as plt
import win32com.client
from main2lib import *
# from tqdm import tqdm
#
# 코스피 200 (180)
# 코스닥 150 (390)

Connect()
#
# marketinfo = MarketInfo('U001')
# info = marketinfo.GetstockPeriodInfo(3300)
# f = open("C:\\Users\\82104\\Desktop\\코스피200!\\코스피지수.txt", 'a+', encoding='utf-8')
# f.write(str(info))
# f.close()
#
# marketinfo = MarketInfo('U201')
# info = marketinfo.GetstockPeriodInfo(3300)
# f = open("C:\\Users\\82104\\Desktop\\코스닥150!\\코스닥지수.txt", 'a+', encoding='utf-8')
# f.write(str(info))
# f.close()

#
# for i in range(5):
#     plt.plot(["a","b"], [3,4])
#     plt.show(block=False)
#     plt.pause(1)
#     plt.close()