---
layout: post
section-type: post
title: Python Library - chap 9. 인터넷상의 데이터 다루기 - 3. 인간친화적인 HTTP 클라이언트
category: python
tags: [ 'python' ]
---

`requests` 패키지는 인간친화적인 HTTP 클라이언트 기능을 제공합니다. urllib.request와 마찬가지로 URL 열기나 GET, POST 요청 등을 수행합니다.

## requests 설치

```
$ pip install requests
```

## 지정한 URL 열기
HTTP 메서드마다 대응하는 인터페이스가 준비되어 있고 매우 직관적입니다.

### HTTP 메서드별 대응 인터페이스

HTTP 메서드 | 대응 인터페이스
---|---
GET | requests.get()
HEAD | requests.head()
POST | requests.post()
PATCH | requests.patch()
PUT | requests.put()
DELETE | requests.delete()
OPTIONS | requests.options()

#### GET 요청하기

```python
>>> import requests
>>> r = requests.get('http://httpbin.org/get')
>>> r
<Response [200]>

>>> r.text
'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Connection": "close", \n    "Host": "httpbin.org", \n    "User-Agent": "python-requests/2.18.4"\n  }, \n  "origin": "1.217.143.243", \n  "url": "http://httpbin.org/get"\n}\n'
```

매개변수에 붙어 GET 요청을 보내고 싶을 때는 params 인수에 문자열 또는 dict를 지정합니다.

#### 매개변수에 붙여 GET 요청하기

```python
>>> r = requests.get('http://httpbin.org/get', params='example')
>>> r.url
'http://httpbin.org/get?example'
>>> r = requests.get('http://httpbin.org/get', params={'key':'value'})
>>> r.url
'http://httpbin.org/get?key=value'
```

문자열을 지정하면 단순히 해당 문자열을 매개변수로 취급합니다. dict를 지정하면 key1=value1&key2=value2와 같이 키와 값의 세트를 문자열로 조합한 것을 매개변수로 취급합니다.  

### 사용자 정의 헤더 설정
HTTP 헤터를 지정하려면, headers 인수로 dict를 지정합니다.

```python
>>> headers = {'Accept': 'application/json'}
>>> r = requests.get('http://httpbin.org/get', headers=headers)
```
이 인터페이스는 모든 HTTP 공통입니다.

### 응답 객체
requests는 requests.models.Response 객체를 반환합니다.  

속성 | 설명
---|---
Response.request | 요청 정보를 지닌 객체
Response.url | 요청한 URL 문자열
Response.cookie | 응답에 포함되는 Cookie 정보를 지닌 객체
Response.headers | dict 형식의 응답 헤더
Response.status_code | 응답의 HTTP 상태 코드
Response.ok | 응답의 HTTP 상태 코드가 정상이면 True, 아니면 False를 반환
Response.text | 문자열로 인코딩 완료된 응답 본문
Response.iter_lines() | 응답 본문을 한 줄씩 반환하는 반복자를 반환한다. 문자열이 아닌 바이트 열로 반환한다.
Response.json() | 응답 본문을 JSON 포맷으로 해석하고 dict형으로 변환하여 반환한다.


#### 응답의 상태 코드 판정
응답 객체는 bool로 평가되면 .ok를 반환하므로, 응답이 오류 상태 코드를 반환하지 않는다는 것을 판정할 수 있습니다.

```python
if requests.head(some_url):
     ...
else:   # 상태 코드가 오류(4XX,5XX)일 때
     ...
```

#### .json()으로 JSON 포맷에서 dict으로 변환
Web API 등 응답 포맷이 JSON이면 .json() 메서드를 사용해 dict로 변환할 수 있습니다.

```python
>>> r.headers['content-type']
'application/json'

>>> r.json()
{'url': 'http://httpbin.org/get', 'args': {}, 'headers': {'Connection': 'close', 'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'python-requests/2.18.4', 'Host': 'httpbin.org', 'Accept': 'application/json'}, 'origin': '1.217.143.243'}
```

### POST 요청하기

```python
>>> payload = {'hoge':'fuga'}
>>> r = requests.post('http://httpbin.org/post', data=payload)
>>> r.request.body
'hoge=fuga'
```

data 인수에 dict를 지정하면, application/x-www-form-urlencoded 형식의 인수로 변환됩니다. dict 외의 문자열이나 file-like 객체를 지정할 수도 있습니다.
