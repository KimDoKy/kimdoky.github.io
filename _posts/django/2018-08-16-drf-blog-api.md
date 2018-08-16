---
layout: post
section-type: post
title: Django Rest Framework - Blog API
category: django
tags: [ 'django' ]
---

- [William S. Vincent's Django Rest Framework - Blog API ](https://wsvincent.com/django-rest-framework-tutorial/)를 번역한 것입니다.

- 해당 소스는 [Doky's Github](https://github.com/KimDoKy/study/tree/master/daily/blog_project)에 업로드 해두었습니다.

# Django Rest Framework - Blog API

- 이 튜토리얼은 DRF를 사용하여 CRUD 기능을 갖춘 블로그 앱용 API를 빌드하는 것
- 초보자용입니다.

## SPA
현대 웹 어플리케이션 프로그램은 고유한 프론트 엔드와 백엔드를 특징으로한 SPA(Single Page Applications)으로 만들어지고 있는 추세입니다. Django와 같은 프레임워크는 필요에 따라 여러 프론트 엔드에서 사용할 수 있는 백엔드 API가 필요합니다. 이런 방법은 회사가 동일한 프론트엔드 애플리케이션(mobile, iOS, Android)을 필요로 할때 잘 작동합니다.

단점은 프로젝트를 위해 별도의 프로트엔트/백엔드를 작성하는데 더 많은 시간과 코드가 필요합니다.

## RESTful APIs
API(Application Programming Interface)는 개발자가 응용 프로그램의 데이터베이스와 상호 작용 할 수 있는 인터페이스를 제공합니다. API에 누군가에게 데이터베이스에 대한 모든 엑세스 권한을 부여하는 대신 로그인, 로그아웃, 블로그 목록 읽기, 개별 블로그 세부 정보 등의 다양한 기능에 대한 규칙, 사용 권한 및 엔드 포인트를 설정합니다.

웹 API를 구성하는 전통적인 방법은 웹 사이트가 서로 통신 할 수 있는 잘 정립된 아키텍처인 REST(Representational State Transfer)를 사용하는 것입니다. 컴퓨터는 웹을 통해 통신하므로 GET, PUT, POST, DELETE와 같은 메소드를 지원하는 HTTP 프로토콜을 사용합니다.

또한 요청이 성공(200), 재지정(301), 누락(404), 최악(500)인지 여부를 나타내는 관련 액세스 코드가 있습니다.

## JSON
API는 다른 컴퓨터와 통신중이므로 공유되는 정보가 표준 웹 페이지에 전송되는 정보가 **아닙니다.** 브라우저는 홈페이지를 요청하면 HTTP 요청을 보내고 HTML, CSS, JavaScript, 이미지 등의 HTTP 응답을 받습니다.

API는 **데이터베이스의 데이터에만** 관심이 있습니다. 이 데이터는 JSON 형식으로 변환되어 효율적으로 전송됩니다. API에는 프론트엔드 클라이언트가 REST 아키텍처를 통해 프론트엔드 클라이언트와 상호 작용할 수 있는 일력의 잘 정의 된 규칙이 있습니다. 예를 들어, 새 사용자를 등록하려면 프론트엔드 프레임워크는 `/api/register` API 엔트 포인트에 엑세스해야 합니다. 이 API 엔드 포인트에는 특정 URL 경로와 자체 사용 권한이 모두 포함되어 있습니다.

## Setup

> 작업경로, 가상환경 셋팅 등은 스킵합니다. django와 drf는 미리 설치한 것으로 가정합니다.

```
# 프로젝트 생성
$ django-admin startproject blog_project .
# 앱 생성
$ python manage.py startapp posts
```

```python
# blog_project/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'posts',  # 생성한 앱 추가
]
```

`posts` 데이터베이스 모델에 필요한 기본적인 4개의 필드(title, content, created_at, updated_at)를 만듭니다.

```python
# posts/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

```
# 마이그레이션 파일을 만들고 데이터베이스를 업데이트
$ python manage.py makemigrations
$ python manage.py migrate
```

```python
# posts/admin.py
# 어드민페이지에 Post 모델을 추가
from django.contrib import admin
from . models import Post

admin.site.register(Post)
```

```
# 관리자 계정을 생성
$ python manage.py createsuperuser
```

```
# 서버 시작
$ python manage.py runserver
```

[http://localhost:8000/admin/](http://localhost:8000/admin/)으로 접속합니다.
![]({{ site.url }}/img/post/django/blog_api/1.png)

`+`버튼을 눌러 새로운 콘텐츠를 입력합니다.
![]({{ site.url }}/img/post/django/blog_api/2.png)
3개의 게시물을 만듭니다.
![]({{ site.url }}/img/post/django/blog_api/3.png)
장고에서 할 일은 끝났습니다. 템플릿과 뷰는 만들 필요가 없습니다. 대신 DRF를 추가하여 모델 데이터를 API로 변환할 것입니다.

## Django Rest Framework

DRF는 데이터베이스 모델을 RESTful API로 변환하는 작업을 처리합니다. 이 프로세스틑 두 가지 기본 단계가 있습니다. 첫 단계는 `serializer`는 데이터를 JSON으로 변환하여 인터넷을 통해 전송할 수 있도록하는데 사용되며, 그러면 어떤 데이터가 전송되는지 정의하는데 사용됩니다.

```python
# blog_project/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  # drf 셋팅

    'posts',
]
```

serializer는 데이터를 JSON 형식으로 변환하는데 사용됩니다.

```python
# posts/serializers.py
from rest_framework import serializers
from . import models

# `serializer` 클래스를 만들고 그 안에 Meta 클래스를 만듭니다.
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        # fields는 데이터베이스 속성을 제어합니다.
        fields = ('id', 'title', 'content', 'created_at', 'updated_at',)
        model = models.Post
```

다음은 뷰를 생성해야합니다. Django가 CBV를 갖는 것처럼 DRF도 일반적인 뷰를 가지고 있습니다. 모든 게시물을 나열하는 뷰 및 특정 게시물의 상세보기를 추가합니다.

```python
# posts/views.py
from rest_framework import generics

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# RetrieveAPIView는 단일 인스턴스용입니다.
class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

마지막으로 URL입니다. 데이터를 사용할 수 있는 URL 경로(API 엔드포인트)를 만들어야 합니다.

```python
# blog_project/urls.py
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
]
```
```python
# posts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
]
```

## Browsable API

DRF 작동을 체크합니다. 서버를 재 시작합니다.

```
$ python manage.py runserver
```

브라우저에서 [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)으로 갑니다.

![]({{ site.url }}/img/post/django/blog_api/4.png)
`api/endpoint`는 블로그 게시물 3개를 JSON 형식으로 표시합니다. 헤더에는 GET, HEAD, OPTIONS 만 허용됩니다. POST는 전송하지 않습니다.

[http://127.0.0.1:8000/api/1/](http://127.0.0.1:8000/api/1/)으로 이동하면 첫 번째 게시의 데이터만 표시합니다.

![]({{ site.url }}/img/post/django/blog_api/5.png)

## CRUD 구현하기
DRF를 사용하여 API에 CRUD를 지원하는 API로 변환하는 것은 매우 쉽습니다.

```python
# posts/views.py
...
# 'class PostDetail'의 'generics.RetrieveAPIView'를
# 'generics.RetrieveUpdateDestroyAPIView'으로 변경합니다.
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
```

[http://127.0.0.1:8000/api/1/](http://127.0.0.1:8000/api/1/) 페이지를 새로고침하면 업데이트된 UI를 확인 할 수 있습니다.

![]({{ site.url }}/img/post/django/blog_api/6.png)

'DELETE' 버튼으로 콘텐츠를 삭제하고, 'PUT'으로 콘텐츠를 업데이트하고, 'GET'으로 다시 검색할 수 있습니다.('GET'을 누르지 않더도, 업데이트하면 업데이트된 내용을 자동으로 가져옵니다.)

예를 들어 3번째 게시물을 수정합니다. [http://127.0.0.1:8000/api/3/](http://127.0.0.1:8000/api/3/)으로 이동합니다.
![]({{ site.url }}/img/post/django/blog_api/7.png)
위 하면처럼 title을 수정하고 'GET'으로 다시 정보를 가져옵니다.
![]({{ site.url }}/img/post/django/blog_api/8.png)

## Next Step
ViewSets과 Router를 결합하면 복잡한 API를 획기적으로 빠르게 작성할 수 있습니다.
