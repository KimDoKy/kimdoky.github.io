---
layout: post
section-type: post
title: Introducing Python - Chap9.웹
category: python
tags: [ 'python' ]
---

# Chap9. 웹

- 원격 사이트에 접근할 수 있는 클라이언트
- 웹사이트와 웹 API에서 데이터를 제공하는 서버
- 웹 페이지 이외의 데이터를 교환하기 위한 웹 API와 서비스

## 9.1 웹 클라이언트

TCP/IP는 low-level의 인터넷 네트워크 배관이다. 컴퓨터 간의 바이트를 전송하고, 그 바이트를 해석하는건 더 높은 수준의 프로토콜이 처리한다.  
HTTP는 웹 데이터를 교환하는 표준 프로토콜이다.  

웹은 클라이언트-서버 시스템이다. 클라이언트는 서버에 대한 request를 만든다. 이 요청은 TCP/IP 커넥션을 열고, HTTP를 통해 URL과 다른 정보를 보낸다. 그리고 요청에 대한 response를 받는다.  

response 포맷 또한 HTTP에 의해 정의되었다. 응답 포맷은 요청에 대한 상태와 응답 데이터를 포함한다.  

잘 알려진 웹 클라이언트는 웹 브라우저다. 웹 브라우저는 다양한 방법으로 HTTP 요청을 만든다. 주소창에 URL을 입력하거나 링크를 클릭하여 요청을 한다. 대부분의 반환된 데이터는 웹사이트를 출력하는데 사용된다.(HTML,CSS,img 등)  

HTTP는 **무상태** 이다. 웹 브라우저에서 생성된 각 HTTP 커넥션은 모두 독립적이다. 이건 웹 작동을 단순하게 하지만, 그 이외의 것들은 웹을 복잡하게 만든다.

- **캐싱(caching)** : 변하지 않는 원격 콘텐츠는 웹 클라이언트에 저장하고, 다시 서버로부터 이 콘텐츠의 다운로드를 피하기 위해 저장된 콘텐츠를 사용한다.
- **세션(session)** : 쇼핑 웹사이트는 쇼핑 카트(장바구니)의 콘텐츠를 기억해야 한다.
- **인증(authentication)** : 아이디와 비밀번호를 요구하는 사이트는 사용자가 로그인할 때, 이 둘을 기억하여 사용자를 식별한다.

무상태에 대한 해결책은 **쿠키(cookie)** 가 있다. 서버가 클라이언트를 식별할 수 있도록 보내는 특정 정보가 쿠키이다. 쿠키는 클라이언트와 서버가 서로 식별할 수 있게 한다.

### 9.1.1 텔넷으로 테스트하기

HTTP는 텍스트 기반 프로토콜이다. 텔넷으로 서버의 포트에 연결하여 명령할 수 있다.

```
# google.com에 80번 포트의 웹서버가 있다면, telnet은 연결이 가능한지 정보를 출력한다.
# 그리고 마지막으로 텔넷 사용자가 입력해야 할 빈 줄을 표시한다.
$ telnet www.google.com 80
Trying 172.217.25.68...
Connected to www.google.com.
Escape character is '^]'.
```

일반적인 HTTP 명령은 GET이다. 이는 HTML파일과 같은 지정된 리소스의 내용을 검색하여 클라이언트에 반환한다. 테스트는 HTTP의 HEAD 메서드를 사용한다. HEAD 메서드는 리소스에 대해 몇 가지 기본 정보를 검색한다.

```
HEAD / HTTP/1.1
```

`HEAD /`는 홈페이지(/)에 대한 정보를 얻기 위해 HTTP HEAD 동사(명령)를 보낸다. 그리고 캐리지 리턴을 추가하여 빈 라인을 보낸다.

```
HTTP/1.0 400 Bad Request      #  .. T^T
Content-Type: text/html; charset=UTF-8
Referrer-Policy: no-referrer
Content-Length: 1555
Date: Thu, 28 Jun 2018 12:17:38 GMT
```

HTTP 응답 헤더와 헤더값이다. Date와 Content-Type 같은 헤더는 꼭 응답이 온다. 그리고 Set-Cookie 같은 헤더는 사용자의 여러 방문 활동을 추적하는데 사용된다.
HTTP HEAD 요청을 할 때 헤더만 응답받는다. HTTP GET 또는 POST 명령을 사용할 홈페이지로부터 데이터도 받게 된다.

텔넷 종료는 `q`다.

### 9.1.2 파이썬 표준 웹 라이브러리

파이썬 3에서는 웹 클라이언트와 서버 모듈이 패키지로 묶여있다.

