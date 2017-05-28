---
layout: post
section-type: post
title: new TDD-Chapter 8. Prettification - Layout and Styling, and What to Test About It
category: tdd
tags: [ 'tdd' ]
---


지금까지 만든 사이트를 출시하기 위한 준비 작업에 들어갑니다. 하지만 출시하기엔 창피할 정도로 모습이 형편없습니다.

기본 스타일링(Styling)방법과 부트스트랩이라 하는  HTML/CSS 프레임워크의 통합 방법을 다룹니다.  

Django의 Static File이 어떻게 동작하는지 살펴봅니다.

## 8.1. What to Functionally Test About Layout and Style

현재 사이트는 전혀 매력적이지 않다.

![]({{ site.url }}/img/post/tdd/7_1.png)

지금부터 해야 할 작업들  

- 신규 및 기존 목록 추가를 위한 크고 멋있는 입력 필드
- 크고 시선을 끄는 중앙 입력 박스

이를 위해 TDD를 어떻게 적용하면 됩니까? 많은 사람들은 테스트에 너무 열을 올리지 말라고 합니다. 상수를 테스트하는 것처럼 테스트 자체에 어떤 값을 추가해서는 안됩니다.

하지만 제대로 동작한다는 것을 확신할 정도는 테스트할 수 있습니다. 예를 들어 스타일링을 위해 CSS를 상용할 텐데, 이 CSS는 정적 파일로 로딩됩니다. 정적 파일은 설정이 약간 어려울 수 있는데(특히 로컬을 꺼나 호스팅으로 가는 경우), 이를  위해 "Smoke Test"란 것을 이용해서 CSS가 로딩됐는지 확인하도록 합니다. 대신 메인 입력 상자가 각 페이지에 제대로 배치되는지를 간단하게 확인합니다. 이 테스트는 이후 페이지 스타일링에 대한 자신감을 줄 것입니다.

먼저 FT에 새로운 테스트 메소드를 추가합니다.

functional_tests/tests.py (ch08l001)

```python
class NewVisitorTest(LiveServerTestCase):
    [...]


    def test_layout_and_styling(self):
        # Edith goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
```

이 코드에 반영된 몇 가지 사항을 보면, 먼저 창 크기를 고정시키고 있습니다. 그리고 입력 요소를 찾은 후 크기와 위치를 취득해서 약간의 수학을 하고 있습니다. 이것은 입력 요소가 페이지 사운데 배치되도록 하기 위함입니다. assertAlmostEqual은 반올림 처리를 위한 것으로 계산 결과가 +/- 10 pixer 내에 있도록 합니다.

FT

```
$ python manage.py test functional_tests
[...]
.F.
======================================================================
FAIL: test_layout_and_styling (functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/functional_tests/tests.py", line 129, in
test_layout_and_styling
    delta=10
AssertionError: 107.0 != 512 within 10 delta

 ---------------------------------------------------------------------
Ran 3 tests in 9.188s

FAILED (failures=1)
```
이것은 예상한 실패입니다. 이론 종류의 FT는 잘못된 방향으로 가기 쉽기 때문에, 빠르긴 하지만 지저분한 '편법'을 사용하도록 합니다.이를 통해 입력 상자가 가운데 있으면 FT가 통과하게 할 수 있습니다. FT 홧인이 끝나고 나서 곧 이 코드를 지울 것입니다.

lists/templates/home.html (ch08l002)

```html
<form method="POST" action="/lists/new">
  <p style="text-align: center;">
    <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
  </p>
  {% raw %}{% csrf_token %}{% endraw %}
</form>
```
이것은 FT를 통과합니다. 이 처리를 확장해서 신규 작업 목록 체이지에서도 입력 상자가 가운데 배치되는지 확인합니다.

functional_tests/tests.py (ch08l003)

```python
    # She starts a new list and sees the input is nicely
    # centered there too
    inputbox.send_keys('testing')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: testing')
    inputbox = self.browser.find_element_by_id('id_new_item')
    self.assertAlmostEqual(
        inputbox.location['x'] + inputbox.size['width'] / 2,
        512,
        delta=10
    )
```
이것은 또 다른 테스트 실패를 초래합니다.

```
File "/.../superlists/functional_tests/tests.py", line 141, in
test_layout_and_styling
  delta=10
AssertionError: 107.0 != 512 within 10 delta
```

FT만 일단 커밋합니다.

