#coding: utf-8
from py2neo import Graph, Node, Relationship
from py2neo.matching import NodeMatcher, RelationshipMatcher
from py2neo.ogm import Label 
import re
import xlrd
import time
from com.wdk.stock.knowledgegraph.py2neo_advanced_tools import copy_all_incoming_relationship,\
    copy_all_outgoing_relationship

# 连接neo4j数据库
graph = Graph("http://127.0.0.1:7474",username="neo4j",password="X111111")

file_name_resume = '上市公司高管简历.xlsx'
file_name_manager_profile = '上市公司高管.xls'

# 把管理层的基本信息输入到图数据库中
def add_manager_profile_to_graph(file_name_manager_profile):
    workbook = xlrd.open_workbook(file_name_manager_profile) 
    sheet_names= workbook.sheet_names()
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)
    
    row_count = 0
    current_year = int(time.strftime('%Y',time.localtime()))
    for rowx in range(1,sheet.nrows):
        row_count += 1
        manager_name = sheet.row_values(rowx)[0]
        stock_name = sheet.row_values(rowx)[1]
        manager_sex = sheet.row_values(rowx)[2]
        manger_birthday = current_year - int(sheet.row_values(rowx)[3])
        manager_degree = sheet.row_values(rowx)[4]
        manager_title = sheet.row_values(rowx)[5]
#         print(row_count, manager_name, stock_name, manager_sex, manger_birthday, manager_degree, manager_title)
#         manager_title = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]", "", manager_title).split('、')

        sex_property = "性别"
        birth_property = "出生年月"
        degree_property = "学历"
        title_property = "职位"
        person_label = "自然人"
        
        manager_node = Node(person_label, name = manager_name)
        manager_node[sex_property] = manager_sex
        manager_node[birth_property] = manger_birthday
        manager_node[title_property] = manager_title
        manager_node[degree_property] = manager_degree
#         print(row_count, manager_node)
        graph.create(manager_node)
        graph.push(manager_node)
        
        # 根据股票名称查出其对应的公司名称，再把管理者和公司创建关系连接起来
        stock_node = graph.nodes.match("股票名称", name = stock_name)
        if len(stock_node) != 0:
            stock_node = stock_node.first()
            company_stock_relationships = graph.match((None, stock_node), r_type = "股票名称是")
            if len(company_stock_relationships) != 0 :
                company_node = company_stock_relationships.first().start_node
                RELATION_TYPE = "管理公司"
                relationship = Relationship(manager_node, RELATION_TYPE, company_node)
                print(row_count, relationship)
                graph.create(relationship)
                graph.push(relationship)

# 读取管理者简历，输入到数据库中
def add_manager_resume_to_graph(file_name_resume):
    workbook = xlrd.open_workbook(file_name_resume) 
    sheet_names= workbook.sheet_names()
    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)

    row_count = 0
    for rowx in range(1,sheet.nrows):
#     for rowx in range(40417,40420):
        row_count += 1
        stock_code = sheet.row_values(rowx)[1].strip()
        manager_name = sheet.row_values(rowx)[2].strip()
        manager_resume = sheet.row_values(rowx)[3].strip()
         
#         print(row_count, stock_code, manager_name, manager_resume)
        MANAGER_EXISTED_IN_GRAPH_FLAG = False
        stock_name_nodes = graph.nodes.match("股票名称", 股票代码__contains =  stock_code)
        if len(stock_name_nodes) != 0:
            stock_name_node = stock_name_nodes.first()
#             print(row_count, stock_name_node)
            company_stock_relationships = graph.match((None, stock_name_node), r_type = "股票名称是") 
            if len(company_stock_relationships) != 0:
                company_stock_relationship = company_stock_relationships.first()
                company_name_node = company_stock_relationship.start_node
#                 print(row_count, company_name_node)
                company_manager_relationships = graph.match((None, company_name_node), r_type = "管理公司")  
                if len(company_manager_relationships) != 0 :
                    for company_manager_relationship in company_manager_relationships:
                        manager_node = company_manager_relationship.start_node
#                         print(row_count, manager_name, manager_node["name"])
                        if manager_name == manager_node["name"]:
                            MANAGER_EXISTED_IN_GRAPH_FLAG = True
                            if len(manager_resume) == 0 :
                                print(row_count, "没有从输入文件中获取到简历", manager_node["name"])
                            if "简介" in manager_node.keys() :
                                print(row_count, "简历已经存在", manager_node["name"])
                            else:
                                manager_node["简介"] = manager_resume
                                graph.push(manager_node)
                                print(row_count, "***成功***",  manager_node["name"], manager_node["简介"])
                    if MANAGER_EXISTED_IN_GRAPH_FLAG == False :
                        manager_node = Node("自然人", name = manager_name)
                        manager_node["简介"] = manager_resume
                        graph.create(manager_node)
                        graph.push(manager_node)
                        company_manager_relationship = Relationship(manager_node,"管理公司", company_name_node)
                        print("**************新增节点**************", company_manager_relationship)
                        graph.create(company_manager_relationship)
                        graph.push(company_manager_relationship)


        
#删除所有公司管理者
def delete_all_mananger():
    for company_node in graph.nodes.match("公司名称"):
        manager_company_relationships = graph.match((None,company_node), r_type = "管理公司")
        if len(manager_company_relationships) != 0 :
            for manager_company_relationship in manager_company_relationships:
#                 print(manager_company_relationship.start_node)
                # 先separate relatonship再delete relationship.start_node节点有问题，
                # 因为separate之后，relationship已经不存在了；直接删除 start_node,relationship应该也被删除了
#                 graph.separate(manager_company_relationship)
                graph.delete(manager_company_relationship.start_node)
  
#把简历作为key，merge相同key的人                
def merge_manager():
    person_dict = {}
    person_node_list = graph.nodes.match("自然人")
    if len(person_node_list) != 0:
        for person_node in person_node_list:
            # 如果节点有“简介”这个属性，再以此作为标准，判断节点是否有同名现象；
            # 其他情况暂不处理
            if "简介" in person_node.keys():
                if person_node["简介"] not in person_dict.keys() :
                    person_dict[person_node["简介"]] = person_node
                    print("加入到字典中", person_node["简介"])
                else:
                     exist_person_node = person_dict[person_node["简介"]] 
                     print("合并同一个人", person_node["简介"], exist_person_node)
                     copy_all_incoming_relationship(graph, person_node, exist_person_node, None)
                     copy_all_outgoing_relationship(graph, person_node, exist_person_node, None) 
                     graph.delete(person_node)
    
# add_manager_profile_to_graph(file_name_manager_profile)
# delete_all_mananger()
add_manager_resume_to_graph(file_name_resume)
# merge_manager()

