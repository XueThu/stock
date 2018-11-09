from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label
from zmq.backend.cython.constants import PUSH
import re
import xlrd
import datetime
from time import sleep



def avg_node(graph, node_lable, node_name):
    nodes = graph.nodes.match(node_lable, name = node_name)
    if len(nodes) == 0:
        node = Node(node_lable, name = node_name)
        graph.create(node)
        graph.push(node)
#         print("创建成功：", node)
    else:
        node = nodes.first()
#         print("同名，同Label，节点已存在",node)
    return node

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")

starttime = datetime.datetime.now()
 
node_label = "股票名称"
node_name = "南方"
relation_type = "持股"

nodes = graph.nodes.match(node_label, name__contains = node_name)
print(nodes)
if len(nodes) == 0:
    print("没有找到这支股票呀，可能股票名称有误，换个名字试试？")
elif len(nodes) == 1:
    node = nodes.first()
    relationships = graph.match((None, node), r_type = relation_type)
    stock_sum = 0
    for relation in relationships:
        stock_sum += relation["股数"]
        print(relation)
    print(stock_sum)
else :
    node_list = []
    for node in nodes:
        node_list.append(node["name"])
        
    print("包含这个股票名字的，有好几支呢", node_list, "您想了解哪一支呢")

endtime = datetime.datetime.now()
print(endtime-starttime)
