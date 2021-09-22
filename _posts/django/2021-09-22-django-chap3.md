---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap3. How to Lay Out Django Projects
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

## 3.1 Django 3's Default Project Layout

`startproject`와 `startapp`으로 실행한 프로젝트 기본 구성은 튜토리얼에는 상관없지만 실제 프로젝트에 적용하기엔 몇 가지 문제가 있습니다.

기본 구성입니다.

```
 mysite/
   ├── manage.py
   ├── my_app
   │   ├── __init__.py
   │   ├── admin.py
   │   ├── apps.py
   │   ├── migrations
   │   │   └── __init__.py
   │   ├── models.py
   │   ├── tests.py
   │   └── views.py
   └── mysite
       ├── __init__.py
       ├── asgi.py
       ├── settings.py
       ├── urls.py
       └── wsgi.py
```

## 3.2 Our Preferred project Layout

저자가 선호하는 구성입니다.

```
<repository_root>/
   ├── <configuration_root>/
   ├── <django_project_root>/
```

### 3.2.1 Top Level: Repository Root

- `configuration_root`
- `django_project_root`
- README.txt
- docs/
- .gitignore
- requirments.txt
- 배포에 필요한 파일들

### 3.2.2 Second Level: Django Project Root

django 프로젝트 소스들이 위치합니다.

### 3.2.3 Second Level: Configuration Root

- settings 모듈들
- 기본 URLConf(urls.py)

이 디렉터리는 파이썬 패키지 형태(`__init__.py`)이어야 합니다.

## 3.3 Sample Project Layout

```
icecreamratings_project
├── config/
│   ├── settings/
│   ├── __init__.py
│   ├── asgi.py
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
├── README.md
├── manage.py
└── requirements.txt
```

file / directory | purpose
---|---
.gitignore | git에서 제외할 대상
config/ | `configuration_root`으로 settings, urls.py, wsgi.py이 포함
Makefile | 간단한 배포 작업 내용과 매크로들 <br/> 복잡할 경우 Invoke, Paver, Fabric 등을 이용
manage.py | 이 파일의 위치가 바뀌어도, 안에 파일은 수정 X
README.md and docs/ | 개발자를 위한 프로젝트 문서들
requirements.txt | 프로젝트에 이용되는 파이썬 패키지 목록
icecreamratings/ | `django_project_root`

directory | purpose
---|---
media/ | 개발 용도의 디렉터리.(미디어파일)
products/ | 예제용. 아이스크림 브랜드를 관리하고 보여주는 앱
profiles/ | 예제용. 이용자 프로필을 관리하고 보여주는 앱
ratings/ | 예제용. 이용자가 매긴 점수를 관리하는 앱
static/ | CSS, JS, 이미지 등 정적파일들이 위치
templates/ | 시스템 통합 템플릿 파일 저장 장소

## 3.4 What About the Virtualenv?

- virtualenv는 `~/.env/`에서 관리합니다.
- .env/ 는 .gitignore에 추가되어 git에서 제외합니다.
- .env의 패키지들은 requirements.txt으로 관리합니다.

### 3.4.1 Listing Current Dependencies

- 종속성 나열: `pip freeze`
- 각 패키지 종속성 저장: `pip freeze > requirements.txt`

## 3.5 Going Beyond `startproject`

django의 `startproject` 명령으로 구성된 기본 구조는 저자가 선호하는 구조와 차이가 있어서 쿠키커터라는 프로젝트 템플릿 도구를 사용하는 방법이 있습니다. 필수 X 

### 3.5.1 Generating Project Boilerplate With Cookiecutter

1. 쿠키커터는 여러 질문을 통해 각종 설정 변수의 내용을 물어본다.
2. 입력되니 값들을 기반으로 프로젝트 표준 코드 구성에 필요한 파일들을 제작한다.

### 3.5.2 Generating a Starting Project With Cookiecutter Django

전 개인적으로 쿠키커터를 사용하지 않습니다.

## 3.6 Other Alternatives to `startproject`

여러 프로젝트 템플릿을 보면서 각자 자신만이 생각하는 '옳은' 방법을 찾으세요. '옳은' 방법은 하나만 있는 것은 아닙니다.
