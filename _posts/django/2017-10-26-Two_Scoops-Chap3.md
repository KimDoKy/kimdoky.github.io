---
layout: post
section-type: post
title: Two Scoops of Django - chap3. 어떻게 장고 프로젝트를 구성할 것인가
category: django
tags: [ 'django' ]
published: false
---

프로젝트 레이아웃은 코어 장고 개발자들 사이에서도 여러 의견이 분분하다. 가장 널리 쓰이는 방법에 대해서 다룬다.

> #### 장고 프로젝트 템플릿  
템플릿을 포함해 장고 프로젝트를 시작하는데 도움이 될 만한 두 가지 프로젝트 템플릿을 소개한다.
- 이번 챕터에서 이용하는 템플릿 : <https://github.com/pydanny/cookiecutter-django>
- 또 다른 쿠키커터(cookiecutter) 템플릿 목록 : <https://djangopackages.org/grids/g/cookiecutters/>

## 3.1 장고 1.11의 기본 프로젝트 구성

```python
$ django-admin startproject mysite
$ cd mysite
$ django-admin startapp my_app
```
앞의 명령어를 통해 생성된 프로젝트 구성입니다.

```
# 예제 3.2

└── mysite
    ├── manage.py
    ├── my_app
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    └── mysite
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```
장고의 기본 프로젝트 구성은 튜토리얼용으로는 유용하지만 실제 프로젝트에 적용하면 그다지 유용하지 않은 부분들이 발견된다.

## 3.2 우리가 선호하는 프로젝트 구성
django-admin startproject 명령을 이용하면 삼단(three-tiered) 방식에 기반을 둔 구조가 생성되며 이를 기반으로 프로젝트를 구성한다. 우선 앞서 내린 명령을 통해 생성된 내용을 깃 저장소의 루트(root)로 이용되는 디렉터리 안으로 모두 옮긴다. 구성의 최상단부는 다음과 같다.

```
# 예제 3.3
<repository_root>
    <django_project_root>
        <configuration_root>
```

### 3.2.1 최상위 레벨: 저장소 루트
최상위 <repository_root>/ 디렉터리는 프로젝트의 최상위 절대 루트다. <django_project_root> 이외에 README.rst, docs/ 디렉터리, requirements.txt, 그리고 배포에 필요한 다른 파일 등 중요한 내용이 위치한다.

![]({{site.url}}/img/post/django/two_scoops/3.1.png)
그림 3.1 저장소가 중요한 이유

> #### 장고 구성에는 다양한 방법이 있다.  
어떤 개발자들은 <django_project_root>를 프로젝트의 <repository_root>로 구성하기도 한다.

### 3.2.2 두 번째 레벨: 프로젝트 루트
두 번째 레벨은 장고 프로젝트 소스들이 위치하는 디렉터리다. 모든 파이썬 코드는 <django_project_root>/ 디렉터리와 그 하부 디렉터리들에 위치한다.  
django-admin startproject 명령어를 이용할 때 명령어를 저장소 루트 디렉터리 안에서 실행하면 생성된 장고 프로젝트가 프로젝트 루트가 된다.  

### 3.2.3 세 번째 레벨: 설정 루트
<configuration_root> 디렉터리는 settins 모듈과 기본 URLconf(urls.py)가 저장되는 장소다. 이 디렉터리는 유효한 파이썬 패키지 형태여야 한다.(__init__.py 모듈이 존재해야 한다는 의미이다.)  
설정 루트 안의 파일은 django-admin startapp 명령으로 생성된 파일의 일부다.

![]({{site.url}}/img/post/django/two_scoops/3.2.png)
그림 3.2 삼단 구조 구성

## 3.3 예제 프로젝트 구성
일반적인 예제로 서로 다른 맛의 아이스크림과 서로 다른 브랜드를 평가하는 아이스크림 평가(Ice Cream Ratings) 웹 애플리케이션을 만듭니다.  

프로젝트 구성은 다음과 같습니다.

```
# 예제 3.4
icecreamratings_project
├── config/
│   ├── settings/
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── docs/
├── icecreamratings/
│   ├── media/  # Development only!
│   ├── products/
│   ├── profiles/
│   ├── ratings/
│   ├── static/
│   └── templates/
├── .gitignore
├── Makefile
├── README.rst
├── manage.py
└── requirements.txt
```

