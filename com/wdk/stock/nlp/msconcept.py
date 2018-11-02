#coding: utf-8

file = '/Users/xuezhenghua/Desktop/WDK/Projects/EventQuantizer/data-concept/data-concept-instance-relations.txt'
lineNum = 0
"""
#分列显示
with open(file, 'r') as f:
    line = f.readline()
    while line:
        line = f.readline()
        print(line)
        column = line.split("\t")
        print(column[0]) 
        lineNum = lineNum + 1
        if lineNum > 9:
            break

"""

#查找统计
instance_keywords = 'baidu'
concept_keywords = 'crm'

lineNum = 0
resNum = 1
with open(file, 'r') as f:
    line = f.readline()
    while line:
        line = f.readline()
        lineNum += 1
        if lineNum >= 33377320:
            break
        column = line.split("\t")
        if  column[0].find(concept_keywords) == 0 :
#         if  column[1] == instance_keywords :
            print (resNum, ": ", line)
            resNum += 1 
