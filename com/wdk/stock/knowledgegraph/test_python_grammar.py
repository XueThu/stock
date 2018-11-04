import re


s="我是一个人(中国人)aaa[真的]bbbb{确定}"
a = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]", "", s)
print (a)

s = "攀钢钒钛;帝欧家居;鹏博士"
a = "攀钢钒w"

if a not in s :
    print(s)