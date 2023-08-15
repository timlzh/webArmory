---
title: 【网络基础】Web应用常识
date: 2020-8-12 20:02:00
---

# 服务端功能

> **HTTP请求主要使用3种方式向应用程序传送参数：**
> **GET、POST、Cookie**	这也是PHP的GPC中所保护的三种传参方式。
>
> 除了这些主要输入源，还能通过Referer、User-Agent等HTTP头传参。

**Web应用程序使用大量技术实现其功能：**

> 脚本语言：PHP (官方称其为世界上最流行的Web开发语言)
>
> Web应用程序平台：Java和ASP.NET (可用C#、VB.NET做开发)
>
> Web服务器：Apache、IIS、Tomcat、Netscape Enterprise
>
> 数据库：MySQL、MSSQL、Oracle
>
> 其它后端组件：如文件系统、基于SOAP的Web服务和目录服务

## JAVA平台

Java平台可在几种基础型操作系统上运行，Windows、Linux、Solaris

> **Enterprise Java Bean（EJB）**是一个相对重量级的软件组件，它将一个特殊业务功能的逻辑组合到应用程序中。
>
> EJB 旨在处理应用程序开发者必须解决的各种技术挑战，如交易完整性。
>
> **简单传统Java对象（Plain Old Java Object，POJO）**是一个普通的Java对象，以区别EJB之类的特殊对象
>
> POJO常用来表示那些用户自定义的、比EJB更简单更轻量级的对象及用在其它框架中的对象
>
> **Java Servlet** 是应用程序服务器中的一个对象，接受客户端HTTP请求并返回HTTP响应。
>
> Servlet可使用大量接口来促进应用程序开发
>
> **Java Web容器** 是一个为基于Java的Web应用程序提供运行时环境的平台或引擎
>
> Apache、Tomcat、WebLogic、JBoss都数据Java Web容器

**关键应用程序常用的组件包括：**

> 身份验证：JAAS、ACEGI
>
> 表示层：SiteMesh、Tapestry
>
> 数据库对象关系映射：Hibernate
>
> 日志：Log4J

如果能确定受攻击应用程序使用的开源软件包，渗透测试员就可以下载它进行代码审计攻击实验。

## Web服务

> 许多应用程序本质上就是一组后端Web服务的GUI前端。
>
> Web服务使用**简单对象访问协议**（SOAP）来交换数据。
>
> 通常SOAP使用HTTP传送消息，并使用XML格式表示数据

如果将用户提交的数据直接组合到后端SOAP消息中，就可能产生SOAP注入漏洞 (与SQL注入类似)

正常情况下，服务器会以Web服务描述语言（WSDL）公布可用的服务和参数。

攻击者可用soapUI之类的工具、基于已公布的WSDL文件创建示例请求

以调用Web服务，获得身份验证令牌、并随后提出任何Web请求

# 客户端功能

HTML、CSS、Javascript

**文档对象模型（documnet，DOM）**

DOM用于控制浏览器行为。

可以按id访问HTML元素，以编程的方式访问这些元素结构。

还可用于读取和更新当前URL和Cookie等数据。

浏览器DOM操纵是基于Ajax的应用程序采用的关键技术。

**Ajax：**是一组编程技术，用于流畅的页面交互，发送异步请求（不一定要发异步请求）

**JSON (Javascript 对象表示法)：**用于对任意数据进行序列化的简单数据交换格式。Ajax经常使用JSON代替原来的XML。

## 编码方案

> **URL编码：**%20-代表空格
>
> **Unicode编码：**%u为前缀，%u2215代表 /
>
> **HTML编码：**`&lt;`代表< 	`&gt;`代表>  **可以用他们的十进制ASCII码编码** `&#x22代表"` `&#x27;代表'`
>
> **Base64编码：**仅用一个可打印的ASCII字符就可以安全转换任何二进制数据，常对电子邮件附件进行编码
>
> **十六进制编码(Hex)：**0x7e代表~

## 远程和序列化框架

> Flex和AMF
>
> Silverlight和WCF
>
> java序列化对象
>
> Shrios