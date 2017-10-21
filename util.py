import db
import random

def get():
    proxies={}
    ip_list=db.get_iplist()
    ip_item=random.choice(ip_list)
    proxies['http']='http://{ip_item}'.format(ip_item=ip_item)
    proxies['https']='https://{ip_item}'.format(ip_item=ip_item)
    return proxies


if __name__=='__main__':
    print (get())