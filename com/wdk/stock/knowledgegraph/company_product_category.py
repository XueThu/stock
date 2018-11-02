#coding: utf-8
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher
import re


import xlrd

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")

file_name = '上市公司产品类型和名称.xlsx'
workbook = xlrd.open_workbook(file_name) 
sheet_names= workbook.sheet_names()
relation = "产品属于"
product_lable = "产品类型"
common_category = []
count = 0

for sheet_name in sheet_names:
    sheet = workbook.sheet_by_name(sheet_name)
    for rowx in range(1,sheet.nrows-2):

        stock_name = sheet.row_values(rowx)[1]
        node_matcher = NodeMatcher(graph)
        listed_company_node = node_matcher.match("上市公司", name = stock_name).first()
        product_categories_tmp = sheet.row_values(rowx)[3]
        #原始数据有些括号，node_matcher.match(label,product_category)会出错，处理一下
        product_categories = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]", "", product_categories_tmp).split('、')
        count += 1
        print(count, ': ', listed_company_node, product_categories)
#         """ 
        for product_category in product_categories:
            product_category_node = node_matcher.match(product_lable,name = product_category).first()
            print(product_category_node)
            #多个上市公司的产品类别可能是重合的，先判断产品类别是否存在，如果已经存在，不创建。
            if (product_category_node == None ):
                product_category_node = Node(product_lable,name = product_category)
#                 graph.create(product_category_node)
                print(product_category_node)
            else:
                common_category.append(product_category+"\/n")
                print("重合类型: ",product_category)
            
            #程序跑错了，重复跑，之前已经建立了部分relation可能会重复,需要检查一下是否relation已经存在，有机会改造一下这块
#             relationship = Relationship(listed_company_node, relation, product_category_node)
#             graph.create(relationship)
#             print(relationship)

print('重合的产品类型共有: ',len(common_category) )  
if len(common_category) != 0:
    common_category_file = open('重合的产品类型', 'a', encoding="utf-8")
    for category in common_category:
        common_category_file.write(category)
    common_category_file.close()
    