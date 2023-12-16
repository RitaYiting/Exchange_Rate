# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:40:12 2023

@author: User
"""

from flask import Flask, render_template, request        #render_template 子分頁的內容嵌入母頁的特定區域
from flask_paginate import Pagination, get_page_parameter
from bankrate import TW_exchange_rate, CTA_exchange_rate, TCB_exchange_rate

#建立一個flask的應用程式
app = Flask(__name__)

#定義一個全域變數來儲存選擇的幣別,預設是None
selected_currency = None

# 模擬換算比率的資料
conversion_rates = {
    'USD': 30.0,
}

@app.route('/compare', methods=['GET'])
def compare():    
    global selected_currency  #使用全域變數
    tw_rates = TW_exchange_rate()   #台灣銀行匯率,並給一個變數名稱tw_rates
    cta_rates = CTA_exchange_rate() #三信商銀匯率,並給一個變數名稱cta_rates
    tcb_rates = TCB_exchange_rate() #台中商銀匯率,並給一個變數名稱tcb_rates
    return render_template('compare.html', **locals())


#轉換匯率為浮點數的函式設定
def convert_rates_to_float(rates):    
    converted_rates = []
    for rate in rates:
        converted_rate = {
            'currency': rate['currency'],
            'cashbuy': float(rate.get('cashbuy', '------')) if rate.get('cashbuy') not in ['-', '------', '0.00000'] else '-',
            'cashsell': float(rate.get('cashsell', '------')) if rate.get('cashsell') not in ['-', '------', '0.00000'] else '-',
            'spotbuy': float(rate.get('spotbuy', '------')) if rate.get('spotbuy') not in ['-', '------', '0.00000'] else '-',
            'spotsell': float(rate.get('spotsell', '------')) if rate.get('spotsell') not in ['-', '------', '0.00000'] else '-'
            }
        converted_rates.append(converted_rate)
    return converted_rates


def get_conversion_rates(base_currency):
    return conversion_rates


@app.route('/compare_table', methods=['GET'])
def compare_table():
    global selected_currency    #使用全域變數
    tw_rates = convert_rates_to_float(TW_exchange_rate())    #轉換成浮點數後的台灣銀行匯率,並給一個變數名稱tw_rates
    cta_rates = convert_rates_to_float(CTA_exchange_rate())  #轉換成浮點數後的三信商銀匯率,並給一個變數名稱cta_rates
    tcb_rates = convert_rates_to_float(TCB_exchange_rate())  #轉換成浮點數後的台中商銀匯率,並給一個變數名稱tcb_rates

    #取得使用者選擇的幣別，還未選擇前，幣別預設為美元。
    selected_currency = request.args.get('currency') or "美元" 
    
    filtered_tw_rates = [rate for rate in tw_rates if selected_currency in rate['currency']]
    filtered_cta_rates = [rate for rate in cta_rates if selected_currency in rate['currency']]
    filtered_tcb_rates = [rate for rate in tcb_rates if selected_currency in rate['currency']]
    cashsells = [float(rate['cashsell']) for rate in filtered_tw_rates + filtered_cta_rates + filtered_tcb_rates if rate['cashsell'] not in ['-', '------' ,'0.00000']]
    min_cashsell = min(cashsells) if cashsells else None
    conversion_rates_data = get_conversion_rates(selected_currency)
   
    return render_template('compare_table.html', 
                           filtered_tw_rates = filtered_tw_rates, 
                           filtered_cta_rates = filtered_cta_rates, 
                           filtered_tcb_rates = filtered_tcb_rates, 
                           selected_currency = selected_currency,
                           min_cashsell = min_cashsell,
                           conversion_rates=conversion_rates_data)
                            
@app.route('/')
def index():             
    return render_template('Base.html',**locals())


if __name__ == '__main__':
    app.run()
