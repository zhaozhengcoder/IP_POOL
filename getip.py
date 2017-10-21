import requests 
import config
import db
from lxml import etree
import threading
import queue
import time



def getpage(target_url):
    page_content=""
    try:
        page_content=requests.get(target_url,headers=config.base_headers).text
    except Exception as e:
        print ('error : ',e)
    return page_content

def getip():
    ip_list=[]
    for url_agent in config.url_agent_pool:
        for num in range(1,config.crawl_pagenum):
            print (url_agent.format(pagenum=num))
            page_content=getpage(url_agent.format(pagenum=num))        
            page_html=etree.HTML(page_content)
            for i in page_html.xpath(config.url_agent_pool[url_agent]['xpath']):
                ip_xpath=config.url_agent_pool[url_agent]['ip_xpath']
                port_xpath=config.url_agent_pool[url_agent]['port_xpath']
                ip=i.findall(ip_xpath[0])[ip_xpath[1]].text
                port=i.findall(port_xpath[0])[port_xpath[1]].text
                ip_list.append("{ip}:{port}".format(ip=ip,port=port))
    return ip_list
        
def verifyip(ip_list):
    verified_iplist=[]
    while (len(ip_list)>0):
        ip_item=ip_list.pop()
        proxies={
            "http":"http://{ip_item}".format(ip_item=ip_item),
            "https":"https://{ip_item}".format(ip_item=ip_item)
        }
        try:
            response=requests.get(config.verifyip,headers=config.base_headers,proxies=proxies,timeout=config.timeout)
            if response.status_code==200:
                verified_iplist.append(ip_item)
        except Exception as e:
            print ('error : ',e)
    return verified_iplist

def task(ip_queue,verified_queue):
    while not ip_queue.empty():
        ip_item=ip_queue.get()
        proxies={
            "http":"http://{ip_item}".format(ip_item=ip_item),
            "https":"https://{ip_item}".format(ip_item=ip_item)
        }
        try:
            response=requests.get(config.verifyip,headers=config.base_headers,proxies=proxies,timeout=config.timeout)
            if response.status_code==200:
                verified_queue.put(ip_item)
        except Exception as e:
            print ('error : ',e)

def verifyip_multithread(ip_list):
    ip_queue=queue.Queue()
    verified_queue=queue.Queue()
    thread_list=[]
    
    for item in ip_list:
        ip_queue.put(item)
    for i in range(0,config.thread_num):
        t=threading.Thread(target=task,name='thread{}'.format(i),args=(ip_queue,verified_queue,))
        thread_list.append(t)
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()
    verified_iplist=[]
    while not verified_queue.empty():
        verified_iplist.append(verified_queue.get())
    return verified_iplist


def data_persistence(verified_iplist):
    db.init()
    db.insert_iplist(verified_iplist)
    
    