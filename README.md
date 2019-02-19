# hostloc-always-online
全天 24 小时 [hostloc](https://www.hostloc.com/) 在线

## Easy
``` bash
docker run -e UID=xxx -e UPWD=xxx i0923/hostloc
```

## Strong
``` bash
docker run -d --restart=always --name=hostloc -e UID=xxx -e UPWD=xxx -e SMIN=300 -e SMAX=600 i0923/hostloc
```

## Config
- UID hostloc 登录名
- UPWD hostloc 登录密码
- SMIN, SMAX 保持在线随机时间
