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
HEAD / HTTP/1.1  # 엔터를 두 번 입력해야 한다.
```

`HEAD /`는 홈페이지(/)에 대한 정보를 얻기 위해 HTTP HEAD 동사(명령)를 보낸다. 그리고 캐리지 리턴을 추가하여 빈 라인을 보낸다.

```
HTTP/1.1 200 OK
Date: Fri, 29 Jun 2018 03:56:37 GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
Server: gws
X-XSS-Protection: 1; mode=block
X-Frame-Options: SAMEORIGIN
Set-Cookie: 1P_JAR=2018-06-29-03; expires=Sun, 29-Jul-2018 03:56:37 GMT; path=/; domain=.google.com
Set-Cookie: NID=133=lS_QRsGGZVxe3T-7Dd8Xkv_oBZOwgGyHjKUfJdhvduVJcrt9IfAqQx-3yq38Cwn-h0PxaRnsIqEeMTLU5p03NtfXXu-4ZCh8tz_6FPq05luPGTxjI8Z4aPLE04wrTbzg; expires=Sat, 29-Dec-2018 03:56:37 GMT; path=/; domain=.google.com; HttpOnly
Transfer-Encoding: chunked
Accept-Ranges: none
Vary: Accept-Encoding
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

```
# requests 설치
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


## 9.2 웹 서버

파이썬은 웹 서버와 서버 사이트 프로그램을 작성하는데 뛰어나다.

웹 프레임워크는 웹사이트를 구축할 수 있는 기능(라우팅(서버 함수의 URL), 템플릿(HTML을 동적으로 생성), 디버깅 등)을 제공한다.  

### 9.2.1 간단한 파이썬 웹 서버

순수한 파이썬 HTTP 서버를 구현한다.

```
$ python -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

`0.0.0.0`은 **모든 TCP 주소** 를 의미한다. 그래서 웹 클라이언트는 서버가 어떤 주소를 가졌든 접근할 수 있다.  

현재 디렉터리에 대한 상대 경로로 파일을 요청할 수 있다. 그럼 요청한 파일이 반환된다.
웹 브라우저 주소창에 'http://localhost:8000/'를 요청하면, 서버를 실행한 경로의 디력터리의 리스트가 출력되고, 아래의 로그가 출력된다.

```
127.0.0.1 - - [29/Jun/2018 13:04:09] "GET / HTTP/1.1" 200 -
```

- '127.0.0.1'와 'localhost'는 **로컬 컴퓨터** 에 대한 TCP 동의어다.(클라이언트의 IP 주소)
- 첫 번째 '-'는 원격 사용자 이름이다.(발견된 경우)
- 두 번째 '-'는 로그인 사용자 이름이다.(요구한 경우)
- '[29/Jun/2018 13:04:09]'는 접근한 날짜와 시간이다.
- "GET / HTTP/1.1"는 웹 서버로 보내는 명령이다.
 - HTTP 메서드(GET)
 - 리소스 요청(/)
 - HTTP 버전(HTTP/1.1)
- 200은 웹 서버로부터 반환된 HTTP 상태 코드다.

브라우저에서 파일을 클릭하면, 브라우저는 포맷을 인식하여 보여준다(HTML, PNG 등). 서버는 요청에 대한 로그를 기록한다.

```
127.0.0.1 - - [29/Jun/2018 13:09:23] "GET /intoro_python/chap7_oreilly.png HTTP/1.1" 200 -
```

기본 포트는 8000이지만, 다른 포트로 지정할 수 있다.

```
$ python -m http.server 9999
```

이 기본 서버는 실제 웹사이트에서 사용하면 안된다. 매개변수를 받아서 동적인 콘텐츠를 처리하는 일을 수행할 수 없다. 아파치나 엔지닉스 등을 사용하면 정적 파일을 더 빠르게 제공한다.

### 9.2.2 웹 서버 게이트웨이 인터페이스

웹 초기 시절, **공용 게이트웨이 인터페이스(CGI.Common Gateway Interface)** 는 클라이언트를 위해 웹 서버가 외부 프로그램을 실행하고, 그 결과를 반환하도록 설계되었다. CGI는 클라이언트에서 받은 입력 인자를 서버를 통해 처리하여 외부 프로그램으로 전달하는데 프로그램은 각 클라이언트의 접근을 위해 처음부터 다시 시작된다. 이런 접근 방식은 작은 프로그램도 시작하는데 상당한 시간이 걸려 확장성이 떨어진다.  

