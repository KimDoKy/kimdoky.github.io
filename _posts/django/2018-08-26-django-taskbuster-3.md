---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 3 - Create a Home Page with TDD, Staticfiles and Templates settings
category: django
tags: [ 'django' ]
---

# [Create a Home Page with TDD, Staticfiles and Templates settings](http://www.marinamele.com/taskbuster-django-tutorial/create-home-page-with-tdd-staticfiles-templates-settings)

작업환경이 설정되변 홈페이지를 만드는데 집중 할 수 있습니다. 그러나 "hello world"가 있는 빈 홈페이지가 아닙니다.  

정적 파일과 템플릿을 모두 구성하고, HTML5와 부트스트랩을 구현한 일반 홈페이지보다 **훨씬 나은** 버전을 만들 것입니다.

또한 Testing Goat에 복종하고 TDD를 따라 홈페이지를 만듭니다.

여기서 다룰 내용들입니다.

- 정적 파일 설정
- 템플릿 설정
- Initializr : HTML5와 부트스트랩
- Home Page with Test Driven Development – Tests first
- TDD - 코드 다음
- 로컬 저장소 및 Git 커밋

## 정적 파일 설정

공통 파일 설정(settings/base.py)에 `INSTALLED_APPS` 변수 안에 `django.contrib.staticfiles` 앱이 포함되어 있는지 확인합니다.

파일의 끝에 `STATIC_URL = '/static/'` 라인을 찾습니다. 이 코드는 DJango에게 각 응용 프로그램 내부의 'static'이라는 폴더에 있는 정적 파일을 찾도록 지시합니다.

그러나 일부 정적 파일은 전체 프로젝트에 사용되며 특정 응용 프로그램 안에 있으면 안됩니다. 'taskbuster' 디렉터리에 들어가서 'settings'와 같은 레벨의 'static' 폴더를 만듭니다.

```
$ cd TaskBuster
$ mkdir static
```

이 디렉터리에는 CSS나 JavaScript 파일과 같은 프로젝트 전역에서 사용되는 정적 파일이 포함됩니다.

'settings/base.py' 파일의 시작 부분을 보면 알 수 있습니다.

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

이 폴더는 실제 파일이 들어 있는 폴더, 즉 taskbuster 폴더를 포함하는 디렉터리를 가리킵니다.

Django가 방금 만든 'taskbuster/static' 디렉토리에서 정적 파일을 찾도록 지시하려면  `STATIC_URL`뒤에 다음 코드를 작성해야 합니다.

```python
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
```
마지막에 콤마(`,`)를 잊으면 안됩니다. 이 설정을 하면 Django는 'taskbuster/static'에서 각 app에서 필요로 하는 정적 파일을 찾습니다.

## 템플릿 설정

템플릿 설정도 비슷합니다. 기본적으로 Django 템플릿 로더는 각 앱 내부의 'templates' 디렉터리에 있는 템플릿을 찾습니다.  

'base.html'이나 오류 페이지와 같은 모든 프로젝트에서 사용되는 전역 템플릿을 포함하기 위해 'taskbuster' 안에 'templates' 디렉터리를 만듭니다.

```
$ cd taskbuster
$ mkdir templates
```

그리고, 셋팅 파일의 `TEMPLATES` 안의 `DIRS` 키를 편집합니다.

