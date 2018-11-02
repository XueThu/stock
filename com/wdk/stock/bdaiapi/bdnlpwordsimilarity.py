#coding: utf-8

import requests
import json
from com.wdk.stock.nlp.myconfigtextcomputation import access_token

txt = {"word_1":"软件", "word_2":"CRM"}
header = {'content-type': 'application/json'}

url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_sim?'\
       + 'access_token='+access_token
print(url)
# response = requests.post(url, json.dumps(txt),header)
# response = requests.post(url=url, data=json.dumps(txt),headers=header)
response = requests.post(url, json.dumps(txt))#上述两种表达亦可

print(response.text)