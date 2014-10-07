#-*- coding:utf-8 –*-
import RepostMain
import time
import random
import sys
import WeiboMain
import testProxy
import urllib2
from selenium import webdriver


def getProxys():
    proxys_on_web=[]
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    #driver = webdriver.PhantomJS(executable_path='E:\Phantomjs')
    driver=webdriver.PhantomJS()
    print 1
    proxys_url=u'http://pachong.org/area/city/name/%E9%A6%99%E6%B8%AF.html'
    driver.get(proxys_url)
    print 2
    #driver.open()
    
    result=driver.find_element_by_class_name('tb').text
    #driver.quit
    #print result
    #content=urllib2.urlopen(url=proxys_url).read()
    
    #proxytestfile=open('testProxy.txt','w')
    #proxytestfile.write(content)
    #proxytestfile.close()
    print 3
    #print result
    records_list=result.split('\n')
    #print records_list
    for record in records_list[1:]:
        print record
        record_dic=content_to_dic(record)
        #print record_dic
        if record_dic['type']=='high':
           #or record_dic['type']=='transparent'\
            if record_dic['status']==u'空闲' or record_dic['status']==u'较忙':
                if testProxy(record_dic['ip']):
                    proxys_on_web.append(record_dic['ip'])
    print 4
    return proxys_on_web

def content_to_dic(record_con):
    temp=record_con.split(' ')
    dic={'ip':'http://'+temp[3]+':'+temp[4],'type':temp[9],'status':temp[10]}
    return dic

def testProxy(proxy):
    res=True
    pattern='''百度一下'''
    proxy_support = urllib2.ProxyHandler({'http':proxy})#
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    try:
        html=urllib2.urlopen('http://www.baidu.com').read()
    except:
        print '##Exception## Delete proxy:'+proxy
        res=False
        return res
    if html.find(pattern)==-1:
        print '##WrongContent Delete proxy:'+proxy
        res=False
    return res
if __name__=='__main__':
    print getProxys()
    