```python
# Templates files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

정적 파일처럼, Django는 'taskbuster/templates' 디렉터리 안에서 각 app 내부의 'templates'라는 디렉터리에 있는 템플릿을 찾습니다.

## Initializr : HTML5와 부트스트랩
템플릿과 정정 파일 설정이 작동하는지 확인하고, HTML5와 부트스트랩을 포함합니다. 이 도구를 사용하면 많은 브라우저에서 작동하는 반응형 템플릿을 만들 수 있습니다.  

여기서는 HTML5와 부트스트랩을 결합한 혼합 버전인 [Initializr](http://www.initializr.com/)를 사용합니다. 웹 사이트로 이동하여 Bootstrap을 선택하고 아래 이미지처럼 구성합니다.

![]({{ site.url }}/img/post/django/TB/Initializr.png)

패키지를 다운받고, 앱축 해제하여 컨텐츠를 재구성합니다.
- 'index.html', '404.html', 'humans.txt', 'robots.txt'파일을 'taskbuster/templates' 폴더안으로 이동합니다.
- 'index.html'파일을 'base.html'으로 이름을 변경합니다. index 파일은 일반적으로 홈페이지의 탬플릿으로 사용하지만, 우리는 base 탬플릿을 사용할 겁니다. 우리의 모든 사이트 템플릿은  base 템플릿을 상속받을 것입니다.
- 그외 파일과 폴더는 'taskbuster/static'안으로 이동합니다.
- 사용하려는 아이콘이 있다면, 'favicon.icon'파일로 대체하세요.
- 'apple-touch-icon.png', 'browserconfig.xml', 'tile-wide.png', 'tile.png'파일은 삭제합니다.

## Home Page with Test Driven Development – Tests first
정적 파일과 템플릿이 정상적으로 로드되었는지 확인하려면 테스트가 필요합니다. 알다시피 테스트 염소에 복종하라! **먼저 테스트 !!**

실제로 TDD를 사용하려면 템플릿과 static 폴더를 설정 하기 전에 테스트를 작성하야 합니다만, 먼저 설정 파일 편집을 끝내고 싶었습니다.(원작자가

먼저, 'functional_tests'폴더를 '__init__.py'라는 빈 파일을 포함시켜 패키지로 변환합니다.

```
$ touch functional_tests/__init__.py
```

이렇게 하면 다음과 같이 기능 테스트를 실행할 수 있습니다.

```
$ python manage.py test functional_tests
```

테스트 러너는 'test'로 시작하는 파일을 찾기 때문에, 'all_users.py'를 'test_all_users.py'로 변경합니다.

변경된 파일도 git에 적용해 줍니다.

```
$ git mv functional_tests/all_users.py functional_tests/test_all_users.py
```
가상환경 'tb_dev'에서 서버를 실행하고, 'tb_test' 가상환경에서 기능 테스트를 진행합니다. 이전처럼 작동해야 하며, 아무 것도 고장나지 않았습니다. 테스에서 서버를 만들지 못하는 이유는 무엇일까요?  

이러한 기능 테스트에 의한 변경은 지속적입니다. 한 번의 테스트 동안 모델의 인스턴스(예: 새 사용자)를 생성한다고 가정합니다. 테스트가 끝나면 해당 인스턴스(새 사용자)는 데이터베이스에서 사라지는 것이 좋습니다. 하지만 기능 테스트를 통해 개발 서버를 실행하고 개발 데이터베이스를 사용하기 때문에 테스트가 끝난 후에도 이러한 변경 사항은 계속 유지됩니다.

하지만 `LiveServerTestCase`를 사용하면 간편하게 할 수 있습니다.

이 클래의 인스턴스는 `unittest`를 실행할 때와 같이 **테스트 데이터베이스** 가 있는 서버를 만듭니다.

'functional_tests/test_all_users.py'를 편집하고, 템플릿과 정적 디렉터리가 예상대로 작동하는지 테스트해 봅시다. 예를 들어 다음의 두 가지를 테스트 할 수 있습니다.
 - 홈페이지의 제목은 "TaskBuster"입니다.
 - 홈페이지의 h1 헤더 텍스트 색상은 `rgba(200,50,255,1)`~ 분홍색입니다.

 테스트를 만들어 봅시다!
 > Note: Part1에서 작성한  test 코드에 NewVisitorTest이 들어 있씁니다. 이 테스트를 다음을 대체해야 합니다.

 ```python
 # functional_tests/test_all_users.py
 # -*- coding: utf-8 -*-
from selenium import webdriver
from django.urls import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase  


class HomeNewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)

    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("TaskBuster", self.browser.title)

    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgba(200, 50, 255, 1)")
```

- `get_full_url`이라는 보조 함수를 정의합니다. 이 함수는 `namespace`라는 인수를 갖습니다.
 - `namespace`는 URL에 대한 식별자입니다. Django의 좋은 점은 식별자를 사용할 때 이전과 같이 코드가 작동하는지 원하는 대로 URL을 변경할 수 있다.
 - `self.live_server_url`은 로컬 호스트 URL을 제공합니다. 테스트 서버가 다른 URL(일반적으로 `http://127.0.0.1:8021`)을 사용하기 때문에 이 방법을 사용합니다. 이 방법은 유연합니다.
 - `reverse`는 주어진 **네임 스페이스의 상대 URL을 제공** 합니다.
 - 이 함수의 결과는 네임 스페이스의 절대 URL(이전 두값의 합)을 제공합니다.
