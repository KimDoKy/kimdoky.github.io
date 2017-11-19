---
layout: post
section-type: post
title: Python Library - chap 9. 인터넷상의 데이터 다루기 - 4. Base16, Base64 등으로 인코딩
category: python
tags: [ 'python' ]
---
`base64` 모듈은 Base64로 인코딩과 디코딩을 합니다.

- Base16
- Base32
- Base64
- Base85

위와 같은 인코딩 방식을 다룰 수 있습니다.  

이들 인코딩 방식은 알파벳과 숫자 등 취급할 수 있는 문자 종류가 한정된 환경에서 그 외의 문자(멀티바이트 문자, 이진 데이터 등)를 사용하기 위한 것입니다.  

이 중 가장 널리 쓰이는 Base64는 주고 Basic 인증이나 이메일 등에서 이용합니다.

## Base64로 인코딩
문자열을 Base64로 인코딩하려면 바이트 문자열을 b64encode()에 넘겨줍니다.

### base64 인코딩
```python
>>> import base64
>>> s = 'Python은 간단히 습득할 수 있고 강력한 언어입니다.'
>>> base64.b64encode(s)  # 문자열을 전달하면 오류
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/base64.py", line 59, in b64encode
    encoded = binascii.b2a_base64(s)[:-1]
TypeError: a bytes-like object is required, not 'str'

>>> s.encode()
b'Python\xec\x9d\x80 \xea\xb0\x84\xeb\x8b\xa8\xed\x9e\x88 \xec\x8a\xb5\xeb\x93\x9d\xed\x95\xa0 \xec\x88\x98 \xec\x9e\x88\xea\xb3\xa0 \xea\xb0\x95\xeb\xa0\xa5\xed\x95\x9c \xec\x96\xb8\xec\x96\xb4\xec\x9e\x85\xeb\x8b\x88\xeb\x8b\xa4.'

>>> base64.b64encode(s.encode())  # 바이트 문자열로 인코딩하여 넘김
b'UHl0aG9u7J2AIOqwhOuLqO2eiCDsirXrk53tlaAg7IiYIOyeiOqzoCDqsJXroKXtlZwg7Ja47Ja07J6F64uI64ukLg=='

>>> base64.b64encode(s.encode(), altchars=b'@*')
b'UHl0aG9u7J2AIOqwhOuLqO2eiCDsirXrk53tlaAg7IiYIOyeiOqzoCDqsJXroKXtlZwg7Ja47Ja07J6F64uI64ukLg=='
```

altchars 인수는 치환할 문자열을 지정함으로써, 인코딩 결과에 포함되는 `+`를 `@`로, `/`를 `*`로 치환하도록 했습니다.  
base64 모듈은 base64.b64encode()와는 문자열 치환 동작이 다른 함수도 제공합니다. urlsafe_b64encode()는 URL의 일부로 안전히 이용할 수 있는 알파벳만을 사용한 인코딩 결과를 반환합니다.

### Base64로 디코딩
b64decode()를 사용하여 Base64로 인코딩된 바이트 문자열을 디코딩할 수 있습니다.


### base64 디코딩

```python
>>> s = b'UHl0aG9u7J2AIOqwhOuLqO2eiCDsirXrk53tlaAg7IiYIOyeiOqzoCDqsJXroKXtlZwg7Ja47Ja07J6F64uI64ukLg=='

>>> base64.b64decode(s)
b'Python\xec\x9d\x80 \xea\xb0\x84\xeb\x8b\xa8\xed\x9e\x88 \xec\x8a\xb5\xeb\x93\x9d\xed\x95\xa0 \xec\x88\x98 \xec\x9e\x88\xea\xb3\xa0 \xea\xb0\x95\xeb\xa0\xa5\xed\x95\x9c \xec\x96\xb8\xec\x96\xb4\xec\x9e\x85\xeb\x8b\x88\xeb\x8b\xa4.'

>>> base64.b64decode(s).decode()
'Python은 간단히 습득할 수 있고 강력한 언어입니다.'
```
인코딩과 마찬가지로 urlsafe_b64decode()가 있습니다. 인코딩 방법에 따라 적절한 방법으로 디코딩을 실행합니다.
