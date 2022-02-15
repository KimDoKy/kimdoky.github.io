---
layout: post
section-type: post
title: Ariadne GraphQL with Django
category: django
tags: [ 'django' ]
---

## Introduction

한빛미디어의 리뷰어 활동으로 GraphQL in action이라는 책을 읽게 되었습니다.  

나중에 해봐야지라고 생각하던 참에 시작해보았습니다.

GraphQL in Action은 Node.js로 진행되어서 진도가 잘 나가지 않아서

Two Scoop of Django에서 GraphQL에 대해 읽었던 내용이 기억나서 Ariadne로 진행해 보았습니다.

구글링 하던중에 [Develop a Microservice Using Ariadne GraphQL with Django](https://www.pluralsight.com/guides/develop-a-microservice-using-ariadne-graphql-with-django)를 발견하여 진행하였습니다.  

원본의 코드도 업데이트가 필요한 부분이 일부 발견되어서 업데이트하였습니다.

## Ariadne GraphQL

Ariadne GraphQL은 Python용 grqphql 라이브러리입니다.  

```bash
$ pip install ariadne graphql-core ariadne_django
```

## Sample App

Django 프로젝트를 생성합니다.

```
django-admin startproject school_list
```

`school_stats` 앱을 생성합니다.

```
$ python3 manage.py startapp school_stats
```

School 모델인 Ariadne GraphQL 스키마를 Query와 Mutation으로 구성하고 GraphQL Playground 인터페이스를 표시하도록 URL을 구성해야 합니다.

`school_stats/models.py`에 `School` 모델을 작성합니다.

```python
from django.db import models

class School(models.Model):
   school_name = models.CharField(max_length=20)
   school_population = models.IntegerField(default=100)
   added_on = models.DateTimeField(auto_now_add=True)
   
   def __str__(self):
       return self.school_name
```

모델에는 데이터가 필요합니다. 데이터를 추가하려면 관리자 패널에 액세스해야 합니다. 이를 위해 superuser 액세스가 필요합니다.  

슈퍼유저 계정을 생성합니다.

```bash
$ python manage.py createsuperuser
```

앱과 모델이 보이려면 `school_list/settings.py`에 Aradne를 등록해야 합니다.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'school_stats',
    'ariadne_django',
]
```

`School`모델이 관리 창에 표시되도록 하려면 `school_stats/admin.py`에 등록해야 합니다.

```python
from django.contrib import admin
from .models import School
admin.site.register(School)
```

### GraphQL Schema and Resolver

GraphQL 개발의 첫 단계는 스키마를 개발하는 것입니다.  

스키마에는 School, School Input, Query, Mutation이 있습니다. 스키마가 간단하므로 파일 내 스키마를 수행할 수 있습니다.  

아래 코드 블록은 스키마를 정의하고 `type_defs` 변수를 할당합니다.  

`school_stats/resolver.py`에 다음 블록을 추가합니다.

```python
type_defs = """
type Query{
    all_schools: [School]
}

type School{
    id: ID
    school_name: String!
    school_population: Int!
}

type Mutation{
    add_school(input: SchoolInput): SchoolResults
}

input SchoolInput{
    school_name: String
    school_population: Int
}

type SchoolResults{
    created: Boolean!
    school: School
    err: String
}
"""
```

### GraphQL Query

Query를 설정하려면 모델에서 데이터를 반환해야 합니다.  

그러려면 스키마에서 생성된 `all_schools` 쿼리에 대한 query resolver가 필요합니다.  

`school_stats/resolver.py`에 다음 내용을 추가합니다.

```
from ariadne import QueryType, make_executable_schema, MutationType
from .models import School
query = QueryType()

@query.field('all_schools')
def resolve_schools(*_):
    return School.objects.all()
```

### GraphQL Mutation

Query와 마찬가지로 데이터베이스에 레코드를 생성할 mutation resolver를 설정합니다.

```python
mutation = MutationType()

@mutation.field('add_school')
def resolve_add_school(_,info, input):
    school = School.objects.create(school_name=input['school_name'], school_population=input['school_population'])      
    return {'created': True, 'school': school, 'err': None}
```

### Make Schema Executable

스키마를 실행하고 GraphQL Playground를 사용하도록 다음 코드를 추가합니다.

```python
schema = make_executable_schema(type_defs, query, mutation)
```

### URL Configuration

트래픽을 `school_stats` 앱에 보내기 위해 url을 셋팅합니다.(`school_list/urls.py')

```python
from django.urls import path, include
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('school_stats.urls')),

]
```

`school_stats`에 `urls.py`를 생성하고 graphQL View와 기본 URL을 로드합니다.

```python
from django.urls import path, include
from ariadne_django.views import GraphQLView
from .resolver import schema

urlpatterns = [
    path('graphql/', GraphQLView.as_view(schema=schema), name='graphql'),
    path('', GraphQLView.as_view(schema=schema), name='graphql'),
]
```

## Run the App

모든 설정을 마친 후, 변경사항을 마이그레이트하고 서버를 실행해야 합니다.  

```
$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py runserver
```

## API Screens

### Sample Mutation

GraphQL Playground에서 mutation을 실행하여 레코드를 만듭니다.

```graphql
mutation {
  add_school(input: {school_name:"SchoolZ", school_population:330})
  {
    created
    school{
      school_name
      school_population
    }
    err
  }
}
```

![]({{ url.site }}/img/post/django/ariadne/mutation.png)

### Sample Query

```graphql
query{
  all_schools{
    school_name
    school_population
  }
}
```

![]({{ url.site }}/img/post/django/ariadne/query.png)

## Conclusion

짠! 이제 프로젝트에 적용해보자구요!