- `test_home_title` 함수는 홈페이지 제목에 'TaskBuster'라는 단어의 유무를 테스트합니다. 템플릿을 만들 깃이므로, 제목이 있으면 템플릿이 올바르게 로드되었음을 의미합니다.
- `test_h1_css` 함수는 h1 텍스트에 원하는 색상이 있는지 테스트합니다. 텍스트 생상에 대한 규칙은 CSS 파일에 있습니다. 즉, 테스트가 통과하면 정적 파일이 올바르게 로드되었음을 의미합니다.
- `functional_tests`가 이제 Django 테스트 러너와 함께 실행되는 패키지이므로, `if__name__=='__main__'`문을 제거했습니다.

테스트가 생성되면 TDD는 다음과 같이 사이클을 수행하도록 알려줍니다.
 - 테스트를 실행하고 실패한 것을 확인하십시오.
 - 테스트 오류 메시지를 수정하도록 코드를 작성하세요.
 (테스트 실패로 표시된 오류 메시지를 수정하는 코드만 작성하고 가능한 다른 오류를 예상하지 마세요.)

 전체 테스트가 끝날 때까지 이 주기를 따라야 합니다.

## Home Page with TDD – Code next

기능 테스트를 갖게 되었으니, 'tb_test'환경에서 테스트를 실행하고 어떻게 실패하는지 확인 할 수 있습니다.

```
$ python manage.py test functional_tests

...
django.urls.exceptions.NoReverseMatch: Reverse for 'home' not found. 'home' is not a valid view function or pattern name.
```

발견된 첫 번째 오류는 네임스페이스 `home`이 정의되어 있지 않다는 것입니다. 'taskbuster/urls.py'에 views.py의 `home`을 임포트합니다.

```python
from .views import home
```

 이렇게 하면 URL을 위반하지 않고 프로젝트 또는 앱의 이름을 변경할 수 있습니다.

 다음 URL을 추가하세요.

 ```python
 urlpatterns = [
    ...
    path('', home, name='home'),
    ...
]
```
그리고 'taskbuster/views.py'을 만들고 `home`을 정의합니다.

```python
def home(request):
     return ""
```

테스트를 실행하면 제목에 'TaskBuster'가 없기 때문에 실패합니다.

이제 템플릿에 초점을 맞우어야 합니다. 'taskbuster/templates/base.html'을 열고 안에 무엇이 있는지 생각해봐야합니다. base.html은 기본 템플릿이 될 것이고 다른 모든 앱 템플릿은 이 템플릿을 상속받습니다.

홈페이지 템플릿을 코딩하고 싶지만... **테스트 염소에 복종!!**

Unittest는 개발자의 관점에서 코드의 작은 조각을 테스트하기 위한 것입니다. 예를 들어 홈페이지 템플릿이 내용을 표시하는 다른 템플릿에서 상속되는지 여부를 사용자는 신경쓰지 않습니다. 그러나 개발자는 관심을 가지고 있으며, 그래서 우리는 unittest를 작성해야 합니다. 더욱이 테스트를 생각할 떄 코드를 보다 명확하게 작성한다는 사실을 깨달았습니다. 테스트를 정의해야만 코드가 원하는 것을 **정확히** 생각할 수 있기 때문입니다. 그리고 그것은 우리의 불안감을 없애줍니다.

'taskbuster' 폴더안의 'test.py' 파일을 작성합니다.

```python
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse


class TestHomePage(TestCase):

    def test_uses_index_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "taskbuster/index.html")

    def test_uses_base_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "base.html")
```

위 테스트는 다음 명령으로 실행할 수 있습니다.

```
$ python manage.py test taskbuster.test
```

테스트는 실패 할 것입니다. 우선, 'taskbuster/index.html' 템플릿을 만듭니다.

```
$ cd taskbuster/templates
$ mkdir taskbuster
$ touch taskbuster/index.html
```

'taskbuster/views.py'를 다음과 같이 편집하세요.

```python
# -*- coding: utf-8 -*-
from django.shortcuts import render

def home(request):
    return render(request, "taskbuster/index.html", {})
```
sourtcuts `render`를 사용하면 ,템플릿을 로드할 수 있습니다. 이러 현재 로그인된 사용자나 현재 언어에 대한 정보와 같은 여러 변수를 기본적으로 추가하는 컨텍스트를 사용하여 모든 기능을 렌더링한 후 'HttpResponse'를 반환합니다.  
Note: 기본적으로 추가된 정보는 설정 파일에 포함된 템플릿 컨텍스트 프로세서에 따라 달라집니다.  

