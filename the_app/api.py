import requests
import json
from the_app import app


API_KEY= app.config['API_KEY']

def convert(symbol_from, amount='1', converTo='EUR'):
    url= 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'
    URL= url.format(amount, symbol_from,converTo, API_KEY )
    
    response = requests.get(URL)
    
    data = response.json()
    try:
        lista= (data['data'])
        quote= lista['quote']
        price= quote[converTo]['price']

        return price
    except:
        error = response.reason
        return error
   
        
   
    


    