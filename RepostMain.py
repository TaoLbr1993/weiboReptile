#-*- coding:utf-8 –*-
#####新浪微博爬虫
#####转发抓取
import WeiboMain
from WeiboMain import Proxy
import urllib2
import re
import sys
import os
import time
import pylab as pl



            
def seconds_to_hms(seconds):
            hour=int(seconds/3600)
            minute=int(seconds-hour*3600)/60
            second=int(seconds-hour*3600-minute*60)
            result={'hour':hour,'minute':minute,'seconds':second}
            return result


def RepostMain(accountlist,url_to_craw,checkey,figure,proxylist):
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
            newdir=os.path.join(origdir,userid)
            if os.path.isdir(newdir):
                    pass
            else:
                    os.mkdir(userid)
            os.chdir(newdir)
            
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
                                                            WeiboMain.get_info(htmlContent,dataFile)
                                            now_time=time.clock()
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




            endtime=time.clock()
            time_running=seconds_to_hms(endtime-starttime)
            runlogFile.write('crawing\nrunning time is '+str(time_running['hour'])+' hours'+str(time_running['minute'])+' minutes'+str(time_running['seconds'])+' seconds\n')
            print 'crawing\nrunning time is '+str(time_running['hour'])+' hours'+str(time_running['minute'])+' minutes'+str(time_running['seconds'])+' seconds'


            #sss='''
            #画图
            #from datatime import datetime
            imagepercent=0.5
            gap=3600
            #print '画图部分'
            #runlogFile.write('画图部分')
            xs=30
            percent=0.5
            
            pattern_time=re.compile(r'\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}')
            starttime=time.clock()

            dataFile=open(filename+'.txt','r')
            times=list()
            for line in open(filename+'.txt'):
                            line=dataFile.readline()
                            #print line
                            result=pattern_time.search(line)
                            #print result
                            if result is not None:
                                            struct_time=result.group(0)
                                            #print struct_time
                                            times.append(time.mktime(time.strptime(struct_time,'%Y-%m-%d %H:%M')))

            subtimes=int(len(times)*(1-percent))
            print '####debug####'+time.strftime('%Y-%m-%d %H:%M',time.localtime(times[0]))
            print '####debug####'+time.strftime('%Y-%m-%d %H:%M',time.localtime(times[-1]))
            print '####debug####'+str(((times[0]-times[-1])*imagepercent))
            #gap=int((((times[0]-times[-1])*imagepercent)/xs)/1800)*1800
            xs=int(((times[0]-times[-1])*imagepercent)/gap)
            xprintstep=int(xs/5)
            begintime=int(times[-1])/gap*gap
            #print time.ctime(begintime)
            endtime=(int(times[0])/gap+1)*gap
            
            records=len(times)
            record_temp=0
            x_time=list()
            x_print=list()
            temp=0
            for i in range(begintime,endtime,gap):
                            x_time.append((i))
                            if temp%xprintstep==0:
                                            #x_print.append(time.strftime('%H:%M\n%mm%dd',time.localtime(i)))
                                            if temp==0 or (int(i-57600)%(24*3600))<(3*gap):
                                                     x_print.append(time.strftime('%H:%M\n%m/%d',time.localtime(i)))
                                            else:
                                                     x_print.append(time.strftime('%H:%M',time.localtime(i)))
                            else:
                                            x_print.append('')
                            temp+=1
                            #if time.localtime(i)[3]==0:
                                     # x_print.append(time.strftime('%mm%dd%Hh',time.localtime(i)))
                            #else:
                                     # x_print.append(time.strftime('%Hh',time.localtime(i)))
                            #print time.ctime(i)+' '+time.strftime('%Hh',time.localtime(i))
            y_repost=[0 for i in range(begintime,endtime,gap)]
            #print len(y_repost)
            reposts_amounts=0
            for reptime in times:
                            y_repost[int((reptime-begintime)/gap)]+=1
                            reposts_amounts+=1
            for rep_time in times:
                            record_temp+=1
                            #print record_temp
                            if record_temp>subtimes:
                                            break
            pl.figure(figure)
            #for i in range(0,xs):
                            #print str(x_print[i])+' '+str(y_repost[i])
            #for i in range(len(x_time)):
                            #print str(x_time[i])+' '+str(y_repost[i])+'\n'
            #print x_time[0]
            #print x_time[-1]
            #print len(x_time)
            #print len(y_repost)
            pl.plot(x_time[0:xs],y_repost[0:xs])
            pl.xticks(x_time[0:xs],x_print[0:xs],color='red')
            #print time.strftime('%Y-%m-%d %H:%M',time.gmtime(times[record_temp]))
            #print len(times)
            #print record_temp
            #print times[0]
            #print times[-1]
            #print times[record_temp]
            seconds_percent=times[record_temp]-times[-1]
            seconds_all=times[0]-time.mktime(repost_time)
            time_percent=seconds_to_hms(seconds_percent)
            time_all=seconds_to_hms(seconds_all)
            runlogFile.write('\n\n达指定百分比所花时间'+str(time_percent['hour'])+'hours '+str(time_percent['minute'])+'minutes '+str(time_percent['seconds'])+'seconds\n')
            print '\n\n达指定百分比所花时间'+str(time_percent['hour'])+'hours '+str(time_percent['minute'])+'minutes '+str(time_percent['seconds'])+'seconds'
            runlogFile.write('总时间'+str(time_all['hour'])+'hours '+str(time_all['minute'])+'minutes '+str(time_all['seconds'])+'seconds\n')
            print '总时间'+str(time_all['hour'])+'hours '+str(time_all['minute'])+'minutes '+str(time_all['seconds'])+'seconds'
            runlogFile.write('所占比例'+str(seconds_percent/seconds_all)+' \n')
            print '所占比例'+str(seconds_percent/seconds_all)
            endtime=time.clock()
            time_running=seconds_to_hms(endtime-starttime)
            runlogFile.write('painting part\nrunning time is '+str(time_running['hour'])+'hours'+str(time_running['minute'])+'minutes'+str(time_running['seconds'])+'seconds\n')
            print 'painting part\nrunning time is '+str(time_running['hour'])+'hours'+str(time_running['minute'])+'minutes'+str(time_running['seconds'])+'seconds'
            all_repost_image=0
            for i in range(0,xs):
                            if i>=len(y_repost):
                                            break
                            all_repost_image+=y_repost[i]
            runlogFile.write(str(all_repost_image)+' reposts printed in image\n')
            print str(all_repost_image)+' reposts printed in image\n'

            pl.grid(True)

            pl.savefig(filename+'.png')
            #pl.show()
            dataFile.close()
            runlogFile.close()
            os.chdir(origdir)
