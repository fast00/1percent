from matplotlib import pyplot as plt
from main2lib import *
# import win32com.client
# from main2lib import *
# from tqdm import tqdm
#
# 코스피 200 (180)
# 코스닥 150 (390)

# Connect()
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

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
code = []
for page in range(6,31):
    url = f"https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find_all("a")
        volum = soup.find_all("")
        for i in tag:
            if "href=\"/item/main.naver?code=" in str(i):
                code.append("A" + i["href"].strip("href=\"/item/main.naver?code="))
print(len(code))
clearcode = []
Connect()
g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
for i in tqdm(code):
    objStockChart.SetInputValue(0, str(i))
    objStockChart.SetInputValue(1, ord('2'))  # 개수로 조회
    objStockChart.SetInputValue(4, 10)  # 최근 10일 치
    objStockChart.SetInputValue(5, [8])  # 날짜,시가,고가,저가,종가,거래량
    objStockChart.SetInputValue(6, ord('D'))  # '차트 주가 - 일간 차트 요청
    objStockChart.SetInputValue(9, ord('1'))  # 수정주가 사용
    objStockChart.BlockRequest()
    GetLimitTime()
    len = objStockChart.GetHeaderValue(3)
    volumesum = 0
    for k in range(len):
        volume = objStockChart.GetDataValue(0, k)
        volumesum += volume
    if g_objCodeMgr.GetStockSectionKind(i) == 1 and volumesum/10 >= 2000000:
        clearcode.append(i)
for i in clearcode:
    marketinfo = MarketInfo(i)
    basket = marketinfo.GetstockPeriodInfo(2000)
    f = open(f"C:\\주가정보\\동전주\\{i}.txt", 'w', encoding='utf-8')
    f.write(str(basket))
    f.close()

f = open(f"C:\\주가정보\\동전주\\codelist.txt", 'w', encoding='utf-8')
f.write(str(clearcode))
f.close()