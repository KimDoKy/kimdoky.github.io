---
layout: post
section-type: post
title: Python Library - chap 9. 인터넷상의 데이터 다루기 - 2. URL 열기
category: python
tags: [ 'python' ]
---

`urllib.request`는 URL을 열기 위한 인터페이스를 제공합니다. 공식문서에서는 같은 용도로 더 편리한 서드파티 패키지인 `requests`의 이용을 권장하고 있습니다.

## 지정한 URL 열기
urllib.request 모듈로 URL을 열기 위한 대표적인 인터페이스는 urlopen()입니다.

### urlopen()

형식 | urlopen(url, data=None, [timeout,]\*, cafile=None, capath=None, cadefault=False, context=None)
---|---
설명 | URL을 열어 콘텐츠를 취득한다.
인수 | url - URL을 지정한다. Request 클래스이 인스턴스를 전달할 수도 있다. <br> data - URL에 POST할 데이터를 bytes 객체로 지정한다. <br> timeout - 타임아웃 시간을 지정한다. <br> cafile - HTTPS 요청을 위한 증명서 파일 경로를 지정한다. <br> capath - HTTPS 요청을 위한 증명서 파일이 저장된 디렉터리 경로를 지정한다. <br> cadefault - 사용하지 않는 인수 <br> context - ssl.SSL.Context 클래스의 인스턴스를 지정한다.
반환값 | http.client.HTTPResponse

### HTTP 메서드별 urlopen() 호출

형식 | 설명
---|---
GET | urlopen(url=<url>) 또는 urlopen(url=Request(url=<url>))
POST | urlopen(url=<url>, data=<data>) 또는 urlopen(url=Request(url=<url>, data=<data>))
HEAD | urlopen(url=Request(url=<url>, method='HEAD'))
PATCH | urlopen(url=Reqeust(url=<url>, data=<data>, method='PACTH'))
PUT | urlopen(url=Reqeust(url=<url>, data=<data>, method='PUT'))
DELETE | urlopen(url=Request(url=<url>, method='DELETE'))
OPTIONS | urlopen(url=Request(url=<url>, method='OPTIONS'))

urlopen()에는 HTTP 메서드를 지정하는 인수가 존재하지 않습니다. GET 메서드와 POST 메서드만이 직접 URL과 데이터를 전달해 요청할 수 있으나, 그 외의 HTTP 메서드를 사용해 요청할 때는 HTTP 요청을 추상화한 urllib.request.Request 클래스 인스턴스를 지정해야 합니다.

## GET 요청하기
URL을 열려면 urlopen()에 문자열로 URL을 지정하기만 하면 됩니다. 문자열 대신에 Request 클래스의 인스턴스를 전달할 수도 있습니다.

### GET 메서드 사용 예

```python
>>> from urllib import request
>>> res = request.urlopen('http://httpbin.org/get')
>>> res.code
200
>>> res.read()
b'{\n  "args": {}, \n  "headers": {\n    "Accept-Encoding": "identity", \n    "Connection": "close", \n    "Host": "httpbin.org", \n    "User-Agent": "Python-urllib/3.5"\n  }, \n  "origin": "124.58.160.186", \n  "url": "http://httpbin.org/get"\n}\n'
```
반환값은 응답 정보를 저장한 객체로서 file-like 객체이기 때문에, read() 등의 메서드로 데이터를 읽어올 수 있습니다. 반환값은 http.client.HTTPResponse 클래스의 인스턴스입니다.  

urlopen()에는 GET할 때 매개변수를 전달하는 특별한 인터페이스는 없습니다. 인수 문자열을 URL의 일부로서 요청해야 합니다.

### 매개변수를 붙여 요청하기

```python
>>> res = request.urlopen('http://httpbin.org/get?key1=value1')
```

urllib.parse 모듈의 urlencode() 등을 사용하면 dict나 튜플로부터 안전하게 매개변수 문자열을 조합할 수 있습니다.

### 사용자 정의 헤더 설정
요청할 때 사용자 정의 헤더를 설정하려면 urllib.request.Request 클래스의 생성자로 dict를 넘겨줍니다.

```python
>>> headers = {'Accept': 'application/json'}
>>> request.Request('http://httpbin.org/get', headers=headers)
<urllib.request.Request object at 0x1023177f0>
```

## POST 요청하기
urlopen()에 두 번째 인수 data를 전달하여 첫 번째 인수 URL 데이터를 POST할 수 있습니다. 인수 data에는 bytes형의 데이터를 전달해야 하므로, 다음 샘플 코드에서는 문자열을 .encode()를 사용하여 변환하고 있습니다.

### POST 메서드 사용 예

```python
>>> data = 'key1=value1&key2=value2'
>>> res = request.urlopen('http://httpbin.org/post', data=data.encode())
>>> res.code
200
```

application/x-www-form-urlencoded 형식의 인수를 data에 전달할 때에도 urllib.parse 모듈을 이용할 수 있습니다.

## GET, POST 이외의 HTTP 메서드 다루기
GET, POST 이외의 HTTP 메서드로 요청하기 위해서는 urllib.request.Request 클래스를 사용합니다. Request 클래스의 생성자로 HTTP 메서드를 전달할 수 있습니다.

### urllib.request.Request 클래스

형식 | class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
---|---
인수 | url - URL을 지정한다. <br> data - URL에 POST할 데이터를 bytes 객체로 지정한다. <br> headers - HTTP 헤더를 dict 형식으로 지정한다. <br> method - HTTP 메서드를 지정한다.

Request 객체를 urlopen()의 첫 번째 인수로 전달하면 임의의 HTTP 메서드를 사용하여 URL을 열 수 있습니다. 다음은 HEAD 메서드로 지정된 URL을 요청하는 샘플 코드입니다.

### HEAD 메서드를 사용하는 샘플 코드

```python
>>> req = request.Request('http://httpbin.org/get', method='HEAD')  # HEAD 메서드를 사용하여 요청 작성
>>> res = request.urlopen(req)
>>> res.code
200

>>> res.read()  # HEAD 메서드이므로 응답 본문(body)은 비어 있음
b''
```

> ### HTTP 클라이언트 테스트에 편리한 서비스 - httpbin  
httpbin에는 다양한 시나리오를 바탕으로 HTTP 응답을 반환하는 엔드 포인트(end point)가 준비되어 있기 때문에, HTTP 클라이언트 라이브러리 증의 테스트에 아주 편리하게 사용할 수 있습니다.  또한 Python 패키지로도 제공되고 있습니다. 따라서 로컬 머신 등 임의의 PC상에서 간단하게 호스트할 수 있습니다.
