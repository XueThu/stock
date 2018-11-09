#coding: utf-8
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label 
import re
import xlrd
import time

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")
industry_category_layer4_label = Label()
concept_block_label = Label()
province_label = Label()
# name属性是label的唯一标识
industry_category_layer4_label.name = "行业四级分类"
concept_block_label.name = "概念板块"
province_label.name = "地域板块"

file_name = '上市公司高管.xls'
workbook = xlrd.open_workbook(file_name) 
sheet_names= workbook.sheet_names()

def check_data(sheet):
    manager_key_value={}
    row_count = 0
    current_year = int(time.strftime('%Y',time.localtime()))
    for rowx in range(1,sheet.nrows):
        manager_name = sheet.row_values(rowx)[0]
        stock_name = sheet.row_values(rowx)[1]
        manager_sex = sheet.row_values(rowx)[2]
        print(sheet.row_values(rowx)[3])
        manger_birthday = current_year - int(sheet.row_values(rowx)[3])
        manager_education_background = sheet.row_values(rowx)[4]
        manager_title = sheet.row_values(rowx)[5]
#         manager_title = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]", "", manager_title).split('、')
        
        manager_key = manager_name + manager_sex + str(manger_birthday) 
        manager_value =  stock_name + manager_title
        # 如果高管在多个公司，担任职务
        if manager_key in manager_key_value :
             #由于数据源需要清洗，合并同一个manager在相同公司的记录
            if manager_value not in manager_key_value[manager_key] :
                manager_key_value[manager_key] += ";"+manager_value 
        else:
            manager_key_value[manager_key] = manager_value
        row_count += 1
        print(row_count, manager_key, manager_key_value[manager_key] )
    
    replicated_manager_count = 0
    for manager_key in manager_key_value.keys() :
        company_list = manager_key_value[manager_key].split(';')
        if len(company_list) > 1 :
            if ("独立" not in manager_key_value[manager_key]):
                if("非执行" not in manager_key_value[manager_key]):
                    replicated_manager_count += 1
                    print(replicated_manager_count, manager_key, manager_key_value[manager_key])

"""
def load_category_and_relationship(sheet,column_num,label_name, relation_name):
    row_count = 0
    common_concept_count = 0
    node_matcher = NodeMatcher(graph)
    
    for rowx in range(1,sheet.nrows):
        stock_name = sheet.row_values(rowx)[1]
        listed_company_node = node_matcher.match("上市公司", name = stock_name).first()
        if listed_company_node == None :
            listed_company_node = Node("上市公司", name = stock_name)
        row_content_tmp = sheet.row_values(rowx)[column_num]
        if len(row_content_tmp) == 0 :
            print("内容没有，需要补全")
            break
        #原始数据有些括号，node_matcher.match(label,product_category)会出错，处理一下
        row_content_list = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]", "", row_content_tmp).split(';')
        row_count += 1
        print(row_count, ': ', listed_company_node, row_content_list)

        for row_content in row_content_list:
            #多个上市公司的概念板块可能是重合的，先判断概念是否存在，如果已经存在，不创建。
            category_node = node_matcher.match(label_name, name = row_content).first()
            if (category_node == None ):
                category_node = Node(label_name, name=row_content)
                graph.create(category_node)
                print(category_node)
            else:
                print("分类已存在，无需重复创建")
                common_category.append(category_node)

            #程序跑错了，重复跑，之前已经建立了部分relation可能会重复,需要检查一下是否relation已经存在，有机会改造一下这块
            relationship = Relationship(listed_company_node, relation_name, category_node)
            graph.create(relationship)
            print(relationship)
"""


for sheet_name in sheet_names:
    sheet = workbook.sheet_by_name(sheet_name)
    check_data(sheet)
#     load_industry_category_layer4(sheet)
#     load_category_and_relationship(sheet,9,concept_block_label.name,concept_block_relation)
#     load_category_and_relationship(sheet, 2, province_label.name, province_block_relation)

"""
if len(common_category) != 0:
    common_category_file = open('重合的行业类型', 'a', encoding="utf-8")
    for category in common_category:
        common_category_file.write(category)
    common_category_file.close()
   """ 
