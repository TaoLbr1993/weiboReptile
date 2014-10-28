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



time.clock()
starttime=time.clock()
filename='Bf15DpocM'
#sss='''
#画图
#from datatime import datetime
imagepercent=0.5
gap=1800
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
