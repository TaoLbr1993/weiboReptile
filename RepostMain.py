#-*- coding:utf-8 –*-
#####新浪微博爬虫
#####转发抓取
from __future__ import division
import WeiboMain
from WeiboMain import Proxy
import urllib2
import re
import sys
import os
import time
import pylab as pl
import pickle
import MySQLdb

def seconds_to_hms(seconds):
    hour=int(seconds/3600)
    minute=int(seconds-hour*3600)/60
    second=int(seconds-hour*3600-minute*60)
    result={'hour':hour,'minute':minute,'seconds':second}
    return result


def RepostMain(accountlist,url_to_craw,checkey,figure,proxylist,startTime,pauseTime):
    time.clock()
    starttime=time.clock()
    #请求输入账号密码目标url
    
    #account=raw_input('Please input username\n')
    #pwd=raw_input('Please input password\n')
    #url_to_craw=raw_input("Please input url\n")
    #pattern=r'''<dd><a href=\\"\\\/.*?\\" title=\\"(.*?)\\" nick\-name=\\".*?\\" usercard=\\".*?\\"> .*?<\\\/a>.*?\s*<em>(.*?)<\\\/em>\s*<a href=.*?title=\\"(,*?)\\"'''
    pattern_userid=re.compile(r'''com\/(\d*?)\/(.*?)\?''')
    result=pattern_userid.search(url_to_craw)
    userid=result.group(1)
    filename=result.group(2)

    origdir=os.getcwd()
    #Statics
    if os.path.exists('statics.data'):#static is a list with 48 elements.
	staticsfile=open('statics.data','r')
	statics=pickle.load(f)
	staticsfile.close()
    else:
	statics={'pages':[0]*50,'time':[0]*50} #    
    newdir=os.path.join(origdir,userid)
    if os.path.isdir(newdir):
	pass
    else:
	os.mkdir(userid)
    os.chdir(newdir)
    
    #建立数据库
    conn=MySQLdb.connect(host='localhost',user='root',passwd='root',charset='utf8')
    cursor=conn.cursor()
    print 10
    try:
	print 123123
	cursor.execute("""CREATE database """+"userid"+userid+";")
    except Exception,e:
	print 'The Database exists'
    #print 23
    conn.select_db("userid"+userid)
    #print 234
    try:
	cursor.execute('set names gbk;')
	cursor.execute('create table '+filename+' (id CHAR(50),time DATETIME, content TEXT,repofrom CHAR(50),polvl TINYINT) ENGINE=MyISAM DEFAULT CHARSET=gbk')
    except Exception,e:
	print "The Table exists\nuserid:"+userid+'\nWarning:This Information of Repost has been reptiled. The following reptiling will make data repeated.'
    #print 234234
    dataFile=open(filename+'.txt','w')
    runlogFile=open('runlog.txt','a')
    runlogFile.write('=============================================================\n')
    runlogFile.write('craw URL:'+url_to_craw+'\noperating time:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')
    runlogFile.write('check key:'+str(checkey)+'\n\n') 

    #登陆
    #weiboLogin = WeiboMain.WeiboLogin(account, pwd,proxyhttp=proxylist.nextProxy())

    WeiboMain.login(accountlist=accountlist,proxylist=proxylist,runlogFile=runlogFile)


    #get essential information such as amounts pages etc.
    while True:
	get_content_result=WeiboMain.get_content(url_to_craw,runlogFile,accountlist,proxylist)

	if get_content_result is not None:
	    break
	print '####get_content_result return None####'
	runlogFile.write('####get_content_result return None####\n')
	WeiboMain.login(accountlist=accountlist,proxylist=proxylist,runlogFile=runlogFile)
    htmlContent=get_content_result['content']
    #htmlContent=WeiboMain.get_content(url_to_craw,runlogFile,account,pwd,proxylist)['content']
    #repost_info=WeiboMain.get_info(htmlContent)
    #dataFile.write(htmlContent)
    #repost_info=WeiboMain.get_info(htmlContent,dataFile)

    #pattern=r'''<dd><a href=\\"\\\/.*?\\" title=\\"(.*?)\\" nick\-name=\\".*?\\" usercard=\\".*?\\"> .*?<\\\/a>.*?\s*<em>(.*?)<\\\/em>\s*<a href=.*?title=\\"(,*?)\\"'''
    #info=re.findall(pattern,sub_content)
    #print repost_info
    #dataFile.write(repost_info[0])
    pages=WeiboMain.get_amounts_pages(htmlContent)
    repost_time=time.strptime(WeiboMain.get_reposts_time(htmlContent),'%Y-%m-%d %H:%M')
    poname=WeiboMain.get_poname(htmlContent)
    potime=WeiboMain.get_po_time(htmlContent)
    #print 'poname=',poname,'\n'
    #poname=WeiboMain.character(poname)
    #print 'po'
    #print poname,'\n'
    cursor.execute("insert into %s (id,time,polvl) values ('%s','%s',%s)" % (filename,WeiboMain.character(poname),potime,0))
    
    if poname==None:
	print "####Warning!Can't find the poname."
	runlogFile.write("####Warning!Can't find the poname.\n")
	poname='Librian-'
    
    ####Some vars when reptiling.
    pagegap=1.5
    partgap=3.1
    denied=0
    proxyLine=5

    if pages>=0:  
	print "\n\nLogin sucess!"
	print str(pages)+' pages to craw'
	levellist=[10,20,30,40,50]
	crawlevel=0
	pre_time=time.clock()
	pagepoint=0
	status=True
	part=0
	pre_time=time.clock()
	while pagepoint<pages:
	    part+=1
	    status=True
	    for i in range(0,levellist[crawlevel]):
		url=url_to_craw+'&page='+str(pagepoint+i+1)
		if pagepoint+1>pages:
		    break
		while True:
		    get_content_result=WeiboMain.get_content(url,runlogFile,accountlist,proxylist)

		    if get_content_result is not None:
			break
		    print '####get_content_result return None####'
		    runlogFile.write('####get_content_result return None####\n')
		    WeiboMain.login(accountlist=accountlist,proxylist=proxylist,runlogFile=runlogFile)
		htmlContent=get_content_result['content']
		if get_content_result['good']==False:
		    denied+=1
		status=get_content_result['good']&status
		WeiboMain.get_info(htmlContent,dataFile,cursor=cursor,filename=filename,poname=poname)
		conn.commit()
		
		#### ==========TimeControl

		if(time.localtime()[3]==pauseTime['hour'] and time.localtime()[4]==pauseTime['minute']):
		    print 'Time to Wait'
		    while False:
			time.sleep(30)
			if time.localtime()[3]==startTime['hour'] and time.localtime()[4]==startTime['minute']:
			    print 'Start again'
			    break
	    
	    now_time=time.clock()
	    strtime=time.localtime(time.time())
	    if strtime[4]<30:
		index_for_statics=strtime[3]*2
	    else:
		index_for_statics=strtime[3]*2+1
	    statics['pages'][index_for_statics]+=levellist[crawlevel]
	    statics['time'][index_for_statics]+=(now_time-pre_time)/60	    
	    runlogFile.write('第'+str(part)+'部分:起始页'+str(pagepoint)+' 步长'+str(levellist[crawlevel])+'页'\
	                     +' 用时'+str(now_time-pre_time)+'seconds'\
	                     +' Proxy:'+proxylist.getProxy()\
	                     +' time:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')
	    print '第'+str(part)+'部分:起始页'+str(pagepoint)+' 步长'+str(levellist[crawlevel])+'页'\
	          +' 用时'+str(now_time-pre_time)+'seconds'\
	          +' Proxy:'+proxylist.getProxy()\
	          +' time:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	    pre_time=now_time
	    pagepoint+=levellist[crawlevel]
	    if status==True:
		if crawlevel==4:
		    pass
		else:
		    crawlevel+=1
	    else:
		crawlevel=0
	    if denied>=proxyLine:
		print '####deniedOverflow####    '+proxylist.getProxy()
		runlogFile.write('####denideOverflow####    '+proxylist.getProxy())
		WeiboMain.login(accountlist=accountlist,proxylist=proxylist,runlogFile=runlogFile) 
		#weiboLogin=WeiboMain.WeiboLogin(account, pwd,proxyhttp=proxylist.nextProxy())
		#weiboLogin.Login()
		#print '####changeProxy####    '+proxylist.getProxy()+'\n'
		#runlogFile.write('####changeProxy####    '+proxylist.getProxy()+'\n')
		denied=0


	    time.sleep(partgap)
	    #if i%100==0:
		    #now_time=time.clock()
		    #runlogFile.write('第'+str(i//100)+'个一百页 用时'+str(now_time-pre_time)+'seconds  time:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')
		    #print '第'+str(i//100)+'个一百页 用时'+str(now_time-pre_time)+'seconds  time:'+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		    #pre_time=now_time
		    #time.sleep(pagegap)
	    #url=url_to_craw+'&page='+str(i+1)
	    #print url
	    #htmlContent=WeiboMain.get_content(url,runlogFile)
	    #contents=htmlContent.split('<!--转发列表-->')
	    #subContent=contents[1]
	    #pattern=r'''<dd><a href=\\"\\\/.*?\\" title=\\"(.*?)\\" nick\-name=\\".*?\\" usercard=\\".*?\\"> .*?<\\\/a>.*?\s*<em>(.*?)<\\\/em>\s*<a href=.*?title=\\"(,*?)\\"'''
	    #WeiboMain.get_info(htmlContent,dataFile)
    else:
	pass
    dataFile.close()
    conn.commit()
    cursor.close()

    os.chdir(origdir)

    endtime=time.clock()
    time_running=seconds_to_hms(endtime-starttime)
    runlogFile.write('crawing\nrunning time is '+str(time_running['hour'])+' hours'+str(time_running['minute'])+' minutes'+str(time_running['seconds'])+' seconds\n')
    print 'crawing\nrunning time is '+str(time_running['hour'])+' hours'+str(time_running['minute'])+' minutes'+str(time_running['seconds'])+' seconds'


    