이러한 시동 지연을 피하기 위해 웹 서버에 인터프리터를 두었다. 아파치는 mod_php 모듈 내에서는 PHP, mod_perl 모듈 내에서는 펄, mod_python 모듈 내에서는 파이썬을 실행한다. 이런 동적 언어의 코드는 장기적으로 작동하는 아파치 프로세스 내에서 실행된다.  

또 다른 방법은 별도의 장기적으로 작동하는 프로그램 내에서 동적 언어를 실행하고, 웹 서버와 통신하는 것이다.(FastCGI, SCGI)  

파이썬 웹 개발은 파이썬 웹 애플리케이셔과 웹 서버 간의 범용적인 API인 **웹 서버 게이트웨이 인터페이스(WSGI.Web Server Gateway Interface)** 의 정의에서부터 시작되었다.


### 9.2.3 프레임워크

웹 서버는 HTTP와 WSGI의 세부사항을 처리하지만 **웹 프레임워크** 를 사용하면 파이썬 코드를 작성하여 강력한 웹 사이트를 만들 수 있다.

웹 프레임워크는 최소한 클라이언트의 요청과 서버의 응답을 처리한다.

- 라우트(route) : URL을 해석하여 해당 서버의 파일이나 파이썬 코드를 찾아준다.
- 템플릿(template) : 서버 사이드의 데이터를 HTML 페이지에 병합한다.
- 인증(authentication) 및 권한(authorization) : 사용자 이름과 비밀번호, 퍼미션(permission:허가)을 처리한다.
- 세션(session) : 웹사이트에 방문하는 동안 사용자의 임시 데이터를 유지한다.

### 9.2.4 Bottle

Bottle은 하나의 파이썬 파일로 구성되어 있어서 쉽게 배포할 수 있다.

```
# bottle 설치
$ pip install bottle
```

간단히 웹서버를 실행해본다. bottle1.py 파일을 생성하여 아래 코드를 저장한다.

```Python
# bottle1.py
from bottle import route, run

@route('/')
def home():
    return 'Hello World'

run(host='localhost', port=9999)
````

파일을 실행하고 'http://localhost:9999'로 접속하면 'Hello World'를 볼 수 있다.

`run()` 함수는 bottle의 내장된 파이썬 테스트 웹 서버를 실행한다. bottle 프로그램에 사용할 필요는 없지만, 초기 개발 및 테스트에 유용하다.

```HTML
# index.html
My <b>new</b> and <i>improved</i> home page!!
````

```Python
# bottle2.py
from bottle import route, run, static_file

@route('/')
def main():
    return static_file('index.html', '.')  # .은 현재 디렉처리를 의미

run(host='localhost', port=9999)
````

My **new** and <i>improved</i> home page!!

```Python
# bottle3.py
from bottle import route, run, static_file

@route('/')
def home():
    return static_file('index.html', '.')

@route('/echo/<thing>')
def echo(thing):
    return "Say hello to my little friend: %s!" % thing

run(host='localhost', root=9999)
```
http://localhost:9999/echo/Makingfunk 으로 요청을 보내면
'Say hello to my little friend: Makingfunk!'을 확인 할 수 있다.

requests와 같은 클라이언트 라이브러리를 사용하여 잘 작동하는지 확인할 수 있다.

```Python
# bottle_test.py
import requests

resp = requests.get('http://localhost:9999/echo/Doky')

if resp.status_code == 200 and \
    resp.text == 'Say hello to my little friend: Doky!':
    print('It worked! That almost never happends!')
else:
  print('Arhg, got this:', resp.text)
