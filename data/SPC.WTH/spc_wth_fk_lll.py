# -*- coding=utf-8  -*-
# @Time: 2020/6/10 14:31
# @Author: LeiLei Li
# @File: spc_wth_fk_lll.py

from utils import get_html


url = 'http://www.qkljiaoyisuo.top/api/system/getFkData?coinName='



import requests
import redis
import time
import threading
import logging
from utils import get_html


r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0"}


def get_fk(fk,):
    while 1:
        try:
            urlDict = ['http://www.qkljiaoyisuo.top/api/system/getFkData?coinName=', str(fk)]
            url = ''.join(urlDict)

            # print(url)
            response = get_html(url,)
            response = float(response)
            r.set('hlg:spc:' + fk+':riskNum', response)
            # print(response)

        except Exception as e:
            print(e)
            pass
        time.sleep(3)


if __name__ == '__main__':
    fks = {'SPC','WTH'}
    threadlist = []
    for fk in fks:
        t1 = threading.Thread(target=get_fk, args=(fk,))
        threadlist.append(t1)
    for t1 in threadlist:
        t1.start()
    for t1 in threadlist:
        t1.join()