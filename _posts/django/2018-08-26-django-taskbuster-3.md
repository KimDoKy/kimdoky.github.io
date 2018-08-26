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

## Home Page with TDD – Code next
## 로컬 저장소 및 Git 커밋
