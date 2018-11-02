#coding: utf-8

from com.wdk.stock.nlp.myconfig import bd_client 
# file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/traindata/baiketoken/'
# file_name = '科大智能科技股份有限公司.json.concept'
# file_name =file_path + file_name
file_name = "news"

#1 词法分析
baike_content_concept = ""
baike_content_instance = ""
with open(file_name, 'r', encoding="utf-8") as f:
    baike_content = f.read()
    baike_content = baike_content.encode('gbk', errors='ignore').decode('gbk')
    
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

print ("Instance: "+baike_content_instance)
print ("Concept: " + baike_content_concept)
