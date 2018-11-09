#coding: utf-8

from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label
from com.wdk.stock.knowledgegraph.py2neo_advanced_tools import create_node

# 参考： https://blog.csdn.net/sinat_26917383/article/details/79901207

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")
node_matcher = NodeMatcher(graph)

create_node(graph, "自然人", "王麻子")
create_node(graph, "美食", "鸡翅")

"""
# *********START：Label操作集及示例************

# node关于label的API：
# labels() 返回node的标签的集合
# has_label(label) node是否有这个标签
# add_label(label) 给node添加标签
# remove_label(label) 删除node的标签
# clear_labels() 清楚node的所有标签
# update_labels(labels) 添加多个标签，注labels为可迭代的


# START: 创建Label,可以Label()，但似乎也要和node在一起操作，否则没办法push到graph
# 一个Node上叠加多个Label：node.add_label('labelname_x')
# 删除graph的label暂时无解,只能把所有节点的该label删除

testLabel3 = Label()
# name属性是label的唯一标识
testLabel3.name = "测试产品分类3"
test_node = node_matcher.match("测试LabelBeverage", name = "可乐").first()
if test_node == None :
    print("节点不存在")
else:
#     if testLabel3 in test_node.labels : #测试证明，此判断无意义。name属性是label的唯一标识
    if testLabel3.name in test_node.labels : #这个是work的，name属性是label的唯一标识
        print(testLabel3.name,"已经存在")
#         testLabel3.name = None   #这样无法删除一个label
        graph.delete(test_node)
        print(test_node,"已经被删除")  #远程服务器直接执行删除操作，无需调用push()
#         graph.push(test_node)
    else :
        test_node.add_label(testLabel3.name)
        graph.push(test_node)
        print(test_node.labels)
# END: 创建Label

# *********END：Label操作集及示例************
"""



"""
#START：查找并更新节点
lable = "测试LabelBeverage"
node_matcher = NodeMatcher(graph)
# 只返回第一个搜索结果，node或者subgraph
data_first = node_matcher.match(lable, name = "可乐").first()
#.first返回的是一个对象，只有None来判断不能用len判断；不带.first的match返回的是一个list，不用用None来判断，要用len判断
if data_first == None :
    print("not found")
else:
    print(data_first)

# 返回所有结果，List(subgraph)或者List(Node)
data = node_matcher.match("测试LabelBeverage", name = "可乐2")
if data == None:
    print("data is None")
if(len( list(data) ) == 0) :
    print("0， None")
else:
    print(list(data))
    print(len( list(data) ))
    for datax in data:
        print(datax)
        key_value = {'name': '汉堡2'}
        datax.update(key_value)
        graph.push(datax)
        print(datax)
        graph.delete(datax)
# END：查找并更新节点
"""


"""
#START：创建节点
temp_node1 = Node("产品",name="TCL冰箱")
temp_node2 = Node("上市公司",name = "TCL集团")
r = Relationship(temp_node2, "生产销售",temp_node1)
graph.create(temp_node1)
graph.create(temp_node2)
graph.create(r)
#END：创建节点
"""


"""
#START：更新节点属性
node2 = graph.nodes[1733]
node2['stockID'] = '001'
node2['别称'] = '临时称呼'
graph.push(node2)
print(graph.nodes[1733])

#多属性批量更新节点
data = {
    'stockID': '002',
    '别称': '惠州TCL'
}
node2.update(data)
graph.push(node2)
print(graph.nodes[1733])
#END：更新节点属性
"""

# """
#START：删除节点后，关系自动删除了
# node2 = graph.nodes[79296]
# graph.delete(node2)
# relationship = graph.match_one(rel_type='KNOWS')
# graph.delete(relationship)
#END：删除节点或关系
"""


# """
#START：查询分为节点查询NodeMatcher和关系查询RelationshipMatcher

# 查询graph中的所有node和所有relationship

# node_list = graph.nodes
# relation_list = graph.relationships
# print(len(node_list))
# for datax in node_list:
#     print(datax)
# print(len(relation_list))
# for datax in relation_list:
#     print(datax)


# 查询graph中的所有label为'产品类型'的节点
# 查询graph中节点label为'产品类型',和其他条件
# 注意graph.nodes的返回类型其实是NodeMatcher
# 
# node_list = graph.nodes.match('概念板块')#match只可以查询label和properties
# for datax in node_list:
#     print(datax)
# print(len(node_list))

# node_list = graph.nodes.match('产品类型').where(" _.name = '财务软件' ")
# node_list = graph.nodes.match('产品类型', name='财务软件' ") #和上面语句是等价的
# print(len(node_list))
# for datax in node_list:
#     print(datax)

# 因为name加label无法确定一个node，所以返回是list
# 如果label和id估计可以，因为id属性是node的identity
# 凡是match回来的结果，必须len判断，否则会制造潜在bug
# data_list = graph.nodes.match("股票名称").where(" _.name = '*ST康达' ")
# if len(data_list) != 0:
#     for datax in data_list:
#         print(datax["name"])
# else :
#     print("none")
# node_matcher = NodeMatcher(graph)
# data_list = node_matcher.match("股票名称", name = "*ST康达")
# for datax in data_list:
#     print(datax)
# data = graph.nodes.match('测试LabelBeverage')

# if(len( list(data) ) == 0) :
#     print("None")
# else:
#     print(len( list(data) ))
#     for datax in data:
#         print(datax)
#         graph.delete(datax)

#     graph.delete(datax)

# 下面的关系查询没试出来
# temp_node1 = Node("测试LabelBeverage",name="可乐")
# temp_node2 = Node("测试产品分类2",name = "汉堡")
# relation = Relationship(temp_node2, "搭配",temp_node1)
# graph.create(temp_node1)
# graph.create(temp_node2)
# graph.create(relation)
#  
# relation_ship =  RelationshipMatcher.match(temp_node1, relation)
# print(relation_ship)

#END：查询
# """

"""
#START:运行Neo4j命令
data = graph.run('MATCH (p:产品) RETURN p LIMIT 5')
print(list(data))

# match(s:上市公司) where s.name="科陆电子"  return s
# MATCH p=()-[r:`公司属于概念板块`]->() RETURN p LIMIT 25
#END:运行Neo4j命令
"""
