# coding=utf-8
import os

from sklearn.feature_extraction.text import TfidfVectorizer
# from com.wdk.stock.nlp.baiketoken import baike_contents

train_texts = []
file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/traindata/baiketoken/'
file_num = 0
token_num = 0

search_enterprise = "用友"
search_enterprise_fileNum = 0
search_enterprise_fileName =""

for file_name in sorted(os.listdir(file_path)):
    if file_name.endswith('.token'):
#         baike_file_path_name = file_path + file_name     
        token_file_path_name = file_path + file_name
#         print(token_file_path_name)
        with open(token_file_path_name, 'r', encoding="utf-8") as f:
            tokens = f.read()
            tokens = tokens.encode('gbk', errors='ignore').decode('gbk')
            train_texts.append(tokens)
            file_num += 1
            print("%d: %d, %s" %(file_num,len(tokens),file_name) )
            if search_enterprise in file_name:
                search_enterprise_fileNum = file_num
                search_enterprise_fileName = file_name
            token_num += len(tokens)
#         if file_num > 3:
#             break
# print(train_texts[3])   


# """
vectorizer = TfidfVectorizer()
tmp_dict = {}
# Learn vocabulary from training texts and vectorize training texts.
x_train = vectorizer.fit_transform(train_texts)
print(x_train.shape)
print(token_num)
feature = vectorizer.get_feature_names()
doc_terms = x_train[search_enterprise_fileNum-1].toarray()[0]
for i in range(0,len(doc_terms)):
    if doc_terms[i] != 0 :
        tmp_dict[feature[i]] =  doc_terms[i]
#         print("%d,: %s, %f" % (i,feature[i],doc_terms[i]))

tmp_list = sorted(tmp_dict.items(),key = lambda x:x[1], reverse=True)        
if search_enterprise_fileName == "": 
    print(search_enterprise + "可能不在A股或H股")
else:
    for tmp in tmp_list :
        print(tmp)

# """

"""
token_collection_file = open("/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/astock/token/token_collection", 'a', encoding="utf-8")
token_collection_file.write(str(feature))
token_collection_file.close()
"""
