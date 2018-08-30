---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 4
category: django
tags: [ 'django' ]
---

# [Template Inheritance, Website files and Testing with coverage](http://www.marinamele.com/taskbuster-django-tutorial/template-inheritance-website-files-and-testing-with-coverage)

다음은 일반 웹 사이트에서 사용되는 파일을 구성하는 방법에 대해 다룹니다.

'robots.txt'파일은 프로젝트 초기에 매우 중요합니다. Google에서 당신의 페이지에 대한 색인을 생성하지 않기를 원하기 때문입니다. 사용자가 Google에서 무언가를 찾고있는 동안 당신의 웹 사이트에 들어가서 나쁜 CSS 스타일과 말도 안되는 텍스트가 있는 개발 사이트를 발견하면 어떨까요.

또한 테스트에서 'Coverage'를 구현하는 방법을 다룹니다. 이 도구는 코드가 테스트에서 처리되는 양을 측정합니다.

여기서 다룰 내용들입니다.

- Template Inheritance
- Robots.txt and humans.txt files
- The favico.ico image
- Testing with Coverage

이 포스팅을 시작하기 전에 작성한 모든 테스트가 통과했는지 확인하세요.

## Template Inheritance

이 튜토리얼의 마지막에 base.html에서 상속받도록 index.html을 설정합니다. 두 파일간의 다른 유일한 내용은 제목이었습니다.

