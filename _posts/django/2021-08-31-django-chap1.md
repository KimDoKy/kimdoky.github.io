---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap1. Coding Style
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

## 1.1 The Importance of Making your Code Readable

- 축약적이거나 함축적인 변수명은 피한다.
- 함수 인자의 이름들은 꼭 써 준다.
- 클래스와 메서드를 문서화한다.
- 코드에 주석은 꼭 달도록 한다. (이 부분은 사람마다 다름. ex) 함수명만으로도 주석의 기능을 해야 한다는 의견도 있음)
- 재사용 가능한 함수 또는 메서드 안에서 반복되는 코드들은 리팩터링을 해둔다.
- 함수와 메서드는 가능한 한 작은 크기를 유지한다. 어림잡아 스크롤 없이 읽을 수 있는 길이가 적합하다.

## 1.2 PEP 8

[PEP 8](https://www.python.org/dev/peps/pep-0008/)

- 새로운 프로젝트에 한해서만 적용한다. 기존 프로젝트가 다른 관례를 다른다면 기존 관례를 따라야 한다.
- [flake8](https://github.com/PyCQA/flake8): 코딩 스타일, 논리적 에러를 점검하는 도구(로컬 or 지속적 통합 환경에 유용)

### 1.2.1 The 79-Charactor Limit

코드 한 라인은 79자를 넘기면 안된다.

- 오픈 소스 프로젝트는 79 컬럼 제약을 반드시 지켜야 한다.
- 프라이빗 프로젝트에 한해서는 99 컬럼까지 제약을 확장함으로써 최신 모니터들의 장점을 좀 더 누릴 수 있다.
- 79 컬럼을 맞추기 위해 변수나 함수, 클래스 이름을 줄여서는 안된다.

## 1.3 The Word on Imports

#### PEP8 imports

1. 표준 라이브러리
2. 연관 외부 라이브러리
3. 로컬 애플리케이션 또는 라이브러리에 한정된 임포트

#### Django imports

```python
# stdlib imports
from math import sqrt
from os.path import abspath

# Core Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third-party app imports
from django_extensions.db.models import TimeStampedModel

# Imports from your apps
from splits.models import BananaSplit
```

1. 표준 라이브러리 임포트
2. 코어 장고 임포트
3. 장고와 무관한 외부 앱 임포트
4. 프로젝트 앱

## 1.4 Understand Explicit Relative Imports

코드의 재사용, 관리 등의 고려하여 상대 경로로 임포트를 해야 한다.  

Code | Import Type | Usage
---|---|---
`from core.views import FoodMixin` | 절대 임포트 | 외부에서 임포트해서 현재 앱에서 이용할 때
`from .models import Wafflecone` | 명시적 상대 | 다른 모듈에서 임포트해서 현재 앱에서 이용할 때

## 1.5 Avoid Using Import *

`import *`는 금지

다른 파이썬 모듈의 이름 공간들이 현재 작업하는 모듈의 이름 공간에 추가로 로딩되거나 기존 것 위에 덮여서 로딩되는 일이 발생할 수 있다.

### 1.5.1 Other Python Naming Collisions

임포트 하는 것 중 같은 이름이 있다면 `as`로 별칭 처리

```python
from django.db.models import CharField as ModelCharField
from django.froms import CharField as FormCharField
```

## 1.6 Django Coding Style

### 1.6.1 Consider the Django Coding Style Guidelines

Django는 내부적으로 PEP 8을 확장한 [스타일 가이드라인](https://docs.djangoproject.com/en/3.2/internals/contributing/writing-code/coding-style/)이 있다.

### 1.6.2 Use Underscores in URL Pattern Names Rather Than Dashes

URL 패턴 이름에는 underscore(`_`)를 사용한다.

```python
patterns = [
    path(route='add/',
        view=views.add_topping,
        name='toppings:add_topping'),
    ]
```

### 1.6.3 Use Underscores in Template Block Names Rather Than Dashes

템플릿 블록에도 underscore를 사용한다.

## 1.7 Choose JS, HTML, and CSS Style Guides

### 1.7.1 JavaScript Style Guides

- JS는 공석직인 가이드 라인은 없다. 자신이 선호하는 비공식 스타일을 이용하면 된다.
- 특정 프레임워크를 사용한다면해당 스타일 가이드를 따라야 한다.
- [ESLint](https://eslint.org/): JS 스타일 점검 도구

### 1.7.2 HTML and CSS Style Guides

- [Code Guide](https://codeguide.co/): HTML, CSS 코드 가이드
- [necolas; idiomatic-css](https://github.com/necolas/idiomatic-css): CSS 작성 원칙
- [CSScomb](https://stylelint.io/): CSS 코딩 스타일 포맷 도구

## 1.8 Never Code to the IDE (Or Text Editor)

IDE에는 자동으로 기본 뼈대를 완성해주는 기능이 있다.
해당 기능에 너무 종속되며 안됩니다.
