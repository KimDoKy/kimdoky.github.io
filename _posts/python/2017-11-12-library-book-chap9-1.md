---
layout: post
section-type: post
title: Python Library - chap 9. 인터넷상의 데이터 다루기 - 1. URL 해석하기
category: python
tags: [ 'python' ]
---

소프트웨어를 인터넷과 연결해주는 입구 역할을 하는 라이브러리들입니다. 그 중에서도 중심이 되는 HTTP를 자유자재로 다루는 것은 인터넷상의 방대한 데이터를 활용하기 위한 기본입니다.

# URL 해석하기

`urllib.parse`모듈은 URL과 쿼리 문자열을 해석하여 구성 요소를 분해하거나 결합하는 기능을 제공합니다.

## URL 해석하기 - urlparse()

urlparse()를 사용하면 URL을 구성 요소로 분해할 수 있습니다.

### urlparse()

형식 | urlparse(urlstring, scheme='', allow_fragments=True)
---|---
설명 | URL을 해석하여 결과를 반환합니다.
인수 | urlstring - 해석 대상 URL을 지정한다. <br> scheme - URL 스키마를 지정한다. 주어진 URL에 스키마가 포함되어 있지 않을 때만 유효하다. <br> allow_fragments - fragment 식별자를 해석할지 여부를 지정한다.
반환값 | urllib.parse.ParseResult 클래스 인스턴스

### URL 해석하기

```python
>>> from urllib import parse
>>> result = parse.urlparse('http://www.python.org/doc/;parameter?q=example#hoge')
>>> result  # parse 결과, ParseResult 클래스 인스턴스를 반환
ParseResult(scheme='http', netloc='www.python.org', path='/doc/', params='parameter', query='q=example', fragment='hoge')

>>> result.geturl()  # parse 결과로부터 URL 취득
'http://www.python.org/doc/;parameter?q=example#hoge'

>>> result.scheme  # 튜플 요소에 이름으로 접근함
'http'

>>> result[0]  # 튜플 요소에 인덱스로 접근함
'http'

>>> result.hostname  # 튜플 요소 이외에도 몇 개의 속성을 가짐
'www.python.org'
```

해석 결과인 ParseResult는 튜플의 서브클래스입니다. 튜플과 마찬가지로 언패킹하거나 슬라이스를 사용하여 요소에 접근할 수 있습니다.

### ParseResult의 속성
표에는 튜플의 각 요소가 URL "scheme://username:password@netloc:port/path;params?query#fragment"의 어떤 부분에 대응하는지 적어두었습니다.  

