import pymysql  
#导入 pymysql 
#打开数据库连接

db= pymysql.connect(host="60.205.202.141",\
                    user="work",\
                    password="Wjbb12345",\
                    db="stock",\
                    port=3306) 
# 使用cursor()方法获取操作游标
cur = db.cursor() 
#1.查询操作
# 编写sql 查询语句  user 对应我的表名
sql = "select date, abs(changePct) from 163bfq where code = 600588 and abs(changePct) > 3 order by date desc"
try:    
    cur.execute(sql)     
    #执行sql语句     
    results = cur.fetchall()    
    #遍历结果
    count = 0    
    for row in results :        
        date = row[0]        
        changePct = row[1]  
        count += 1      
        print(str(count)+": ",date,changePct)
except Exception as e:    
    raise e
finally:    
    db.close()    
    #关闭连接