from py2neo import Graph, Node, Relationship

import xlrd

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")


file_name = '上市公司产品类型和名称.xlsx'
workbook = xlrd.open_workbook(file_name)
sheet_names= workbook.sheet_names()
relation = "生产销售"
count = 0

for sheet_name in sheet_names:
    sheet = workbook.sheet_by_name(sheet_name)
    for rowx in range(1,sheet.nrows-2):

        stock_name = sheet.row_values(rowx)[1]
        listed_company_node = Node('上市公司', name=stock_name)
        graph.create(listed_company_node)
        products = sheet.row_values(rowx)[2].split('、') 
         
        for product in products:
            count += 1
            print(stock_name, product, count)
            product_node = Node('产品',name = product)
            relationship = Relationship(listed_company_node, "生产销售", product_node)
      
            graph.create(product_node)
            graph.create(relationship)
# #         
#     cols = sheet.col_values(0) # 获取第一列内容
# # 　　 print rows
#     for col in cols:
#         print(col)
#     print(len(cols))



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

# 
# #START：更新节点
# node2 = graph.nodes[1733]
# node2['stockID'] = '001'
# node2['别称'] = '临时称呼'
# print(graph.nodes[1733])
# 
# data = {
#     'stockID': '002',
#     '别称': '惠州TCL'
# }
# node2.update(data)
# graph.nodes[1733]._set_attr('别称','临时称呼')
# print(graph.nodes[1733])
#END：更新节点

"""
#Start：删除节点后，关系自动删除了
# node1 = graph.nodes[771]
node2 = graph.nodes[1713]
# relationship = graph.match_one(rel_type='KNOWS')
# graph.delete(relationship)
graph.delete(node2)
#END：删除节点
"""

"""
#START:运行Neo4j命令
data = graph.run('MATCH (p:产品) RETURN p LIMIT 5')
print(list(data))
#END:运行Neo4j命令
"""
# print(graph.nodes.match("Test","TCLtest"))
# print(temp_node1)
# temp_node1 = Node(lable="产品",name="TCL4k电视")
# temp_node1 = Node(lable="产品",name="TCL高清电视")
# temp_node2 = Node(lable="冰箱",name="TCL双开冰箱")
# graph.create(temp_node1)
# graph.create(temp_node2)
