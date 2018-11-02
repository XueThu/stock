#coding: utf-8

from com.wdk.stock.nlp.myconfig import bd_client 
file_name = "news"
with open(file_name, 'r', encoding="utf-8") as f:
    content = f.read().encode('gbk', errors='ignore').decode('gbk')
title = "用友公司"
res = bd_client.keyword(title, content)
for item in res["items"]:
    print(item)
    
"""    
#3 文章分类
res = client.topic(title, content);
for item in res["item"]:
        print json.dumps(item, ensure_ascii=False)
"""