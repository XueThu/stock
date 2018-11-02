#coding: utf-8

import requests
import json
from com.wdk.stock.nlp.myconfigtextcomputation import access_token

txt = {'text':'五道口学院越办越好'} #只有13个行业可用，否则返回错误
header = {'content-type': 'application/json'}

url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?'\
       + 'access_token='+access_token
print(url)
# response = requests.post(url, json.dumps(txt),header)
# response = requests.post(url=url, data=json.dumps(txt),headers=header)
response = requests.post(url, json.dumps(txt))#上述两种表达亦可

# 返回结果中，sentiment表示：该情感搭配的极性（0表示消极，1表示中性，2表示积极）
print(response.text)