unittest를 다시 실행하면 첫 번째 페이지가 무사히 통과하여 홈페이지가 'taskbuster/index.html' 템플릿을 사용하고 있음을 알 수 있습니다. 이 템플릿은 'base.html' 템플릿을 상속받아야 합니다.  

```
AssertionError: False is not true : Template 'base.html' was not a template used to render the response. Actual template(s) used: taskbuster/index.html
```

이제 base.html 템플릿을 수정합니다. 지금은 head 태그 안에 있는 **title 태그** 에만 관심이 있습니다.
{% raw %}
```html
<head>
    ...
    <title>{% block head_title %}{% endblock %}</title>
    ...
</head>
```

두 개의 템플릿 태그(`{% block head_title %}`와 `{% endblock %}`)는 컨텐츠가 하위 템플릿을 대체할 수 있는 컨텐츠 블록의 시작과 끝입니다. 1분안에 명확히 알아 볼 수 있습니다.  

'index.html'파일을 다시 편집하여 'base.html'파일을 상속받고 제목을 추가하세요.

```html
{% extends "base.html" %}
{% block head_title %}TaskBuster Django Tutorial{% endblock %}
```

이러한 특수 템플릿 태그로 표시된 블록을 제외하고 index.html이 base.html를 상속받는 것이 좋습니다. 이 경우 index.html의 template 태그 안의 내용을 base.html의 해당 블록으로 대체합니다.

unittest를 다시 실행합니다.

```
$ python manage.py test taskbuster.test
```

```
...
Ran 2 tests in 0.017s

OK
```
완벽히 통과했습니다. 기능 테스트는 어떨까요?

```
$ python manage.py test functional_tests
```
하나는 통과했고 하나는 실패했습니다. 실패응 정적 파일에 관한 것입니다.

먼저, 'taskbuster/static/css/main.css' 파일에 다음 내용을 추가합니다.

```css
.jumbotron h1 {
    color: rgba(200, 50, 255, 1);
}
```

그런 다음 'base.html'의 시작부분에 추가하세요.(`<!DOCTIPE html`부분)

```html
{% load staticfiles %} # Django 3.0 이후로 staticfiles -> static 으로 변경됨 
```
그런다음 JavaScript의 정적 파일과 스크립트에 대한 모든 링크를 찾습니다.

```html
<link rel="stylesheet" href="css/xxx.css">
<script src="js/xxx.js"></script>
```

이 코드를 다음과 같이 변경하세요.

```html
<link rel="stylesheet" href="{% static 'css/xxx.css' %}">
<script src="{% static 'js/xxx.js' %}">
```

apple_touch_icon.png 링크는 제거해도 됩니다.

파일 중간에 다음 코드를 발견할 수 있습니다.
```html
document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>
```

이 코드에는 `"{% static 'xxx'%}` 태그를 추가할 수 없습니다. 문자열을 꺠뜨리기 떄문입니다. 이 경우 상대 경로를 지정하는 정적 파일을 포함할 수 있습니다.
{% endraw %}
```
document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>
```

Note: 정적 파일을 가져오는 두 가지 방법이 모두 작동하더라도 정적 파일 제공에 CDN(Content Delivery Network)을 사용하려는 경우 template 태그를 사용하는 것이 좋습니다.

다시 기능 테스트를 실행해봅니다.... 실패!!

`LiveServerTestCase`는 정적 파일을 지원하지 않기 때문에 오류가 일어납니다.

하지만 해결책이 있습니다. 정적 파이을 지원하는 다른클래스가 있습니다!

'functional_tests/test_all_users.py'를 편집해야하는데, '-' 행을 '+'행으로 바꾸세요.

```python
- from django.test import LiveServerTestCase
+ from django.contrib.staticfiles.testing import StaticLiveServerTestCase

- class HomeNewVisitorTest(LiveServerTestCase):
+ class HomeNewVisitorTest(StaticLiveServerTestCase):
```
테스트를 다시 실행하면 모두 통과됩니다.

```
Ran 2 tests in 5.785s

OK
```

unittest와 functional_tests를 모두 실행하려면 다음 명령어를 사용하면 된다.

```
$ python manage.py test
```

```
Ran 4 tests in 5.938s

OK
```

또한 localhost를 보고 CSS 파일이 올바르게 로드되고 있는 예쁜 홈페이지를 확인 할 수 있습니다.

## 로컬 저장소 및 Git 커밋
git은 알아서 변경사항 추가해서 push하세요.
