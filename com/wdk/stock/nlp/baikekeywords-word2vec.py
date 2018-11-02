#用word2vec建立起来的相似度更倾向于同类分类，比如“王文京”的相似词Top20几乎全部是企业家，研究一下实现机理

# coding=utf-8
import os
from com.wdk.stock.nlp.myconfig import bd_client
from gensim.models import word2vec
import gensim

file_path = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/traindata/'
file_num = 0
FILE_NUM_LIMIT = 10000
token_corpus = []
for file_name in sorted(os.listdir(file_path)):
    if file_name.endswith('.token'):
        file_path_name = file_path + file_name
        with open(file_path_name, 'r', encoding="utf-8" ) as f:
            if file_num > FILE_NUM_LIMIT-1 :
                break
            file_num += 1
            token = f.read()
            token_corpus.append( token.split(' ') )
#             print(str(file_num)+": "+str(len(token_corpus)))
print(len(token_corpus))

save_model_file = file_path+"word2vec.model"
model = gensim.models.Word2Vec(token_corpus, size=300, window=3, min_count=0, workers=4)  # 训练skip-gram模型; 默认window=5
model.save(save_model_file)
# print( model.most_similar(positive = "TCL",topn = 100) )
# print(model.similarity("企业管理", "用友"))
print(model.similar_by_word("王文京", topn=100, restrict_vocab=None))

"""
# 加载已训练好的模型
model_test = word2vec.Word2Vec.load(save_model_file)
# 计算两个词的相似度/相关程度
# y1 = model_test.similarity(u"263", u"企业管理")
# print("相似度为："+ str(y1))
model_test.most_similar('tcl',topn = 360)
"""