이 구성에 대해 한 단계 더 들어가서 보면 <repository_root>인 icecreamratings_project/ 디렉터리 안에 다음과 같은 파일들과 디렉터리가 있다.

파일/디렉터리 | 설명
---|---
.gitignore | 깃이 처리하지 않을 파일과 디렉터리
README.rst, docs/ | 개발자를 위한 프로젝트 문서들
Makefile | 간단한 배포 작업 내용과 매크로들을 포함한 파일. 복잡한 구성의 경우에는 인보크, 패브릭 등의 도구를 이용한다.
requirements.txt | 프로젝트에서 이용되는 파이썬 패키지 목록
icecreamratings/ | 프로젝트의 <django_project_root>

이러한 방식은 비개발자들도 함께 일하기 편하도록 알기 쉽게 구성되어 있다. 예를 들어 디자이너를 위한 디렉터리가 루트 디렉터리 안에 생성되는 경우도 있다.  
많은 개발자들이 디자이너를 위한 디렉터리를 <repository_root>와 같은 레벨에 만들기도 한다. 문제가 되는건 아니지만 프로젝트를 좀 더 구분 지어지게 만들기 위해 <django_project_root>인 icecreamratings_project/icecreamratings 디렉터리 안에 다음과 같은 파일과 디렉터리를 만들었다.

파일/디렉터리 | 설명
---|---
config | 프로젝트의 <configuration_root>로 프로젝트 전반에 걸친 settings 파일, urls.py, wsgi.py 모듈들이 자리잡는 곳이다.
manage.py | manage.py를 이곳에 위치시킬 경우 manage.py 안의 내용을 수정하지 않은 상태에서 이용해야한다.
media/ | 개발 용도로 이용되는 디렉터리다. 사용자가 올리는 사진 등의 미디어 파일이 올라가는 장소이다. 큰 프로젝트는 미디어 파일용 독립 서버에서 호스팅한다.
products/ | 아이스크림 브랜드를 관리하고 보여주는 앱
profiles/ | 이용자 프로필을 관리하고 보여주는 앱
ratings/ | 이용자가 매긴 점수를 관리하는 앱
static/ | CSS, 자바스크립트, 이미지 등 사용자가 올리는 것 이외의 정적 파일들이 위치하는 곳. 큰 프로젝트의 경우 독립된 서버에서 호스팅한다.
templates/ | 시스템 통합 템플릿 파일 저장 장소

> #### 정적 미디어 디렉터리 이름 관례
미디어 디렉터리(static media directory)를 static/ 이라고 공식 장고 문서의 이름을 그대로 따랐지만, 이를 assets/ 또는 site_assets/ 라고 바꾸려면 STATICFILES_DIRS 세팅에 해당 정보를 업데이트함으로 디렉터리 이름을 바꿀 수 있다.

## 3.4 virtualenv 설정
맥 OS X나 리눅스에서는 다음과 같은 위치에 있다.

```
~/projects/icecreamratings_project/
~/.envs/icecreamratings/
```

> #### 의존성 확인하기
지금 이용중인 virtualenv 환경에서 어떤 버전의 라이브러리가 쓰이는지 알아보려면 다음의 명령어를 이용한다.
```
$ pip freeze
```

requirements.txt 파일은 반드시 버전 컨트롤 시스템으로 관리해야 합니다.

## 3.5 startproject 살펴보기
장고의 startproject 명령은 기본적인 장고 프로젝트 템플릿을 생성하고 바로 프로젝트 개발을 가능하게 해준다. 하지만 기존 장고의 템플릿의 한계점으로 인해 더 강력한 프로젝트 템플릿 도구로 쿠키커터(cookiecutter) 템플릿을 사용한다.

### 3.5.1 쿠키커터로 프로젝트 구성 템플릿 만들기
장고 프로젝트 템플릿을 이용하려면 쿠키커터라는 가벼운 명령행 도구가 필요하다. 쿠키커터는 장고 프로젝트 구성을 위한 발전된 형태의 프로젝트 구성 템플릿 도구다.  
쿠키커터의 작동 내용은 다음과 같다.

1. 우선 쿠키커터는 여러 질문을 통해 각종 설정 변수의 내용을 물어본다.(예: project_name에 들어갈 내용 등)
2. 그런 후 입력된 값들을 기반으로 프로젝트 표준 코드 구성에 필요한 파일들을 제작한다.

