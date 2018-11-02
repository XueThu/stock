# coding=utf-8
import os

from sklearn.feature_extraction.text import TfidfVectorizer
# from com.wdk.stock.nlp.baiketoken import baike_contents

train_texts = []
file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/traindata/baiketoken/'
file_num = 0
token_num = 0

search_enterprise = "TCL"
search_enterprise_fileNum = 0
enterprise_token_type_weights = {"instance":10, "concept":1}
enterprise_token_key_value = {}

#Start：把每个企业的token分别放入enterprise_token_key_value里，key是企业名
for file_name in sorted(os.listdir(file_path)):
    with open(file_path+file_name, 'r', encoding="utf-8") as f:
        enterprise_name = file_name.split('.')[0]#去掉后、
#         print(enterprise_name)
        enterprise_token_type = file_name.split('.')[len(file_name.split('.'))-1] #只留后缀
#         print(enterprise_token_type)
        enterprise_token = ""
        tmp_tokens = f.read()
        tmp_tokens.encode('gbk', errors='ignore').decode('gbk')
        for i in range(0, enterprise_token_type_weights[enterprise_token_type]) :
            enterprise_token += tmp_tokens 
        if enterprise_token_key_value.get(enterprise_name) != None :
            enterprise_token += enterprise_token_key_value.get(enterprise_name)
        enterprise_token_key_value.update({enterprise_name:enterprise_token})
        file_num += 1
# End：把每个企业的token分别放入enterprise_token_key_value里，key是企业名

search_enterprise_fullname = ""
enterprise_num = 0
search_enterprise_num = 0
for key in enterprise_token_key_value.keys():
    train_texts.append(enterprise_token_key_value.get(key))
    print("%d: %d, %s" %(enterprise_num,len(enterprise_token_key_value.get(key)),key) )
    if search_enterprise in key:
        search_enterprise_num = enterprise_num
        search_enterprise_fullname = key
    enterprise_num += 1

print(search_enterprise)
print(search_enterprise_num)
# print(train_texts[3])   


vectorizer = TfidfVectorizer()
tmp_dict = {}
# Learn vocabulary from training texts and vectorize training texts.
x_train = vectorizer.fit_transform(train_texts)
feature = vectorizer.get_feature_names()
print(x_train.shape)

SimMatrix = (x_train * x_train.T).A
print(SimMatrix[1,3])


#search tf-idf of specified enterprise
doc_terms = x_train[search_enterprise_num].toarray()[0]
for i in range(0,len(doc_terms)):
    if doc_terms[i] != 0 :
        tmp_dict[feature[i]] =  doc_terms[i]
#         print("%d,: %s, %f" % (i,feature[i],doc_terms[i]))
print(len(doc_terms))
print(len(tmp_dict))


tmp_list = sorted(tmp_dict.items(),key = lambda x:x[1], reverse=True)        

if search_enterprise_fullname == "" : 
    print(search_enterprise+"可能不在A股或H股")
else:
    for tmp in tmp_list :
        print(tmp)



