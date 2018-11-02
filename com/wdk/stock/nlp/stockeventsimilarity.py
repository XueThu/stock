#coding: utf-8
import os
import requests
import json
from com.wdk.stock.nlp.myconfigtextcomputation import access_token

"""
def sentence_similarity(title) :
    title_similarityscore = {}
    txt = {'text_1':'用友网络股票大涨', 'text_2':title}
    url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?'\
       + 'access_token='+access_token
    response = requests.post(url, json.dumps(txt))
    score = json.loads(response.text)["score"]
    return title_similarityscore.update({title:score})
"""

new_title = "浦发分行行长非法集资获刑12年 原浙商证券副总被查"    
LIMIT_NUM = 200
LIMIT_SCORE = 0.4
file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/sinastocknews/'
num = 0
title_similarityscore = {}
for file_name in sorted(os.listdir(file_path)):
    if file_name.endswith('.csv'):
        file_path_name = file_path + file_name
        with open(file_path_name, 'r', encoding="utf-8") as f:
            for line in f.readlines():
                hisory_title = line.split("||||")[2]
                num += 1
                txt = {'text_1':new_title, 'text_2':hisory_title}
                url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/simnet?'\
                        + 'access_token='+access_token
                response = requests.post(url, json.dumps(txt))
                score = json.loads(response.text)["score"]
                if num > LIMIT_NUM :
                    break
                if score > LIMIT_SCORE :
                    title_similarityscore.update({hisory_title:score}) 
#                     print(str(num)+ " Score: " +str(score) + " "+hisory_title)
                
tmp_list = sorted(title_similarityscore.items(),key = lambda x:x[1], reverse=True)        
for tmp in tmp_list :
    print(tmp)
