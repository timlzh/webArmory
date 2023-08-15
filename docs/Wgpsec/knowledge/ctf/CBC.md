---
title: 【CRYPTO】CBC
---

# CBC

## 现代密码体制

> 现代密码中的加密体制一般分为对称加密体制(Symmetric Key Encryption)和非对称加密体制(Asymmetric Key Encryption)。对称加密又被分为分组加密和序列密码。 
>
> 分组密码：也叫块加密(block cyphers)，一次加密明文中的一个块。分组密码是将明文按一定的位长分组，明文组经过加密运算得到密文组，密文组经过解密运算（加密运算的逆运算），还原成明文组，主要有 ECB（电子密码本模式） ，CBC （密码分组链接模式） ，CFB （密文反馈模式） ，OFB （输出反馈模式），  CTR模式（计数器模式） 五种工作模式。
>
> 序列密码：也叫流加密(stream cyphers)，一次加密明文中的一个位。序列密码是指利用少量的密钥（制乱元素）通过某种复杂的运算（密码算法）产生大量的伪随机位流，用于对明文位流的加密。解密是指用同样的密钥和密码算法及与加密相同的伪随机位流，用以还原明文位流。  

## CBC 模式

> CBC (Cipher Block Chaining, 密码分组链接) 模式中每一个分组要先和前一个分组加密后的数据进行XOR异或操作，然后再进行加密。这样每个密文块依赖该块之前的所有明文块，为了保持每条消息都具有唯一性，第一个数据块进行加密之前需要用初始化向量IV进行异或操作。CBC模式是一种最常用的加密模式，它主要缺点是需要初始向量，加密是连续的，不能并行处理，并且与ECB一样消息块必须填充到块大小的整倍数。 

## CBC 工作模式

### 加密过程

![CBC](/assets/wgpsec/images/CBC/CBCE.png)

上图为CBC加密原理图

> - Plaintext：明文，待加密的数据
> - IV ：初始向量，用于随机化加密的比特块，保证即使对相同明文多次加密，也可以得到不同的密文
> - Key：分组加密使用的对称密钥，由AES，Blowfish，DES，Triple DES等对称加密算法使用
> - Ciphertext：加密后的数据，也叫密文数据
> - 固定分组：CBC在一个固定长度的位组上工作，称为块。这里使用包含16字节的块进行说明

#### 文字流程

主要流程：前一组密文块用来产生后一组密文块

> 1. 首先将明文分组(常见的以16字节为一组)，位数不足的使用特殊字符填充
> 2. 生成一个随机的初始化向量(IV)和一个密钥
> 3. 将IV和第一组明文异或产生初步密文，再用密钥对初步密文加密生成最终密文块
> 4. 用密钥对3中xor后产生的密文进行加密
> 5. 用4中产生的密文对第二组明文进行xor操作
> 6. 用密钥对5中产生的密文进行加密
> 7. 重复4-7，直至最后一组明文
> 8. 将IV和加密后的密文块拼接在一起，得到最终的密文

从第一块 Plaintext 开始，首先与一个初始向量IV异或（IV只在第一块发挥作用），然后把异或的结果经过key进行加密，得到第一块的密文，并且把加密的结果与下一块的明文进行异或，一直这样重复进行下去直至最后一组明文。

#### 公式描述

