---
layout: post
section-type: post
title: pyDjango - chap2. Bookmark 앱
category: django
tags: [ 'django' ]
---

북마크(Bookmark) 앱을 개발합니다. '즐겨찾기' 정도로 이해하면 되는 기능입니다.  

북마크 앱은 로직이 간단해서 웹 프로그래밍을 시작하기에 좋은 예제입니다. 북마크에 등록된 URL을 따라 다른 사이트로 이동하는 링크 기능을 구현해볼 수 있고, 북마크의 생성, 수정, 삭제 등의 기능을 어렵지 않게 작성해 볼 수 있기 때문입니다.  

이번 챕터에서는 북마크라는 간단한 예제를 통해 장고의 MTV 패턴에 따라 개발 로직을 풀어나가는 과정에 대해 다룹니다.

## 2.1 애플리케이션 설계하기

사용자의 눈에 보이는 화면 UI, 그 화면에 접속하기 위한 URL, 서버에서 필요한 테이블 및 처리 로직 등을 설계해야 합니다. 모두 중요하지만, 특히 UI 설계는 웹 프로그래밍에서 비중이 큰 편입니다. UI 설계에 따라, 애플리케이션의 코딩이 많이 달라집니다. 북마크를 메뉴로 만들 수도 있고, 이미지에 북마크 URL을 링크할 수도 있습니다. 여기서는 간단하게 텍스트 위주의 북마크 앱을 개발합니다.

### 2.1.1 화면 UI 설계

화면 UI 설계는 주로 템플릿 코딩에 반영되고, templates/ 디렉터리 하위의 `*.html` 파일에 코딩합니다. 실제 프로젝트에서는 화면 정의서라는 문서를 별도로 작성하는 경우가 많습니다.  

본문 제목은 텍스트로 표시할 예정이고, Bookmark.title 및 Bookmark.url 부분은 Bookmark 테이블의 컬럼명을 표시합니다.

### 2.1.2 테이블 설계

테이블 설계 내용은 모델 코딩에 반영되고, models.py 파일에 코딩합니다.  
간단한 앱이므로 Bookmark 테이블 하나만 필요하기 때문에 다음과 같이 설계하였습니다.

필드명 | 타입 | 제약 조건 | 설명
---|---|---|---
id | Int | PK, Auth Increment | Primary Key
title | Char(100) | Blank, Null | 북마크 제목
url | URLField | Unique | 북마크 URL

### 2.1.3 로직 설계

로직 설계는 처리 흐름을 설계하는 것으로, 웹 프로그래밍에서는 URL을 받아서 최종 HTML 템플릿 파일을 만드는 과정이 하나의 로직이 됩니다. 그 과정에서 리다이렉션(redirection)이 일어날 수도 있고, 템플릿 파일에서 URL 요청이 발생할 수도 있습니다. 이런 과정들을 모두 고려해서 문서로 표현하는 것이 로직 설계 과정이며, 설계의 핵심입니다.

여기서는 로직 설계를 간략화해 URL-뷰-템플릿 간의 처리 흐름만 효시했고, 이는 바로 다음 단계인 URL 설계에 반영됩니다.

### 2.1.4 URL 설계

URL 설계 내용은 URLconf 코딩에 반영되고, urls.py 파일에 코딩합니다. 이 단계에서 중요한 점은 URL 패턴, 뷰 이름, 템플릿 파일 이름 및 뷰에서 어떤 제네릭 뷰를 사용할 것인지 등을 결정하는 것입니다.

