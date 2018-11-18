from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label
from zmq.backend.cython.constants import PUSH
import re
import xlrd

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")
node_matcher = NodeMatcher(graph)

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

# copy一个节点所有关系类型为relation_type的imcoming relationship给另外一个节点    
def copy_all_incoming_relationship(graph, from_node, to_node, relaiton_type):
    result = {}
    relationships = graph.match((None,from_node), r_type = relaiton_type)
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
    result["message"] = from_node["name"] + " incoming relationship count is："+str(len(relationships))
    return result  

# copy一个节点所有关系类型为relation_type的outgoing relationship给另外一个节点    
def copy_all_outgoing_relationship(graph, from_node, to_node, relaiton_type):
    result = {}
    # 没有下面这个声明，直接append会出错
    result["relation_list"]=[]
    relationships = graph.match((from_node,None), r_type = relaiton_type)
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
    result["message"] = from_node["name"] + "outgoing relationship count is："+str(len(relationships))
    return result  

# 查询没有任何relationship的节点
def check_isolated_node(graph, node):
    if len(graph.match((node,None), r_type = None)) == 0 and \
        len(graph.match((node,None), r_type = None)) == 0 :
        print("孤儿节点", node["name"])
        return True
    else:
        return False

# 查找同一Label里的同名节点
def find_same_name_node(graph, label_name):
    node_matcher = graph.nodes.match(label_name) 
    # 创建节点名为key，node_list为value的dict
    # 算出len(value)大于1的节点即为重名节点
    node_dict = {}
    for node in node_matcher:
        # 没有下面这个初始化，后面append会出错
        if node["name"] not in node_dict:
            node_dict[node["name"]] = node
#             print(node["name"], node_dict.get(node["name"]))
        else:
            node_list = []
#             print(node["name"], node_dict[node["name"]])
            for node_i in node_dict[node["name"]]:
                node_list.append(node_i)
            node_dict[node["name"]] = node_list.append(node)
            for node_j in node_list: 
                print(node["name"], node_j)
        
    # 遍历字典的项
#     for key in node_dict:
#         print(key, len(node_dict.get(key))) 
    
# find_same_name_node(graph, "自然人") 
        
    