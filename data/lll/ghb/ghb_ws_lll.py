from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            currency=Currency()
            currency.name=name
            currency.name2='ghb'
            # currency.sub_bian()
            #   currency.sub_ok(k=3)
            currency.sub_huobi(k=3)
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['xrp']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


