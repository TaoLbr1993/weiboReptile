import urllib2
def testProxy(proxy):
    url='http://www.baidu.com'
    #url='http://www.baidu.com'

    proxy_support = urllib2.ProxyHandler({'http':proxy})#
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

    urllib2.install_opener(opener)
    try:
        html=urllib2.urlopen(url).read()
    except:
        return False
    return True
