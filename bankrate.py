from flask import Flask, render_template, request, url_for
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from flask_paginate import Pagination,get_page_parameter

app = Flask(__name__)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
curr_name = {
    '美元': '美金 USD', '港幣': '港幣 HKD', '英鎊': '英鎊 GBP', '澳幣': '澳幣 AUD',
    '加拿大幣': '加拿大幣 CAD', '新加坡幣': '新加坡幣 SGD', '瑞士法郎': '瑞士法郎 CHF',
    '日圓': '日圓 JPY', '南非幣': '南非幣 ZAR', '瑞典幣': '瑞典幣 SEK', '紐元': '紐元 NZD',
    '泰幣': '泰幣 THB', '菲國比索': '菲國比索 PHP', '印尼幣': '印尼幣 IDR', '歐元': '歐元 EUR',
    '韓元': '韓元 KRW', '越南盾': '越南盾 VND', '馬來幣': '馬來幣 MYR', '人民幣': '人民幣 CNY'
}

currency_to_search_default = '美元'

def TW_exchange_rate():
        url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(3)
        data = driver.page_source
        driver.close()
        soup = BeautifulSoup(data, 'html.parser')
        rate = soup.find('table').find('tbody').find_all('tr')
        rates = []
        print('台灣銀行:')
        for row in rate:
            currency = row.find('div', {'class': 'hidden-phone print_show xrt-cur-indent'}).text.strip().replace('(', '').replace(')', '').replace('美金 USD', '美元 USD')
            tds = row.find_all('td')
            result = {}                
            result['currency'] = currency
            result['cashbuy'] = tds[1].text.strip()
            result['cashsell'] = tds[2].text.strip()
            result['spotbuy'] = tds[3].text.strip()
            result['spotsell'] = tds[4].text.strip()                
            rates.append(result)

        return rates

           
   
def CTA_exchange_rate():
        url = 'https://www.cotabank.com.tw/web/interest_3/'
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(3)
        data = driver.page_source
        driver.close()
        soup = BeautifulSoup(data, 'html.parser')
        rate = soup.find('div', {'class': 'scrollbox'})
        tbody = rate.find('tbody')
        trs = tbody.find_all('tr')[2:]
        rates = []
        print('三信商銀:')
        for row in trs:
            tds = row.find_all('td')
            currency = tds[0].text.strip().replace('美元USD', '美元 USD').replace('日圓JPY', '日圓 JPY').replace('人民幣CNY', '人民幣 CNY').replace(
                '港幣HKD', '港幣 HKD').replace('歐元EUR', '歐元 EUR').replace('英鎊GBP', '英鎊 GBP').replace('加幣CAD', '加拿大幣 CAD').replace(
                '瑞郎CHF', '瑞士法郎 CHF').replace('澳幣AUD', '澳幣 AUD').replace('紐元NZD', '紐元 NZD').replace('新幣SGD', '新加坡幣 SGD').replace(
                '泰銖THB', '泰幣 THB').replace('菲國比索PHP', '菲國比索 PHP').replace('印尼幣IDR', '印尼幣 IDR').replace('馬來幣MYR', '馬來幣 MYR').replace(
                '韓元KRW', '韓元 KRW').replace('越南盾VND', '越南盾 VND').replace('南非幣ZAR', '南非幣 ZAR')
            result = {}                
            result['currency'] = currency
            result['cashbuy'] = tds[3].text.strip()
            result['cashsell'] = tds[4].text.strip()
            result['spotbuy'] = tds[1].text.strip()
            result['spotsell'] = tds[2].text.strip()
            rates.append(result)

        return rates

    

def TCB_exchange_rate():
        url = 'https://rate.tcbbank.com.tw/CIB/cb5/cb501014/CB501014_01.faces'
        driver = webdriver.Chrome()
        driver.get(url)
        driver.implicitly_wait(3)
        data = driver.page_source
        driver.close()
        data = requests.get(url, headers=header).text
        soup = BeautifulSoup(data, 'html.parser')
        rate = soup.find(id='datagrid_DataGridBody')
        tbody_in_tr = rate.find('tr', {'class': 'hd1'})
        tr_in_th = tbody_in_tr.find_all('th', {'class': 'hd1'})
        ratedata = rate.find_all('tr')[1:]
        rates = []
        print('台中商銀:')
        for row in ratedata:
            tds = row.find_all('td', {'class': 'lt'})
            currency = tds[0].text.strip().replace('美金 USD', '美元 USD').replace('港幣 HKD', '港幣 HKD').replace('英鎊 GBP', '英鎊 GBP').replace(
                '澳幣 AUD', '澳幣 AUD').replace('加拿大幣 CAD', '加拿大幣 CAD').replace('新加坡幣 SGD', '新加坡幣 SGD').replace('瑞士法郎 CHF', '瑞士法郎 CHF').replace(
                '日圓 JPY', '日圓 JPY').replace('南非幣ZAR', '南非幣 ZAR').replace('瑞典幣 CHF', '瑞士法郎 CHF').replace('紐西蘭幣 NZD', '紐元 NZD').replace(
                '歐元 EUR', '歐元 EUR').replace('人民幣 CNY', '人民幣 CNY')
            tds1 = row.find_all('td', {'class': 'rt'})
            result = {}                
            result['currency'] = currency
            result['cashbuy'] = tds1[0].text
            result['cashsell'] = tds1[1].text
            result['spotbuy'] =tds1[2].text
            result['spotsell'] = tds1[3].text
            rates.append(result)

        return rates
    