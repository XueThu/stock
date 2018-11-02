import re


s="我是一个人(中国人)aaa[真的]bbbb{确定}"
a = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]", "", s)
print (a)