URL 패턴 | 뷰 이름 | 템플릿 파일 이름
---|---|---
/bookmark/ | BookmarkLV(ListView) | bookmark_list.html
/bookmark/99/* | BookmarkDV(DetailView) | bookmark_detail.html
/admin/ | (장고 제공 기능) |

> URL 패턴에서 99는 예시로, 테이블 레코드의 기본 키가 채워지는 자리입니다.

### 2.1.5 작업/코딩 순서

장고는 MTV 패턴에 따라 개발하도록 되어 있습니다. 테이블 정의가 중요하고, 모델 코딩은 뷰 또는 템플릿과 독립적으로 이뤄지므로 가장 먼저 코딩해야 합니다. 그리고 URL, 뷰, 템플릿 매핑은 URLconf 코딩시 결정되고, 클래스형 뷰를 사용하므로 템플릿보다는 뷰를 먼저 코딩하는 것이 편리합니다. 그래서 코딩 순서는 모델, URLconf, 뷰, 템플릿 순서로 진행합니다. 코딩 외에도 장고 셸 명령이 필요하므로, 작업순서는 다음과 같습니다.

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | startproject <br> settings.py <br> migrate <br> createsuperuser <br> startapp <br> settings.py | mysite 프로젝트 생성 <br> 프로젝트 설정 항목 변경 <br> User/Group 테이블 생성 <br> 프로젝트 관리자 생성 <br> 북마크 앱 생성 <br> 북마크 앱 등록
모델 코딩하기 | models.py <br> admin.py <br> makemigrations <br> migrate | 모델(테이블)정의 <br> Admin 사이트에 모델 등록 <br> 모델을 데이터베이스에 반영
URLconf 코딩하기 | urls.py | URL 정의
뷰 코딩하기 | views.py | 뷰 로직 작성
템플릿 코딩하기 | templates 디렉터리 | 템플릿 파일 작성
그 외 코딩하기 | - | (없음)

## 2.2 개발 코딩하기 - 뼈대

코딩의 시작은 프로젝트 뼈대를 만드는 것으로 시작합니다. 즉 프로젝트에 필요한 디렉터리 및 파일을 구성하고, 설정 파일을 셋팅합니다. 그 외에도 기본 테이블을 생성하고, 관리자 계정을 생성하는 것이 필요합니다. 프로젝트가 만들어지면 그 하위에 애플리케이션 디렉터리 및 파일을 구성합니다. 장고는 이런 작업을 위한 장고 셸 커맨드를 제공합니다.

### 2.2.1 프로젝트 생성

mysite 프로젝트를 만듭니다.

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
상위 mysite 디렉터리는 프로젝트 관련 디렉터리/파일을 모으는 역할만 하는 디렉터리이고, 하위 mysite 디렉터리는 프로젝트 디렉터리입니다. 상위 mystie 디렉터리는 특별한 의미를 가지고 있지 않기 때문에 이름을 변경해도 무방합니다.

### 2.2.2 프로젝트 설정 파일 변경

프로젝트 설정 파일인 settings.py 파일에 필요한 사항을 지정합니다. Database, INSTALED_APPS, TIME_ZONE 항목 등 6가지를 지정하거나 확인합니다. 이 6개 항목 코두가 지금 당장 사용되는 건 아니지만, 프로젝트를 진행하면서 사용할 항목이기 때문에 미리 확인해둡니다.  

또한 이 6개의 항목들은 대부분의 프로젝트에서 필요한 항목들이므로, 프로젝트를 시작할 때 이 항목들에 대해 수정하거나 추가가 필요한지 확인하는 습관을 가져야 합니다. 물론 필요한 항목이 더 있으면 원하는 항목을 이 파일에 지정해주면 됩니다.  

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
보통 DIRS 항목을 제외한 나머지 항목들은 변경하지 않고 사용합니다. DIRS 항목은 프로젝트 템플릿 파일이 위치한 디렉터리를 지정합니다. 템플릿 파일을 찾을 때, 프로젝트 템플릿 디렉터리는 애플리케이션 템플릿 디렉터리보다 먼저 검색합니다.

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
STATIC_URL 항목은 최고 settings.py 파일이 만들어 질때 장고가 지정해준 그대로이고, STATICFILES_DRIS 항목은 프로젝트 정적 파일이 위치한 디렉터리를 의미하는데 수동으로 직접 지정합니다.  

템플릿 파일을 찾는 순서와 비슷하게, 정적 파일을 찾을 때도 각 애플리케이션의 static/ 디렉터리보다 STATICFILES_DRIS 항목으로 지정한 디렉터리를 먼저 검색합니다.  

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
파일 업로드 기능을 개발할 때 필요한 설정입니다.
```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### (6) 애플리케이션 등록
INSTALLED_APPS 항목으로 설정합니다.

### 2.2.3 기본 테이블 생성

```
python manage.py migrate
```

아직 데이터베이스 테이블을 만들지도 않았는데, 왜 이 명령이 필요할까요? 장고는 모든 웹 프로젝트 개발 시 사용자와 사용자의 권한 그룹 테이블이 반드시 필요하다는 가정 하에 설계되었습니다. 그래서 테이블을 전혀 만들지 않았더라도, 사용자 및 권한 그룹 테이블을 만들어 주기 위해서 프로젝트 개발 시점에 이 명령을 실행하는 것입니다. 명령을 실행하면 migrate 명령에 대한 로그가 보이고, 실행 결과로 SQLite3 데이터베이스 파일인 db.sqlite3 파일이 생성됩니다.

```
~/Git/Book_Study/pyDjango/2nd(master*) » python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying sessions.0001_initial... OK
(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master*) » tree
.
├── db.sqlite3
├── manage.py
└── mysite
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-35.pyc
    │   ├── settings.cpython-35.pyc
    │   └── urls.cpython-35.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

2 directories, 9 files
```

### 2.2.4 슈퍼유저 생성

```
python manage.py createsuperuser
```

```
~/Git/Book_Study/pyDjango/2nd(master) » python manage.py createsuperuser
Username (leave blank to use 'dokyungkim'): makingfunk
Email address:
Password:
Password (again):
Superuser created successfully.
```

이메일은 빈 값으로 해도 됩니다.

### 2.2.5 애플리케이션 생성

```
python manage.py startapp bookmark
```

```
~/Git/Book_Study/pyDjango/2nd(master) » python manage.py startapp bookmark
(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master*) » tree
.
├── bookmark
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── manage.py
└── mysite
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-35.pyc
    │   ├── settings.cpython-35.pyc
    │   └── urls.cpython-35.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

4 directories, 16 files
```
이제부터 각 파일마다 이름에 맞는 내용들을 채워주면 됩니다. apps.py 파일은 애플리케이션의 설정 클래스를 정의하는 파일입니다. 또한 장고가 자동으로 만들어준 파일 이외에도, 필요하다면 개발자가 임의의 파일을 생성해도 됩니다.

### 2.2.6 애플리케이션 등록

프로젝트에 포함되는 애플리케이션들은 모두 설정 파일에 지정되어야 합니다. 따라서 개발하고 있는 북마크 앱도 settings.py 파일에 등록해야 합니다. 애플리케이션의 모듈명인 'bookmark'만 등록해도 되지만, 애플리케이션의 설정 클래스로 등록하는 것이 더 정확한 방법입니다. 북마크 앱의 설정 클래스는 'bookmark.apps.BookmarkConfig'입니다.

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

> #### 애플리케이션 설정 클래스
애플리케이션의 설정 클래스는 해당 애플리케이션에 대한 메타 정보를 저장하기 위한 클래스로, **django.apps.AppConfig** 클래스를 상속받아 작성합니다. 앱 설정 클래스에는 앱 이름(name), 레이블(label), 별칭(verbose_name), 경로(path) 등을 설정할 수 있으며, 이 중 이름(name)은 필수 속성입니다.  
설정 클래스를 작성하는 위치는 애플리케이션 디렉터리 하위의 apps.py 파일입니다.  
만일 애플리케이션을 INSTALLED_APPS 항목에 등록 시 설정 클래스 대신에 애플리케이션 디렉터리만 지정하면, __init__.py 파일에서 **default_app_config** 항목으로 지정된 클래스를 설정 클래스로 사용합니다. default_app_config 항목도 정의되지 않으면 장고의 기본 AppConfig 클래스로 설정 클래스를 사용합니다.

## 2.3 개발 코딩하기 - 모델

모델은 데이터베이스 테이블을 생성하는 작업입니다.

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
장고에서는 테이블을 하나의 클래스로 정의하고, 테이블의 컬럼은 클래스의 변수(속성)로 매핑합니다. 테이블 클래스는 django.db.models.Model 클래스를 상속받아 정의하고, 각 클래스 변수의 타입도 장고에서 미리 정의해 둔 필드 클래스를 사용합니다.

모델 클래스의 정의에서 유의해야 할 점들입니다.
- title 컬럼은 공백(blank) 값을 가질 수도 있고, 값이 없을(null) 수도 있습니다.
- URLField() 필드 클래스의 첫 번째 파라미터인 'url' 문구는 url 컬럼에 대한 레이블 문구입니다. Admin 사이트에서 이 문구를 볼 수 있습니다. Field.verbose_name, 즉 필드의 별칭이라고도 합니다.
- __str__() 함수는 객체를 문자열로 표현할 때 사용하는 함수입니다. Admin 사이트나 장고 셸 등에서 테이블명을 보여줘야 하는데, 이때 __str__() 함수를 정의하지 않으면 테이블명이 제대로 표현되지 않습니다.

### 2.3.2 Admin 사이트에 테이블 반영

models.py 파일에서 정의한 테이블도 Admin 사이트에 보이도록 등록합니다.
- bookmark/admin.py

```python
from django.contrib import admin
from bookmark.models import Bookmark

# Register your models here.

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')

admin.site.register(Bookmark, BookmarkAdmin)
```
BookmarkAdmin 클래스는 Bookmark 클래스가 Admin 사이트에서 어떤 모습으로 보여줄지를 정의하는 클래스입니다. Bookmark 내용을 보여줄 때, title과 url을 화면에 출력하라고 지정했습니다. 그리고 admin.site.register() 함수를 사용해 Bookmark와 BookmarkAdmin 클래스를 등록합니다.  

이와 같이 테이블을 새로 만들 때는 models.py와 admin.py 두 개의 파일을 함께 수정해야 합니다.

### 2.3.3 데이터베이스 변경 사항 반영

테이블의 신규 생성, 테이블의 정의 변경 등 데이터베이트에 변경이 필요한 사항이 있으면, 이를 데이터베이스에 실제로 반영해주는 작업을 해야 합니다. 아직까지는 클래스로 테이블 정의까지만 한 상태입니다. 다음 명령으로 변경 사항을 데이터베이스에 반영해야 합니다.

```
python manage.py makemigrations
python manage.py migrate
```
마이그레이션 정보는 애플리케이션 디렉터리별로 존재합니다.  
즉, makemigrations 명령에 의해 bookmark/migrations 디렉터리 하위에 마이그레이션 파일들이 생기고, 이 마이그레이션 파일들을 이용해 migrate 명령으로 데이터베이스에 테이블을 만들어 줍니다.

```
~/Git/Book_Study/pyDjango/2nd(master) » python manage.py makemigrations
Migrations for 'bookmark':
  bookmark/migrations/0001_initial.py
    - Create model Bookmark
(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master*) » python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, bookmark, contenttypes, sessions
Running migrations:
  Applying bookmark.0001_initial... OK
```
마이그레이트 진행 후 디렉터리 구조입니다.
```
├── bookmark
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-35.pyc
│   │   ├── admin.cpython-35.pyc
│   │   ├── apps.cpython-35.pyc
│   │   └── models.cpython-35.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-35.pyc
│   │       └── __init__.cpython-35.pyc
│   ├── models.py
│   ├── tests.py
│   └── views.py
```

### 2.3.4 테이블 모습 확인하기

Admin 사이트를 통해 데이터베이스에 테이블이 잘 등록되었는지, 테이블이 어떤 모습인지 UI 화면에서 쉽게 확인할 수 있습니다.

```
python manage.py runserver 0.0.0.0:8000
```
```
~/Git/Book_Study/pyDjango/2nd(master) » python manage.py runserver 0.0.0.0:8000 &
[1] 9814
(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master) » Performing system checks...

System check identified no issues (0 silenced).
August 27, 2017 - 18:45:41
Django version 1.11.1, using settings 'mysite.settings'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.


(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master) » jobs
[1]  + running    python3 manage.py runserver 0.0.0.0:8000
```
명령어 뒤에 `&`를 붙이면 백그라운드에서 명령이 실행되며, `jobs` 명령으로 실행 중인 프로세스 목록을 볼 수 있습니다.

## 2.4 개발 코딩하기 - URLconf

## 2.5 개발 코딩하기 - 뷰

## 2.6 개발 코딩하기 - 템플릿

### 2.6.1 bookmark_list.html 템플릿 작성하기

### 2.6.2 bookmark_detail.html 템플릿 작성하기

## 2.7 지금까지의 작업 확인하기

### 2.7.1 Admin에서 데이터 입력하기

### 2.7.2 브라우저로 확인하기
