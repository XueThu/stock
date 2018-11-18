#coding: utf-8
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label
from zmq.backend.cython.constants import PUSH
import re
import xlrd
from com.wdk.stock.knowledgegraph.py2neo_advanced_tools import copy_all_incoming_relationship,\
    copy_all_outgoing_relationship

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")
node_matcher = NodeMatcher(graph)

# 把这个函数里的copy***()函数注释掉，该函数的功能为：检查是否有重名节点
def delete_isolated_node(label_name):
    for node in graph.nodes.match(label_name) :
        outgoing_relation = graph.match((node,None), r_type = None)
        incoming_relation = graph.match((None,node), r_type = None)
        if len(outgoing_relation) == 0 and len(incoming_relation) == 0 :
            print(node['name'])
            graph.delete(node)
        
# 把这个函数里的copy***()函数注释掉，该函数的功能为：检查是否有重名节点
def merge_same_name_node(label_name):
    # stock_name: 节点名为key，节点为value
    stock_name = {} 
    for from_node in graph.nodes.match(label_name) :
        if from_node["name"]  in stock_name :
            to_node = stock_name[from_node["name"]]
            print(from_node["name"], from_node, to_node)
            
            print("...........incoming...........")
            incoming_result = copy_all_incoming_relationship(graph, from_node, to_node)
            print(incoming_result)
             
            print("...........outgoing...........")
            outgoing_result = copy_all_outgoing_relationship(graph, from_node, to_node)
            print(outgoing_result)
        else :
            stock_name[from_node["name"]] = from_node

# 更新股票名并把股票代码作为属性加上
def update_stock_name(file_name):
    print(file_name)
    workbook = xlrd.open_workbook(file_name) 
    sheet_names= workbook.sheet_names()
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)
        for rowx in range(1,sheet.nrows):
            old_stock_name = sheet.row_values(rowx)[0]
            stock_code = sheet.row_values(rowx)[1]
            new_stock_name = sheet.row_values(rowx)[2]
            company_name = sheet.row_values(rowx)[3]
            print(old_stock_name, new_stock_name, company_name)
 
            condition_clause = "_.name = '" + old_stock_name + "'"
            node = graph.nodes.match('股票名称').where(condition_clause).first()
            
            node["name"] = new_stock_name
            node["股票代码"] = stock_code
            print(node["name"],node["股票代码"])
            graph.push(node)

def check_sotck_has_enterpise():
    count = 0
    for node in graph.nodes.match("股票名称"):
        count += 1
        relationships = graph.match((None,node), r_type = "股票名称是")
        if len(relationships) == 0:
            print(count, node)
        else:
            for relationship in relationships:
                print(count, relationship)                

# 把“生产销售”关系从股票名称节点移到公司名称节点
def move_product_relaiton_from_stock_to_company():
    stock_name_nodes = graph.nodes.match("股票名称")
    relation_type = "生产销售"
    
    if len(stock_name_nodes) != 0:
        for stock_name_node in stock_name_nodes:
            stock_company_relationships = graph.match((None, stock_name_node), r_type="股票名称是")
            if len(stock_company_relationships) != 0:
                company_name_node = stock_company_relationships.first().start_node
                result = copy_all_outgoing_relationship(graph, stock_name_node, company_name_node, relation_type)
                print(result)
                
            
        
        
    #list所有待迁移的relation
#     if len(stock_nodes) != 0:
#         for stock_node in stock_nodes:
#             relationships = graph.match((stock_node,None), r_type=relation_name)
#             print(len(relationships) )
#             if len(relationships) != 0:
#                 for relationship in relationships:
#                     print(relationship)
#             
        


# merge_same_name_node("股票名称")
# delete_isolated_node("股票名称")
# update_stock_name("更名企业.xlsx")
# check_sotck_has_enterpise()
# find_same_name_node(graph, "自然人")  

# move_product_relaiton_from_stock_to_company()
delete_isolated_node("自然人")
