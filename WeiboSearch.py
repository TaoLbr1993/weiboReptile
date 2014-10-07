import re
import json

def sServerData(serverData):
    "Search the server time & nonce from server data"

    p = re.compile('\((.*)\)')
    jsonData = p.search(serverData).group(1)
    data = json.loads(jsonData)
    serverTime = str(data['servertime'])
    nonce = data['nonce']
    pubkey = data['pubkey']#
    rsakv = data['rsakv']#
    pcid=data['pcid']
    print "========>Server time is:", serverTime
    print "========>Nonce is:", nonce
    print '========>pcid is:',pcid
    return serverTime, nonce, pubkey, rsakv,pcid

def sRedirectData(text):
    p = re.compile(r'location\.replace\([\'"](.*?)[\'"]\)')
    loginUrl = p.search(text).group(1)
    print 'loginUrl:',loginUrl
    return loginUrl
