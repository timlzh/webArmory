---
title: 【CRYPTO】哈希长度拓展攻击
---

# 哈希长度扩展攻击

## Message Authentication Codes

> Message Authentication Codes (MACs)是用于验证信息真实性的算法。最简单的MAC算法是这样的：服务器把key和message连接到一起，然后用摘要算法如`MD5`或`SHA1`取出摘要。例如有一个网站，在用户下载文件之前需验证下载权限。这个网站会用如下的算法产生一个关于文件名的MAC： 
>
> ```
> def Create_MAC(key, filename)
>    	return Digest::MD5.hexdigest(key + filename)
> end
> ```
>
> 最终产生的URL会是这样的：
>
> ```
> http://www.example.com/download?file=test.pdf&mac=ca21cf672b66a5ee6fa7fc7c1c314ff3
> ```
>
> 当用户发起请求要下载一个文件时，会执行下面这个函数：
>
> ```
> def verify_mac(key, filename, userMAC)
>     	validMAC = create_MAC(key, filename)
>     	if (validMAC == userMAC) do
>         	initiateDownload()
>     	else
>         	displayError()
>     	end
> end
> ```
>
> 这样，只有当用户没有擅自更改文件名时服务器才会执行`initiateDownload()`开始下载。但是这种生成MAC的方式，会给攻击者在文件名后添加自定义的字符串留下隐患。 这种方法就是哈希长度拓展攻击。

## 简要介绍

> 哈希长度扩展攻击(Hash Length Extension Attacks)是指针对某些允许包含额外信息的加密散列函数的攻击手段。次攻击适用于`MD5`和`SHA-1`等基于`Merkle–Damgård`构造的算法。这类算法有个很有意思的问题：如果你知道message和MAC，只需要再知道key的长度，尽管key的值是你是不知道的，但是你能够再message后面添加信息并算出相应的MAC。

## 哈希与加密的区别

> 哈希（Hash）与加密最大的不同在于：
>
> 哈希将目标转换为具有相同长度的、不可逆的杂凑字符串；
>
> 加密则是将目标转化为不同长度的、可逆的密文，长度一般随明文增长而增加；

## 常用哈希算法的介绍

> 当前最常用的哈希算法有`MD5`、`SHA-1`、`SHA-2（SHA-224、SHA-256、SHA-384，和SHA-512并称为SHA-2）`等。

### MD5的加密过程

> - MD5加密过程中512bit（64byte）为一组，属于分组加密，在加密运算过程中，将512bit分为16块32bit，进行分块运算
> - MD5的填充，也叫补位，即对加密的字符串进行填充（bit第一位为1其余比特为0），使之（二进制）对 512 取模后的值为 448 ，即长度为512的倍数减64，最后的64位再补充为原来字符串的长度，这样刚好补满512位的倍数，如果当前明文正好是512bit的倍数则再加上一组512bit
> - MD5无论如何加密， 每一块加密得到的密文将作为下一次加密的初始向量IV

### SHA-1的加密过程

> - 当hash函数拿到需要被hash的字符串后，先将其字节长度对64取模。如果余数正好等于56，那么就在该字符串最后添加上8个字节的长度描述符（具体用bit表示）。如果不等于56，就先对字符串进行长度填充，填充时规定第一个字节为hex(80)，其余字节均用hex(00)填充，填充至余数为56以后，增加8个字节的长度描述符（该长度描述符为需要被hash的字符串的长度，不是填充之后整个字符串的长度）。以上流程，称为补位。
>
> - 补位完成后，字符串以64位一组进行分组（上面通过补位后的余数为56,加上8个字节的长度描述符后变为64位，刚好凑成一组）。字符串能被分成几组就会进行多少次”复杂的数学变化”。每次进行“复杂的数学变化”都会生成一组新的registers值供下一次“复杂的数学变化”来调用。第一次“复杂的数学变化”会调用程序中的默认值
>
> - 默认值一般为
>
>   ```
>   h0:67452301
>   h1:EFCDAB89
>   h2:988ADCFE
>   h3:10325476
>   h4:C3D2E1F0
>   ```
>
> - 当后面已经没有分组可以进行数学变化时，该组生成的registers值就是最后的hash值。
>
> - 在SHA-1的运算过程中，为确保同一个字符串的`SHA-1`值唯一，所以需要保证第一次registers的值也唯一。所以在`SHA-1`算法中，registers具有初始值。

### 填充步骤

> - 举个例子，计算字符串"admin"，它的十六进制为0x61646d696e，一共12位
> - 补位后的数据如下
>
> ```
> 0x61646d696e
> 8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002800000000000000
> ```
>
> - 2800000000000000描述加密字符串的长度，一共8个字节
> - 注意MD5运算的时候是小端序存储，假设我们最后8个字节的值为0000001234567890那么存储在MD5运算时的存储方式为9078563412000000，每两个字节构成一个十六进制并且按照逆序的顺序存储。“admin”的长度是40bit，所以长度为0x28=40bit

### 攻击步骤

> - 以MD5扩展攻击为例，假设我们需要`$COOKIE["key"]==md5($secret+$username+$password)`才能进入系统，已知$secret为12位的神秘字符串，$username和$password均为"admin"
> - 这时我们需要主动将 `$secret+”admin”+”admin”+第一组MD5填充`作为第一组明文，第二组明文为自定义的值， 同时我们利用已经知道的key作为我们构造的明文最后一块加密的初始向量IV，那么加密出来的结果应该和`$secret+”admin”+”admin”+第一组MD5填充+第二组明文`的MD5值一样
> - 前面的$secret我们只知道位数，于是补充上足够的位数即可，本文补充了12个1。
> - 于是MD5填充如下 ：
>
> ```
> 111111111111adminadmin + '\x80' + '\x00'*33 + '\xB0' + '\x00'*7
> ```
>
> - 这个时候是111111111111adminadmin加密填充后的内容，假设得到的MD5值为m，假设`$a=111111111111adminadmin`，我们构造`$b=hacker`作为加密$b时候的初始变量，那么就能够得到MD5($a+$b)
> - MD5进行运算的时候是小端序存储，设置VI值要遵循规则，比如我们得到的key值为 9ee0c5cb 6ee7ed13 37ffe75e 6e0b2a2a，那我们构造的初始VI值为
>
> ```
> A=0xcbc5e09e
> B=0x13ede76e
> C=0x5ee7ff37
> D=0x2a2a0b6e
> ```
>
> - 接着利用脚本就能够得到我们新的key值，构造出来的IV结果是和MD5加密的结果是一样

## 工具使用

[hash_extender](https://github.com/iagox86/hash_extender)

简要的使用说明

```
-d 被扩展的明文
-a 附加的到原来hash的padding
-l 盐的长度
-f 加密方式
-s 带盐加密的hash值
--out-data-format 输出格式
--quiet 仅输出必要的值
```



题目示例：

![img](/assets/wgpsec/images/hash-leng-extension/27.png)

>首先我们根据ctt函数反解出变量 s 为 adminadmin，即变量 role1 为 adminadmin
>
>然后 role 已知，url 解码后为 YVPweR3oRN;{nj32
>
>该类算法有一个特性，我们已知原文及密文和 key 长度，就可以直接在密文中替换内容，在不知道key的情况下生成新的密文

![71](/assets/wgpsec/images/hash-leng-extension/71.png)

> 根据长度生成 role ，构造出符合规则的密文

![72](/assets/wgpsec/images/hash-leng-extension/72.png)

> 长度不同的时候

![73](/assets/wgpsec/images/hash-leng-extension/73.png)