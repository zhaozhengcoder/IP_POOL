import pymysql
import config


def init():
    try:
        conn=pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER,config.MYSQL_PASSWD,config.MYSQL_DBNAME)
        cursor=conn.cursor()
        mysql="create table if not exists {tablename} ( ip_port varchar(30) primary key not null ); ".format(tablename=config.MYSQL_TABLE_NAME)
        #print (mysql)
        cursor.execute(mysql)
        conn.commit()
    except Exception as e:
        print (e) 
        conn.rollback()
    finally:
        conn.close()

def insert_item(ip_port):
    try:
        conn=pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER,config.MYSQL_PASSWD,config.MYSQL_DBNAME)
        cursor=conn.cursor()
        mysql="insert ignore into {tablename} values ('{ip_port}') ".format(tablename=config.MYSQL_TABLE_NAME,ip_port=ip_port)
        print (mysql)
        cursor.execute(mysql)
        conn.commit()
    except Exception as e:
        print (e) 
        conn.rollback()
    finally:
        conn.close()

def insert_iplist(ip_list):
    try:
        conn=pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER,config.MYSQL_PASSWD,config.MYSQL_DBNAME)
        cursor=conn.cursor()
        for item in ip_list:
            mysql="insert ignore into {tablename} values ('{ip_port}') ".format(tablename=config.MYSQL_TABLE_NAME,ip_port=item)
            print (mysql)
            cursor.execute(mysql)
        conn.commit()
    except Exception as e:
        print (e) 
        conn.rollback()
    finally:
        conn.close()    

def get_iplist():
    iplist=[]
    try:
        conn=pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER,config.MYSQL_PASSWD,config.MYSQL_DBNAME)
        cursor=conn.cursor()
        mysql="select * from {tablename} ;".format(tablename=config.MYSQL_TABLE_NAME)
        #print (mysql)
        cursor.execute(mysql)
        res=cursor.fetchall()
        for row in res:
            iplist.append(row[0])
    except Exception as e:
        print (e)
        conn.rollback()
    finally:
        conn.close()
        return iplist

def drop_table():
    try:
        conn=pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER,config.MYSQL_PASSWD,config.MYSQL_DBNAME)
        cursor=conn.cursor()       
        cursor.execute('drop table if exists {}'.format(config.MYSQL_TABLE_NAME))
        conn.commit()
    except Exception as e:
        print (e)
        conn.rollback()
    finally:
        conn.close()