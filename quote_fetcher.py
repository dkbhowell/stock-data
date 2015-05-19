'''
Created on Dec 9, 2014

@author: Dustin
'''

import csv
import urllib

def get_stock_lists_from_file(ticker_filename):
    ticker_lists = [[]]
    with open(ticker_filename, 'U') as ticker_file:
        reader = csv.DictReader(ticker_file)
        list_count = 0
        for row in reader:
            ticker = row['tickers']
            if len(ticker_lists[list_count]) < 50:
                ticker_lists[list_count].append(ticker)
            else:
                ticker_lists.append([ticker])
                list_count += 1
    return ticker_lists

def convert_market_cap(row_dict):
    market_cap = row_dict['Market cap']
    last_char = market_cap[len(market_cap)-1:]
    if last_char == 'B':
        market_cap = market_cap[:len(market_cap)-1]
        market_cap = float(market_cap) * 1000
    elif last_char == 'M':
        market_cap = market_cap[:len(market_cap)-1]
    row_dict['Market cap'] = market_cap

def get_stock_data(ticker_lists, new_filename):
    fields = 'snl1opb4p2ryj1'
    fieldnames = ['Ticker', 'Name', 'last value', 'Open', 'Previous close', 'Book value per share', 'Change in percent', 'PE ratio', 'Div yield', 'Market cap']
    with open(new_filename, 'wb') as new_file:
        writer = csv.DictWriter(new_file, fieldnames)
        writer.writeheader()
        for list in ticker_lists:
            url = 'http://download.finance.yahoo.com/d/quotes.csv?s='
            for ticker in list:
                url += ticker + ', '
            url = url[:(len(url)-2)]
            url += '&f=' + fields
            url += '&e=.csv'
            response = urllib.urlopen(url)
            reader = csv.DictReader(response, fieldnames)
            for row in reader:
                convert_market_cap(row)
                writer.writerow(row)
        
lists = get_stock_lists_from_file('tickers.csv')
get_stock_data(lists, 'stock_data.csv')

    
