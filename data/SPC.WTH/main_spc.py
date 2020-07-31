from core import Currency
from threading import Thread
import time

def sub(name):
    while 1:
        try:
            paramDict = {'HT':['SPC','spc','SPC', 1.88, 0],'ETH':['WTH','spc','WTH', 0.175438, 0]}
            riskManageUrl = 'http://www.qkljiaoyisuo.top/api/system/getFkData?coinName='
            currency=Currency()
            currency.name=name
            currency.name2=paramDict[name][0]
            currency.projectName=paramDict[name][1]
            # currency.riskUrl=riskManageUrl + str(paramDict[name][2])
            # currency.sub_bian(k=paramDict[name][3], b=paramDict[name][4])
            # currency.sub_ok(k=paramDict[name][3], b=paramDict[name][4])
            currency.sub_huobi(k=paramDict[name][3], b=paramDict[name][4])
        except Exception as e:
            print(e)
        time.sleep(10)



currency_list=['HT', 'ETH']
for currency in currency_list:
    t1 = Thread(target=sub,args=(currency,))
    t1.start()
    print(currency, 'ok')
t1.join()


