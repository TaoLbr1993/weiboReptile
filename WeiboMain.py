#-*- coding:utf-8 –*-

import urllib2
import cookielib
import re
import WeiboEncode
import WeiboSearch
import string
import time
import os
import urllib

class Proxy:
    def __init__(self):
        self.list=[]
        self.point=-1
    def add(self,s):
        self.list.append(s)
        
    def nextProxy(self):
        self.point+=1
        if self.point>=len(self.list):
            self.point=0
        return self.list[self.point]
    def record(self,dataFile):  
        dataFile.write('Proxy:'+self.list[self.point]+'\n')
        print 'Proxy:'+self.list[self.point]
    def getProxy(self):
        return self.list[self.point]
    def delProxy(self):
        del self.list[self.point]
        self.point-=1
        if(self.point<0):
            self.point=len(self.list)-1

class Account:
    def __init__(self):
        self.list=[]
        self.point=-1
    def add(self,s):
        self.list.append(s)
    
    def next(self):
        self.point+=1
        if self.point==len(self.list):
            self.point=0
        return self.list[self.point]
    def record(self,dataFile):
        dataFile.write('Account:'+self.list[self.point]+'\n')
        print 'Account:'+self.list[self.point]
    def getAccount(self):
        return self.list[self.point]
    
    
class WeiboLogin:
    def __init__(self, user, pwd,proxyhttp,enableProxy = True):
        print "Initializing WeiboLogin..."
        self.userName = user
        self.passWord = pwd
        self.enableProxy = enableProxy
        self.proxyhttp=proxyhttp
        #self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="+WeiboEncode.GetUserName(user)+"&rsakt=mod&client=ssologin.js(v1.4.11)&_="+str(time.time()*1000)
        self.serverUrl='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683'
        self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
        #self.loginUrl='http://login.sina.com.cn/signup/signin.php?entry=sso'
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',\
                           'Referer':'http://www.cnbeta.com/articles'}

    def Login(self):
            print '====LoginInformation======================='
            self.EnableCookie(self.enableProxy)
            serverTime, nonce, pubkey, rsakv,pcid = self.GetServerTime()#
            print '========>GetServerTime Finished'
            postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)#
            print "========>Post data length:", len(postData)

            req = urllib2.Request(self.loginUrl, postData, self.postHeader)
            print "========>Posting request..."
            result = urllib2.urlopen(req,timeout=30)#
            text = result.read()
            #print 'text='+text
            retcode=getRetcode(text)
            reason=getReason(text)
            verifyCode=''
            while retcode!=0:
                print 'retcode=',retcode
                print 'reason:',reason
                if retcode==-1:
                    print 'unknown error'
                    return False
                if retcode==4049 or retcode==2070:
                    return False
                    #imageurl='http://login.sina.com.cn/cgi/pin.php?r=53324&s=0&p='+pcid
                    #image=urllib2.urlopen(imageurl)
                    #imageFile=open('check.png','wb')
                    #imageFile.write(image.read())
                    #imageFile.close()
                    #print 'image path:'+os.getcwd()+'\check.png'
                    #verifyCode=raw_input(u'请输入验证码image path:'+os.getcwd()+'\check.png\n')
                if retcode==4040:
                    return False
                postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv,pcid,verifyCode)
                req=urllib2.Request(self.loginUrl,postData,self.postHeader)
                result=urllib2.urlopen(req,timeout=30)
                text=result.read()
                retcode=getRetcode(text)
                reason=getReason(text)
                print 'retcode',retcode
            try:
                loginUrl = WeiboSearch.sRedirectData(text)#
                urllib2.urlopen(loginUrl,timeout=40)
            except:
                print 'Login error!'
                return False

            #print 'Login sucess!'
            return True

    def EnableCookie(self, enableProxy):
        "Enable cookie & proxy (if needed)."

        cookiejar = cookielib.LWPCookieJar()#
        cookie_support = urllib2.HTTPCookieProcessor(cookiejar)

        if enableProxy:
            proxy_support = urllib2.ProxyHandler({'http':self.proxyhttp})#
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
            print "========>Proxy enabled"
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

        urllib2.install_opener(opener)#

    def GetServerTime(self):
        "Get server time and nonce, which are used to encode the password"

        print "========>Getting server time and nonce..."
        serverData = urllib2.urlopen(self.serverUrl,timeout=30).read()#
        print '========>'+serverData

        try:
            serverTime, nonce, pubkey, rsakv,pcid = WeiboSearch.sServerData(serverData)#
            return serverTime, nonce, pubkey, rsakv,pcid
        except:
            print '========>Get server time & nonce error!'
            return None


    
