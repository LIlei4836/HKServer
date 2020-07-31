# -*- coding=utf-8  -*-
# @Time: 2020/6/10 14:24
# @Author: LeiLei Li
# @File: test.py


import requests

url = 'http://www.qkljiaoyisuo.top/api/system/getFkData?coinName=WTH'

html = requests.get(url)
print(html.status_code)