> - Ciphertext-0 = Encrypt(Plaintext XOR IV)		#  只用于第一个组块  
> - Ciphertext-N = Encrypt(Plaintext XOR Ciphertext-(N-1)		#  用于第二及剩下的组块(N > 1)

#### 代码解析

```C
cypher_t* aes_cbc_encrypt(uint8_t* key, cypher_t* data_in)
{
    //pad last block with 0
    cypher_t* data_in_padding = block_padding(data_in);
    cypher_t* cypher_out = (cypher_t*)malloc(sizeof(uint8_t) + data_in->len_data);
    cypher_out->len_data = data_in_padding->len_data;

    uint8_t iv[16] = {0};
    memcpy(iv, IV, 16);
    uint8_t temp_out[16] = {0};
    for (uint8_t index = 0; index < data_in_padding->len_data/16 ; ++index){
        array_xor(16, temp_out, data_in_padding->data + (index * 16), iv);      //明文与iv异或
        _aes128_encryption(key, cypher_out->data + index * 16, temp_out);       //进行块加密得到密文，同时密文是下次加密的iv
        memcpy(iv, cypher_out->data + index * 16, 16);                          //本次的密文是下次加密的iv
    }
    free(data_in_padding);
    return cypher_out;
}
```

### 解密过程

![CBCD](/assets/wgpsec/images/CBC/CBCD.png)

上图为CBC解密原理图

只要了解了解密加密过程，反过来看解密过程也就比较简单了

#### 文字流程

主要流程：前一组密文块影响后一组密文块的还原

> 1. 从密文中提取出IV，然后将密文分组
> 2. 使用密钥对第一组密文进行解密，然后和IV进行xor得到明文
> 3. 使用密钥对第二组密文进行解密，然后和2中的密文xor得到明文
> 4. 重复2-3，直至最后一组密文

#### 公式描述

> - Plaintext-0 = Decrypt(Ciphertext) XOR IV		#  只用于第一个组块  
> - Plaintext-N = Decrypt(Ciphertext) XOR Ciphertext-(N-1)		#  用于第二及剩下的组块(N > 1)

#### 代码解析

```c
cypher_t* aes_cbc_decrypt(uint8_t* key, cypher_t* data_in)
{
    cypher_t* cypher_padding = block_padding(data_in);
    cypher_t* plain = (cypher_t*)malloc(data_in->len_data);
    plain->len_data = cypher_padding->len_data;
    uint8_t iv[16] = {0};
    memcpy(iv, IV, 16);
    uint8_t temp_out[16] = {0};
    for (uint8_t index = 0; index < cypher_padding->len_data/16 ; ++index){
        _aes128_decryption(key, temp_out, cypher_padding->data + (index*16));   //密文块解密
        array_xor(16, plain->data + (index*16), temp_out, iv);                  //与iv异或得到明文
        memcpy(iv, cypher_padding->data + (index*16), 16);                      //设置下次解密用到的iv
    }
    free(cypher_padding);
    return plain;
}
```

## Padding oracle

### 攻击流程

明文填充

> - 分组密码 Block Cipher 需要在加载前确保每个每组的长度都是分组长度的整数倍。一般情况下，明文的最后一个分组很有可能会出现长度不足分组的长度。
>
> - 这个时候，普遍的做法是在最后一组密文块后填充一个固定的值，这个值的大小为填充的字节总数。
>
> ```
> 最后还差1个字符，则填充1个0x01；
> 最后还差2个字符，则填充2个0x02；
> 最后还差3个字符，则填充3个0x03；
> 最后还差4个字符，则填充4个0x04；
> 这里特别需要注意的是：如果明文长度为16的整数字节长，它也需要填充（它会一次填充16位，且填充的字符为0x10）
> ```
>
> - 填充主要发生在最后一组密文块，我们需要格外关注最后一个分组。
> - 例如最后一组的末尾为0x02,即表示填充了2个Padding，如果最后的Padding不正确，即值和数量不一致，那么解密程序往往会抛出异常(Padding Error)。我们可以通过应用的错误回显，判断出Padding是否正确。
> - 前提条件是服务器会对我们显示padding error的异常，如果不回显那么就无法判断并进行利用。
> - 例如在web应用中，如果Padding不正确，则应用程序很可能会返回500的错误（程序执行错误）；如果Padding正确，但解密出来的内容不正确，则可能会返回200的自定义错误（业务上的规定）。所以，这种区别就可以成为一个二值逻辑的“注入点”。

攻击成立的两个重要的假设前提：

```
1. 攻击者能够获得密文（Ciphertext），以及附带在密文前面的IV（初始化向量）
2. 攻击者能够触发密文的解密过程，且能够知道密文的解密结果
```

> - 攻击流程实际上是不断地调整IV的值，在解密之后，最后一个字节的值为正确的Padding Byte，因为padding正确时，这时padding正确是指最终解密并异或出来的明文最后一个字节在正确padding的范围内就是正确的，虽然最后得到的明文不一定正确，但是padding是合法的，所以服务器返回200 。
> - 判断情况
> ```
> （1）正常解密，得到明文
> （2）解密成功，但是解密得到的和明文不匹配
> （3）解密错误，抛出异常
> ```
>
> - 例如加密数据应用于cookie

## CBC字节翻转攻击

### 攻击原理

> - 在 CBC 解密的公式描述中可以注意到Ciphertext-(N-1)是用来产生下一块明文，这里是字节翻转攻击发挥作用的地方。如果我们改变Ciphertext-N-1中的一个字节，然后和下一块解密后的密文xor，就可以得到一个不同的明文，而这个明文是我们可以控制的。
> - 在此基础上，通过破坏密文中的字节来改变明文中的字节，因此在破坏的密文中添加单引号等恶意字符来绕过过滤器，或通过将用户ID更改为admin来提升权限，或者更改应用程序所需的明文造成其他后果。

### 攻击流程

![CBCDturn](/assets/wgpsec/images/CBC/CBCDturn.jpg)

> - 通过修改第一组的密文块字节，来构造我们需要的第二组明文， 当第一组密文块字节发生改变时会影响第一组明文块和第二组明文块。 
>
> - 假如我们已知的明文解密后为1dmin，我们想构造一个初始IV，使其解密成admin，因此有以下逻辑：
>
> ```
> 原始的IV[1]^middle[i]=plain[1]  <<<  题目逻辑
> 修改的IV[1]^middle[i]='a'       <<<  我们想要
> 构造的IV[1]=middle[1]^'a'       <<<  我们可以得到
> ```
>
> - 用公式表示
>
> ```
> A = B ^ C
> C = A ^ B
> A ^ B ^ C = 0
> A ^ B ^ C ^ C' = C'
> ```
>
> - 而原来的中间明文可以如下方式通过，原来的明文第一位又是可以通过Padding Oracle攻击得到的
>
> ```
> middle[1]=原来的IV[1]^plain[1]	      <<<  Padding Oracle 攻击
> 构造的IV[1]=原来的IV[1]^plain[1]^'a' 	<<<  IV的第一位
> ```

## 题目参考

[[NCTF2017] Be Admin](https://buuoj.cn/challenges#[NCTF2017]Be%20admin)

[[NPUCTF2020]web🐕](https://buuoj.cn/challenges#[NPUCTF2020]web%F0%9F%90%95)

