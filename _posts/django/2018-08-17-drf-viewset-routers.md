---
layout: post
section-type: post
title: Django Rest Framework - Serializers, ViewSets, and Routers
category: django
tags: [ 'django' ]
---

- [William S. Vincent's Django Rest Framework - Serializers, ViewSets, and Routers](https://wsvincent.com/django-rest-framework-serializers-viewsets-routers/)를 번역한 것입니다.

- 해당 소스는 (Doky's Github)[https://github.com/KimDoKy/study/tree/master/daily/demo_project]에 업로드 해두었습니다.

# Django Rest Framework - Serializers, ViewSets, and Routers
DRF는 모델과 데이터베이스가 있는 기존 Django 프로젝트(view, url 또는 template이 필요 없음)가 있으면 최소한의 코드로 신속하게 RESTful API로 변환할 수 있습니다.

이 튜토리얼에서는 기본 Django To Do 앱을 만들어, serializer,viewsets, router를 사용하여 API로 변환합니다.

> django, drf 설치 및 가상환경 설정은 스킵하였습니다.

## Initial Setup
프로젝트와 앱을 생성합니다.

```
$ django-admin startproject demo_project .
$ python manage.py startapp todos
```

```python
# demo_project/settings.py
INSTALLED_APPS = [
  ...
  'todos',
]
```
초기 데이터베이스를 설정하기 위해 마이그레이션을 합니다.
```
$ python manage.py migrate
```

'Todo' 앱을 위한 기본 모델을 만듭니다.

```python
# todos/models.py
from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
```
데이터베이스에 적용하기 위해 마이그레이션을 수행합니다.

```
$ python manage.py makemigrations todos
$ python manage.py migrate todos
```

어드민에 등록합니다.

```python
# todos/admin.py
from django.contrib import admin
from .models import Todo

admin.site.register(Todo)
```
관리자 계정을 생성하고 서버를 실행합니다.

```
$ python manage.py createsuperuser
$ python manage.py runserver
```

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)으로 접속하여 관리자 게정으로 로그인합니다.

![]({{ site.url }}/img/post/django/drf_viewsets/1.png)

`+` 버튼을 누르고 2개의 항목을 추가합니다.

![]({{ site.url }}/img/post/django/drf_viewsets/2.png)

## Django Rest Framework
DRF를 설치하고 API 앱을 생성합니다.
모든 API 정보는 여기를 통해 전달됩니다. 프로젝트의 여러 앱이 있더라도 하나의 API만 있으면 API의 기능을 제어할 수 있습니다.

서버를 정지하고 앱을 생성합니다.
```
$ python manage.py startapp api
```
`rest_framework`와 `api` 앱을 `INSTALLED_APPS` 설정에 추가합니다. 그리고 기본 권한을 추가합니다. 실제로는 로그인한 사용자만 API에 엑세스 할 수 있도록 다양한 권한을 설정하지만, 이 튜토리얼에서는 간단하게 모든 사람에게 API를 개방합니다.(로컬에서 실행되기 때문에 보안 위험은 없습니다.)

```python
# demo_project/settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
    'todos',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
```

Django 앱은 해당 데이터베이스의 정보를 웹페이지로 변환하기 위해 전용 `URL`, `View`, `Template`이 필요합니다. DRF에서는 `url`, `view`, `serializer`가 필요합니다.
`URL`은 API 엔드포인트에 대한 엑세스를 제어하고, `Views`는 전송되는 데이터의 논리를 제어하고, `Serializer`는 인터넷을 통한 전송에 적합한 JSON으로 정보를 변환합니다.

API에 익숙하지 않다면 `Serializer`가 가장 혼란스러울 것입니다. 일반적인 웹페이지는 HTML, CSS, JavaScript가 필요합니다. 하지만 API는 JSON형식의 데이터만 전송합니다. `Serializer`는 Django 모델을 JSON으로 변환하여 클라이언트 응용 프로그램이 JSON을 본격적인 웹 페이지로 변환합니다. `Deserializer`는 API가 사용자 입력을 받아들일 때 발생합니다.( 예: HTML에서 JSON으로 변환된 후 Django 모델로 변환)

이러한 과정은 대부분 DRF 내의 serializers 클래스에서 나옵니다. 원하는 모델을 가져와 노출한 필드를 지정합니다.

```python
# api/serializers.py
from rest_framework import serializers
from todos import models


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description',
        )
        model = models.Todo
```

다음은 `view`입니다. DRF의 뷰는 Django의 뷰와 매우 비슷하며, 최소한의 코드로 많은 기능을 제공하는 generics 뷰도 제공합니다.
개별 작업 관리 항목에 대한 `DetailView`와 `ListView`을 구현합니다.

```python
# api/views.py
from rest_framework import generics

from todos import models
from . import serializers

class ListTodo(generics.ListCreateAPIView):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer
```

DRF는 `generics` 클래스 내에서 모든 무거운 리프팅 작업을 수행합니다. 이건 Django의 `generics` 클래스 기반과 매우 유사합니다. 각 뷰에 대해 모델 및 serializer를 지정합니다.

`URLs`만 업데이트하면 됩니다. 프로젝트 수준에서 `api` 앱을 포함시키려합니다. 따라서 전용 URL 경로를 추가합니다. 형식은 `api/v1/`입니다. API는 향후 변경될 가능성이 높지만 기존 사용자는 빠르게 업데이트하기 어렵기 때문에 항상 API를 버전화 하는 것이 좋습니다. 따라서 `api/v2/`에서 큰 변화가 있을 수 있습니다.

```python
# demo_project/urls.py
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
]
```

마지막으로 api 앱애서 urls.py를 업데이트 합니다. 모든 todo 목록은 `api/v1/`에 있습니다. 개별 todo 항목은 자동으로 Django가 설정한 `pk`에 있습니다. 따라서 처음 작업은 `api/v1/1`에, 두번째 작업은 `api/v1/2`에 배치됩니다.

```python
# api/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListTodo.as_view()),
    path('<int:pk>/', views.DetailTodo.as_view()),
]
```
To Do 프로젝트의 API 작업이 끝탔습니다. 서버를 재실행합니다.

```
$ python manage.py runserver
```

## Testing with the web browser
DRF는 멋진 GUI를 제공합니다. 단순히 API 엔드포인트로 가면 시각화 된 것을 확인할 수 있습니다.

모든 항목의 목록보기는 http://127.0.0.1:8000/api/v1/에 있습니다.

![]({{ site.url }}/img/post/django/drf_viewsets/3.png)

DetailView는 http://127.0.0.1:8000/api/v1/1/에 있습니다.

![]({{ site.url }}/img/post/django/drf_viewsets/4.png)

각 페이지 하단의 양식을 사용하여 새로운 항목을 작성, 검색, 삭제, 업데이트 할 수 있습니다. API가 더 복잡해지만 개발자들은 PostMan을 사용하여 API를 탐색하고 테스트하는 것을 더 좋아합니다.(여기서는 PostMan을 다루지 않습니다.)

## Viewsets
더 많은 API를 빌드할 때마다 같은 패턴을 사용하게 됩니다. 대부분의 API 엔드포인트는 공통 CRUD 기능의 일부를 조합합니다.
views.py에 이러한 뷰를 하나씩 작성하고 urls.py에 개별 경로를 제공하는 대신, 작업 대부분을 추상화하는 `ViewSet`을 사용할 수 있습니다.  

예를 들어 4개의 view와 url 경로를 하나의 viewset과 하나의 url으로 바꿀 수 있습니다.

```python
# api/views.py
from rest_framework import viewsets

from todos import models
from . import serializers


class TodoViewSet(viewsets.ModelViewSet):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoSerializer
```

`viewsets` 클래스는 모든 마법을 처리합니다. 특히 `ModelViewSet`은 자동으로 목록을 제공하고, 작업 생성, 검색, 업데이트, 파기를 합니다.

urls.py를 간단하게 업데이트 할 수 있습니다.

```python
# api/urls.py
from django.urls import path

from .views import TodoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', TodoViewSet, base_name='todos')
urlpatterns = router.urls
```

이제 다시 http://127.0.0.1:8000/api/v1/ 을 보면 목록보기가 이전과 동일하게 동작함을 볼 수 있습니다.

![]({{ site.url }}/img/post/django/drf_viewsets/5.png)

http://127.0.0.1:8000/api/v1/1/는 detailview와 같은 기능을 가지고 있습니다. 동일한 HTTP 메소드가 허용됩니다.

![]({{ site.url }}/img/post/django/drf_viewsets/6.png)

이처럼 API가 늘어남에 따라 API 엔드포인트에서 `viewsets`와 `router`를 사용하면 많은 개발 시간을 절약하고, 더 쉽게 구현할 수 있을 뿐 아니라, 기본 코드에 대해 쉽게 추론할 수 있습니다.
