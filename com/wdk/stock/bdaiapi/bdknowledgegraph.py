#coding: utf-8

import requests
import json
from com.wdk.stock.nlp.myconfigtextcomputation import access_token
txt ="　当然，还应该关注到不同群体的消费意愿差异，更精准地调节以激活消费能力。客观地说，这些年来，因房价上涨导致的家庭杠杆率上升对消费有一定的挤出效应；而一些（准备）生二孩的家庭也可能倾向“勒紧裤腰带”，对某些领域的消费从长计议。"
postdata = {"data":txt}
header = 'content-type: application/json'
# postdata = urldata.encode('latin-1', 'ignore')

url = 'https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/entity_annotation?'\
       + 'access_token='+access_token
#urlheaders = 'content-type: application/json'
print(url)


response = requests.post(url,data=json.dumps(postdata))
print(response.text)