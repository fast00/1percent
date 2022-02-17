from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import datetime
import time



header = {'Connection': 'keep-alive',
            'Expires': '-1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
            }

result = {}
https = "https://finance.naver.com"
for page in range(1,8):
    response = requests.get(f'https://finance.naver.com/sise/theme.naver?&page={page}') #테마 목록
    soup = BeautifulSoup(response.content.decode('euc-kr','replace'), "lxml")
    theme = soup.findAll('td','col_type1')
    for i in range(len(theme)):
        themename = theme[i].select("a")[0].text
        print(themename)
        address = str(theme[i].select("a")[0]["href"])
        address = https + address
        print(address)

        response = requests.get(address)  #종목 목록
        soup = BeautifulSoup(response.content.decode('euc-kr','replace'), "lxml")
        stockname = soup.findAll('div', 'name_area')
        stocklist = []
        for k in range(len(stockname)):
            stockcode = stockname[k].select("a")[0]["href"][-6:]
            stockcode = "A"+stockcode
            stocklist.append(stockcode)
        result[themename] = stocklist


print(result)