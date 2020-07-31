from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            currency=Currency()
            currency.name=name
            currency.sub_bian()
            #  currency.sub_ok()
            # currency.sub_huobi(100)
        except Exception as e:
            print(e)
        time.sleep(10)



# currency_list=['BTC','LTC','ETH','EOS','XRP','BCH','BSV','ETC','ZEC','ATOM','DASH','TRX','XMR']
currency_list=['BTC','LTC','ETH','EOS','ETC','BCH']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


