import pymysql  
import re
from com.wdk.stock.eventanalysis.eventcomments import stock_code
#导入 pymysql 
#打开数据库连接

db_file_config=[]
with open('database_config', 'r') as f:
    for line in f.readlines():
        line = re.sub("\\(.*\\)|\\{.*?}|\\[.*?]|\\\n", "", line)
        db_file_config.append(line)
    
db= pymysql.connect(host=db_file_config[0], \
                    user=db_file_config[1], \
                    password=db_file_config[2], \
                    db=db_file_config[3], \
                    port=int(db_file_config[4])) 
# 使用cursor()方法获取操作游标
cur = db.cursor() 
#1.查询操作
# 编写sql 查询语句  user 对应我的表名
sql = "select stock_code, ent_name, word, tfidf from stock_keywords where ent_name like '%tcl%' order by tfidf desc"

try:    
    cur.execute(sql)     
    #执行sql语句     
    results = cur.fetchall()    
    #遍历结果
    count = 0    
    for row in results :  
        stock_code = row[0]  
        ent_name = row[1]    
        word = row[2]        
        tfidf = row[3]  
        count += 1      
        print(str(count),": ", stock_code, ent_name, word,tfidf)
except Exception as e:    
    raise e
finally:    
    db.close()    
    #关闭连接