#-*- coding:utf-8 –*-
import RepostMain
import time
import random
import sys
import WeiboMain
import testProxy
import GetProxy

#account=raw_input('Please input username\n')
#pwd=raw_input('Please input password\n')
checkey=random.randint(0,sys.maxint)
proxylist=WeiboMain.Proxy()
accountlist=WeiboMain.Account()
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
print '####Getting Proxys####'
#proxys=GetProxy.getProxys()
proxys=['http://110.4.12.173:80',\
        'http://218.254.1.13:80',\
        'http://203.78.36.232:9000',\
        'http://182.239.127.140:80']
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
        RepostMain.RepostMain(accountlist,line[:-1],checkey,figure,proxylist)
    else:
        RepostMain.RepostMain(accountlist,line,checkey,figure,proxylist)
    print '####crawing over\n\n'
    time.sleep(10)
