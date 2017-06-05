---
layout: post
section-type: post
title: new TDD-Chapter 3. Testing a Simple Home Page with Unit Tests
category: tdd
tags: [ 'tdd' ]
---

## 3.1. Our First Django App, and Our First Unit Test
Django는 코드를 앱(app) 형태로 구조화하도록 도와줍니다. 이론상 하나의 프로젝트는 여러 앱을 가질 수 있으며, 다른 사람이 만든 외부 앱도 사용할 수 있습니다. 또한 다른 프로젝트에서 만든 자신의 앱을 재사용할 수도 있습니다. 하지만 여기서는 이런 방식들을 사용하지 않습니다.  

작업 목록 앱을 시작합니다.

```
$ python manage.py startapp lists
```
이것을 실행하면 `superlists/superlists`외 같은 위치에서 `superlists/lists`라는 폴더가 생성됩니다. 이 폴더는 다음과 같이 모델(Model), 뷰(View) 등의 템플릿을 가지고 있으며, **test** 템플릿도 포함합니다.

```
superlists/
├── db.sqlite3
├── functional_tests.py
├── lists
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
└── superlists
    ├── __init__.py
    ├── __pycache__
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

## 3.2. Unit Tests, and How They Differ from Functional Tests
**기능 테스트**는 사용자 관점에서 애플리케이션 외부를 테스트하는 것이고, **단위 테스트**는 프로그래머 관점에서 그 내부를 테스트한 것입니다.  

여기서 다루는 TDD 접근법은 양쪽 테스트를 모두 적용합니다. 이후 작업 순서는 다음과 같습니다.

1. 기능 테스트를 작성해서 사용자 관점의 새로운 기능성을 정의하는 것부터 시작합니다.
2. 기능 테스트가 실패하고 나면 어떻게 코드를 작성해야 테스트를 통과할지(또는 적어도 현재 문제를 해결할 수 있는 방법)을 생각해봅니다. 이 시점에서 하나 또는 그 이상의 단위 테스트를 이용해서 어떻게 코드가 동작해야 하는지 정의합니다.(기본적으로 모든 코드가 (적어도) 하나 이상의 단위 테스트에 의해 테스트돼야 합니다.)
3. 단위 테스트가 실패하고 나면 단위 테스트가 통과할 수 있을 정도의 최소한의 코드만 작성합니다. 기능 테스트가 완전해질 때까지 과정 2,3을 반복해야 할 수도 있습니다.
4. 기능 테스트를 재실행해서 통과하는지 또는 제대로 동작하는지 확인합니다. 이 과정에서 새로운 단위 테스트를 작성해야 할 수도 있습니다.

이 과정을 잘 보면, 기능 테스트는 상위 레벨의 개발을 주도하고 단위 테스트는 하위 레벨을 주도한다는 것을 알 수 있습니다.  

과정이 너무 많다고 느껴질 수도 있지만 기능 테스트와 단위 테스트가 전혀 다른 목적을 가지고 있어서 서로 다른 결과를 초래할 수 있기 때문에 꼭 필요한 과정입니다.

> 기능 테스트는 제대로 된 기능성을 같춘 애플리케이션을 구축하도록 도우며, 그 기능성이 망가지지 않도록 보장해 줍니다. 반면, 단위 테스트는 깔끔하고 버그 없는 코드를 작성하도록 돕습니다.

## 3.3. Unit Testing in Django

홈페이지 뷰를 위한 단위 테스트를 어떻게 작성하는지 봅니다.

lists/tests.py

```python
from django.test import TestCase

# Create your tests here.
```
Django는 특수한 `TestCase` 버전을 사용하도록 하고 있습니다. 기본 `unittest.TestCase`의 확장 버전으로, 다음 섹션에서 다룰 몇 가지 Django 특화 기능들이 추가돼 있습니다.  

TDD 주기는 실패 테스트를 작성한 후 테스트를 통과할 수 있는 코드를 작성하는 과정이라는 것을 보았습니다. 단위 테스트의 경우에는 그것이 어떠한 형태든 자동화된 테스트 실행자에 의해 실행된다는 것을 알아둘 필요가 있습니다. `functional_tests.py`는 직접 실행해야 하지만, Django를 이용해 만든 파일은 좀더 마법같이 느껴집니다. 고의적인 실패 테스트를 만들어서 이를 확인해봅니다.

lists/tests.py

```python
from django.test import TestCase

