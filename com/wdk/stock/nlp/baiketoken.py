# coding=utf-8

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from com.wdk.stock.nlp.myconfig import bd_client

contents = []
file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/traindata/'
file_num = 1

for file_name in sorted(os.listdir(file_path +"baikeweb/")):
    if file_name.endswith('.json'):
        baike_file_path_name = file_path +"baikeweb/"+ file_name
        token_file_path_name = file_path + "baiketoken/" + file_name+".token"
        if os.path.exists(token_file_path_name):
            print (token_file_path_name)
            file_num += 1
            continue
        else :
            token_file = open(token_file_path_name, 'a', encoding="utf-8")
            with open(baike_file_path_name, 'r', encoding="utf-8" ) as f:
                baike_contents_tokens = ''
                baike_contents = f.read()
                baike_contents = baike_contents.encode('gbk', errors='ignore').decode('gbk')
                file_block = 5000
                for i in range(0, int(len(baike_contents)/file_block)+1):
                    if (i == len(baike_contents)/file_block):
                        baike_contents_lexer = bd_client.lexer( baike_contents[i*file_block:len(baike_contents)] )
                        for item in baike_contents_lexer["items"]:
                            if item["pos"] == "n" or item["ne"] == "ORG":
                                baike_contents_tokens += item["item"]+" "
                    else:
                        baike_contents_lexer = bd_client.lexer( baike_contents[i*file_block:(i+1)*file_block-1] )
                        for item in baike_contents_lexer["items"]:
                            if item["pos"] == "n" or item["pos"] == "nr" or \
                                item["pos"] == "ns" or item["pos"] == "nt" or \
                                item["pos"] == "nw" or item["pos"] == "nz" or \
                                item["ne"] == "PER" or item["ne"] == "LOC" or \
                                item["ne"] == "ORG":
                                baike_contents_tokens += item["item"]+" "
                print("%d: %s" %(file_num,file_name) )
    #             print(baike_contents_tokens)
                file_num += 1
                token_file.write(baike_contents_tokens)
                token_file.close()            