base.html 템플릿을 보다 유연하게 준비합니다. 이 파일의 최종 버전은 [base.html](https://gist.github.com/mineta/5546c0f3f1953f8f38d1), [index.html](https://gist.github.com/mineta/9deadb890b03e5aaec97)에서 확인할 수 있습니다.


------------------------------
base.html의 head 태그 끝에 두 개의 블록을 추가합니다.
{% raw %}
```html
{% block head_css %}{% endblock %}
{% block head_javascript %}{% endblock %}
```

템플릿에 더 많은 CSS나 JavaScript 파일을 포함할 수 있습니다. 다음으로 `navbar` 요소를 감싸는 `navbar block`을 추가합니다.

```html
{% block navbar %}
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    ...
    </nav>
{% endblock %}
```
이 방법으로 템플릿에서 navbar의 내용을 대체할 수는 있지만, 아무것도 지정하지 않으면 navbar가 기본적으로 나타납니다.  

메인 콘텐츠는 **block content** 라는 별도의 콘텐츠 블록에 있어야 합니다. 그러나 기본값으로 값을 필요로하지 않으므로 jumbotron과 컨테이너 div의 모든 내용을 잘라서 index.html에 붙여 넣습니다.

```html
# index.html
{% extends "base.html" %}

{% block head_title %}TaskBuster Django Tutorial{% endblock %}

{% block content %}
    <div class="jumbotron">
    ...
    </div>
    <div class="container">
    ...
    </div>
{% endblock %}
```
그리고 base.html에서 누락된 내용을 바꾸기만 하면 됩니다.

```html
{% block content %}{% endblock %}
```

HTML boilerplate의 일부 버전에서는 `<footer>`요소는 `<container>`안에 있습니다. 이 요소를 base.html 파일에 보존할 수 있습니다.

마지막으로, 때로는 HTML 문서 끝에 스크립트를 추가해야하므로 `</body>` 태그 앞에 다음 행을 추가하세요.

```html
{% block footer_javascript %}{% endblock %}
```

두 파일을 저장하고 테스트를 실행하세요. 모든 테스트가 통과해야 합니다.

```
Ran 4 tests in 5.826s

OK
```

-------------------------------------------

## Robots.txt and humans.txt files
일반적으로 검색 엔진은 다음 위치에서 이 파일을 찾습니다.
 - /robots.txt
 - /humans.txt

그래서 해당 URL을 사용할 수 있도록 해야합니다. 짐작할 수 있듯이, 이 것을 위한 기능 테스트를 만들 것입니다.

'functional_tests/test_all_users.py'의 `HomeNewVisitorTest` 클래스에 다음 메소드를 정의하세요.

```python
def test_home_files(self):
    self.browser.get(self.live_server_url + "/robots.txt")
    self.assertNotIn("Not Found", self.browser.title)
    self.browser.get(self.live_server_url + "/humans.txt")
    self.assertNotIn("Not Found", self.browser.title)
```
해당 URL로 접속하면 Not Found 404 페이지가 표시되는지 확인해야 합니다.

테스트를 실행하고 실패를 확인하세요. 다음으로 'urls.py' 파일을 업데이트 합니다.

```python
from .views import home, home_files

...

urlpatterns = patterns(
    ...
    path('<filename>', home_files, name='home-files'),
    ...
)
```

이것은 원하는 url을 취사고 파일이름을 인수로 전달하는 정규 표현식입니다.

다음으로, 'views.py'에 `home_files` 뷰를 추가하세요.

```python
def home_files(request, filename):
    return render(request, filename, {}, content_type="text/plain")
```
테스트를 다시 실행하세요. 이제 모두 통과해야 합니다.

이 파일들에는 무엇이 들어어야 할까요?

웹사이트를 개발하는 동안 Google에서 내 페이지의 색인을 생성하지 않기를 바라기 때문에 'robots.txt' 파일에 다음의 내용을 작성합니다.

```
User-agent: *
Disallow: /
```
반면에, 'humans.txt'에는 팀에 대한 정보를 써야 합니다. 예를 들어

```
# humanstxt.org/
# The humans responsible & technology colophon

# TEAM
    Marina Mele -- Developer -- @marina_mele

# THANKS
    Thanks to all my Blog readers, who encouraged me to write the
    TaskBuster Django Tutorial

# TECHNOLOGY COLOPHON
    Django
    HTML5 Boilerplate
    Twitter Bootstrap
```

페이지가 게시되면 'robots.txt'를 다시 편집하고 Google에서 페이지 색인을 생성하도록 기억해야 합니다. 그렇지 않으면 사람들은 검색 엔진을 통해 우리의 웹 사이트를 찾을 수 없습니다.

## The favico.ico image
우리의 파비콘 이미지 파일(favicon.ico)파일이 'taskbuster/static' 폴더 안에 있어도 홈페이지에는 보이지 않습니다. 템플릿에 포함하지 않았기 때문입니다.

따라서 'base.html' 템플릿의 title 태그 아래에 다음의 코드를 추가하세요.

```html
<link rel="shortcut icon" href="{% static 'favicon.ico' %}"
  type="image/x-icon">
```
{% endraw %}
페이지를 새로 고침하면 브라우저의 페이지 태그에 아이콘이 표시됩니다.

## Testing with Coverage

커버리지는 테스트에 유용한 도구입니다. 커버리지는 코드의 어느 부분이 어떤 테스트에 의해 커버되는지 알려줍니다. 프로덕션을 시작하기 전에 코드의 적용 범위가 매우 중요합니다.

테스트 환경에만 설치하므로 'tb_test'를 활성화하고 커버리지를 설치합니다.

```
$ pip install coverage
```

pip freeze로 설치된 버전을 확인하고 'requirements/test.txt'에 추가하세요.

다음 명령을 사용하여 적용 범위가 있는 테스트를 실행하세요.

```
$ coverage run --source='.' manage.py test
```

unittest와 기능 테스트 모두를 실행할 것입니다. 다음을 통해 커버리지 보고서를 볼 수 있습니다.

```
$ coverage report
```

HTML으로도 볼 수 있습니다.

```
$ coverage html
```

'htmlcov/index.html'에서 결과를 확인할 수 있습니다. 'htmlcov/index.html'에서는 각 파일에서 테스트로 커버되는 행을 볼 수 있습니다.

이 명령은 git에서 유지하지 않기 위해 gitignore에 추가합니다.

```
$ echo ".coverage" >> .gitignore
$ echo "htmlcov" >> .gitignore
```
