import pymysql
import config


def init():
    try:
        conn=pymysql.connect(config.MYSQL_HOST,config.MYSQL_USER,config.MYSQL_PASSWD,config.MYSQL_DBNAME)
        cursor=conn.cursor()
        mysql="create table if not exists {tablename} ( ip_port varchar(20) primary key not null ); ".format(tablename=config.MYSQL_TABLE_NAME)
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
        mysql="insert into {tablename} values ('{ip_port}') ".format(tablename=config.MYSQL_TABLE_NAME,ip_port=ip_port)
        #print (mysql)
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
            mysql="insert into {tablename} values ('{ip_port}') ".format(tablename=config.MYSQL_TABLE_NAME,ip_port=item)
            #print (mysql)
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



if __name__=="__main__":
    print ("ok")
    """
    ip_list=['192.168.100.21:10000','192.168.200.21:10000']
    insert_iplist(ip_list)
    get_iplist=get_iplist()
    for i in get_iplist:
        print (i)
    insert('192.168.3.21:10000')
    insert('192.168.3.22:10000')
    """