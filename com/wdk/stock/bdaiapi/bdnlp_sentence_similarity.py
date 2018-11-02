#coding: utf-8

import requests
import json
from com.wdk.stock.nlp.myconfigtextcomputation import access_token

txt = {'text_1':'资本助力软件板块走强 机构看好', 'text_2':'机构扎堆看好7只龙头股'}
header = {'content-type': 'application/json'}

url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?'\
       + 'access_token='+access_token
print(url)
# response = requests.post(url, json.dumps(txt),header)
# response = requests.post(url=url, data=json.dumps(txt),headers=header)
response = requests.post(url, json.dumps(txt))#上述两种表达亦可
result = response.text
print(result)
print(json.loads(result)["score"])