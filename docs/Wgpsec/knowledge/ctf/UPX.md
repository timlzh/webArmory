---
title: 【RE】UPX
---



## UPX原理

UPX本质是压缩程序代码，减少程序体积，属于压缩壳

它是用命令行方式操作的可执行文件压缩程序，兼容性和稳定性好

具有特征码：

**55 50 58 UPX**

![image-20210908215205809](/assets/wgpsec/images/UPX/image-20210908215205809.png)

UPX在内存中的样子

![image-20210908214726938](/assets/wgpsec/images/UPX/image-20210908214726938.png)

来看看汇编代码

![image-20210910204739595](/assets/wgpsec/images/UPX/image-20210910204739595.png)

一开始停在PUSHAD这，将EAX~EDI寄存器的值保存到栈

将第二节区的地址（rmvbfix.004F1000=004F1000）放到esi

将第一节区的地址地址（dword ptr ds:[esi-0xF0000]=00489080）放到edi

![image-20210910091527233](/assets/wgpsec/images/UPX/image-20210910091527233.png)

感觉这也算特征

## UPX脱壳

先查壳

![image-20210910204643364](/assets/wgpsec/images/UPX/image-20210910204643364.png)

### 方法一 单步跟踪

OD在载入

![image-20210910204739595](/assets/wgpsec/images/UPX/image-20210910204739595.png)

一步一步跟踪，一直让程序向下跳转

遇到向上的跳转时

在跳转的下一行 F4 运行到该位置

一直到出现

![image-20210910205441044](/assets/wgpsec/images/UPX/image-20210910205441044.png)

popad和一个较大的跳转

popad指令则是pushad指令的逆操作。popad指令按照与上面相反的顺序依次弹出寄存器的值。

顺序为 **EDI,ESI,EBP,ESP,EBX,EDX,ECX,EAX.**

下面就直接跳转到了OEP

![image-20210910205737034](/assets/wgpsec/images/UPX/image-20210910205737034.png)

然后借助工具在入口处右键 ![image-20210910213205992](/assets/wgpsec/images/UPX/image-20210910213205992.png)（记录一下正确的入口 7738C

![image-20210910210041820](/assets/wgpsec/images/UPX/image-20210910210041820.png)

可以用方式1，也可以用方式2脱壳

### 方法二 ESP定律法

ESP定理脱壳（ESP在OD的寄存器中，我们只要在命令行下ESP的硬件访问断点，就会一下来到程序的OEP了！） 

1.开始就点F8，注意观察OD右上角的寄存器中ESP有没突现（变成红色）。（这只是一般情况下，更确切的说我们选择的ESP值是关键句之后的第一个ESP值） 

2.在命令行下：dd XXXXXXXX(指在当前代码中的ESP地址，或者是hr XXXXXXXX)，按回车！ 

3.选中下断的地址，断点--->硬件访--->WORD断点。 

4.按一下F9运行程序，直接来到了跳转处，按下F8，到达程序OEP。 

### 方法三 内存镜像法

1：用OD打开软件！ 

2：点击选项——调试选项——异常，把里面的忽略全部√上！CTRL+F2重载下程序！ 

3：按ALT+M,打开内存镜象，找到程序的第一个.rsrc.按F2下断点，然后按SHIFT+F9运行到断点，接着再按ALT+M,打开内存镜象，找到程序的第一个.rsrc.上面的.CODE（也就是00401000处），按F2下断点！然后按SHIFT+F9（或者是在没异常情况下按F9），直接到达程序OEP！ 

### **方法四 一步到达OEP** 

1.开始按Ctrl+F,输入：popad（只适合少数壳，包括UPX，ASPACK壳），然后按下F2，F9运行到此处 

2.来到大跳转处，点下F8，到达OEP！ 

### 方法五 模拟跟踪

查看内存包含SFX，imports，relocations的

tc eip< 地址

### 方法六 SFX

选项，调试设置

SFX

选方式



###UPX脱壳步骤总结

**查壳**(PEID、FI、PE-SCAN)--->**寻找**OEP(OD)--->**脱壳**/Dump(LordPE、PeDumper、OD自带的脱壳插件、PETools)--->**修复**(Import REConstructor) 





### 手动脱UPX壳

加壳是为了保护程序的逻辑，有一些壳可以用脱壳机脱掉，但是有一些强壳或者动过手脚的壳或者是自己写的壳，就不能被脱掉，壳相当于是加在代码外面的一层保护措施，可以理解为对程序资源的压缩，然后在运行的时候，会先运行外面的壳，然后才会运行内部的代码，接下来，手动脱一下upx壳



UPX的版本为3.91

![image-20211221200254137](/assets/wgpsec/images/UPX/15.png)



正常打开什么也看不到

![image-20211221200316345](/assets/wgpsec/images/UPX/16.png)



然后拖入OD

![image-20211221201805880](/assets/wgpsec/images/UPX/17.png)



F8单步执行，当ESP和EIP同时变红的时候，表示有数据压入了栈1中，这个时候数据跟随，只有他们两个是红色的,ESP为

![image-20211221202007271](/assets/wgpsec/images/UPX/18.png)



然后右键ESP的地址，数据窗口中跟随，可以看到地址就是前4个数据

![image-20211221202118500](/assets/wgpsec/images/UPX/19.png)



然后选中地址，右键---断点---硬件访问---word，然后F9运行，程序就运行到了这

![image-20211221202407016](/assets/wgpsec/images/UPX/20.png)



可以看到这里的汇编

```
push 0
cmp esp ,eax
jnz short Random.00378033
```



选择JNZ下面的这一行，然后F4，跳过判断

![image-20211221202739607](/assets/wgpsec/images/UPX/21.png)



然后F8继续运行，就到了push ebp这里

![image-20211221202829377](/assets/wgpsec/images/UPX/22.png)





重新运行了一遍，ESP为6FFD74

![image-20211221203917133](/assets/wgpsec/images/UPX/23.png)



![image-20211221204026259](/assets/wgpsec/images/UPX/24.png)



然后把已经存在的断点全部删除，点击调试---硬件断点，然后全部删除

![image-20211221204401302](/assets/wgpsec/images/UPX/25.png)





这就是OEP了，然后右键---用OLLDEBUG脱壳

![image-20211221204112360](/assets/wgpsec/images/UPX/26.png)



但是它显示了无法读取被调试的进程

![image-20211221204703732](/assets/wgpsec/images/UPX/27.png)



这个自带的dump不好使，所以重新使用x32dbg来脱壳

![image-20211221223957118](/assets/wgpsec/images/UPX/28.png)



和之前是一样的流程

![image-20211221224033578](/assets/wgpsec/images/UPX/29.png)



然后F9到达push 0的地方，然后F4跳过，到达oep处，然后点击插件，开始dump



![image-20211221224757300](/assets/wgpsec/images/UPX/30.png)



然后就成功脱壳了

![image-20211221224842938](/assets/wgpsec/images/UPX/31.png)



用ida打开也能看到正确的逻辑

![image-20211221224908829](/assets/wgpsec/images/UPX/32.png)



但是这个壳有点问题，不能调试

