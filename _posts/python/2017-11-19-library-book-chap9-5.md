---
layout: post
section-type: post
title: Python Library - chap 9. 인터넷상의 데이터 다루기 - 5. 이메일 데이터 다루기
category: python
tags: [ 'python' ]
---

`email`모듈은 이메일 메시지나 헤더 해석과 작성을 위한 기능을 제공합니다. 이메일에는 텍스트뿐만 아니라 이미지나 첨부 파일 등의 다양한 데이터가 포함됩니다. 이는 MIME(Multipurpose Internet Mail Extensions)라는 사양에 의해 구현되지만, MIME 형식의 데이터는 복잡합니다. email 모듈을 사용하면 MIME 형식의 데이터를 해석하고 생성할 수 있습니다.

- 이메일 메시지 해석 - `email.parser`
- 메시지 데이터 관리 - `email.message`
- MIME 형식의 이메일 작성 - `email.mime`

그외에도 여러 서브 모듈들이 있습니다.

## 이메일 해석하기 - email.parser

### Parser()

형식 | Parser(\_class=email.message.Message, \*, policy=policy.compat32)
---|---
설명 | 메일을 해석하기 위한 parser를 생성하는 생성자

### Parser 객체의 메서드

함수 이름 | 설명 | 반환값
---|---|---
parse(fp, headersonly=False) | 파일 기술자로 지정된 파일의 내용을 해석한다. headersonly를 True로 지정하면 메일의 헤더 부분만을 해석한다. | email.message.Message
parsestr(text, headersonly=False) | 지정된 텍스트를 해석한다. | email.message.Message

비슷한 클래스와 메서드로는 입력으로 바이트열을 넘기는 BytesParser가 있습니다. BytesParser의 메서드는 parse()와 parsebytes()가 있고, 사용법은 같습니다.  

이러한 네 종류의 해석 방법에는 email 패키지로부터 직접 호출할 수 있는 4개의 메서드가 있습니다.

- email.message_from_string(s) : Parser().parsestr(s)에 해당
- email.message_from_bytes(s) : BytesParser.parsebytes(s)에 해당
- email.message_from_file(fp) : Parser().parse(fp)에 해당
- email.message_from_binary_file(fp) : BytesParser().parse(fp)에 해당


실습을 위한 email.txt를 생성합니다.

```
From: doky@gmail.com
Subject: test email

This is test.
```

### email.parser 샘플 코드

```python
>>> import email
>>> import email.parser
>>> parser = email.parser.Parser()  # Parser 생성
>>> with open('email.txt') as f:
...     m = parser.parse(f)  # 파일 내용을 해석
...     type(m)
...     m.items()  # 헤더 취득
...
<class 'email.message.Message'>
[('From', 'doky@gmail.com'), ('Subject', 'test email')]

>>> with open('email.txt') as f:
...     s = f.read()
...     m = email.message_from_string(s)  # 문자열을 해석
...     m.items()
...
[('From', 'doky@gmail.com'), ('Subject', 'test email')]
```

## 메시지 데이터 관리하기 - email.message
`email.message` 모듈은 메일의 데이터를 관리하는 클래스를 제공합니다. 메일을 표시하는 객체 email.message.Message는 email.parser, email.mime로 생성합니다.

### Message 객체의 메서드

함수 이름 | 설명 | 반환값
---|---|---
as_string() | 메시지 전체를 문자열로 반환한다. | str
as.bytes() | 메시지 전체를 바이트열로 반환한다. | bytes
is.multipart() | 메일이 멀티파트(여러 가지 데이터를 포함)일 때 True를 반환한다. | MIME
get_payload(i=None, decode=False) | 메시지의 페이로드를 구한다. 멀티파트일 때는 Message 객체의 리스트를 반환한다. 또한 i에 수치를 지정하면 지정된 위치의 페이로드를 반환한다. | Message 또는 str
keys() | 헤더의 필드 이름을 리스트로 반환한다. | list
items() | 헤더의 필드 이름과 값을 튜플 리스트로 반환한다. | list
get(name, failobj=None) | name으로 지정된 헤더 값을 구한다. 존재하지 않으면 failobj로 지정된 값을 반환한다. | str
get_all(name, failobj=None) | name으로 지정된 헤더 값을 모두 구하여 리스트로 반환한다. | list

### email.message 샘플 코드

```python
>>> import email
>>> f = open('email.txt')
>>> msg = email.message_from_file(f)
>>> type(msg)
<class 'email.message.Message'>

>>> msg.is_multipart()  # 멀티파트인지 확인
False

>>> msg.get_payload()  # 페이로드(본문)을 얻음
'This is test.\n'

>>> msg.keys()  # 헤더의 리스트를 얻음
['From', 'Subject']

>>> msg.get('From')  # From 값을 얻음
'doky@gmail.com'

>>> msg.as_string()  # 메시지 전체를 문자열로 얻음
'From: doky@gmail.com\nSubject: test email\n\nThis is test.\n'
```

