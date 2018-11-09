#coding: utf-8
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label 
import re
import xlrd
import time
from com.wdk.stock.eventanalysis.eventcomments import stock_code

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")

file_name = 'A股上市公司全名.xlsx'
workbook = xlrd.open_workbook(file_name) 
sheet_names= workbook.sheet_names()

def check_data(sheet):
    row_count = 0
    for rowx in range(1,sheet.nrows):
        row_count += 1
        stock_code = sheet.row_values(rowx)[0]
        stock_name = sheet.row_values(rowx)[1]
        company_name = sheet.row_values(rowx)[2]
        print(row_count, stock_code, stock_name, company_name)
        

        
def add_propterty():
    STOCK_NAME_LABEL = '股票名称'
    COMPANY_NAME_LABEL = '公司名称'
    STOCK_CODE_PROPERTY = '股票代码'
    COMPANY_STOCK_RELATIONSHIP = '股票名称是'
    
    row_count = 0
    node_matcher = NodeMatcher(graph)
    for rowx in range(1,sheet.nrows):
        row_count += 1
        stock_code = sheet.row_values(rowx)[0]
        stock_name = sheet.row_values(rowx)[1]
        company_name = sheet.row_values(rowx)[2]
#         print(row_count, stock_code, stock_name, company_name)
        data_list = node_matcher.match(STOCK_NAME_LABEL,name = stock_name)
        #检查1、是否有没在图谱中出现的新股票
        #检查2、图谱中是否有重复股票名称（数据清洗）
        if len( list(data_list) ) < 1 :
            print("没有此股票名称")
            stock_node = Node(STOCK_NAME_LABEL, name = stock_name)
#             graph.push(stock_node)
            print(row_count, stock_code, stock_name, company_name)
        elif len( list(data_list) ) > 1 : 
                for data in data_list :
                    print(data)
                print(row_count, stock_code, stock_name, company_name)       
        else :
            stock_node = data_list.first()
    
        stock_node[STOCK_CODE_PROPERTY] = stock_code
        company_node = Node(COMPANY_NAME_LABEL, name = company_name)
        graph.create(company_node) 
        company_stock_relation = Relationship(company_node, COMPANY_STOCK_RELATIONSHIP, stock_node) 
        graph.create(company_stock_relation)              
        print(row_count, company_node)


for sheet_name in sheet_names:
    sheet = workbook.sheet_by_name(sheet_name)
#     check_data(sheet)
    add_propterty()
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