################################################################
#####some functions to analyse the source codes
def get_amounts_pages(content):#return amounts of pages according content(source codes)
    #print mycontent
    pages=re.findall(r'''action\-type=\\"feed_list_page\\">(.*?)<\\\/a>''',content)
    #print pages
    try:
        return string.atoi(pages[len(pages)-1])
    except IndexError,e:
        return -1
def get_info(content,data_file,cursor,filename):#get infomamtion according to content(source code) and put it into data_file
# 

    all_contents=content.split('<!--转发列表-->')
    sub_content=all_contents[1]
    contents=re.split(r'<dd>',sub_content)
    #print contents[5]
    pattern=re.compile(r'''<a href=\\"\\\/.*?\\" title=\\"(.*?)\\".*?<\\\/a>.*?<em>(.*?)<\\\/em>[\s\S]*?\\" title=\\"([0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2})\\"''')
    for con in contents[::]:
        #con=contents[conindex]
        result=pattern.search(con)
        if result is not None:
            name=result.group(1)
            contents=result.group(2)
            time=result.group(3)
            try:
                if isinstance(name,unicode):
                    #print 'name-->unicode'
                    final_name=name.encode('gb2312')
                else:
                    #print 'name-->not unicode'
                    final_name=name.decode('utf-8').encode('cp936')
            except UnicodeEncodeError,e:
                #print 'name-->error'
                final_name='Warning!InvalidString'
            try:
                if isinstance(contents,unicode):
                    #print 'contents-->unicode'
                    final_contents=contents.encode('gb2312')
                else:
                    #print 'contents-->not unicode'
                    final_contents=contents.decode('utf-8').encode('cp936')
            except UnicodeEncodeError,e:
                #print 'contents-->error'
                final_contents='Warning!InvalidString'
            try:
                if isinstance(time,unicode):
                    #print 'time-->unicode'
                    final_time=time.encode('gb2312')
                else:
                    #print 'time-->not unicode'
                    final_time=time.decode('utf-8').encode('cp936')
            except UnicodeEncodeError,e:
                #print 'time-->error'
                final_time=time
            #print result.group(1).decode('utf-8').encode('cp936')
            #data_file.write(final_name+' # '+final_time+' # '+final_contents+' \n')
            #data_file.write('##################\n')            
            sqlCommand='insert into '+filename+'(id,time,content) values(%s,%s,%s);'
            param=(final_name,final_time,final_contents)
            #cursor.execute('set names gbk;')
            n=cursor.execute(sqlCommand,param)

            #n to be used later
        #data_file.write(record[0]+' '+record[1]+' '+record[2]+'\n')
    #info=re.findall(pattern,sub_content)

def get_reposts_time(content):
    pattern=re.compile(r'''class=\\"S_link2 WB_time\\" title=\\"(\d{4}\-\d{2}\-\d{2} \d{2}:\d{2})\\"''')
    result=pattern.search(content)
    return result.group(1)

def get_content(url,runlogFile,accountlist,proxylist):
    good=True
    urlerror=False
    wait_list_min=[0.1,0.5,1.2,2.3,3.55,5.1,10.2,14.9,20.4,24.7,29.9,60.3,89.8,120,150.1,178,1]
    htmlContent=''
    for i in wait_list_min:
        try:
            htmlContent=urllib2.urlopen(url,timeout=30).read()
        except Exception,e:
            good=False
            urlerror=True
            runlogFile.write('###Exception###sleep '+str(i)+'minutes when get '+url+'\n')
            print '###Exception###sleep '+str(i)+'minutes when get '+url
            print 'Trying to relogin'
            #weiboLogin=WeiboLogin(user,pwd,proxyhttp=proxylist.nextProxy())
            #weiboLogin.Login()
            login(accountlist,proxylist,runlogFile)
        pattern_forbadden=re.compile(r'''(上一页|下一页)''')
        result=pattern_forbadden.search(htmlContent)
        if result is not None:
            return {'content':htmlContent,'good':good,'urlerror':urlerror}
        else:
            good=False
            urlerror=False
            runlogFile.write('###WrongContent###sleep '+str(i)+'minutes when get '+url+'\n')
            print '###WrongContent###sleep '+str(i)+'minutes when get '+url
            #print htmlContent
            time.sleep(i*60)
        

