from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            currency=Currency()
            currency.name=name
            currency.sub_bian()
            # currency.sub_ok()
            # currency.sub_huobi()
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=[['BNB']]
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency[0],))
    t1.start()
    print(currency[0], 'ok')
t1.join()