```
$ git add functional_tests/tests.py
$ git commit -m "first steps of FT for layout + styling"
```
스타일링을 적용하기 위한 '적절한' 솔루션을 찾아야 할 것 같습니다. 편법으로 설정했던 `<p style="text-align: center">`를 다시 원상 복귀하도록 합니다.

```
$ git reset --hard
```
> `git reset --hard`는 커밋되지 않은 모든 변경 내용을 날려버리는 명령어로 사용 시에는 주의해야합니다. Git으로 거의 모든 것이 가능하지만, 이 명령 실행 후에 복구하는 것은 불가능합니다.

## 8.2. Prettification: Using a CSS Framework

디자인은 어렵고 손이 많이 가는 작업으로, 요즘에는 모바일이나 태블릿 사이트용 페이지 디자인도 신경 써야 합니다. 이런 문제를 해결하기 위해 프로그래머들은 CSS 프레임워크를 이용합니다. 많은 프레임워크가 존재하지만, 그중에서도 가장 큰 인기를 끌고 있는 것이 트위터의 부트스트랩(Bootstrap)입니다. <http://getbootstrap.com/>에서 다운로드 할 수 있습니다.

다운로드한 후에 list 앱 내에 'static'이라는 폴더를 만들어서 저장하도록 합니다.

