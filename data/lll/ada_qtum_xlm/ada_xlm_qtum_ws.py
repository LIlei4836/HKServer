from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            currency=Currency()
            currency.name=name
            # currency.name2 = paramDict[name][0]
            # currency.projectName = paramDict[name][1]
            # currency.riskUrl = riskManageUrl+paramDict[name][2]
            # currency.sub_bian()
            # currency.sub_ok()
            currency.sub_huobi()
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['ada','xlm','qtum']
# currency_list=['eos']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


