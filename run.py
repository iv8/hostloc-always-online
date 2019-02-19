# encoding=utf-8
import requests
from bs4 import BeautifulSoup
import re
import sys
import datetime
import time
import random

# 用户名
uid = 'useruid'
# 密码
pwd = 'userpwd'
# 休眠时间
sMin = time1
sMax = time2
# 新用户帖子数据
newuser = None
newthread = None
i = 1
http = requests.Session()
# 假装是 MacBook
http.headers.update({
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Accept-Language':"zh-CN,zh;q=0.8,ko;q=0.6,zh-TW;q=0.4"
})

def login():
    # 打开登陆界面
    res=http.get("https://www.hostloc.com/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login")
    match=re.search(r'name="formhash" value="(\S+)"',res.text)
    if(match):
        formhash=match.group(1)
    else:
        exit(0)
    # 登陆
    form={
        "formhash":formhash
        ,"referer":"https://www.hostloc.com/thread-12949-1-1.html"
        ,"loginfield":"username"
        ,"username":uid
        ,"password":pwd
        ,"questionid":0
        ,"answer":""
        ,"loginsubmit":"true"
    }
    res=http.post("https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LWKbr&inajax=1",data=form)
    match=re.search(r"'uid':'",res.text)
    return match

def getNew():
    global newuser, newthread
    newuser = http.get('https://www.hostloc.com/forum.php').text
    newuser = newuser[newuser.find(u'欢迎新会员: <em><a href="') + len(u'欢迎新会员: <em><a href="'): newuser.find(u'最新回复')]
    newuser = http.get('https://www.hostloc.com/' + newuser[0: newuser.find(u'" target')]).text
    newuser = int(newuser[newuser.find(u'<a id="domainurl" href="https://www.hostloc.com/?') + len(u'<a id="domainurl" href="https://www.hostloc.com/?'): newuser.find(u'" onclick="setCopy')])
    newthread = http.get('https://www.hostloc.com/forum.php?mod=guide&view=newthread').text
    newthread = newthread[newthread.find(u'<th class="common">'): newthread.find(u'<th class="common">') + 90]
    newthread = newthread[newthread.find(u'href="thread-') + len(u'href="thread-'): len(newthread)]
    newthread = int(newthread[0: newthread.find(u'-')])

getNew()

while True:
    res=http.post("https://www.hostloc.com/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LWKbr&inajax=1")
    match=re.search(r"'uid':'",res.text)
    if not match:
        if login():
            print("没有检测到登陆状态或者登陆超时，重新登录成功")
        else:
            # 如果配置无误, 依然提示登陆失败 可能公网 IP 封禁 或者密码尝试失败太多次 休眠 15 分钟
            print("没有检测到登陆状态或者登陆超时，重新登录失败")
            time.sleep(15 * 60)
    tp = random.randint(1, 2)
    uri = ''
    if tp - 1 == 0:
        uri = "https://www.hostloc.com/?" + str(random.randint(1, newuser))
    else:
        uri = "https://www.hostloc.com/thread-" + str(random.randint(1, newthread)) + "-1-1.html"
    print('#' + str(i) + ':' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time() + 8 * 60 * 60)) + ' - 访问地址: ' + uri)
    i += 1
    if i % 10 == 0:
        getNew()
    http.get(uri)
    # 随机休眠 300 ～ 600 秒
    time.sleep(random.randint(sMin, sMax))