- http는 모든 클라이언트-서버 HTTP 세부사항을 관리한다.
 - client는 클라이언트 부분을 관리한다.
 - server는 파이썬 웹 서버를 작성하는데 도움을 준다.
 - cookie와 cookiejar는 사이트 방문자의 데이터를 저장하는 쿠키를 관리한다.
- urllib는 http 위에서 실행된다.
 - request는 클라이언트의 요청을 처리한다.
 - response는 서버의 응답을 처리한다.
 - parser는 URL을 분석한다.

```Python
# 포춘 쿠키와 유사한 임의의 텍스트 문장을 반환하는 URL
>>> import urllib.request as ur
>>> url = 'http://quotesondesign.com/wp-json/posts'
>>> conn = ur.urlopen(url)
>>> print(conn)
<http.client.HTTPResponse object at 0x106082ef0>
```

`conn`은 다수의 메서드를 지닌 'HTTPResponse' 객체이다. 그리고 `read()` 메서드는 웹 페이지로부터 데이터를 읽어온다.  

```Python
>>> data = conn.read()
>>> print(data)
b'[{"ID":2463,"title":"Antoine de Saint-Exupery","content":"<p>If you want to build a ship, don&#8217;t drum up people to collect wood and don&#8217;t assign them tasks and work, but rather teach them to long for the endless immensity of the sea.<\\/p>\\n","link":"https:\\/\\/quotesondesign.com\\/antoine-de-saint-exupery-4\\/"}]'
```

이 코드로 원격 인용구 서버에 TCP/IP 커넥션을 열었고, HTTP 요청을 만들었고, HTTP 응답을 받았다. 중요한 부분 중 하나는 **HTTP 상태 코드** 다.

```Python
>>> print(conn.status)
200
```

#### 응답 코드

- 1xx(조건부 응답) : 서버는 요청을 받았지만, 클라이언트에 대한 몇 가지 추가 정보가 필요하다.
- 2xx(성공) : 성공적으로 처리되었다. 200 이외의 모든 성공 코드는 추가사항을 전달한다.
- 3xx(리다이렉션) : 리소스가 이전되어 클라이언트에 새로운 URL을 응답해준다.
- 4xx(클라이언트 에러) : 자주 발생하는 404는 클라이언트 측에 문제가 있음을 나타낸다. 418과 같은 만우절 농담고 있다.
- 5xx(서버 에러) : 500은 서버 에러를 나타낸다. 웹 서버와 백엔드 애플리케이션 서버가 연결되어 있지 않다면 502(불량 게이트웨이)를 볼 것이다.

웹 서버는 원하는 포맷으로 데이터를 전송할 수 있다. 일반적으로 HTML을 전송하지만, 포춘쿠키에 대한 예는 json 포맷이다.  
데이터 포맷은 google.com 예에서 본 것처럼 HTTP 헤더의 Content-Type 값에 있다.

```Python
>>> print(conn.getheader('Content-Type'))
application/json; charset=UTF-8
```

application/json 문자열은 MIME(Multipurpose Internet Mail Extensinos) 타입이다. HTML을 위한 MIME 타입은 text/html이다.

다른 HTTP 헤더는?

```Python
>>> for key, value in conn.getheaders():
...      print(key, value)
...
Server nginx
Date Thu, 28 Jun 2018 12:34:20 GMT
Content-Type application/json; charset=UTF-8
Content-Length 322
Connection close
X-Powered-By PHP/5.4.13
X-Content-Type-Options nosniff
Link </wp-json/posts?page=2>; rel="next", <https://quotesondesign.com/wp-json/posts/2463>; rel="item"; title="Antoine de Saint-Exupery"
X-WP-Total 1065
X-WP-TotalPages 1065
Last-Modified Thu, 08 Mar 2018 20:05:23 GMT
X-Powered-By PleskLin
```

파이썬 라이브러리는 모든 HTTP 응답 헤더를 파싱하여 딕셔너리로 제공한다.

### 9.1.3 표준 라이브러리를 넘어서: Requests

써드파티의 'requests' 모듈을 사용하여 앞과 같은 프로그램을 만든다.

'requests' 모듈을 사용하면 개발이 더 쉬워진다.

##### 설치

```
$ pip install requests
```

```Python
>>> import requests
>>> url = 'http://quotesondesign.com/wp-json/posts'
>>> resp = requests.get(url)
>>> resp
<Response [200]>
>>> print(resp.text)
[{"ID":2463,"title":"Antoine de Saint-Exupery","content":"<p>If you want to build a ship, don&#8217;t drum up people to collect wood and don&#8217;t assign them tasks and work, but rather teach them to long for the endless immensity of the sea.<\/p>\n","link":"https:\/\/quotesondesign.com\/antoine-de-saint-exupery-4\/"}]
```

'urllib.request.urlopen' 모듈과 사용한 것과 차이는 없지만, 코드가 더 간편하다.
