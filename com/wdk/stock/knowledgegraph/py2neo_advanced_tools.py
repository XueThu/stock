from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label
from zmq.backend.cython.constants import PUSH
import re
import xlrd

def create_node(graph, node_label, node_name):
    nodes = graph.nodes.match(node_label, name = node_name)
    if len(nodes) == 0:
        node = Node(node_label, name = node_name)
        graph.create(node)
        graph.push(node)
#         print("创建成功：", node)
    else:
        node = nodes.first()
#         print("同名，同Label，节点已存在",node)
    return node

# 查询一个节点所有的imcoming relationship    
def get_all_incoming_relationship(graph, destination_node):
    relationships = graph.match((None,destination_node), r_type = None)
    if len(relationships) != 0 :
        for relationship in relationships :
            re = Relationship(relationship.start_node, relationship.types(), relationship.end_node) 
    else :
        print(destination_node["name"] + ": has no incoming relationship")   

# 查询一个节点所有的outgoing relationship    
def get_all_outgoing_relationship(graph, destination_node):
    relationships = graph.match((destination_node,None), r_type = None)
    if len(relationships) != 0 :
        for relationship in relationships :
            re = Relationship(relationship.start_node, relationship.types(), relationship.end_node) 
            print(re)
    else :
        print(destination_node["name"] + ": has no outgoing relationship") 

# copy一个节点所有的imcoming relationship给另外一个节点    
def copy_all_incoming_relationship(graph, from_node, to_node):
    result = {}
    relationships = graph.match((None,from_node), r_type = None)
    # 没有下面这个声明，直接append会出错
    result["relation_list"]=[]
    if len(relationships) != 0 :
        for relationship in relationships :
            for i in relationship.types() :
                relationship_type = i
            new_relationship = Relationship(relationship.start_node, relationship_type, to_node) 
            graph.create(new_relationship)
            graph.push(new_relationship)
            graph.separate(relationship) 
            result["relation_list"].append(new_relationship)
    result["message"] = "incoming relationship count is："+str(len(relationships))
    return result  

# copy一个节点所有的imcoming relationship给另外一个节点    
def copy_all_outgoing_relationship(graph, from_node, to_node):
    result = {}
    # 没有下面这个声明，直接append会出错
    result["relation_list"]=[]
    relationships = graph.match((from_node,None), r_type = None)
    if len(relationships) != 0 :
        for relationship in relationships :
            for i in relationship.types() :
                relationship_type = i
            new_relationship = Relationship(to_node, relationship_type, relationship.end_node)
            print(relationship)
            print(new_relationship)
            graph.create(new_relationship)
            graph.push(new_relationship)
            graph.separate(relationship) 
            result["relation_list"].append(new_relationship)
    result["message"] = "outgoing relationship count is："+str(len(relationships))
    return result  