## MIME 형식의 메일 작성하기 - email.mime
email.mime 모듈은 MIME 형식의 메일을 작성할 때, 다양한 메시지를 다루는 클래스를 제공합니다.

### multipart.MIMEMultipart 클래스

형식 | class.multipart.MIMEMultipart(\_subtype='mixed', boundary=None, \_subparts=None, \**\_params)
---|---
설명 | 멀티파트 형식의 MIME 메시지를 다루기 위한 클래스 생성자
인수 | \subtypr - 콘텐츠 타입의 서브타입을 지정한다. 기본값은 mixed <br> boundary - 각 메시지의 경계 문자열을 지정한다. 기본으로는 임의의 문자열이 생성된다.

### application.MIMEApplication 클래스

형식 | class application.MIMEApplication(\_data, \_subtype='octet-stream', \_encode=email.encoders.encode_base64, \**\_params)
---|---
설명 | 애플리케이션 데이터(application/\_subtype)의 MIME 메시지를 다루기 위한 클래스 생성자
인수 | \_data - 애플리케이션 데이터를 바이트열로 전달한다. <br> \_subtype - 콘텐츠 타입의 서브타입(gzip, pdf 등)을 지정한다. 기본값은 octet-stream <br> \_encoder - 데이터를 인코딩하기 위한 함수를 지정한다.

### audio.MIMEAudio 클래스

형식 | class audio.MIMEAudio(\_audiodata, \_subtype=None, \_encoder=email.encoders.encode_base64, \**\_params)
---|---
설명 | 음성 데이터(audio/\_subtype)의 MIME 메시지를 다루기 위한 클래스 생성자
인수 | \_audiodata - 음성 데이터를 바이트열로 전달한다. <br> \_subtype - 콘텐츠 타입의 서브타입(wav, mpeg 등)을 지정한다. <br> \_encoder - 데이터를 인코딩하기 위한 함수를 지정한다.

### image.MIMEImage 클래스

형식 | class image.MIMEImage(\_imagedata, \_subtype=None, \_encoder=email.encoders.encode_base64, \**\_params)
---|---
설명 | 이미지 데이터(image/\_subtype)의 MIME 메시지를 다루기 위한 클래스 생성자
인수 | \_imagedata - 이미지 데이터를 바이트열로 전달한다. <br> \_subtype - 콘텐츠 타입의 서브타입(jpg, png 등)을 지정한다. <br> \_encoder - 데이터를 인코딩하기 위한 함수를 지정한다.

### text.MIMEText 클래스

형식 | class text.MIMEText(\_text, \_subtype='plain', \_charset=None)
---|---
설명 | 텍스트 데이터(text/\_subtype)의 MIME 메시지를 다루기 위한 클래스 생성자
인수 | \_text - 텍스트 데이터를 문자열로 전달한다. <br> \_subtype - 콘텐츠 타입의 서브타입(html, xml 등)을 지정한다. 기본값은 plain <br> \_charset - 문자열의 문자 코드 세트를 지정한다.

다음은 이미지 파일을 포함한 멀티파트 메시지를 작성하는 샘플 코드입니다. 스크립트를 실행하는 디렉터리에 각종 파일이 배치되어 있는 가정하에 작성되었습니다.

```python
>>> from email.mime.image import MIMEImage
>>> from email.mime.multipart import MIMEMultipart
>>> from email.mime.text import MIMEText
>>> from email.mime.application import MIMEApplication
>>> message = MIMEMultipart()  # 멀티파트 메시지를 작성
>>> with open('sample.html', 'r') as f:  # 텍스트 데이터를 작성
...     text = MIMEText(f.read(), _subtype='html')
...

>>> message.attach(text)  # 메시지에 텍스트 추가
>>> with open('sample.jpg', 'rb') as f:  # 이미지 데이터를 작성
...     image = MIMEImage(f.read(), _subtype='jpg')
...

>>> message.attach(image)
>>> with open('sample.pdf', 'rb') as f:  # 애플리케이션 데이터를 작성
...     app = MIMEApplication(f.read(), _subtype='pdf')
...

>>> message.attach(app)
>>> message.is_multipart()  # 멀티파트 형식을 확인
True

>>> for payload in message.get_payload():  # 페이로드 얻기
...     type(payload)  # 클래스 확인
...     payload.get_content_type()  # 콘텐츠 타입 얻기
...
<class 'email.mime.text.MIMEText'>
'text/html'
<class 'email.mime.image.MIMEImage'>
'image/jpg'
<class 'email.mime.application.MIMEApplication'>
'application/pdf'
```
