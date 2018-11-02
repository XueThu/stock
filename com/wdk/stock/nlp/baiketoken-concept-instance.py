# coding=utf-8

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from com.wdk.stock.nlp.myconfig import bd_client

content = []
file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/traindata/'
file_num = 1

for file_name in sorted(os.listdir(file_path +"baikeweb/")):
    if file_name.endswith('.json'):
        baike_file_path_name = file_path +"baikeweb/"+ file_name
        concetp_path_file_name = file_path + "baiketoken/" + file_name+".concept"
        instance_path_file_name = file_path + "baiketoken/" + file_name+".instance"
        # If failures happened, it can start from the breakpoint, check the last file, it may be 0 bytes
        if os.path.exists(concetp_path_file_name and instance_path_file_name) and \
            os.path.getsize(concetp_path_file_name) != 0 and \
            os.path.getsize(instance_path_file_name) != 0:
            
            file_num += 1
            continue
        # End
        else :
            
            concept_file = open(concetp_path_file_name, 'a', encoding="utf-8")
            instance_file = open(instance_path_file_name, 'a', encoding="utf-8")
            baike_content_concept = ""
            baike_content_instance = ""
            
            with open(baike_file_path_name, 'r', encoding="utf-8" ) as f:
                baike_content_tokens = ''
                baike_content = f.read()
                baike_content = baike_content.encode('gbk', errors='ignore').decode('gbk')
                #Since BaiduAI has limit on the length of lexer, the big file will be split into blocks.
                FILE_BLOCK = 5000
                for i in range(0, int(len(baike_content)/FILE_BLOCK)+1):
                    if (i == len(baike_content)/FILE_BLOCK):
                        baike_content_lexer = bd_client.lexer( baike_content[i*FILE_BLOCK:len(baike_content)] )
                        for item in baike_content_lexer["items"]:
                            if item["pos"] == "n" :
                                baike_content_concept += item["item"]+" "
                            elif item["pos"] == "nr" or \
                                 item["ne"] == "ORG"or item["pos"] == "nt" or \
                                item["pos"] == "nw" or item["pos"] == "nz" or \
                                item["ne"] == "PER" :
                                baike_content_instance += item["item"]+" "   
                           
                    else:
                        baike_content_lexer = bd_client.lexer( baike_content[i*FILE_BLOCK:(i+1)*FILE_BLOCK-1] )
                        for item in baike_content_lexer["items"]:
                            if item["pos"] == "n" :
                                baike_content_concept += item["item"]+" "
                            elif item["pos"] == "nr" or \
                                 item["ne"] == "ORG"or item["pos"] == "nt" or \
                                item["pos"] == "nw" or item["pos"] == "nz" or \
                                item["ne"] == "PER":
                                baike_content_instance += item["item"]+" "
                                
            concept_file.write(baike_content_concept)
            concept_file.close()
            instance_file.write(baike_content_instance)
            instance_file.close()
            file_num += 1
            
            print("%d: %s" %(file_num,file_name) )
           
