---
layout: post
section-type: post
title: pyDjango - chap7. Blog 앱 확장 - Tag 달기
category: django
tags: [ 'django' ]
---
각 포스트마다 태그를 달 수 있는 기능을 개발합니다.  

태그 기능을 제공하는 오픈 소스로, django-tagging 패키지를 사용합니다.  

상용화를 목표로 장고 프로젝트를 개발한다면 오픈 소스를 활용하는 작업은 필수 입니다.

## 7.1 애플리케이션 설계하기
블로그의 각 포스트마다 태그를 보여주고 해당 태그를 클릭하는 경우, 그 태그를 가진 모든 포스트의 리스트를 보여줍니다. 그리고 태그만 모아서 보여주는 태그 클라우드 기능도 개발합니다.

### 7.1.1 화면 UI 설계
기존 포스트 상세 화면은 수정을, 태그와 관련된 2개의 화면은 신규로 추가합니다.

### 7.1.2 테이블 설계
태그 기능을 위해 Post 테이블에 필드 하나를 추가합니다.

필드명 | 타입 | 제약 조건 | 설명
---|---|---|---
tag | TagField | Blank | 포스트에 등록한 태그

### 7.1.3 URL 설계
기존 URL에 태그와 관련된 2개의 URL을 추가합니다 첫 번째는 태그 클라우드를 보기 위한 URL이고, 두 번째는 특정 태그가 달려 있는 포스트들의 리스트를 보여주는 URL입니다.

URL 패턴 | 뷰 이름 | 템플릿 파일명
---|---|---
/blog/tag/ | TagTV(TemplateView) | tagging_cloud.html
/blog/tag/tagname/ | PostTOL(TaggedObjectList) | tagging_post_list.html

### 7.1.4 작업/코딩 순서

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | startapp <br> settings.py | django-tagging 패키지 설치 <br> tagging 앱을 등록
모델 코딩하기 | models.py <br> makemigrations <br> migrate | tag 필드 추가 <br> 모델이 변경되므로 이를 데이터베이스에 반영
URLconf 코딩하기 | urls.py | URL 정의 추가
뷰 코딩하기 | views.py | 뷰 로직 추가
템플릿 코딩하기 |templates 디렉터리 | 템플릿 파일 추가
그 외 코딩하기 | static 디렉터리 | 태그 클라우드용 tag.css 추가

## 7.2 개발 코딩하기
오픈 소스로부터 설치한 tagging 앱을 등록하고, tagging 앱에서 제공하는 기능을 사용하기 위해 관련 파일들을 수정합니다.

### 7.2.1 뼈대 만들기
django-tagging 패키지도 settings.py 파일에 애플리케이션으로 등록합니다. 주의할 점은 설정 파일에 등록할지 여부와 등록하는 경우 어떤 애플리케이션명으로 등록할지를 확인해야 합니다. django-tagging 패키지의 공식 문서를 보면, 애플리케이션명이 tagging 이라는 것을 확인할 수 있습니다. 그래서 'tagging'으로 등록해도 무방합니다.  

그런데 django-tagging 패키지의 소스 디렉터리를 살펴보면, 앱 설정 파일인 apps.py 파일에 TaggingConfig 클래스가 정의되어 있습니다. 설정 클래스를 등록하는 것이 더 정확한 방법이므로 이를 등록합니다.

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark.apps.BookmarkConfig',
    'blog.apps.BlogConfig',
    'tagging.apps.TaggingConfig', #  추가
]
```

### 7.2.2 모델 코딩하기
기존 Post 테이블에 tag 필드만 추가합니다.

- blog/models.py

```python
from tagging.fields import TagField # 1

