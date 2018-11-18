#coding: utf-8
import datetime
import requests
import json
from com.wdk.stock.nlp.myconfigtextcomputation import access_token

starttime = datetime.datetime.now()
text2 = '用友持股最多的股东是谁'
text3 = '金蝶持股最多的股东是谁'
text4 = '用友今天股价是多少'
text5 = '王文京多少身价'
text6 = '刘德华有多帅'



txt = {'text_1':'用友的股东是谁', 'text_2' : text5}
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

endtime = datetime.datetime.now()
print(endtime-starttime)