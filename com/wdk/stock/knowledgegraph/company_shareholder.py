#coding: utf-8
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label 
import re
import xlrd
import time
from venv import create
from com.wdk.stock.knowledgegraph.py2neo_advanced_tools import create_node


compound_surname = ["竹田","胡白","藤野", "欧阳", "令狐", "赫连", "诸葛"]

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")

file_name = '股东_1102.xls'
workbook = xlrd.open_workbook(file_name) 
sheet_names= workbook.sheet_names()

def check_data(sheet_names):
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)
        manager_key_value={}
        row_count = 0
        current_year = int(time.strftime('%Y',time.localtime()))
        for rowx in range(1,sheet.nrows):
            row_count += 1
            stock_name = sheet.row_values(rowx)[0]
            share_holder = sheet.row_values(rowx)[2]
            share_type = sheet.row_values(rowx)[3]
            share_number = sheet.row_values(rowx)[4]
            share_holder_detail = share_holder.split('-')
            share_holder = share_holder_detail[0]
                        
            STOCK_NAME_LABEL = "股票名称"           
            stock_node = create_node(graph, STOCK_NAME_LABEL, stock_name)
            
            share_holder_label = ""
            SHARE_HOLDER_LABEL_PERSON = "自然人"  
            SHARE_HOLDER_LABEL_COMPANY = "公司名称"  
            if len(share_holder) < 4 :
                share_holder_label = SHARE_HOLDER_LABEL_PERSON
            elif len(share_holder) == 4 :
                Person_FlAG = False
                for surname in compound_surname:
                    if surname in share_holder:
                        Person_FlAG = True
                        break 
                if (Person_FlAG == True):
                    share_holder_label = SHARE_HOLDER_LABEL_PERSON
                else:
                    share_holder_label = SHARE_HOLDER_LABEL_COMPANY   
            else:
                    share_holder_label = SHARE_HOLDER_LABEL_COMPANY
            
            share_holder_node = create_node(graph, share_holder_label, share_holder)  
#             print(row_count, stock_node, share_holder_node )
            
            
            RELATION_TYPE = "持股"
            relationship = Relationship(share_holder_node, RELATION_TYPE, stock_node)
            relationship["股数"] = share_number
            graph.create(relationship)
            graph.push(relationship)
#             print(row_count, relationship)
            print(row_count)
            
check_data(sheet_names)