# Create your models here.
class Post(models.Model):
    title = models.CharField('TITLE', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.')
    descriptions = models.CharField('DESCRAIPTION', max_length=100, blank=True, help_text='simple description text')
    content = models.TextField('CONTENT')
    create_date = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY DATE', auto_now=True)
    tag = TagField() # 2
```

- 1 : 새로 설치한 tagging 앱은 자체 필드인 TagField를 정의하고 있습니다. 이를 임포트합니다.
- 2 : tag 컬럼을 TagField로 정의합니다. TagField 필드는 CharField 필드를 상속받아서 디폴트로 max_length=255, Blank=True 로 정의하고 있어서 tag 컬럼은 내용을 채우지 않아도 됩니다.

> #### TagField() 정의  
django-tagging 패키지에는 tagging 앱이 들어 있고, tagging 앱 디렉터리 하위의 fields.py 파일에 TagField() 클래스가 정의되어 있습니다.

Post 테이블 정의가 변경되었으므로, 마이그레이션을 해줍니다.

```
~/Git/Book_Study/pyDjango/2nd(master) » python manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0002_post_tag.py
    - Add field tag to post
(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master*) » python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, bookmark, contenttypes, sessions, tagging
Running migrations:
  Applying blog.0002_post_tag... OK
  Applying tagging.0001_initial... OK
  Applying tagging.0002_on_delete... OK
```

유의할 점은 tagging 패키지에는 자체 테이블이 2개로 정의되어 있어서, makemigrations/migrate 명령을 실행하면 tag 컬럼만 추가되는 것이 아니라 새로운 2개의 테이블이 데이터베이스에 추가된다는 것입니다.

이 사항을 Admin 사이트에서 UI 화면으로 확인할 수 있습니다. [Add] 버튼을 클릭해 테이블 모습을 확인합니다.

tagging 앱의 테이블 - TaggedItem, Tag
![]({{site.url}}/img/post/python/django/book_7_1.png)
Post 테이블 - tag 컬럼 추가
![]({{site.url}}/img/post/python/django/book_7_2.png)
tagging 앱의 TaggedItem 테이블
![]({{site.url}}/img/post/python/django/book_7_3.png)
tagging 앱의 Tag 테이블
![]({{site.url}}/img/post/python/django/book_7_4.png)

### 7.2.3 URLconf 코딩하기

- blog/urls.py

```python

    # ex: /today/
    url(r'^today/$', PostTAV.as_view(), name='post_today_archive'),

    # ex: /tag/
    url(r'^tag/$', TagTV.as_view(), name='tag_cloud'), # 1

    # ex: /tag/tagname/
    url(r'^tag/(?P<tag>[^/]+(?u))/$', PostTOL.as_view(), name='tagged_object_list'), # 2
]
```

- 1 : URL /tag/ 요청을 처리한 뷰 클래스를 TagTV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:tag_cloud'가 됩니다. TagTV 클래스형 뷰는 태그 클라우드를 보여주기 위한 뷰로써 템플릿 처리만 하면 되므로 TemplateView를 상속받아 정의할 것입니다.
- 2 : URL /tag/tagname/ 요청을 처리할 뷰 클래스를 PostTOL로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:tagged_object_list'가 됩니다. PostTOL 클래스형 뷰는 태그 단어를 인자로 받아서, 해당 태그가 달린 포스트들의 리스트를 보여줍니다. tagging 앱에서 정의하고 있는 TaggedObjectList(ListView) 클래스를 상속받아 정의할 예정입니다.

### 7.2.4 뷰 코딩하기

- blog/views.py

```python
from django.views.generic import ListView, DetailView, TemplateView # 1
from tagging.models import Tag, TaggedItem # 2
from tagging.views import TaggedObjectList # 3

# Create your views here.

#-- TemplateView
class TagTV(TemplateView): # 4
    template_name = 'tagging/tagging_cloud.html'

#-- ListView
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

class PostTOL(TaggedObjectList): # 5
    model = Post
    template_name = 'tagging/tagging_post_list.html'

#-- DetailView
```

- 1 : TemplateView 클래스형 제네릭 뷰를 임포트합니다.
- 2 : tagging 패키지에서 정의한 2개의 모델 클래스를 임포트합니다.
- 3 : tagging 패키지에서 정의한 TaggedObjectList 뷰 클래스를 임포트합니다.
- 4 : TemplateView 제네릭 뷰를 상속받아 PostTV 클래스형 뷰를 정의합니다. TemplateView 제네릭 뷰는 테이블 처리가 없이 단순히 템플릿 렌더링 처리만 하는 뷰입니다.
- 5 : TaggedObjectList 클래스형 뷰를 상속받아 PostTOL 클래스형 뷰를 정의합니다. TaggedObjectList 클래스는 ListView를 상속받는 뷰입니다. TaggedObjectList 뷰는 tagging 패키지의 views.py 파일에 정의되어 있는데, 그 기능은 모델과 태그가 주어지면 그 태그가 달려 있는 모델의 객체 리스트를 보여줍니다.
