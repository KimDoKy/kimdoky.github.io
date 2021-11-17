---
layout: post
section-type: post
title: pyDjango - chap2. Bookmark 앱
category: django
tags: [ 'django' ]
---

> Django 1.11.1 / Python 3.5.2 버전으로 실습 진행하였습니다.
실습 당시와 지금은 버전 차이가 있기 때문에 오류들을 만나시게 될 겁니다.
하나하나 해결해 나가셔도 되겠지만, 이 글을 보신다면 파이썬에 익숙하지 않으실 가능성이 높으므로,
최신 버전으로 개정된 [파이썬 웹 프로그래밍(개정판)](http://www.hanbit.co.kr/store/books/look.php?p_code=B4329597070)을 구매시는 걸 추천 드립니다. 이 포스팅은 개정되기 전 버전의 [파이썬 웹 프로그래밍](http://www.hanbit.co.kr/store/books/look.php?p_code=B7703021280)을 실습한 내용입니다.


북마크(Bookmark) 앱을 개발합니다.

북마크는 생성, 수정, 삭제 등의 기능이 있어 연습하기에 적당함.
{% raw %}

## 2.1 애플리케이션 설계하기

UI, URL, 테이블, 처리 로직 등을 설계해야 함.
UI 설계는 웹 프로그래밍에서 비중이 큼.

### 2.1.1 화면 UI 설계

화면 UI 설계는 주로 템플릿 코딩에 반영되고, templates/ 디렉터리 하위의 `*.html` 파일에 코딩

### 2.1.2 테이블 설계

필드명 | 타입 | 제약 조건 | 설명
---|---|---|---
id | Int | PK, Auth Increment | Primary Key
title | Char(100) | Blank, Null | 북마크 제목
url | URLField | Unique | 북마크 URL

### 2.1.3 로직 설계

로직 설계는 처리 흐름을 설계하는 것.  

로직 설계를 간략화해 URL-뷰-템플릿 간의 처리 흐름만 정리.

### 2.1.4 URL 설계

URL 설계 내용은 URLconf 코딩에 반영되고, urls.py 파일에 코딩.

URL 패턴 | 뷰 이름 | 템플릿 파일 이름
---|---|---
/bookmark/ | BookmarkLV(ListView) | bookmark_list.html
/bookmark/99/* | BookmarkDV(DetailView) | bookmark_detail.html
/admin/ | (장고 제공 기능) |

### 2.1.5 작업/코딩 순서

장고는 MTV 패턴에 따라 개발하도록 되어 있음  
모델 코딩은 뷰 또는 템플릿과 독립적으로 이뤄지므로 가장 먼저 코딩해야 함  
URL, 뷰, 템플릿 매핑은 URLconf 코딩시 결정되고, 클래스형 뷰를 사용하므로 템플릿보다는 뷰를 먼저 코딩

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | startproject <br> settings.py <br> migrate <br> createsuperuser <br> startapp <br> settings.py | mysite 프로젝트 생성 <br> 프로젝트 설정 항목 변경 <br> User/Group 테이블 생성 <br> 프로젝트 관리자 생성 <br> 북마크 앱 생성 <br> 북마크 앱 등록
모델 코딩하기 | models.py <br> admin.py <br> makemigrations <br> migrate | 모델(테이블)정의 <br> Admin 사이트에 모델 등록 <br> 모델을 데이터베이스에 반영
URLconf 코딩하기 | urls.py | URL 정의
뷰 코딩하기 | views.py | 뷰 로직 작성
템플릿 코딩하기 | templates 디렉터리 | 템플릿 파일 작성
그 외 코딩하기 | - | (없음)

## 2.2 개발 코딩하기 - 뼈대

### 2.2.1 프로젝트 생성

```
django-admin.py startproject mysite
```

```
└── mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

### 2.2.2 프로젝트 설정 파일 변경

settings.py 파일에 필요한 사항을 지정  
Database, INSTALED_APPS, TIME_ZONE 항목 등 6가지를 지정하거나 확인  

#### (1) 베이스데이터 설정확인
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### (2) 템플릿 설정확인

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 수정
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

#### (3) 정적 파일 설정확인

```
STATIC_URL = '/static/'

STATICFILES_DIRS =  [os.path.join(BASE_DIR, 'static')]  # 추가
```

#### (4) 타임존 지정

```
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Seoul'
```

#### (5) 미디어 관련 지정

```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### (6) 애플리케이션 등록


### 2.2.3 기본 테이블 생성

```
python manage.py migrate
```

테이블을 만들지 않았더라도, 사용자 및 권한 그룹 테이블을 만들어 주기 위해서 프로젝트 개발 시점에 마이그레이트를 실행해야 함.

### 2.2.4 슈퍼유저 생성

```
python manage.py createsuperuser
```

### 2.2.5 애플리케이션 생성

```
python manage.py startapp bookmark
```

### 2.2.6 애플리케이션 등록

프로젝트에 포함되는 애플리케이션들은 모두 설정 파일에 지정해야 함.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark.apps.BookmarkConfig',  # 추가
]
```

## 2.3 개발 코딩하기 - 모델

### 2.3.1 테이블 정의

- bookmark/models.py  

```python
from django.db import models

# Create your models here.

class Bookmark(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField('url', unique=True)

    def __str__(self):
        return self.title
```

### 2.3.2 Admin 사이트에 테이블 반영

- bookmark/admin.py

```python
from django.contrib import admin
from bookmark.models import Bookmark

# Register your models here.

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

admin.site.register(Bookmark, BookmarkAdmin)
```

### 2.3.3 데이터베이스 변경 사항 반영

데이터베이스에 변경이 필요한 사항이 있으면, 이를 데이터베이스에 실제로 반영해주는 작업을 해야 함.

```
python manage.py makemigrations
python manage.py migrate
```

### 2.3.4 테이블 모습 확인하기

```
python manage.py runserver 0.0.0.0:8000
```
```
» python manage.py runserver 0.0.0.0:8000 &
[1] 9814
» Performing system checks...

System check identified no issues (0 silenced).
August 27, 2017 - 18:45:41
Django version 1.11.1, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.


» jobs
[1]  + running    python3 manage.py runserver 0.0.0.0:8000
```
**명령어 뒤에 `&`를 붙이면 백그라운드에서 명령이 실행되며, `jobs` 명령으로 실행 중인 프로세스 목록을 볼 수 있음(꿀 팁)**

```
http://127.0.0.1:8000/admin
```
위 주소로 접속하여 Admin 사이트의 로그인 페이지가 나타면 정상.

앞에서 생성한 슈퍼유저로 로그인

장고에서 기본적으로 만들어주는 User, Group 테이블 이외에 Bookmark 테이블을 볼 수 있음

[ADD] 버튼을 클릭하면, models.py 파일에 정의한 테이블이 어떤 모습인지 UI 화면을 볼 수 있음.

## 2.4 개발 코딩하기 - URLconf

- mysite/urls.py

```python
from django.conf.urls import url
from django.contrib import admin

from bookmark.views import BookmarkLV, BookmarkDV

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bookmark/$', BookmarkLV.as_view(), name='index'), # 1
    url(r'^bookmark/(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'),  # 2
]
```

간단한 뷰라도 views.py 파일에 코딩할 것을 권장(향후 확장성이나 임포트 관계를 단순하게 유지하는 장점)

views.py를 작성하지 않고 urls.py 파일 하나만으로 작성할 수도 있음(비추)

```python
from django.conf.urls import url
from django.contrib import admin

from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Class-based views for Bookmark app
    url(r'^bookmark/$', ListView.as_view(model=Bookmark), name='index'),
    url(r'^bookmark/(?P<pk>\d+)/$', DetailView.as_view(model=Bookmark), name='detail'),
]
```

## 2.5 개발 코딩하기 - 뷰

개발하고자 하는 애플리케이션의 로직을 분석해보고 가장 적합한 제네릭 뷰를 찾을 수 있어야 함.

- bookmark/views.py

```python
from django.views.generic import ListView, DetailView # 1
from bookmark.models import Bookmark # 2

class BookmarkLV(ListView): # 3
    model = Bookmark

class BookmarkDV(DetailView): # 4
    model = Bookmark
```

## 2.6 개발 코딩하기 - 템플릿

### 2.6.1 bookmark_list.html 템플릿 작성하기

- bookmark/templates/bookmark/bookmark_list.html

```html
<!doctype html>
<html>
<head>
    <title>Django Bookmark List</title>
</head>
<body>

<div id="content">
    <h1>Bookmark LIst</h1>

    <ul>
        {% for bookmark in object_list %} # 1
            <li><a href="{% url 'detail' bookmark.id %}">{{ bookmark }}</a></li> # 2
        {% endfor %}
    </ul>
</div>

</body>
</html>
```

```python
def __str__(self):
    return self.title
```

`{{ bookmark }}` 템플릿 변수를 프린트하면 해당 객체의 title이 출력됩니다.


### 2.6.2 bookmark_detail.html 템플릿 작성하기

- bookmark/templates/bookmark/bookmark_detail.html

```html
<!doctype html>
<html>
<head>
    <title>Django Bookmark Detail</title>
</head>
<body>

<div id="content">

    <h1>{{  object.title }}</h1> # 1

    <ul>
        <li>URL: <a href="{{ object.url }}">{{ object.url }}</a></li> # 2
    </ul>
</div>
</body>
</html>
```

## 2.7 지금까지의 작업 확인하기

### 2.7.1 Admin에서 데이터 입력하기

Bookmark 테이블에 입력할 데이터

title | url
---|---
Google | http://www.google.com
Daum | http://wwww.daum.net
Naver | http://www.naver.com

### 2.7.2 브라우저로 확인하기

`http://127.0.0.1:8000/bookmark/` 으로 접속합니다.

각 항목을 클릭하여 상세 화면도 확인해봅니다.
{% endraw %}