속성 | 값 | URL 대응 부분
---|---|---
scheme | URL 스키마(http, https 등) | scheme
netloc | 네트워크상의 위치 | username:password@netloc:port
path | 경로 계층 | /path
params | URL 인수(; 뒤의 문자열) | ;params
query | 쿼리 문자열(?hoge=hoge&fuga=fuga) | ?query
fragment | fragmant 식별자(# 뒤 문자열) | #fragment
username | 사용자 이름 | username
password | 패스워드 | password
hostname | 호스트 이름 | netloc
port | 포트 번호 | port(실제로는 수치)

## 쿼리 문자열 해석하기 - parse_qs()
parse_qs()는 쿼리 문자열을 해석하여 Python 자료구조로 변환합니다.

### parse_qs()

형식 | parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace')
---|---
설명 | 인수 qs에 지정된 쿼리 문자열을 해석한다.
인수 | qs - 쿼리 문자열을 지정한다. <br> keep_blank_values - 빈 값이 있는 쌍이 쿼리 문자열에 포함된 경우, 이 인수가 False이면 해석 결과에서 제외된다. <br> strict_parsing - False이면, parse 처리 중 오류를 무시한다. <br> encoding - Unicode로 디코딩할 때의 문자 코드를 지정한다. <br> errors - Unicode로 디코딩할 때의 동작을 지정한다.
반환값 | dict

이 함수의 결과를 dict로 반환하지만, parse_qsl()를 사용하면 각각의 쌍이 하나의 튜플을 이루는 리스트로 받을 수 있습니다. parse_qsl()의 인수는 parse_qs()와 같습니다.

### 쿼리 문자열 해석하기

```python
>>> result = parse.urlparse('https://www.google.com/search?q=python&oq=python&sourceid=chrome&ie=UTF-8')

>>> result.query
'q=python&oq=python&sourceid=chrome&ie=UTF-8'

>>> parse.parse_qs(result.query)  # parse 결과를 dict로 받고 싶으면 parse_qs를 사용
{'sourceid': ['chrome'], 'ie': ['UTF-8'], 'q': ['python'], 'oq': ['python']}

>>> parse.parse_qs('key=1&key=2')  # 하나의 키에 대한 값이 여럿일 때
{'key': ['1', '2']}

>>> parse.parse_qsl(result.query)  # parse 결과를 튜플로 받고 싶으면 parse_qsl를 사용
[('q', 'python'), ('oq', 'python'), ('sourceid', 'chrome'), ('ie', 'UTF-8')]

>>> parse.parse_qsl('key=1&key=2')  # 하나의 키에 대한 값이 여럿일 때 parse_qs와는 달리 두 개의 튜플이 됨
[('key', '1'), ('key', '2')]
```

### 인수 keep_blank_values에 따른 동작 차이

```python
>>> parse.parse_qs('key1=&key2=hoge')  # 기본으로 key1은 값이 없으므로 무시된다.
{'key2': ['hoge']}

>>> parse.parse_qs('key1=&key2=hoge', keep_blank_values=True)  # 인수를 True로 지정하면 빈 문자로 취급된다.
{'key2': ['hoge'], 'key1': ['']}
```

## 쿼리 문자열 조합하기 - urlencode()
urlencode()는 Python의 자료구조로부터 application/x-www-form-urlencoded와 같은 폼 데이터나 URL 쿼리 문자열로 사용할 수 있는 문자열을 조합합니다.

### urlcode()

형식 | urlencode(query, doseq=False, safe='', encoding=None, errors=None)
---|---
설명 | Python
인수 | query - 쿼리를 나타낼 자료구조를 지정한다. <br> doseq - True를 지정하면, 각 쌍의 값 요소에 시퀀스를 주었을 때 올바르게 해석된다. False일 때는 문자열로 해석된다. <br> encoding - Unicode로 디코딩할 때의 문자 코드를 지정한다. <br> errors - Unicode로 디코딩할 때의 동작을 지정한다.
반환값 | str

인수 query에는 dict 등 매핑형 객체 또는 두 요소로 된 튜플 리스트를 넘길 수 있습니다. dict일 때, 쿼리 문자열의 조합 순서는 보장되지 않습니다.

### 쿼리 문자열 조합하기

```python
>>> parse.urlencode({'key1':1, 'key2':2, 'key3': '파이썬'})
'key3=%ED%8C%8C%EC%9D%B4%EC%8D%AC&key2=2&key1=1'

>>> parse.urlencode([('key1',1), ('key2',2), ('key3', '파이썬')])
'key1=1&key2=2&key3=%ED%8C%8C%EC%9D%B4%EC%8D%AC'
```

### 인수 doseq에 따른 동작 차이

```python
>>> query = {'key1':'hoge', 'key2':['fuga', 'piyo']}  # key2의 값이 시퀀스인 자료구조
>>> parse.urlencode(query)  # 기본으로 deseq는 False
'key2=%5B%27fuga%27%2C+%27piyo%27%5D&key1=hoge'  # 시퀀스 ['fuga', 'piyo']는 문자열로 평가됨
>>> parse.urlencode(query, doseq=True)  # doseq에 True를 지정
'key2=fuga&key2=piyo&key1=hoge'  # 하나의 키에 여러 개의 값이 존재하는 것으로 해석됨
```