def relogin(user,pwd,proxylist,runlogFile):
    while True:
        weiboLogin=WeiboLogin(user,pwd,proxyhttp=proxylist.nextProxy())
        print '####change Proxy####    '+proxylist.getProxy()
        runlogFile.write('####change Proxy####    '+proxylist.getProxy()+'\n')    
        try:
            weiboLogin.Login()
        except Exception,e:
            print '####Login Error####    '+proxylist.getProxy()
            runlogFile.write('####Login Error####    '+proxylist.getProxy()+'\n')
            continue
        
        content=urllib2.urlopen('http://weibo.com/1855335174/B96RtlApL?type=repost',timeout=30).read()
        pattern=re.compile(r'''下一页''')
        result=pattern.search(content)
        if result is not None:
            break
        else:
            print '####Login Failed####    '+proxylist.getProxy()
            runlogFile.write('####Login Failed####    '+proxylist.getProxy()+'\n')

def login(accountlist,proxylist,runlogFile):
    while True:
        account=accountlist.next()
        username=account['username']
        
        weiboMain=WeiboLogin(username,account['pwd'],proxyhttp=proxylist.nextProxy())
        print '####login####    '+'username:'+username+'   proxy:'+proxylist.getProxy()
        runlogFile.write('####login####    '+'username:'+username+'   proxy:'+proxylist.getProxy()+'\n')
        try:
            result=weiboMain.Login()
        except Exception,e:
            print '####Login Error|Delete Proxy####    '+'username:'+username+'   proxy:'+proxylist.getProxy()
            runlogFile.write('####Login Error|Delete Proxy####    '+'username:'+username+'   proxy:'+proxylist.getProxy()+'\n')
            #proxylist.delProxy()
            continue
        if(result==False):
            print '####Login Exception|Delete Proxy####    '+'username:'+username+'    proxy:'+proxylist.getProxy()
            runlogFile.write('####Login Exception|Delete Proxy####    '+'username:'+username+'   proxy:'+proxylist.getProxy()+'\n')
            #proxylist.delProxy()
            continue
        try:
            content=urllib2.urlopen('http://weibo.com/1855335174/B96RtlApL?type=repost',timeout=30).read()
        except Exception:
            print '####CheckException####    '+'username:'+username+'    proxy:'+proxylist.getProxy()
            runlogFile.write('####CheckException####    '+'username:'+username+'    proxy:'+proxylist.getProxy()+'\n')
            #proxylist.delProxy()
            continue
        pattern=re.compile(r'''下一页''')
        result=pattern.search(content)
        if result is not None:
            break
        else:
            print '####Login Failed####    '+'username:'+username+'   proxy:'+proxylist.getProxy()
            runlogFile.write('####Login Failed####    '+'username:'+username+'   proxy:'+proxylist.getProxy()+'\n')  
            #proxylist.delProxy()
            
            
            
def getRetcode(s):
    pattern_1=re.compile(r'retcode=(\d*)')
    pattern_2=re.compile(r'\"retcode\"\:(\d*)')
    result=pattern_1.search(s)
    if result is not None:
        #print '###############'
        #print result
        #print result.group(1)
        retcode=string.atoi(result.group(1))
    else:
        result=pattern_2.search(s)
        #print '324234234324'
        #print result
        #print result.group(1)
        if result==None:
            return -1
        retcode=string.atoi(result.group(1))
    return retcode

def getReason(s):
    pattern=re.compile(r'reason=(.*?)\"')
    result=pattern.search(s)
    if result is not None:
        reason=result.group(1)
        return urllib.unquote(reason)
    else:
        return None
if __name__ == '__main__':
    weiboLogin = WeiboLogin('', '')
    if weiboLogin.Login() == True:
        print "login sucess!"
    myurl='http://weibo.com/1764590687/BbHcy7uI6?mod=weibotime&type=repost'
    htmlContent=urllib2.urlopen(myurl).read()
    testFile=open('test.txt','w')
    testFile.write(htmlContent)
    print get_reposts_time(htmlContent)
    
