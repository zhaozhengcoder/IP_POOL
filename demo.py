import getip
import util

def main():
    ip_list=getip.getip()
    verified_iplist=getip.verifyip_multithread(ip_list)
    getip.data_persistence(verified_iplist)
    print ('crawl verified ip list is : ',verified_iplist)



if __name__=='__main__':
    # get ip and save in db
    main()
    # random choice ip
    print (util.get())
