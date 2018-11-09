#coding: utf-8

from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label
from venv import create
from com.wdk.stock.knowledgegraph.py2neo_advanced_tools import copy_all_incoming_relationship,copy_all_outgoing_relationship

# 参考： https://blog.csdn.net/sinat_26917383/article/details/79901207

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")
node_matcher = NodeMatcher(graph)

"""
# *********操作关系的属性************

# hash(relationship) 返回一个关系的hash值
# relationship[key] 返回关系的属性值
# relationship[key] = value 设定关系的属性值
# del relationship[key] 删除关系的属性值
# len(relationship) 返回关系的属性值数目
# dict(relationship) 以字典的形式返回关系的所有属性
# walk(relationship) 返回一个生成器包含起始node、关系本身、终止node
# type() 返回关系type


#**********查找关系********************
https://py2neo.org/v4/database.html#py2neo.database.Transaction.separate
# match(nodes=None, r_type=None, limit=None)
# Match and return all relationships with specific criteria.
# For example, to find all of Alice’s friends:
# for rel in graph.match((alice, ), r_type="FRIEND"):
#     print(rel.end_node["name"])
# nodes – Sequence or Set of start and end nodes (None means any node); a Set implies a match in any direction
# r_type – type of relationships to match (None means any type)  以后或许需要使用
# limit – maximum number of relationships to match (None means unlimited)

# Neo4j支持两个节点之间可以有多个关系；
# 如果start_node, end_node, r_type已经存在，重复创建，Neo4j不会重复生成relation
# graph.delete(relationship),这条命令的结果是不仅删除了关系，也删除了节点，即时节点上还有其他关系!!!
# delete(subgraph)[source]
# Delete the remote nodes and relationships that correspond to those in a local subgraph. 
# To delete only the relationships, use the transaction.separate() method.


"""
label = '美食'
node_list = graph.nodes.match(label)
# print(node_list)
relation_type1 = '搭配'
relation_type2 = '绝配'
 
# node1 = Node(label, name = '汉堡' )
# node2 = Node(label, name = '薯条' )
# relationship12 = Relationship(node1,relation_type2,node2)
# graph.create(relationship12)
# graph.push(relationship12)

# for start_node in node_list :
#     matcher = graph.match((start_node,), r_type = None)
#     if len(matcher) == 0 :
#         print("no relationship")
#     else: 
#         for relationship in matcher:
#             print(relationship.start_node["name"])
#             print(relationship.end_node["name"])
#             print(relationship.types())
#             for i in relationship.types() :
#                 relation_type = i
#             new_relationship = Relationship(relationship.start_node, relation_type, relationship.end_node) 
#             print(new_relationship)
#             print(relationship)
#         graph.separate(relationship)
#         graph.delete(relationship) #dangerous! Nodes will be deleted also. 

def check_same_name_node():
    # stock_name: 节点名为key，节点为value
    stock_name = {} 
    for from_node in graph.nodes.match("美食") :
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

check_same_name_node()