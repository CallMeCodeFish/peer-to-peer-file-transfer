代码文件:
    activepeer.py
    registration.py
    func.py

#clientAsclient.py 是我写的简要的client短的代码，做测试用的

#p2p-pi/1.0协议
#request的格式

client -> rs:

GET Register(Leave/PQuery/KeepAlive) P2P-DI/1.0
Date: time.ctime(time.time())
OS: Mac OS
[Cookie: int]
\r\n\r\n
请求主体...



#response的格式

rs -> client:

P2P-DI/1.0 200 OK
Date: time.ctime(time.time())
OS: Mac OS
[Set-cookie: int]
\r\n\r\n
192.168.1.1:8080
192.168.1.101:80
192.168.1.202:5000

