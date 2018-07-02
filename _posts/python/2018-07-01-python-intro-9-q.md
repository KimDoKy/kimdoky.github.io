---
layout: post
section-type: post
title: Introducing Python - chap9 - 연습문제
category: python
tags: [ 'python' ]
---

## 9.1 아직 Flask를 설치하지 않았다면 지금 설치하라. Flask는 werkzeug와 jinja2, 다른 패키지들을 설치한다.

```
$ pip install flask
```

## 9.2 Flask의 디버그/리로드 개발 웹 서버를 사용하여 웹사이트의 기본 뼈대를 구축하라. 호스트 이름은 localhost, 포트 번호는 5000을 사용한다. 만약 5000번이 이미 사용되고 있다면 다른 포트 번호를 사용한다.

```Python
from flask import Flask

app = Flask(__name__)

app.run(host='localhost', port=5000)
```

## 9.3 홈 페이지에 대한 요청을 처리하는 home() 함수를 추가하라. 이 함수는 It's alive! 문자열을 반환한다.

```Python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "It's alive!"

app.run(host='localhost', port=5000)
```

## 9.4 다음 내용이 들어 있는 home.html이라는 이름의 jinja2 템플릿 파일을 생성하라.

```
I'm of course referring to {{thing}}, which is {{height}} geet tall and {{color}}.
```

```html
# templates/home.index
<html>
  <head>
    <title>home</title>
  </head>
  <body>
   I'm of course referring to {{thing}}, which is {{height}} geet tall and {{color}}.
  </body>
</html>
```

## 9.5 home.html 템플릿을 사용하기 위해 서버의 home() 함수를 수정하라. 이 함수에는 3개의 매개변수(thing, height, color)가 있다.

```Python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    kwargs = {}
    kwargs['thing'] = request.args.get('thing')
    kwargs['height'] = request.args.get('height')
    kwargs['color'] = request.args.get('color')
    return render_template('home.html', **kwargs)

app.run(host='localhost', port=5000)
```
