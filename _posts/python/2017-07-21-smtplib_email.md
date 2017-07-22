---
layout: post
section-type: post
title: Python의 SMTP를 이용하여 E-mail 발송하기
category: python
tags: [ 'python' ]
---

> 실습 코드는 <https://github.com/KimDoKy/WebScrapingWithPython/tree/master/chap5>{:target="`_`blank"} 에서 원본을 볼 수 있습니다.

## python으로 smtp를 이용하여 email 보내기

우선 이메일 내용을 작성한 파일을 준비합니다.

`../textFile.txt`

다음 코드를 작성합니다.

```python
# 이메일을 발송하기 위해서 smtplib, email 모듈을 import 합니다.
# MIME(Multipurpose Internet Mail Extensions)는 email을 위한 인터넷 표준입니다.
>>> import smtplib
>>> from email.mime.text import MIMEText
>>> email_text = open('./textFile.txt' , 'rb')

>>> msg = MIMEText(email_text.read())
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/email/mime/text.py", line 34, in __init__
    _text.encode('us-ascii')
AttributeError: 'bytes' object has no attribute 'encode'

# textFile.txt 안에 한글이 들어 있기 때문에 utf-8 으로 인코딩하여 열어주어야 합니다.
>>> import codecs
>>> email_text = codecs.open('./textFile.txt' , 'rb', 'utf-8')

# 읽어들인 파일의 텍스트를 MIME 객체화 한다.
>>> msg = MIMEText(email_text.read())
>>> email_text.close()

# msg 는 무엇이 들어있는 확인해보았습니다. 헤더의 내용과 email_text에서 불러온 본문이 들어있습니다.
>>> print(msg)
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: base64

cHl0aG9u7JeQ7IScIHNtdHDrpbwg7J207Jqp7ZWcIGVtYWlsIOuwnOyGoSDsmIjsoJwg7YWN7Iqk
7Yq4IO2MjOydvOyeheuLiOuLpC4KUklQIGNoZXN0ZXIuLi4K

# 제목을 추가하였습니다.
>>> msg['Subject'] = 'Email example content %s' % email_text

# MIMEText는 처음 다루어보기 때문에, 안에 어떤 구조인지, 어떤 정보가 들어가는지 확인해봤습니다.
>>> msg
<email.mime.text.MIMEText object at 0x10db2b160>
>>> len(msg)
4
>>> for i in msg:
...     print(i)
...
Content-Type
MIME-Version
Content-Transfer-Encoding
# 좀전에 위에서 추가한 제목이 추가되었습니다.
Subject
# msg안에 추가시킨 Subject만 불러와봤습니다.
>>> msg['Subject']
'Email example content <codecs.StreamReaderWriter object at 0x10db2b198>'

# 보내는 사람을 추가합니다.
>>> msg['From'] = 'makingfunk@naver.com'

# 처음이니까 MIMEText 객체의 변화를 모니터링 했습니다.
>>> len(msg)
5
>>> for i in msg:
...     print(i)
...
Content-Type
MIME-Version
Content-Transfer-Encoding
Subject
From
# 바로 위에서 작성한 From이 추가 되었습니다.

# 받는 이를 추가합니다.
>>> msg['To'] = 'abmu333@hanmail.net'

# 로컬 SMTP 서버를 이용하여 email을 보냅니다.
>>> s = smtplib.SMTP('localhost')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/smtplib.py", line 251, in __init__
    (code, msg) = self.connect(host, port)
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/smtplib.py", line 335, in connect
    self.sock = self._get_socket(host, port, self.timeout)
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/smtplib.py", line 306, in _get_socket
    self.source_address)
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/socket.py", line 711, in create_connection
    raise err
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/socket.py", line 702, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [Errno 61] Connection refused

# 로컬 SMTP 서버가 없어서 에러가 일어났습니다. 없는 경우 다른 서버를 이용하면 됩니다.
# 여기서는 gmail 서버를 사용하였습니다.
>>> smtp_gmail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
>>> smtp_gmail
<smtplib.SMTP_SSL object at 0x10e00ba90>

# gmail의 비밀번호를 잃어 버려서 에러가 났습니다. 실습하기 전에 꼭 계정 정보를 확인해두세요.
>>> smtp_gmail.login(id, passwd)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/smtplib.py", line 729, in login
    raise last_exception
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/smtplib.py", line 720, in login
    initial_response_ok=initial_response_ok)
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/smtplib.py", line 641, in auth
    raise SMTPAuthenticationError(code, resp)
smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n5.7.8  https://support.google.com/mail/?p=BadCredentials 73sm9027497pemail_text.103 - gsmtp')

# login이 성공했다는 메시지가 출력됩니다.
>>> smtp_gmail.login(id, passwd)
(235, b'2.7.0 Accepted')

# 처음이니까 일일이 다 확인해봅니다.
>>> smtp_gmail
<smtplib.SMTP_SSL object at 0x10e024780>

# 메일을 발송합니다.
# SMTP.sendmail(from_addr, to_addrs, msg, mail_options=[], rcpt_options=[])  // from_addr은 필수요소이지만 빈칸으로 넣어도 정상작동합니다.
>>> smtp_gmail.sendmail('makingfunk0@gmail.com','abmu333@hanmail.net', msg.as_string())
{}

>>> smtp_gmail.quit()
(221, b'2.0.0 closing connection c76sm8724276pfj.91 - gsmtp')
>>>
```

이메일이 정상적으로 발송되었음을 확인 할 수 있습니다.

![]({{site.url}}/img/post/python/email_example.png)

자세한 내용은 [문서](https://docs.python.org/3/library/smtplib.html){:target="`_`blank"}를 참조하세요.  

## 이미지 파일을 이메일에 첨부하는 예제입니다.

```python
# 이메일을 보내기 위해 smtplib를 import합니다.
import smtplib
# 이메일에 이미지를 첨부하기 위한 모듈들도 import 합니다.
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
family = 'abmu333@hanmail.net','makingfunk0@gmail.com'

# 이메일 메세지 컨테이너를 만듭니다.
msg = MIMEMultipart()
msg['Subject'] = 'image send mail test 2'
msg['From'] = 'makingfunk0@gmail.com'
msg['To'] = COMMASPACE.join(family)
# preamble 이 어떤 역할을 하는 속성인는 모르겠습니다.
msg.preamble = 'what the..'
pngfiles = ['./img/example.png', './img/example2.png']

for file in pngfiles:
    fp = open(file, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    # 첨부한 파일의 파일이름을 입력합니다. (이 구문이 없으면 noname으로 발송됩니다.)
    img.add_header('Content-Disposition', 'attachment', filename=file)
    msg.attach(img)

# 로컬 서버를 통해 메일을 보낼 때
s = smtplib.SMTP('localhost')
s.sendmail(me, family, msg.as_string())
s.quit()
# 외부 SMTP 서버를 이용할 때
s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
s.login(id, passwd)
s.sendmail("","",msg.as_string())
s.quit()
```

파일이름 지정 구문이 없다면 naname으로 가지만, naver의 메일으로 발송하면 attach(0).txt 으로 파일이 보내집니다. 즉, 메일을 받는 사람 입장에서는 이미지를 보려면 확장자를 하나하나 변경해서 봐야 합니다.
