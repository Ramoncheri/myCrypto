from requests import Request, Session
import json
from the_app import app

def convert(symbol_from):
    url= 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?'

    parameters = {
    'amount': '1',
    'symbol': symbol_from,
    'convert': 'EUR'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': app.config['SECRET_KEY'],
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    data = response.json()
    lista= (data['data'])
    quote= lista['quote']
    price= quote['EUR']['price']
    print( price)
    return price
    

def lista_criptos():
    from requests import Request, Session
    import json

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?'
    
    parameters = {
    'start':'1',
    'limit':'10',
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '41399db7-0249-4a2a-bc68-8bca943b5337',
    'symbol': 'BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,B SV,XLM,ADA,TRX'
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    data = response.json()
    lista= (data['data'])
    for dicc in lista:
        print (dicc['name'], dicc['symbol'])
    