```
$ wget -O bootstrap.zip https://github.com/twbs/bootstrap/releases/download/\
v3.3.4/bootstrap-3.3.4-dist.zip
$ unzip bootstrap.zip
$ mkdir lists/static
$ mv bootstrap-3.3.4-dist lists/static/bootstrap
$ rm bootstrap.zip
```
부트스트랩은 dist 폴더 내에 존재하며 별도의 설치가 필요하지 않습니다. 지금은 초기 상태의 부트스트랩을 그대로 사용하지만, 실제 사이트 개발 시에는 이 방법을 사용해서는 안됩니다. 이런 기본 상태의부트스트랩 사이트는 외형이 모두 동일하기 때문에, 이용자의 관점에선 디자인에 전혀 노력을 들이지 않았다고 생각할 수 있습니다. 따라서 LESS 사용법과 폰트 변경 방법 등을 배워서 적용하도록 합니다. 관련 정보는 [부트스트랩 문서](https://www.smashingmagazine.com/2013/03/customizing-bootstrap/)를 참고합니다.

작업 후 lists 폴더는 다음과 같은 구조가 됩니다.

```
$ tree lists
lists
├── __init__.py
├── __pycache__
│   └── [...]
├── admin.py
├── models.py
├── static
│   └── bootstrap
│       ├── css
│       │   ├── bootstrap.css
│       │   ├── bootstrap.css.map
│       │   ├── bootstrap.min.css
│       │   ├── bootstrap-theme.css
│       │   ├── bootstrap-theme.css.map
│       │   └── bootstrap-theme.min.css
│       ├── fonts
│       │   ├── glyphicons-halflings-regular.eot
│       │   ├── glyphicons-halflings-regular.svg
│       │   ├── glyphicons-halflings-regular.ttf
│       │   ├── glyphicons-halflings-regular.woff
│       │   └── glyphicons-halflings-regular.woff2
│       └── js
│           ├── bootstrap.js
│           ├── bootstrap.min.js
│           └── npm.js
├── templates
│   ├── home.html
│   └── list.html
├── tests.py
├── urls.py
└── views.py
```
부트스트랩 "Getting Started" 부분을 보면, HTML 템플릿에 다음과 같이 적용할 수 있다는 것을 알 수 있습니다.

```
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap 101 Template</title>
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
    <h1>Hello, world!</h1>
    <script src="http://code.jquery.com/jquery.js"></script>
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>
```
이미 두 개의 HTML 템플릿을 가지고 있습니다. 각각의 템플릿에 전체 상용구 코드(boilerplate)를 추가하는 것은 올바르지 않습니다. DRY 규칙을 적용할 시점입니다. 공통 부분을 추출해서 사용합니다. Django 템플릿 언어에는 템플릿 상속이라는 기능이 있어서 쉽게 구현이 가능합니다.

## 8.3. Django Template Inheritance

homt.html과 list.html의 차이점을 살펴봅니다.

```
$ diff lists/templates/home.html lists/templates/list.html
<     <h1>Start a new To-Do list</h1>
<     <form method="POST" action="/lists/new">
---
>     <h1>Your To-Do list</h1>
>     <form method="POST" action="/lists/{{ list.id }}/add_item">
[...]
>     <table id="id_list_table">
>       {% for item in list.item_set.all %}
>         <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
>       {% endfor %}
>     </table>
```
헤더 텍스트가 다르고 Form이 다른 URL을 사용하고 있습니다. 또한 list.html은 추가로 `<table>`요소를 가지고 있습니다.

이제 어떤 것이 공통적이고 어떤 것이 다른지 명확해졌습니다. 따라서 공통 템플릿인 'superclass'를 만들어서 두 개 템플릿이 이것을 상소갛도록 합니다. 먼저  home.html을 복사합니다.

```
$ cp lists/templates/home.html lists/templates/base.html
```
base.html 이라는 공통 템플릿을 만들어서 여기에 상용구 코드를 추가하고, 자식 템플릿이 커스터마이징할 수 있는 'block'을 설정하도록 합니다.

lists/templates/base.html

```html
<html>
  <head>
    <title>To-Do lists</title>
  </head>

  <body>
    <h1>{% raw %}{% block header_text %}{% endblock %}{% endraw %}</h1>
    <form method="POST" action="{% raw %}{% block form_action %}{% endblock %}{% endraw %}">
      <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
      {% raw %}{% csrf_token %}{% endraw %}
    </form>{% raw %}
    {% block table %}
    {% endblock %}{% endraw %}
  </body>
</html>
```
base 템플릿에는 'block'이라는 연속 영역을 정의합니다. 이것은 자식 템플릿의 콘텐츠를 추가하거나 연동할 수 있는 영역입니다. home.html이 base.html을 "상속"하도록 변경해서 어떻게 동작하는지 확인해봅니다.

lists/templates/home.html

```html
{% raw %}
{% extends 'base.html' %}


{% block header_text %}Start a new To-Do list{% endblock %}

{% block form_action %}/lists/new{% endblock %}
{% endraw %}
```
많은 사용구 HTML이 제외되고 커스텀마이징 부분에 더 집중할 수 있는 것을 확인 할 수 있습니다. list.html에도 동일한 작업을 해줍니다.

lists/templates/list.html

```html
{% raw %}
{% extends 'base.html' %}

{% block header_text %}Your To-Do list{% endblock %}

{% block form_action %}/lists/{{ list.id }}/add_item{% endblock %}

{% block table %}
  <table id="id_list_table">
    {% for item in list.item_set.all %}
      <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
    {% endfor %}
  </table>
{% endblock %}
{% endraw %}
```
이것으로 리택터링을 마쳤습니다. FT를 재실행해서 망가진 것이 없는지 확인합니다.

```
AssertionError: 107.0 != 512 within 10 delta
```
이전과 동일한 실패이기 때문에 괜찮습니다. 커밋합니다.

```
$ git diff -b
# -b 는 공백을 무시하라는 의미입니다. html 들여쓰기를 건드렸기 때문에 필요합니다.
$ git status
$ git add lists/templates # static은 일단 그대로 둡니다.
$ git commit -m "refactor templates to use a base template"
```

## 8.4. Integrating Bootstrap
이제 상용구 코드를 통합하기가 더 쉬워졌습니다.(부트스트랩을 위해 필요한 것) 아직 자바 스크립트는 사용하지 않고 CSS만 적용하도록 합니다.

lists/templates/base.html (ch08l006)

```hmtl
<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>To-Do lists</title>
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>
[...]
```

### Rows and Columns

마지막으로 부트스트랩 마법을 실제로 사용해봅니다. 그리드 시스템과 text-center 클래스를 이용하기 위해서는 관련 자료를 스스로 읽어보아야 합니다.

lists/templates/base.html (ch08l007)

```html
{% raw %}
  <body>
    <div class="container">

      <div class="row">
        <div class="col-md-6 col-md-offset-3">
          <div class="text-center">
            <h1>{% block header_text %}{% endblock %}</h1>
            <form method="POST" action="{% block form_action %}{% endblock %}">
              <input name="item_text" id="id_new_item"
                     placeholder="Enter a to-do item" />
              {% csrf_token %}
            </form>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-md-6 col-md-offset-3">
          {% block table %}
          {% endblock %}
        </div>
      </div>

    </div>
  </body>
{% endraw %}
```
> 부트스트랩이 처음이라면 시간을 내서 관련 자료를 읽어봐야합니다.  사이트에 적용하기 위한 툴들로 가득합니다.  
공식자료 : <http://getbootstrap.com/>  
한글자료 : <http://bootstrapk.com/BS3/>

동작할까요?

```
AssertionError: 107.0 != 512 within 10 delta
```

동작하지 않습니다. 왜 CSS가 로딩되지 않을까요?

## 8.5. Static Files in Django

Django 뿐만 아니라 일반 웹 서버에서 Static File을 다루기 위해서는 두 가지 사항을 고려해야 합니다.

1. URL이 Static File을 위한 것인지, 뷰 함수를 경유해서 제공되는 HTML을 위한 것인지 구분할 수 있는가?
2. 사용자가 원할 때 어디서 Static File을 찾을 수 있는가?

Static File은 특정 URL을 디스트상에 있는 파일과 매칭시키는 역할을 합니다.  

작업 아이템 1을 위해서 Django가 요구하는 것은 URL의 접두사를 정의하는 것입니다. 즉 특정 접두사로 시작하는 URL은 Static File을 위한 요청이라고 인식하는 것입니다. 이 접두사는 `/static/`으로 초기 설정돼 있습니다. 이 설정은 settings.py 파일을 통해 조정할 수 있습니다.

superlists/settings.py

```python
[...]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
```

이번 섹션에 추가할 나머지 설정들은 모두 작업 아이템 2와 관련있는 것으로, 디스크 상에 있는 실제 static file을 찾습니다.

Django의 개발 서버를 이용하고 있는 동안은(manage.py runserver), Django가 제공하는 마법같은 솔루션을 이용해서 static file을 찾을 수 있습니다. 즉 Django가 앱의 서브 폴더를 모두 검색해서 static이라는 폴더를 찾는 것입니다.

부트스트랩의 static file을 왜 `lists/static` 폴더에 두었는지 이제 그 이유를 알 수 있을 것입니다. 그런데 왜 동작하지 않습니까? 이것은 `/static/`이라는 URL 접두사를 사용하지 않았기 때문입니다. base.html에 있는 CSS 파일 링크부분을 봅니다.

lists/templates/base.html

```html
    <link href="css/bootstrap.min.css" rel="stylesheet">
```
이것을 다음과 같이 수정하면 됩니다.

lists/templates/base.html

```html
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
```
`/static/`으로 시작하기 때문에 runserver는 이 요청이 static file을 위한 것이라는 것을 알게 되었습니다. 그리고 `bootstrap/css/bootstrap.min.css`라는 파일을 찾으려고 static이라는 폴더를 검색합니다. 최종적으로는 `lists/static/bootstrap/css/bootstrap.min.css` 파일을 찾습니다.

수동으로 접속해서(localhost:8000) 제대로 동작하는 것을 확인 할 수 있습니다.

![]({{ site.url }}/img/post/tdd/8_1.png)

### Switching to StaticLiveServerTestCase

FT를 실행해보면 실패하는 것을 알 수 있다.

```
AssertionError: 107.0 != 512 within 10 delta
```

이것은 runserver가 자동으로 staticfiles을 찾을 수 있어도, `LiveServerTestCase`는 그렇지 못하기 때문입니다. 걱정할 필요는 없습니다. Django 개발자가 더 마법같은 테스트 함수를 만들었습니다. `StaticLiveServerTestCase`라는 것입니다.([참고자료](https://docs.djangoproject.com/en/1.7/howto/static-files/#staticfiles-testing-support))

그럼 이 함수로 교체해 봅니다.

functional_tests/tests.py

```python
@@ -1,14 +1,14 @@
-from django.test import LiveServerTestCase
+from django.contrib.staticfiles.testing import StaticLiveServerTestCase
 from selenium import webdriver
 from selenium.common.exceptions import WebDriverException
 from selenium.webdriver.common.keys import Keys
 import time

 MAX_WAIT = 10


-class NewVisitorTest(LiveServerTestCase):
+class NewVisitorTest(StaticLiveServerTestCase):

     def setUp(self):
```
## 8.6. Using Bootstrap Components to Improve the Look of the Site

부트스트랩이 제공하는 강력한 툴들을 이용해서 외형을 좀더 멋있게 만듭니다.

### Jumbotron!

부트스트랩은 `Jumbotron`이라는 클래스를 제공합니다. 이것은 페이지에 있는 특정 콘텐츠를 강조해주는 스타일로, 메인 페이지의 헤더와 입력 폼을 강조하기 위해 사용합니다.

lists/templates/base.html (ch08l009)

```html
{% raw %}
    <div class="col-md-6 col-md-offset-3 jumbotron">
      <div class="text-center">
        <h1>{% block header_text %}{% endblock %}</h1>
        <form method="POST" action="{% block form_action %}{% endblock %}">
          [...]
{% endraw %}
```
> 디자인이나 레이아웃을 수정할 때는 브라우저 창을 띄워 두는 것이 좋습니다. 수정시마다 브라우저를 새로고침해서 처리 결과를 바로 확인할 수 있기 때문입니다.

### Large Inputs

점보트론이 적용됐습니다. 하지만 입력 상자가 다른 것에 비해 너무 작은 글자를 보여주고 있습니다. 부트스트랩의 `form-control` 클래스를 이용하면 입력 상자를 크게 만들 수 있습니다.

lists/templates/base.html (ch08l010)

```html
    <input name="item_text" id="id_new_item"
           class="form-control input-lg"
           placeholder="Enter a to-do item" />
```

### Table Styling

이제는 테이블 글자도 다른 것들에 비해 너무 작게 보입니다. 부트스트랩의 table 클래스를 이용해서 개선해줍니다.

lists/templates/list.html (ch08l011)

```html
  <table id="id_list_table" class="table">
```

## 8.7. Using Our Own CSS

마지막으로 타이틀과 입력 상자 사이에 간격을 만듭니다. 이것을 위한 부트스트랩 기능이 없기 때문에 직접 만들어야 합니다. 사용자 지정 CSS를 설정해주어야 합니다.

lists/templates/base.html

```html
  [...]
    <title>To-Do lists</title>
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="/static/base.css" rel="stylesheet">
  </head>
```

`lists/static/base.css`라는 파일을 생성하고 신규 CSS 규칙을 정의하도록 합니다. 입력(input) 요소의 id(id_new_item)를 이용해서 해당 요소를 찾고 여기에 사용자 지정 스타일을 적용하도록 합니다.

lists/static/base.css

```html
#id_new_item {
    margin-top: 2ex;
}
```
뭔가 많이 바뀌진 않았지만 많이 개선되었습니다.

![]({{ site.url }}/img/post/tdd/8_2.png)

부트스트랩을 좀더 커스터마이징하고 싶다면 LESS 파일을 컴파일해야 합니다. 이 작업을 해볼 것을 강력 추천합니다. LESS와 유사 CSS인 SCSS는 단조로운 옛날 CSS를 크게 향상시킨 것으로, 부트스트랩을 사용하지 않더라도 매우 유용한 튤이 될 것입니다.

FT를 실행해서 모든 동작이 잘되는지 확인합니다.

```
$ python manage.py test functional_tests
[...]
...
 ---------------------------------------------------------------------
Ran 3 tests in 10.084s

OK
```

커밋하고 다음으로 넘어갑니다.

```
$ git status # changes tests.py, base.html, list.html + untracked lists/static
$ git add .
$ git status # 추가된 모든 부트스트랩 파일을 보여줍니다.
$ git commit -m "Use Bootstrap to improve layout"
```

## 8.8. What We Glossed Over: collectstatic and Other Static Directories

Django 개발 서버가 앱 폴더 내의 모든 staticfiles을 마법처럼 찾아내서 제공하는 것을 보았습니다. 이것은 개발 단계에선 괜찮지만, 실제 운영 중인 웹서버에서 Django가 정적 콘텐츠를 제공하도록 하는 것은 매우 느리며 비효율적입니다. Apache 나 Nginx 같은 웹 서버도 같은 역할을 할 수 있습니다. 또는 직접 staticfile을 호스팅하는 대신 모두 CDN(Cintent Delivery Network)에 업로드해서 호스팅하는 방법도 있습니다.

이런 이유로 여러 앱이 존재하는 모든 staticfiles을 한 곳에 모아서 배포용으로 만들어 둘 필요가 있습니다. 이 작업을 해주는 것이 `collectstatic` 명령입니다.  

수집된 staticfiles이 모이는 위치는 settings.py의 `STATIC_ROOT` 항목을 통해 설정합니다. 해당 항목 값을 리포지토리 밖에 있는 폴더로 지정합니다.

```
workspace
│    ├── superlists
│    │    ├── lists
│    │    │     ├── models.py
│    │    │
│    │    ├── manage.py
│    │    ├── superlists
│    │
│    ├── static
│    │    ├── base.css
│    │    ├── etc...
```

staticfiles이 리포지토리 밖에 있어야 하는 것이 중요합니다. lists/static 폴더 내에 있는 파일과 동일하기 때문에 굳이 코드 관리를 해줄 필요가 없기 때문입니다.  

이제 이 폴더를 설정하기 위해 프로젝트의 base 디렉터리를 기준으로 상대 경로를 지정해줍니다.

superlists/settings.py (ch08l018)

```python
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
```
상단 파일의 상단을 보면 `BASE_DIR` 변수가 `__file__`(파이썬에서는 매우 유용한 상수입니다.)을 이용해서 이미 설정돼 있는 것을 볼 수 있습니다.

준비됐으면 `collectstatic`을 실행해봅니다.

```
$ python manage.py collectstatic
[...]
Copying '/.../superlists/lists/static/bootstrap/css/bootstrap-theme.css'
Copying '/.../superlists/lists/static/bootstrap/css/bootstrap.min.css'

76 static files copied to '/.../static'.
```
생성된 `../static` 폴더를 보면 모든 CSS 파일이 복사된 것을 알 수 있습니다.

```
$ tree ../static/
../static/
├── admin
│   ├── css
│   │   ├── base.css

[...]

│               └── xregexp.min.js
├── base.css
└── bootstrap
    ├── css
    │   ├── bootstrap.css
    │   ├── bootstrap.css.map
    │   ├── bootstrap.min.css
    │   ├── bootstrap-theme.css
    │   ├── bootstrap-theme.css.map
    │   └── bootstrap-theme.min.css
    ├── fonts
    │   ├── glyphicons-halflings-regular.eot
    │   ├── glyphicons-halflings-regular.svg
    │   ├── glyphicons-halflings-regular.ttf
    │   ├── glyphicons-halflings-regular.woff
    │   └── glyphicons-halflings-regular.woff2
    └── js
        ├── bootstrap.js
        ├── bootstrap.min.js
        └── npm.js


14 directories, 76 files
```
`collectstatic`이 admin site에 있는 CSS 파일까지 가지고 온 것을 볼 수 있습니다. admin site는 Django가 가진 강력한 기능 중 하나입니다. 지금 단계에서는 필요가 없기 때문에 꺼둡니다.

superlists/settings.py

```python
INSTALLED_APPS = [
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lists',
]
```
`collectstatic`을 재실행합니다.

```
$ rm -rf ../static/
$ python manage.py collectstatic --noinput
Copying '/.../superlists/lists/static/base.css'
[...]
Copying '/.../superlists/lists/static/bootstrap/css/bootstrap-theme.css'
Copying '/.../superlists/lists/static/bootstrap/css/bootstrap.min.css'


15 static files copied to '/.../static'.
```

흩어져 있는 staticfiles을 한 폴더에 옮기는 방법을 배웠습니다.

settings.py 수정사항을 커밋합니다.

```
$ git diff # settings.py 변경 표시
$ git commit -am "set STATIC_ROOT in settings and disable admin"
```
## 8.9. A Few Things That Didn’t Make

- LESS나 SASS를 이용한 부트스트랩 커스터마이징
- DRY와 손쉬운 URL 코딩을 위한 {% raw %}{% static %}{% endraw %} 템플릿 태그
- bower, npm 같은 클라이언트 측 패키징 툴


## 정리: 디자인 및 레이아웃 테스트

디자인과 레이아웃용 테스트는 작성할 필요가 없습니다. 이것은 상수를 테스트하거나 취약성이 잠재돼 있는 테스트를 작성하는 것과 같습니다.  

디자인 및 레이아웃 구현은 CSS와 staticfiles을 내포하고 있습니다. 결과적으로 최소한의 "Smoke Test"를 이용해서 CSS와 staticfiles이 동작하는지만 확인하는 것이 좋습니다. 이를 통해 코드를 상용 서버에 배포할 때 발생할 수 있는 문제들을 찾을 수 있습니다.  

또한 작은 스타일링 코드를 적용하기 위해 다량의 클라이언트 측 자바스크립트가 요구되는 경우, 이를 위한 테스트도 반드시 필요합니다.(자바스크립트 경량화를 위해 동적 리사이징이 도움이 됩니다.)  

따라서 디자인 테스트 문제는 위험한 영역이기도 합니다. 디자인과 레이아웃이 동작한다는 것을 확신할 수 있게 하는 최소한의 테스트만 작성합니다.(이것은 디자인 코드 자체에 대한 테스트가 아닙니다.) 그리고 디자인과 레이아웃을 자유롭게 변경할 수 있도록 하고, 변경 시마자 테스트를 하거나 이전 상태로 돌리는 등의 작업은 배제하도록 합니다.