```

파일을 실행하면 'It worked! That almost never happends!'라는 결과를 볼 수 있따.

이것은 **유닛 테스트(unit test)** 의 작은 예이다.  

`run()` 함수를 호출할 때 아래 인자를 추가하여 실행할 수 있다.

- `debug=True` : HTTP 에러가 발생하면 디버깅 페이지를 생성한다.
- `reloader=True` : 파이썬 코드가 변경되면 변경된 코드를 다시 불러온다.

시간이 되면 [튜토리얼](https://bottlepy.org/docs/0.12/tutorial.html#installation)을 진행해보자.

### 9.2.5 Flask

Flask는 2010년 만우절 농담으로 등장했는데, bottle(병)에 대한 익살로 flask(실험용 병)이라고 지었다.  

Bottle처럼 간단히 사용할 수 있지만, 페이스북 인증과 데이터베이스 연결 등 전문적인 웹 개발에 유용한 기능들을 지원한다.

Flask 패키지는 werkzeug WSGI 라이브러리와 jinja2 템플릿 라이브러리를 포함한다.

```
# flask 설치
$ pip install flask
```

Bottle의 예를 Flask로 바꾼다. 두 가지 참조 사항이다.

- Flask의 기본 정적 파일 디렉터리는 static이다. 파일에 대한 URL 또한 /static으로 시작한다. 포더를 '.'(현재 디렉터리)로, URL 접두사를 ''(빈 문자열)로 바꿔서 URL /를 index.html 파일로 매핑할 수 있다.
- `run()` 함수에서 `debug=True`는 서버의 코드를 다시 불러온다. Bottle에서는 디버깅과 코드를 다시 불러오는 인자가 분리되어 있다.

```Python
# flask1.py
from flask import Flask

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/echo/<thing>')
def echo(thing):
    return "Say hello to my little friend: %s" % thing

app.run(port=9999, debug=True)
```

Bottle의 예와 똑같은 결과을 볼 수 있다.

`run()` 함수를 호출할 때 `debug=True`로 설정하면 여러 이점이 있다. 서버 코드에서 예외가 발생하면 Flask는 오류 정보와 어디가 잘못되었는지에 대한 내용을 페이지로 표시해준다. 더 좋은 점은 서버 프로그램의 변숫값을 보기 위해 몇 가지 명령을 입력할 수 있다.

Bottle에서는 할 수 없는 것들 중 하나는 템플릿 시스템이다.(jinja2)  

templates 디렉터리를 생성하고, flask2.html 파일을 생성한다.

```html
<html>
  <head>
    <title>Flask2 Example</title>
  </head>
  <body>
    Say hello my little friend: {{ thing }}
  </body>
</html>
```

여러 방법으로 두 번째 인자를 echo URL에 전달할 수 있다.

#### URL 경로로 인자 전달하기

```html
# flask3.html
<html>
  <head>
    <title>Flask2 Example</title>
  </head>
  <body>
    Say hello my little friend: {{ thing }}.
    Alas, it just destroyed {{ place }}!
  </body>
</html>
```

```Python
# flask3a.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/echo/<thing>/<place>')
def echo(thing, place):
    return render_template('flask3.html', thing=thing, place=place)

app.run(port=9999, debug=True)
```
http://localhost:9999/echo/doky/Corea 으로 접속하면 "Say hello my little friend: doky. Alas, it just destroyed Corea!"라는 결과를 볼 수 있다.

#### GET 매개변수로 인자 제공

```Python
# flask3b.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/echo/')
def echo():
    thing = request.args.get('thing')
    place = request.args.get('place')
    return render_template('flask3.html', thing=thing, place=place)

app.run(port=9999, debug=True)
```

http://localhost:9999/echo/?thing=Doky&place=Corea 으로 접속하면 "Say hello my little friend: Doky. Alas, it just destroyed Corea!"라는 결과를 볼 수 있다.

GET 명령이 URL에 사용되는 경우 인자가 `&key=val1&key2=val2&...` 형태로 전달된다. 또한 딕셔너리 `**` 연산자를 사용하여 한 딕셔너리로부터 여러 인자를 템플릿에 전달할 수 있다.

```python
# flask3c.py
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/echo/')
def echo():
    kwargs = {}
    kwargs['thing'] = request.args.get('thing')
    kwargs['place'] = request.args.get('place')
    return render_template('flask3.html', **kwargs)

app.run(port=9999, debug=True)
```

동일한 결과를 같는다.

`**kwargs`는 `thing=thing, place=place`처럼 동작한다. 입력 인자가 많을 경우 타이핑을 줄일 수 있다.