class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
```
실행자는 manage.py 명령을 이용하면 됩니다.

```
$ python manage.py test
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_bad_maths (lists.tests.SmokeTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/lists/tests.py", line 6, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

 ---------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```
제대로 동작하는 것 같습니다. 커밋합니다.

```
$ git status  # should show you lists/ is untracked
$ git add lists
$ git diff --staged  # will show you the diff that you're about to commit
$ git commit -m "Add app for lists, with deliberately failing unit test"
```

## 3.4. Django’s MVC, URLs, and View Functions

Django는 대체로 **모델-뷰-컨트롤러(Model-View-Controller,MVC)** 라는 고전적인 패턴을 따릅니다. 이런 개념적인 부분이 있지만, Django의 주요 역할은 일반적인 웹 서버처럼 사용자가 특정 URL을 요청했을 때 어떤 처리를 할지 결정하는 것입니다. Django의 처리 흐름은 다음과 같습니다.  

1. 특정 URL에 대한 HTTP "요청"을 받습니다.
2. Django는 특정 규칙을 이용해서 해당 요청에 어떤 뷰 함수를 실행할지 결정합니다.(URL "해석"이라고 하는 처리입니다.)
3. 이 뷰 기능이 요청을 처리해서 HTTP "응답"으로 반환합니다.

따라서 테스트해야 할 것은 두 가지입니다.

- URL의 사이트 루트("/")를 해석해서 특정 뷰 기능에 매칭시킬 수 있는가?
- 이 뷰 기능이 특정 HTML을 반환하게 해서 기능 테스트를 통과할 수 있는가?

첫 번째 것부터 시작합니다.

lists/tests.py

```python
from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page  #2

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  #1
        self.assertEqual(found.func, home_page)  #1
```

> #1 : `resolve`는 Django가 내부적으로 사용하는 함수로, URL을 해석해서 일치하는 뷰 함수를 찾습니다. 여기서는 "/"(사이트 루트)가 호출될 때 `resolve`를 실행해서 `home_page`라는 함수를 호출합니다.
> #2 : `home_page` 함수는 무엇입니까? 곧 작성하게 될 뷰 함수로 HTML을 반환합니다.

이 테스트를 실행하면 어떤 일이 발생할까요?

```
$ python manage.py test
ImportError: cannot import name 'home_page'
```
예상한 대로 import 실패 에러가 발생합니다.

## 3.5. At Last! We Actually Write Some Application Code!

TDD는 인내를 요하는 작업으로 점진적으로 진행되며 개선 속도도 느립니다. 특히 지금은 배우는 과정이기 때문에, 한 번에 한 줄의 코드만 수정(또는 추가)해 갈 것입니다. 실패 테스트를 해겨랗기 위한 최소한의 수정만 하도로고 합니다.  

현재 실패 테스트는 임포트 실패입니다. 해결해 봅시다.

lists/views.py

```python
from django.shortcuts import render

# Create your views here.
home_page = None
```
"응?" 이것이 이후 실습의 시발점이자 모든 것이라는 곳을 곧 알게 될 것입니다. 일단 시키는 대로 ㄱ
ㄱ !!

테스트를 실행해봅니다.

```
$ python manage.py test
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (lists.tests.HomePageTest) #2
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/lists/tests.py", line 8, in
test_root_url_resolves_to_home_page_view
    found = resolve('/') #3
  File ".../django/urls/base.py", line 27, in resolve
    return get_resolver(urlconf).resolve(path)
  File ".../django/urls/resolvers.py", line 392, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.urls.exceptions.Resolver404: {'tried': [[<RegexURLResolver #1
<RegexURLPattern list> (admin:admin) ^admin/>]], 'path': ''} #1

 ---------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (errors=1)
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

> ## 트래이스백 읽기  
> 트래이스백을 빠르게 읽어서 필요한 단서를 찾는 방법을 배웁시다.
> #1 : 먼저 확인해야 할 것이 "에러"입니다. 이 에러 부분이 핵심인데, 어떤 때는 이 부분만 읽고 바로 문제를 파악할 수 있습니다. 여기서는 이 에러만으로는 파악이 어렵습니다.  
> #2 : 다음으로 확인할 것은 "어떤 테스트가 실패하고 있는가?"입니다. 이 실패가 예측된 실패인지를 확인해야 합니다. 이 예에서는 예측된 실패입니다.  
> #3 : 마지막으로 실패를  발생시키는 "테스트 코드"를 찾습니다. 트래이스백 상단부터 아래로 내려가면서 테스트 파일명을 찾습니다. 그래서 어떤 테스트 함수의 몇 번째 코드 라인에서 실패가 발생하는지 확인합니다. 이 예에선 `resolve` 함수를 호출해서 "/" URL을 해석하는 부분입니다.  
문제 있는 코드를 확인할 때 일반적으로 사용하는 4단계 과정입니다. 이후로 계속 이 4단계 과정을 통해  django 코드를 확인하는 것을 보게 될 것입니다.  
이렇게 모든 정보를 취합해 트래이스백을 해석한 결과, "/"를 확인하려고 할 때 Django가 404 에러를 발생시키고 있다는 것을 알게 되었습니다. 즉 Django가 "/"에 해당하는 URL 맵핑을 찾을 수 없습니다.

## 3.6. urls.py

Django는 urls.py라는 파일을 이용해서 어떻게 URL을 뷰 함수에 맵핑할지 정의합니다.

superlists/urls.py

```python
"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
```

이전과 마찬가지로 도움이 되는 주석과 사용 방법 등이 적혀 있습니다.  

url 항목은 정규표현으로 시작하며, 어떤 URL을 해석해서 어떤 함수로 요청을 보낼지를 정의합니다. 대상 함수는 `superlists.views.home`처럼 마침표 조합의 형태입니다. 또는 `include`를 이용해서 다른 urls.py 파일을 지정할 수도 있습니다.

첫 번째 예제 항목은 정규표현식 `^$`을 가지고 있는데, 이는 빈 문자열을 의미합니다. 이것이 "/"로 테스트한 우리 사이트의 루트와 같을 수 있을까요?

> 정규표현이 처음이라면, 지금 시점에서는 중요하지 않으니 넘어가도 되지만 배워두면 이후에 도움이 될 것입니다.

기본으로 관리 사이트를 위한 하나의 url 항목이 존재하는 것을 볼 수 있습니다. 지금은 사용하지 않기 때문에 주석처리 하도록 합니다.

superlists/urls.py

```python
from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
]
```
**python manage.py test** 으로 단위 테스트를 다시 실행해봅니다.

```
python manage.py test

[...]
TypeError: view must be a callable or a list/tuple in the case of include().
```
지전이 있습니다. 더 이상 404 에러가 발생하지 않습니다. 대신에 "/"와 lists/views.py의 `home_page = None` 사이의 링크를 만들었지만 `home_page` 뷰를 호출 할 수 없다고 합니다. 이것은 `None`에서 실제 기능으로 바꾸는것에 대한 정당성을 줍니다. 모든 단일 코드 변경은 테스트를 통해 이루어 집니다.

lists/views.py

```python
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```

테스트를 진행합니다.

```
$ python manage.py test
Creating test database for alias 'default'...
.
 ---------------------------------------------------------------------
Ran 1 test in 0.003s

OK
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```
첫 단위 테스트가 성공했습니다. 커밋합니다.

```
$ git diff  # should show changes to urls.py, tests.py, and views.py
$ git commit -am "First unit test and url mapping, dummy view"
```

> `git commit -am`은 빠른 처리를 위한 것으로 최소한의 커밋 내용만 보여줍니다. 따라서 사전에 `git status`나  `git diff`를 이용해서 변경 내역을 잘 파악해두는 것이 좋습니다.

## 3.7. Unit Testing a View

뷰를 위한 테스트를 작성할 때는 단순히 빈 함수를 반복하는 것이 아니라 HTML 형식의 실제 응답을 반환하는 함수를 작성해야 합니다. lists/tests.py를 열어서 새로운 테스트를 추가합니다.

lists/tests.py

```python
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  #1
        response = home_page(request)  #2
        html = response.content.decode('utf8')  #3
        self.assertTrue(html.startswith('<html>'))  #4
        self.assertIn('<title>To-Do lists</title>', html)  #5
        self.assertTrue(html.endswith('</html>'))  #4
```
새로운 테스트에선 어떤 일이 벌어지고 있습니까?

> #1 : `HttpRequest` 객체를 생성해서 사용자가 어떤 요청을 브라우저에 보내는지 확인합니다.  
> #2 : 이것을 `home_page` 뷰에 전달해서 응답을 취득합니다. 이 객체는 `HttpResponse`라는 클래스의 인스턴스입니다. 응답 내용(HTML 형태로 사용자에게 보내는 것)이 특정 속성을 가지고 잇는지 확인합니다.  
> #3 : 그런 다음 응답의 내용을 추출합니다. 이 내용은 raw byte으로 1, 0으로 브라우저로 전송됩니다. `decode()`를 호출해서 사용자에게 보내지는 HTML 문자열로 변환합니다.
> #4 : 시작과 끝이 `<HTML>, </HTML>` 태그로 되는지 확인합니다.
> #5 : 변환 내용의 `<title>`태그에 "To-Do lists"라는 단어가 있는지 확인합니다. 앞선 기능 테스트에서 확인한 것이기 때문에 단위 테스트도 확인해주어야 합니다.

한 번 더 강조하지만, 단위 테스트는 기능 테스트에 의해 파생되며 더 실제 코드에 가깝습니다. 따라서 지금은 프로그래머처럼 생각해야 합니다.

FT를 실행힙니다.

```
TypeError: home_page() takes 0 positional arguments but 1 was given
```

### The Unit-Test/Code Cycle
여기서부터  **TDD 단위 테스트-코드 주기** 에 대해 생각해야 합니다.

1. 터미널에서 단위 테스트를 실행해서 어떻게 실행하는지 확인합니다.
2. 편집기상에서 현재 실패 테스트를 수정하기 위한 최소한의 코드를 변경합니다.

그리고 이것을 반복합니다.

코드 품질을 높이고 싶다면 코드 변경을 최소화해야 합니다. 또한 이렇게 최소화한 코드는 하나하나 테스트에 의해 검증되어야 합니다. 매우 고된 작업이라고 생각될 수 있지만, 한번 익숙해지기 시작하면 속도는 빨라집니다. 따라서 아무리 자신 있는 부분이라도 작은 다누이로 나누어 코드를 변경하도록 합니다.  

얼마나 빨리 이 주기를 따라갈 수 있는지 봅시다.

- 최소한의 코드 변경:  
lists/views.py

```
def home_page(request):
    pass
```

- 테스트

```
html = response.content.decode('utf8')
AttributeError: 'NoneType' object has no attribute 'content'
```

- 코드 :  가정한 대로 `django.http.HttpResponse`를 사용합니다.

lists/views.py

```
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse()
```

- 다시 테스트:

```
self.assertTrue(html.startswith('<html>'))
AssertionError: False is not true
```

- 다시 코드:

lists/views.py

```
def home_page(request):
    return HttpResponse('<html>')
```

- 테스트:

```
AssertionError: '<title>To-Do lists</title>' not found in '<html>'
```

- 코드:

lists/views.py

```
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title>')
```

- 테스트 - 거의 다 했습니다.

```
self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true
```

- 드디어 마지막!

lists/views.py

```
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')
```

- 확실합니까?

```
$ python manage.py test
Creating test database for alias 'default'...
..
 ---------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```
이제 FT를 실행해봅시다. 개발 서버를 가동하는 것을 잊지 마세요. 정말 끝낼 수 있을까요?

```
$ python functional_tests.py
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 19, in
test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

 ---------------------------------------------------------------------
Ran 1 test in 1.609s

FAILED (failures=1)
```
실패? 여기서 실패는 작업 완료 메시지를 출력하기 위해 심어둔 `AssertionError` 때문입니다. 성공한 것입니다. 드디어 웹 페이지를 갖게 되었습니다.  

커밋합니다.

```
$ git diff  # should show our new test in tests.py, and the view in views.py
$ git commit -am "Basic view now returns minimal HTML"
```
꽤 많은 작업을 하였습니다. `git log --oneline`을 실행해서 지금까지 작업한 것을 확인합니다.

```
$ git log --oneline
a6e6cc9 Basic view now returns minimal HTML
450c0f3 First unit test and url mapping, dummy view
ea2b037 Add app for lists, with deliberately failing unit test
[...]
```
지금까지 다룬 것을 정리해 보면 다음과 같습니다.

- Django 앱 실행
- Django 단위 테스트 실행자
- FT 와 UT 의 차이
- Django URL 해석 및 urls.py
- Django 뷰 함수 및 요청, 응답 객체
- 기본 HTML 반환

### Useful Commands and Concepts
>
#### Django 개발 서버 실행
python manage.py runserver
>
#### functional tests 실행
python functional_tests.py
>
#### unit tests 실행
python manage.py test
>
#### 단위 테스트-코드 주기
>
1. 터미널에서 UT 실행
2. 편집기에서 최소 코드 수정
3. 반복
