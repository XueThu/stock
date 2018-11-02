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
"""
sql = "CREATE TABLE `eventcomment` (\
  `id` bigint(20) NOT NULL AUTO_INCREMENT,\
  `date` datetime DEFAULT NULL,\
  `code` int(10) DEFAULT NULL,\
  `name` varchar(32) DEFAULT NULL,\
  `low` double(32,4) DEFAULT NULL,\
  `open` double(32,4) DEFAULT NULL,\
  `close` double(32,4) DEFAULT NULL,\
  `high` double(32,4) DEFAULT NULL,\
  `volume` bigint(20) DEFAULT NULL,\
  `turnover` double(32,4) DEFAULT NULL,\
  `securityId` varchar(32) DEFAULT NULL,\
  `preClose` double(32,4) DEFAULT NULL,\
  `change` double(16,4) DEFAULT NULL,\
  `changePct` double(16,4) DEFAULT NULL,\
  `turnoverRate` double(16,4) DEFAULT NULL,\
  `tCap` double(16,4) DEFAULT NULL,\
  `mCap` double(16,4) DEFAULT NULL,\
  `comment` varchar(32) DEFAULT NULL,\
  PRIMARY KEY (`id`)\
) ENGINE=InnoDB AUTO_INCREMENT=4079909 DEFAULT CHARSET=utf8;"

sql = "alter table eventcomment add column comment varchar(20) not null;"
sql = "select * from eventcomment where Date(date) = '2018-07-13' and code =600588"
"""
event_date = '2018-07-13'
stock_code = "600588"
event_comment = '经用友网络科技股份有限公司财务部门初步测算，预计2018年半年度实现归属于上市公司股东的净利润与上年同期相比，将实现扭亏为盈，实现归属于上市公司股东的净利润10,000万元到13,000万元。归属于上市公司股东扣除非经常性损益后的净利润8,000万元到11,000万元。'
sql = "UPDATE eventcomment SET comment = \'"+event_comment+"\'"   + \
     " where Date(date) = \'"+event_date+"\'" +\
     " and code ="+stock_code  

try:    
    cur.execute(sql) 
    #执行sql语句     
    results = cur.fetchall() 
    db.commit()
    
    print(results)
except Exception as e:    
    raise e
finally:    
    db.close()    
    #关闭连接