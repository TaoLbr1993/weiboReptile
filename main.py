#-*- coding:utf-8 –*-
import RepostMain
import time
import random
import sys
import WeiboMain
import testProxy
import GetProxy
import traceback
import os

#account=raw_input('Please input username\n')
#pwd=raw_input('Please input password\n')
checkey=random.randint(0,sys.maxint)
proxylist=WeiboMain.Proxy()
originPath=os.getcwd()
accountlist=WeiboMain.Account()
#### =========Time Control

startTime={'hour':0,'minute':0,'second':0}
pauseTime={'hour':12,'minute':0,'second':0}

print 'Waiting to begin'


#### ==========Time Control

while False:
    time.sleep(30)
    if  time.localtime()[3]==startTime['hour'] and time.localtime()[4]==startTime['minute']:
	print "It's time to go"
	break
    
#### ==========Add acounts here.
accounts=[\
    #{'username':'a250879398@163.com','pwd':'librian930819'},\
    {'username':'buaatao4@163.com','pwd':'buaa12061021'},\
    {'username':'buaatao1@163.com','pwd':'buaa12061021'},\
    {'username':'buaatao2@163.com','pwd':'buaa12061021'},\
    {'username':'buaatao3@163.com','pwd':'buaa12061021'},\
    {'username':'250879398@qq.com','pwd':'librian930819'}\
    #{'username':'buaatao4@163.com','pwd':'buaa12061021'},\
    #{'username':'buaatao5@163.com','pwd':'buaa12061021'}\
]
try:
    print '####Getting Proxys####'
    
    proxys=['http://110.4.12.173:80',\
	            'http://203.78.36.232:9000',\
	            'http://182.239.127.140:80',\
	            'http://182.239.95.137:80'] 
    proxys=GetProxy.getProxys()
    #print 5
    print 'Amounts of proxys:',len(proxys)
    print '####Getting Proxys finished####' 
    
    for account in accounts:
	accountlist.add(account)
    
    for proxy in proxys:
	#if testProxy.testProxy(proxy):
	proxylist.add(proxy)
    
    urlFile=open('url.txt','r')
    
    figure=0
    for line in open('url.txt','r'):
	line=urlFile.readline()
	print '####'+line
	figure+=1
	if line[-1]=='\n':
	    RepostMain.RepostMain(accountlist,line[:-1],checkey,figure,proxylist,startTime=startTime,pauseTime=pauseTime)
	else:
	    RepostMain.RepostMain(accountlist,line,checkey,figure,proxylist,startTime=startTime,pauseTime=pauseTime)
	print '####crawing over\n\n'
	time.sleep(10)	
	    
except Exception,e:
    os.chdir(originPath)
    excfile=open('exception.txt','a')
    var=traceback.format_exc()

    excfile.write('####'+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'+var)
    excfile.close()
    #print 'length of proxylist',proxylist.list
    raise e
