---
title: '金山WPS Office远程堆损坏漏洞导致代码执行'
date: Sat, 12 Sep 2020 03:49:01 +0000
draft: false
tags: ['白阁-漏洞库']
---

#### 总览

WPS Office是由Microsoft珠海的中国软件开发商金山软件开发的办公套件，适用于Microsoft Windows，macOS，Linux，iOS和Android。WPS Office由三个主要组件组成：WPS Writer，WPS Presentation和WPS Spreadsheet。个人基本版本可以免费使用。WPS Office软件中存在一个远程执行代码漏洞，是当Office软件在分析特制Office文件时不正确地处理内存中的对象时引起的。成功利用此漏洞的攻击者可以在当前用户的上下文中运行任意代码。故障可能会导致拒绝服务。漏洞产品WPS Office，影响版本11.2.0.9453。

#### 漏洞分析

在WPS Office中用于图像格式解析的Qt模块中发现堆损坏。嵌入WPS office的特制图像文件可能会触发此漏洞。打开特制的文档文件时，触发访问冲突。EDX指向数组的指针，而EAX是指向数组的索引。```
0:000> g
(c50.b4): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=000000c0 ebx=006f1c48 ecx=cd2aefbc edx=cd2c6f80 esi=2ed7ae18 edi=0000001c
eip=6ba13321 esp=006f1b44 ebp=006f1b44 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00210202
QtCore4!QMatrix::dy+0x48a8:
6ba13321 8b448210        mov     eax,dword ptr [edx+eax*4+10h] ds:002b:cd2c7290=???????? 
```崩溃是如何触发的？让我们看一下PNG标头格式。```
00029E30  FF 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44  ÿ‰PNG........IHD
00029E40  52 00 00 02 80 00 00 01 C6 04 03 00 00 00 16 0A  R...€...Æ.......
00029E50  27 FC 00 00 00 04 67 41 4D 41 00 00 B1 88 95 98  'ü....gAMA..±ˆ•˜
00029E60  F4 A6 00 00 00 30 50 4C 54 45 00 00 00 80 00 00  ô¦...0PLTE...€..
00029E70  00 80 00 80 80 00 00 00 80 80 00 80 00 80 80 80  .€.€€...€€.€.€€€
00029E80  80 80 C0 C0 C0 FF 00 00 00 FF 00 FF FF 00 00 00  €€ÀÀÀÿ...ÿ.ÿÿ...
00029E90  FF FF 00 FF 00 FF FF FF FF FF 7B 1F B1 C4 00 00  ÿÿ.ÿ.ÿÿÿÿÿ{.±Ä.. 
```从偏移量0x29E31开始-0x29E34是PNG文件格式的签名标头。PNG头文件的结构：```
PNG signature --> IHDR --> gAMA --> PLTE --> pHYs --> IDAT --> IEND 
```在这种情况下，当WPS Office Suite中使用的QtCore库解析PLTE结构并触发堆破坏时，该漏洞位于Word文档中的嵌入式PNG文件中。在偏移量0x29E82到0x29E85处，调色板的解析失败，从而触发了堆中的内存损坏。崩溃触发之前的堆栈跟踪：```
00 00ee1790 6b8143ef QtCore4!path_gradient_span_gen::path_gradient_span_gen+0x6a71
01 00ee17f0 6b814259 QtCore4!QBrush::setMatrix+0x234
02 00ee58d4 6b8249a4 QtCore4!QBrush::setMatrix+0x9e
03 00ee58ec 6b80cc84 QtCore4!QImage::rect+0x22b
04 00ee5908 6b857ccc QtCore4!QTransform::inverted+0xec8
05 00ee629c 6b81c55b QtCore4!QSvgFillStyle::setFillOpacity+0x1b59
06 00ee6480 6b896844 QtCore4!QPainter::drawPixmap+0x1c98
07 00ee6574 6d1e0fbd QtCore4!QPainter::drawImage+0x325
08 00ee6594 6d0dd155 kso!GdiDrawHoriLineIAlt+0x11a1a 
```在QtCore4解析嵌入式图像之前，我们可以看到来自KSO模块的最后一次调用，试图处理图像kso！GdiDrawHoriLineIAlt。使用IDA Pro分解应用程序来分析发生异常的功能。最后的崩溃路径如下（WinDBG结果）：```
QtCore4!QMatrix::dy+0x48a8:
6ba13321 8b448210        mov     eax,dword ptr [edx+eax*4+10h] ds:002b:cd2c7290=???????? 
```在IDA Pro中打开时，我们可以按以下方式反汇编该函数：```
.text:67353315                 push    ebp
.text:67353316                 mov     ebp, esp
.text:67353318                 movzx   eax, byte ptr [ecx+edx]  ; crash here
.text:6735331C                 mov     ecx, [ebp+arg_0]
.text:6735331F                 mov     edx, [ecx]
.text:67353321                 mov     eax, [edx+eax*4+10h]
.text:67353325                 mov     ecx, eax 
```使用故障转储中的信息，我们知道应用程序在`0x67353321（移动eax，[edx + eax * 4 + 10h]）`处触发了访问冲突。我们可以看到EAX寄存器由0xc0值控制。因此，从这里我们可以根据导致异常的指令对寄存器的状态进行一些假设。需要注意的重要一点是，在发生异常之前，我们可以看到ECX（0xc0）中包含的值正在写入到以下指令所定义的任意位置：```
mov     ecx, [ebp+arg_0] 
```此外，我们注意到，在我们的故障指令之外，EBP的偏移量存储在ECX寄存器中。我们在前面提到的指令（偏移量为0x6ba1331c）上设置了一个断点，以观察内存。断点触发后，我们可以看到第一个值c45adfbc引用了另一个指针，该指针应该是指向数组的指针。```
Breakpoint 0 hit
eax=0000000f ebx=004f1b40 ecx=d3544100 edx=0000001c esi=d1200e18 edi=0000001c
eip=6ba1331c esp=004f1a34 ebp=004f1a34 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00200202
QtCore4!QMatrix::dy+0x48a3:
6ba1331c 8b4d08          mov     ecx,dword ptr [ebp+8] ss:002b:004f1a3c=c45adfbc

0:000> dc ebp+8
004f1a3c  c45adfbc 00000048 00000000 6f13830f  ..Z.H..........o
004f1a4c  004f5cc8 00000000 00000000 00000000  .\O.............
004f1a5c  00000000 004f65a0 004f662c 00000000  .....eO.,fO.....
004f1a6c  779eae8e 00000000 00000001 3f800000  ...w...........?
004f1a7c  3f800000 3f31e4f8 3f800000 3f800000  ...?..1?...?...?
004f1a8c  3f800000 3f31e4f8 3f800000 3de38800  ...?..1?...?...=
004f1a9c  3de38800 3d9e1c8a 3c834080 004f3c00  ...=...=.@.<.<O.
004f1aac  4101c71c 6ba13315 3f800000 4081c71c  ...A.3.k...?...@ 
```从c45adfbc观察内存引用，发现另一个指针。第一个值ab69cf80始终表示为指向它所引用的任何地方的指针。指针ab69cf80基本上是我们指针的索引数组。 0:000> dc c45adfbc```
c45adfbc  ab69cf80 d3544100 00000003 00000280  ..i..AT.........
c45adfcc  0000055a 00000012 c0c0c0c0 1c3870e2  Z............p8.
c45adfdc  40ad870e 1c3870e2 40ad870e 00000000  ...@.p8....@....
c45adfec  00000000 c0c0c0c1 6c1d12c0 00000000  ...........l....
c45adffc  c0c0c0c0 ???????? ???????? ????????  ....????????????
c45ae00c  ???????? ???????? ???????? ????????  ????????????????
c45ae01c  ???????? ???????? ???????? ????????  ????????????????
c45ae02c  ???????? ???????? ???????? ????????  ????????????????

0:000> dc ab69cf80
ab69cf80  00000001 0000001c 00000010 00000001  ................ // 0000001c is overwritten in the register EDX and EDI before we trigger crash
ab69cf90  ff000000 ff800000 ff008000 ff808000  ................ 
ab69cfa0  ff000080 ff800080 ff008080 ff808080  ................
ab69cfb0  ffc0c0c0 ffff0000 ff00ff00 ffffff00  ................ // ffc0c0c0 where it will be stored in EAX after crash, at the moment it only takes 0xf value in EAX
ab69cfc0  ff0000ff ffff00ff ff00ffff ffffffff  ................
ab69cfd0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................
ab69cfe0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................
ab69cff0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................ 
```因为我们知道崩溃的路径，所以我们可以使用下面的命令简单地设置一个断点。该命令将获得指针值“ edx + eax \* 4 + 10”，并检查其是否满足0xc0。```
bp 6ba13321 ".if (poi(edx+eax*4+10) == 0xc0) {} .else {gc}"

0:000> g
eax=000000c0 ebx=004f1b40 ecx=c45adfbc edx=ab69cf80 esi=d1200e18 edi=0000001c
eip=6ba13321 esp=004f1a34 ebp=004f1a34 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00200202
QtCore4!QMatrix::dy+0x48a8:
6ba13321 8b448210        mov     eax,dword ptr [edx+eax*4+10h] ds:002b:ab69d290=???????? 
```如果观察堆栈，可以看到以下执行：```
004f1a38 6ba3cb98 QtCore4!path_gradient_span_gen::path_gradient_span_gen+0x6a74
004f1a3c c45adfbc 
004f1a40 00000048 
004f1a44 00000000 
004f1a48 6f13830f verifier!DphCommitMemoryForPageHeap+0x16f
004f1a4c 004f5cc8 
004f1a50 00000000 
004f1a54 00000000 
004f1a58 00000000 
004f1a5c 00000000 
004f1a60 004f65a0 
004f1a64 004f662c 
004f1a68 00000000 
004f1a6c 779eae8e ntdll!RtlAllocateHeap+0x3e 
```如果我们反汇编6ba3cb98，则可以看到以下反汇编代码。真正的根本原因在于此代码。```
6ba3cb89 8b96b4000000    mov     edx,dword ptr [esi+0B4h]
6ba3cb8f 8b4df4          mov     ecx,dword ptr [ebp-0Ch]
6ba3cb92 52              push    edx
6ba3cb93 8bd7            mov     edx,edi
6ba3cb95 ff5580          call    dword ptr [ebp-80h]
6ba3cb98 8b4e7c          mov     ecx,dword ptr [esi+7Ch]


C pseudo code

grad = *(&ptr_grad);
if ( grad > 0.0099999998 )
{
   input_value = grad_size(check, size, input);
   ptr_grad = *(input);
   ... cut here ... 
```我们在6ba3cb89地址上设置断点，并观察ESI + 0xB4，我们可以看到一个指针指向另一个位置：```
0:000> r
eax=00000000 ebx=00791878 ecx=00000005 edx=00793938 esi=cb07de18 edi=0000001c
eip=6ba3cb89 esp=00791780 ebp=00791870 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00200202
QtCore4!path_gradient_span_gen::path_gradient_span_gen+0x6a65:
6ba3cb89 8b96b4000000    mov     edx,dword ptr [esi+0B4h] ds:002b:cb07decc=cf69afbc

0:000> dc esi+0B4h
cb07decc  cf69afbc c0c0c000 00000000 00000100  ..i.............
cb07dedc  c0c0c0c0 00000000 00000000 00000000  ................
cb07deec  00000000 00000000 00000000 00000000  ................
cb07defc  00000000 cf030fd0 00000000 00000000  ................
cb07df0c  00000000 00000000 00000000 00000000  ................
cb07df1c  c0c0c0c0 00000000 3ff00000 00000000  ...........?....
cb07df2c  00000000 00000000 00000000 00000000  ................
cb07df3c  00000000 00000000 3ff00000 00000000  ...........?....

0:000> dc cf69afbc
cf69afbc  c88baf80 d1326100 00000003 00000280  .....a2.........
cf69afcc  0000055f 00000012 c0c0c0c0 1c3870e2  _............p8.
cf69afdc  40ad870e 1c3870e2 40ad870e 00000000  ...@.p8....@....
cf69afec  00000000 c0c0c0c1 6c1d12c0 00000000  ...........l....
cf69affc  c0c0c0c0 ???????? ???????? ????????  ....????????????
cf69b00c  ???????? ???????? ???????? ????????  ????????????????
cf69b01c  ???????? ???????? ???????? ????????  ????????????????
cf69b02c  ???????? ???????? ???????? ????????  ????????????????

0:000> dc c88baf80
c88baf80  00000001 0000001c 00000010 00000001  ................
c88baf90  ff000000 ff800000 ff008000 ff808000  ................
c88bafa0  ff000080 ff800080 ff008080 ff808080  ................
c88bafb0  ffc0c0c0 ffff0000 ff00ff00 ffffff00  ................
c88bafc0  ff0000ff ffff00ff ff00ffff ffffffff  ................
c88bafd0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................
c88bafe0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................
c88baff0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................ 
```从这里我们可以知道代码实际上没有从指针释放任何东西。一旦移至EDX，EDX将保留指向索引数组的指针：```
eax=00000000 ebx=00791878 ecx=00000005 edx=cf69afbc esi=cb07de18 edi=0000001c
eip=6ba3cb8f esp=00791780 ebp=00791870 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00200202
QtCore4!path_gradient_span_gen::path_gradient_span_gen+0x6a6b:
6ba3cb8f 8b4df4          mov     ecx,dword ptr [ebp-0Ch] ss:002b:00791864=d1326100

0:000> dc cf69afbc
cf69afbc  c88baf80 d1326100 00000003 00000280  .....a2.........
cf69afcc  0000055f 00000012 c0c0c0c0 1c3870e2  _............p8.
cf69afdc  40ad870e 1c3870e2 40ad870e 00000000  ...@.p8....@....
cf69afec  00000000 c0c0c0c1 6c1d12c0 00000000  ...........l....
cf69affc  c0c0c0c0 ???????? ???????? ????????  ....????????????
cf69b00c  ???????? ???????? ???????? ????????  ????????????????
cf69b01c  ???????? ???????? ???????? ????????  ????????????????
cf69b02c  ???????? ???????? ???????? ????????  ????????????????

0:000> dc c88baf80
c88baf80  00000001 0000001c 00000010 00000001  ................
c88baf90  ff000000 ff800000 ff008000 ff808000  ................
c88bafa0  ff000080 ff800080 ff008080 ff808080  ................
c88bafb0  ffc0c0c0 ffff0000 ff00ff00 ffffff00  ................
c88bafc0  ff0000ff ffff00ff ff00ffff ffffffff  ................
c88bafd0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................
c88bafe0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................
c88baff0  c0c0c0c0 c0c0c0c0 c0c0c0c0 c0c0c0c0  ................ 
```崩溃后的堆栈跟踪：```
0:000> kvL
 # ChildEBP RetAddr  Args to Child              
00 012f18d4 6ba3cb98 cc53afbc 00000048 00000000 QtCore4!QMatrix::dy+0x48a8
01 012f19d0 6b8143ef 00000000 012f1b78 012f1a5c QtCore4!path_gradient_span_gen::path_gradient_span_gen+0x6a74
02 012f1a30 6b814259 0000002e 012f5bd0 00000000 QtCore4!QBrush::setMatrix+0x234
03 012f5b14 6b8249a4 0000003b 012f5b68 cc780e18 QtCore4!QBrush::setMatrix+0x9e
04 012f5b2c 6b80cc84 0000003b 012f5b68 cc780e18 QtCore4!QImage::rect+0x22b
05 012f5b48 6b857ccc 0000003b 012f5b68 cc780e18 QtCore4!QTransform::inverted+0xec8
06 012f64dc 6b81c55b 00000000 003c0000 00000000 QtCore4!QSvgFillStyle::setFillOpacity+0x1b59
07 012f66c0 6b896844 012f6724 cc818ff0 0000001c QtCore4!QPainter::drawPixmap+0x1c98
08 012f67b4 6d1e0fbd 012f69ec 012f66d4 012f6864 QtCore4!QPainter::drawImage+0x325
09 012f67d4 6d0dd155 012f6a54 012f69ec 012f6864 kso!GdiDrawHoriLineIAlt+0x11a1a
0a 012f67ec 6d0c8d88 012f69ec 012f68e0 012f6864 kso!kpt::PainterExt::drawBitmap+0x23 
```堆分析：```
0:000> !heap -p -a cc53afbc
    address cc53afbc found in
    _DPH_HEAP_ROOT @ 6731000
    in busy allocation (  DPH_HEAP_BLOCK:         UserAddr         UserSize -         VirtAddr         VirtSize)
                                cc36323c:         cc53afa8               58 -         cc53a000             2000
    6f13ab70 verifier!AVrfDebugPageHeapAllocate+0x00000240
    77a9909b ntdll!RtlDebugAllocateHeap+0x00000039
    779ebbad ntdll!RtlpAllocateHeap+0x000000ed
    779eb0cf ntdll!RtlpAllocateHeapInternal+0x0000022f
    779eae8e ntdll!RtlAllocateHeap+0x0000003e
    6f080269 MSVCR100!malloc+0x0000004b
    6f08233b MSVCR100!operator new+0x0000001f
    6b726c67 QtCore4!QImageData::create+0x000000fa
    6b726b54 QtCore4!QImage::QImage+0x0000004e
    6b7a0e21 QtCore4!png_get_text+0x00000436
    6b79d7a8 QtCore4!QImageIOHandler::setFormat+0x000000de
    6b79d457 QtCore4!QPixmapData::fromFile+0x000002bf
    6b725eb4 QtCore4!QImageReader::read+0x000001e2
    6d0ca585 kso!kpt::VariantImage::forceUpdateCacheImage+0x0000254e
    6d0c5964 kso!kpt::Direct2DPaintEngineHelper::operator=+0x00000693
    6d0c70d0 kso!kpt::RelativeRect::unclipped+0x00001146
    6d0c8d0c kso!kpt::VariantImage::forceUpdateCacheImage+0x00000cd5
    6d451d5c kso!BlipCacheMgr::BrushCache+0x0000049a
    6d451e85 kso!BlipCacheMgr::GenerateBitmap+0x0000001d
    6d453227 kso!BlipCacheMgr::GenCachedBitmap+0x00000083
    6d29bb92 kso!drawing::PictureRenderLayer::render+0x000009b6
    6d450fb1 kso!drawing::RenderTargetImpl::paint+0x00000090
    6d29b528 kso!drawing::PictureRenderLayer::render+0x0000034c
    6d2a2d83 kso!drawing::VisualRenderer::render+0x00000060
    6d2b8970 kso!drawing::SingleVisualRenderer::drawNormal+0x000002b5
    6d2b86a7 kso!drawing::SingleVisualRenderer::draw+0x000001e1
    6d2b945e kso!drawing::SingleVisualRenderer::draw+0x00000046
    6d3d0142 kso!drawing::ShapeVisual::paintEvent+0x0000044a
    680a2b5c wpsmain!WpsShapeTreeVisual::getHittestSubVisuals+0x000068f1
    6d0e36df kso!AbstractVisual::visualEvent+0x00000051
    6d3cbe97 kso!drawing::ShapeVisual::visualEvent+0x0000018f
    6d0eba90 kso!VisualPaintEvent::arriveVisual+0x0000004e

0:000> dt _DPH_BLOCK_INFORMATION cc780e18-0x20
verifier!_DPH_BLOCK_INFORMATION
   +0x000 StartStamp       : 0xc0c0c0c0
   +0x004 Heap             : 0xc0c0c0c0 Void
   +0x008 RequestedSize    : 0xc0c0c0c0
   +0x00c ActualSize       : 0xc0c0c0c0
   +0x010 Internal         : _DPH_BLOCK_INTERNAL_INFORMATION
   +0x018 StackTrace       : 0xc0c0c0c0 Void
   +0x01c EndStamp         : 0xc0c0c0c0 
```段中的最后一个堆条目通常是一个空闲块。堆块的状态指示为空闲块。堆块声明前一个块的大小为00108，而当前块的大小为00a30。前一块报告其自身大小为0x20字节，不匹配。位置为05f61000的堆块的使用似乎是该堆块的使用导致以下块的元数据损坏的可能性。堆块：```
0:000> !heap -a 05f60000 
Index   Address  Name      Debugging options enabled
  1:   05f60000 
    Segment at 05f60000 to 0605f000 (00001000 bytes committed)
    Flags:                00000002
    ForceFlags:           00000000
    Granularity:          8 bytes
    Segment Reserve:      00100000
    Segment Commit:       00002000
    DeCommit Block Thres: 00000200
    DeCommit Total Thres: 00002000
    Total Free Size:      00000146
    Max. Allocation Size: fffdefff
    Lock Variable at:     05f60258
    Next TagIndex:        0000
    Maximum TagIndex:     0000
    Tag Entries:          00000000
    PsuedoTag Entries:    00000000
    Virtual Alloc List:   05f6009c
    Uncommitted ranges:   05f6008c
            05f61000: 000fe000  (1040384 bytes)
    FreeList[ 00 ] at 05f600c0: 05f605b8 . 05f605b8  
        05f605b0: 00108 . 00a30 [100] - free

    Segment00 at 05f60000:
        Flags:           00000000
        Base:            05f60000
        First Entry:     05f604a8
        Last Entry:      0605f000
        Total Pages:     000000ff
        Total UnCommit:  000000fe
        Largest UnCommit:00000000
        UnCommitted Ranges: (1)

    Heap entries for Segment00 in Heap 05f60000
         address: psize . size  flags   state (requested size)
        05f60000: 00000 . 004a8 [101] - busy (4a7)
        05f604a8: 004a8 . 00108 [101] - busy (107) Internal 
        05f605b0: 00108 . 00a30 [100]
        05f60fe0: 00a30 . 00020 [111] - busy (1d)
        05f61000:      000fe000      - uncommitted bytes.

0:000> dd 05f60fe0
05f60fe0  a9b3c836 03007087 05f6008c 05f6008c
05f60ff0  05f60038 05f60038 05f61000 000fe000
05f61000  ???????? ???????? ???????? ????????
05f61010  ???????? ???????? ???????? ????????
05f61020  ???????? ???????? ???????? ????????
05f61030  ???????? ???????? ???????? ????????
05f61040  ???????? ???????? ???????? ????????
05f61050  ???????? ???????? ???????? ???????? 
```

#### 披露时间表

该漏洞于2020年8月报告。披露时间表： 2020-08-04-将电子邮件发送到公开提供的WPS的各种邮件列表（销售和支持）。 2020-08-10-WPS团队回应该报告可以转发给他们。 2020-08-11-要求进一步的信息，例如咨询和向适当的渠道披露等。 2020-08-17-根据先前的要求与WPS团队进行跟进。 2020-08-18-WPS团队做出回应，他们会照顾好它，并转交给开发团队。 2020-08-18-通过电子邮件提供技术报告和概念验证（未加密）。 2020-08-25-WPS跟进报告进度。 2020-08-26-WPS更新说此问题已转发给开发团队。 2020-08-28-WPS发送了一封电子邮件，指出该问题已在最新的下载版本11.2.0.9403中得到解决。 2020-08-28-针对提供的PoC测试了新版本，并确认问题已解决。 2020-08-28-向WPS团队寻求咨询或更改日志更新。 2020-08-31-WPS团队通知他们不再更新或维护任何安全公告。 2020-09-03-漏洞写信 要求CVE。