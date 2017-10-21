import requests 
import config
import db
from lxml import etree

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


def data_persistence(verified_iplist):
    db.init()
    db.insert_iplist(verified_iplist)
    


if __name__=='__main__':
    print ('ok')
    ip_list=getip()
    
    verified_iplist=verifyip(ip_list)
    data_persistence(verified_iplist)
    print (verified_iplist)
    