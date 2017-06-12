---
layout: post
section-type: post
title: urllib 라이브러리
category: python
tags: [ 'python' ]
---
urllib 라이브러리는 Python에서 웹과 관련된 데이터를 쉽게 이용하게 도와주는 라이브러리입니다.  

## 1. `urllib`의 주요 모듈 활용하기
urllib 라이브러리 안에 총 4개의 모듈이 존재하는데 그 중 하나는 웹을 열어서 데이터를 읽어오는 역할을 하는 `request` 모듈입니다.

### 웹 문서 불러오기
```python
>>> import urllib.request
>>>
>>> req = urllib.request
>>> req.urlopen("https://kimdoky.github.io")
<http.client.HTTPResponse object at 0x102745358>
```
`urlopen`함수의 인수에 데이터를 얻고 싶은 웹 페이지의 주소를 넣어주면 됩니다. `urlopen`함수는 우베에서 얻은 데이터에 대한 객체를 돌려줍니다.

### 웹 서버의 정보 받아오기
```python
>>> d = req.urlopen("https://kimdoky.github.io")
>>> status = d.getheaders()
>>> for s in status:
...     print(s)
...
('Server', 'GitHub.com')
('Content-Type', 'text/html; charset=utf-8')
('Strict-Transport-Security', 'max-age=31557600')
('Last-Modified', 'Sun, 11 Jun 2017 17:05:29 GMT')
('Access-Control-Allow-Origin', '*')
('Expires', 'Mon, 12 Jun 2017 06:48:26 GMT')
('Cache-Control', 'max-age=600')
('X-GitHub-Request-Id', 'D688:078B:3674E2D:4493F9A:593E36E2')
('Content-Length', '18158')
('Accept-Ranges', 'bytes')
('Date', 'Mon, 12 Jun 2017 06:40:59 GMT')
('Via', '1.1 varnish')
('Age', '152')
('Connection', 'close')
('X-Served-By', 'cache-nrt6122-NRT')
('X-Cache', 'HIT')
('X-Cache-Hits', '1')
('X-Timer', 'S1497249659.109658,VS0,VE1')
('Vary', 'Accept-Encoding')
('X-Fastly-Request-ID', 'e7d21faf9dc1c9baf4f8c6ee11bba5bf187b0ebe')
>>>
```
`getheaders()` 함수를 사용하면 서버에 대한 정보를 리스트로 돌려줍니다. 리스트를 출력해보면 운영체제나 날짜, 타입 등 여러 가지 정보를 알 수 있습니다. 이 정보들은 그롤링하려는 홈페이지가 어떤 형식으로 만들어 졌는지 알 수 있습니다.  

### 웹 페이지의 상태 확인하기
```python
>>> d = req.urlopen("https://kimdoky.github.io")
>>> d.status
200
```
`status`라는 변수를 조회하니까 200이 출력된 걸 볼 수 있습니다.

### 웹 페이지의 데이터를 읽어오기
```python
>>> d = req.urlopen("https://kimdoky.github.io")
>>> d.status
200
>>> d = req.urlopen("https://kimdoky.github.io")
>>> d.read()
b'\n<!-- Index Layout Start -->\n\n<!DOCTYPE html>\n<html lang="ko">\n\n  \n<!-- HEAD Start -->\n\n<head>\n  \n\n\n  <!-- Force HTTPS Start -->\n  <script>\n  // Don\'t force http when serving the website locally\n  if (!(window.location.host.startsWith("127.0.0.1")) && (window.location.protocol != "https:"))\n    window.location.protocol = "https";\n  </script>\n\n  <!-- Force HTTPS End -->\n\n\n\n  <meta charset="utf-8">\n  <meta http-equiv="X-UA-Compatible" content="IE=edge">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <meta name="description" content="Python, Django Web Developer">\n  <meta name="author" content="DoKy">\n  <meta name="keywords" content="makingfunk, KimDoKy, \xeb\x8f\x84\xea\xb2\xbd, django, python">\n
# 이하 생략
```
`read()` 함수를 사용하게 되면 문서의 HTML 코드를 출력합니다.  
크롤러를 제작할 때도 `read()`함수를 사용해서 HTML 코드를 불러온 뒤 원하는 데이터만 골라내는 작업을 하게 됩니다.

다음은 `urllib.parse`라는 모듈을 살펴보겠습니다. `urllib.parse`모듈은 url에 한글 검색어를 입력할 수 있도록 도와주는 모듈입니다.  

한글로 검색을 하기 위해서는 한글을 인코딩이란 과정을 거쳐서 데이터를 요청해야 하는데 이때 인코딩을 해주는 모듈이 `urllib.parse` 모듈입니다.
```python
>>> import urllib.parse
>>>
>>> def input_query():
...     q = str(input("검색어를 입력하세요: "))
...     return "&quuery=" + q
...
>>> input_query()
검색어를 입력하세요: 무한도전
'&quuery=무한도전'
>>>
>>> def input_query2():
...     q = urllib.parse.quote_plus(str(input("검색어를 입력하세요: ")))
...     return "&query=" + q
...
>>> input_query2()
검색어를 입력하세요: 무한도전
'&query=%EB%AC%B4%ED%95%9C%EB%8F%84%EC%A0%84'
>>>
```
첫 번째 함수는 `urllib.parse.quote_plus`를 사용하지 않아서 결과값에서 한글이 그대로 보이지만 두 번째 함수는 변환이 되어서 출력되었습니다.  

첫 번째 함수의 결과를 웹 브라우저에게 전달하면 웹 브라우저는 무슨 말인지 알아 듣지 못합니다. 그래서 웹에서 처리하기 좋은 방법으로 변환을 하는데 그때 `urllib.parse` 함수가 힘을 발휘합니다.  

url에 한글로 검색어를 요청하기 위해서는 반드시 `quote_plus` 함수를 사용해야 합니다.  
그리고 `quote_plus`함수 말고 `quote`라는 기본적인 함수도 있는데 이 함수와 `quote_plus` 함수의 차이점은 `quote_plus`는 공뱃을 `+` 기호로 처리하고 `quote` 함수는 공백을 `%20`으로 인코딩합니다.

`quote_plus`가 권장하는 함수이지만, `quote`를 써도 검색이 제대로 되니까 무엇을 사용하든 상관없습니다.