### 3.5.2 우리가 선호하는 프로젝트 템플릿
지금부터 이용한 프로젝트 템플릿은 cookiecutter-django다.  

```
$ cookiecutter https://github.com/pydanny/cookiecutter-django

Cloning into 'cookiecutter-django'...
remote: Counting objects: 2358, done.
remote: Compressing objects: 100% (12/12), done.
remote: Total 2358 (delta 4), reused 0 (delta 0), pack-reused 2346
Receiving objects: 100% (2358/2358), 461.95 KiB, done.
Resolving deltas: 100% (1346/1346), done.

project_name ('project_name')? icecreamratings
repo_name ('icecreamratings')? icecreamratings_project
author_name ('Your Name')? Daniel and Audrey Roy Greenfeld
email ('audreyr@gmail.com')? hello@twoscoopspress.com
description ('A short description of the project.')? A website
 for rating ice cream flavors and brands.
domain_name ('example.com')? icecreamratings.audreyr.com
version ('0.1.0')? 0.1.0
timezone ('UTC')? America/Los_Angeles
now ('2017/04/02')? 2017/04/02
year ('2017')?
use_whitenoise ('n')?
github_username ('audreyr')? twoscoops
full_name ('Audrey Roy')? Daniel and Audrey Roy Greenfeld
```

설정 변수들이 입력되고 난 후 쿠키커터를 실행한 디렉터리에 프로젝트가 생성된다. 앞에서 입력한 값에 따라 icecreamratings_project 디렉터리가 생성된다.  

생성된 파일들은 settings, requirements, 초기문서들, 초기 테스트 환경등이 포함된다.

> #### cookiecutter-django를 설치하니 기본적인 파일 외에 여러 파일이 많이 설치되는데 어떤 것들인가?
```
# cookiecutter-django 설치 전.
Django==1.11.6
pytz==2017.2

# cookiecutter-django 설치 후.
arrow (0.10.0)
binaryornot (0.4.4)
certifi (2017.7.27.1)
chardet (3.0.4)
click (6.7)
cookiecutter (1.6.0)
Django (1.11.6)
future (0.16.0)
idna (2.6)
Jinja2 (2.9.6)
jinja2-time (0.2.0)
MarkupSafe (1.0)
pip (9.0.1)
poyo (0.4.1)
python-dateutil (2.6.1)
pytz (2017.2)
requests (2.18.4)
setuptools (20.10.1)
six (1.11.0)
urllib3 (1.22)
whichcraft (0.4.1)
```
cookiecutter-django는 기본적인 구성보다 몇 단계 더 깊게 나아간 구성을 제공한다. 실제 프로젝트에서 이용하는 강력한 형태의 장고 프로젝트 템플릿으로 다양한 부가 기능을 내장하고 있다.

### 3.5.3 대안 템플릿: django-kevin
케빈 쉬는 Two Scoops project를 포크해서 그만의 버젼으로 발전시켰다.  
<https://github.com/imkevinxu/django-kevin>에서 받을 수 있다.

### 3.5.4 다른 대안들
사람들은 각자 자신만이 생각하는 '옳은 방법'을 가지고 있다. 옳은 방법은 하나만 있는 것이 아니다.  
프로젝트 구성이 앞서 언급한 구성과 다르다 하더라도 프로젝트 구성 요소(docs, templates, apps, settings 등)의 위치가 루트의 README.rst 파일에 잘 정리되어 있다면 크게 문제 될 것은 없다.

![]({{site.url}}/img/post/django/two_scoops/3.4.png)
그림 3.4 프로젝트 레이아웃에 대한 서로 다른 의견 때문에 때론 아이스크림 싸움을 유발할 수도 있다.

## 3.6 요약
이번 챕터에서는 선호하는 기본 장고 프로젝트 구성에 대해 다루었다.  
프로젝트 구성은 개발자 또는 개발자 그룹마다 서로 사뭇 다른 이용 모습을 보인다. 작인 팀에서 최적으로 효과를 내었더라도 큰 팀에서는 잘 적용되지 않거나 효과를 볼 수 없을수도 있다. 핵심은 어떤 구성을 택하더라도 반드시 명확하게 문서로 남겨야 한다는 것이다.
