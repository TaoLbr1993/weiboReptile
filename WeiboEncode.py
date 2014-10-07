import urllib
import base64
import rsa
import binascii

def PostEncode(userName, passWord, serverTime, nonce, pubkey, rsakv,pcid='',door=''):
    "Used to generate POST data"

    encodedUserName = GetUserName(userName)
    encodedPassWord = get_pwd(passWord, serverTime, nonce, pubkey)
    postPara = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': encodedUserName,
        'service': 'miniblog',
        'servertime': serverTime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'sp': encodedPassWord,
        'encoding': 'UTF-8',
        'prelt': '115',
        'rsakv': rsakv,     
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META',
        'pcid': pcid,
        'door': door
    }
    postData = urllib.urlencode(postPara)
    return postData

def GetUserName(userName):
    "Used to encode user name"

    userNameTemp = urllib.quote(userName)
    userNameEncoded = base64.encodestring(userNameTemp)[:-1]
    return userNameEncoded


def get_pwd(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) 
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    passwd = rsa.encrypt(message, key) 
    passwd = binascii.b2a_hex(passwd) 
    return passwd

