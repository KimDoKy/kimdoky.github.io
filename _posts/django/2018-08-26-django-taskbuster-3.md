---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 3
category: django
tags: [ 'django' ]
---

# [Create a Home Page with TDD, Staticfiles and Templates settings](http://www.marinamele.com/taskbuster-django-tutorial/create-home-page-with-tdd-staticfiles-templates-settings)

작업환경이 설정되변 웹페이지를 만드는데 집중 할 수 있습니다. 그러나 "hello world"가 있는 빈 홈페이지가 아닙니다.  

정적 파일과 템플릿을 모두 구성하고, HTML5와 부트스트랩을 구현한 일반 웹페이지보다 **훨씬 나은** 버전을 만들 것입니다.

또한 Testing Goat에 복종하고 TDD를 따라 웹페이지를 만듭니다.

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

먼저, 'function_tests'폴더를 '__init__.py'라는 빈 파일을 포함시켜 패키지로 변환합니다.

```
$ touch function_tests/__init__.py
```

이렇게 하면 다음과 같이 기능 테스트를 실행할 수 있습니다.

```
$ python manage.py test function_tests
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
 - 웹페이지의 제목은 "TaskBuster"입니다.
 - 웹페이지의 h1 헤더 텍스트 색상은 `rgba(200,50,255,1)`~ 분홍색입니다.

 테스트를 만들어 봅시다!
 > Note: Part1에서 작성한  test 코드에 NewVisitorTest이 들어 있씁니다. 이 테스트를 다음을 대체해야 합니다.

 ```python
 # functional_tests/test_all_users.py
 # -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
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
- `test_home_title` 함수는 웹페이지 제목에 'TaskBuster'라는 단어의 유무를 테스트합니다. 템플릿을 만들 깃이므로, 제목이 있으면 템플릿이 올바르게 로드되었음을 의미합니다.
- `test_h1_css` 함수는 h1 텍스트에 원하는 색상이 있는지 테스트합니다. 텍스트 생상에 대한 규칙은 CSS 파일에 있습니다. 즉, 테스트가 통과하면 정적 파일이 올바르게 로드되었음을 의미합니다.
- `functional_tests`가 이제 Django 테스트 러너와 함께 실행되는 패키지이므로, `if__name__=='__main__'`문을 제거했습니다.

테스트가 생성되면 TDD는 다음과 같이 사이클을 수행하도록 알려줍니다.
 - 테스트를 실행하고 실패한 것을 확인하십시오.
 - 테스트 오류 메시지를 수정하도록 코드를 작성하세요.
 (테스트 실패로 표시된 오류 메시지를 수정하는 코드만 작성하고 가능한 다른 오류를 예상하지 마세요.)

 전체 테스트가 끝날 때까지 이 주기를 따라야 합니다. 


## Home Page with TDD – Code next
## 로컬 저장소 및 Git 커밋
