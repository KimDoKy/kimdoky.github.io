---
layout: post
section-type: post
title: pyDjango - chap3. Blog 앱
category: django
tags: [ 'django' ]
---

블로그의 기본 기능이라 할 수 있는 포스트 등록 및 열람, 태그 달기, 댓글 및 검색 기능, 콘텐츠 생성 및 편집 기능을 다룹니다.

## 3.1 애플리케이션 설계하기

블로그의 포스트에 대한 리스트를 보여주고 포스트를 클릭하면 해당 글을 읽을 수 있는 기능을 개발합니다.

### 3.1.1 화면 UI 설계

각 화면의 템플릿 파일명과 화면 요소들이 무엇을 의미하는지, 어느 테이블 컬럼에 해당하는지 등을 표시합니다. 'Post.title'과 같이 영문으로 표시된 항목들이 테이블 컬럼, 즉 사용하는 모델 필드입니다.

### 3.1.2 테이블 설계

필드명 | 타입 | 제약 조건 | 설명
---|---|---|---
id | int | PK, Auto Increment | 기본 키
title | CharField(50) |  | 포스트 제목
slug | SlugField(50) | Unique | 포스트 제목 별칭
description | CharField(100) | Blank | 포스트 내용 한줄 설명
content | TextField | | 포스트 내용 기록
create_date | DateTimeField | auto_now_add | 포스트를 생성한 날짜
modify_date | DateTimeField | auto_now | 포스트를 수정한 날짜

### 3.1.3 로직 설계

실제 프로젝트에서 로직 설계는 애플리케이션의 처리 흐름을 설계하는 중요한 단계입니다. 이 과정을 통해 개발 대상 기능을 도출하고, 각 기능을 모델-뷰-템플릿 간에 어떻게 배치할지가 결정됩니다. 또한 개발 기능이 누락되지 않도록 도출하고, 도출된 기능들은 URL 설계에 누락되지 않게 반영해야 합니다. 규모가 큰 프로젝트라면 로직 설계를 반드시 수행해야 합니다.

### 3.1.4 URL 설계

간단한 프로젝트라도 URL 설계는 필수입니다. 테이블 설계와는 독립적으로 진행할 수 있으며, 기능 개발은 URL을 정의하는 것에서부터 시작되기 때문입니다.  

URL 패턴 | 뷰 이름 | 템플릿 파일명
---|---|---
/blog/ | PostLV(ListView) | post_all.html
/blog/post/ | PostLV(ListView) | post_all.html
/blog/post/slug-ex/ | PostDV(DetailView) | post_detail.html
/blog/archive/ | PostAV(ArchiveIndexView) | post_archive.html
/blog/2017/ | PostYAV(YearArchiveView) | post_achive_year.html
/blog/2017/nov/ | PostMAV(MonthArchiveView) | post_archive_month.html
/blog/2017/nov/10/ | PostDAV(DayArchiveView) | post_archive_day.html
/blog/today/ | PostTAV(TodayArchiveView) | post_archive_day.html
/admin/ | (장고 제공 기능) |

### 3.1.5 작업/코딩 순서

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | startproject<br>settings.py<br>migrate<br>createsuperuer<br>startapp<br>settings.py | <br><br><br><br>블로그 앱을 생성<br>블로그 앱을 등록
모델 코딩하기 | models.py<br>admin.py<br>makemigrations<br>migrate | 모델(테이블)정의 <br> Admin 사이트에 모델 등록 <br> 모델을 데이터베이스에 반영
URLconf | urls.py | URL 정의
뷰 코딩하기 | views.py | 뷰 로직 작성
템플릿 코딩하기 | templates 디렉터리 | 템플릿 파일 작성
그 외 코딩하기 | - | (없음)

## 3.2 개발 코딩하기

### 3.2.1 뼈대 만들기

```
python manage.py startapp blog
```
블로그 앱에 대한 설정 클래스를 settings.py 파일에 들록

- mysite/settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookmark.apps.BookmarkConfig',
    'blog.apps.BlogConfig', # 추가
]
```

### 3.2.2 모델 코딩하기

블로그 앱은 Post 테이블 하나만 필요합니다. 테이블을 클래스로 정의하는 ORM 기법 덕분에 원한다면 모델 클래스와 관련된 메소드도 같이 정의할 수 있습니다.

- blog/models.py

```python
from django.db import models
from django.core.urlresolvers import resolve # 1

# Create your models here.
class Post(models.Model):
    title = models.CharField('TITLE', max_length=50) # 2
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias.') # 3
    descriptions = models.CharField('DESCRAIPTION', max_length=100, blank=True, help_text='simple description text')
    content = models.TextField('CONTENT')
    create_date = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_date = models.DateTimeField('MODIFY DATE', auto_now=True)

    class Meta:
        verbose_name = 'post' # 4
        verbose_name_plural = 'posts' # 5
        db_table = 'my_post' # 6
        ordering = ('-modify_date',) # 7

    def __str__(self): # 8
        return self.title

    def get_absolute_url(self): # 9
        return reversed('blog:post_detail', args=(self.slug,))

    def get_previous_post(self): # 10
        return self.get_previous_by_modify_date()

    def get_next_post(self): # 11
        return self.get_next_by_modify_date()
```

- 1 : `reversed()` 함수를 사용하기 위해 임포트합니다. reversed() 함수는 URL 패턴을 만들어주는 장고의 내장 함수입니다.
- 2 : title 컬럼에 대한 레이블은 'TITLE'입니다. 레이블은 폼 화면에 나타나는 문구로, Admin 사이트에서 확인할 수 있습니다.
- 3 : slug 컬럼은 제목의 별칭입니다. SlugField에 Unique 옵션을 추가해 특정 포스트를 검색시 기본 키 대신에 사용됩니다. allow_unicode 옵션을 추가하면 한글 처리가 가능합니다. help_text는 해당 컬럼을 설명해주는 문구로 폼 화면에 나타납니다. Admin 사이트에서 확인이 가능합니다.
> #### 슬러그란?  
슬러그(slug)는 페이지나 포스트를 설명하는 핵심 단어의 집합입니다. 원래 신문이나 잡지 등에서 제목을 쓸 때, 중요한 의미를 포함하는 단어만을 이용해 제목응ㄹ 작성하는 방법을 말합니다. 웹 개발 분야에서는 콘텐츠의 고유 주소로 사용되어, 콘텐츠의 주소가 어떤 내용인지를 쉽게 이해할 수 있도록 합니다.  
보통 슬러그는 페이지나 포스트의 제목에서 조사, 전치사, 쉼표, 마침표 등을 빼고 띄어쓰기는 하이픈(-)으로 대체해서 만들며, URL에 사용됩니다. 슬러그를 URL에 사용함으로써 검색 엔진에서 더 빨리 페이지를 찾아주고 검색 엔진의 정확도를 높여줍니다.

> #### SlugField 필드 타입  
슬로그는 보통 제목의 단어들을 하이픈으로 연결해 생성하며, URL에서 pk 대신으로 사용되는 경우가 많습니다. pk를 사용하면 숫자로만 되어 있어 그 내용을 유추하기 어렵지만, 슬러그를 사용하면 보통의 단어들이라서 이해하시 쉽기 때문입니다.  

- 4 : 테이블의 별칭은 단수와 복수로 가질 수 있는데, 단수 별칭을 'post'로 합니다.
- 5 : 테이블의 복수 별칭을 'posts'로 합니다.
- 6 : 데이터베이스에 저장되는 테이블의 이름을 'my_post'로 지정합니다. 이 항목을 생략하면 디폴트는 '앱명_모델클래스명'을 테이블명으로 지정합니다. 즉, db_table 항목을 지정하지 않았다면 테이블명은 blog_post 가 되었을 것입니다.
- 7 : 모델 객체의 리스트 출력시 modify_date 컬럼을 기준으로 내림차순으로 정렬합니다.
- 8: 객체의 문자열을 객체.title 속성으로 표시되도록 합니다.
- 9 : get_absolute_url() 메소드는 이 메소드가 정의된 객체를 지칭하는 URL을 반환합니다. 메소드 내에서는 장소의 내장 함수인 reverse()를 호출합니다.
- 10 : get_previous_post() 메소드는 modify_date 컬럼을 기준으로 이전 포스트를 반환합니다. 메소드 내에서는 장고의 내장 함수인 get_previous_by_modify_date()를 호출합니다.
- 11 : get_next_post() 메소드는 modify_date 컬럼을 기준으로 다음 포스트를 반환합니다. 메소드 내에서는 장고의 내장 함수인 get_next_by_modify_date()를 호출합니다.

앞에서 정의한 테이블도 Admin 사이트레 보이도록 admin.py 파일에 등록합니다. 또한 Admin 사이트의 모습을 정의하는 PostAdmin 클래스도 정의합니다.

- blog/admin.py

```python
from django.contrib import admin
from blog.models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin): # 1
    list_display = ('title', 'modify_date') # 2
    list_filter = ('modify_date',) # 3
    search_fields = ('title', 'content') # 4
    prepopulated_fields = {'slug':('title',)} # 5

admin.site.register(Post, PostAdmin) # 6
```

- 1 : PostAdmin 클래스는 Post 클래스가 Admin 사이트에 어떤 모습으로 보여줄지 정의하는 클래스입니다.
- 2 : Post 객체를 보여줄 때 title과 modify_date를 화면에 출력하라고 지정합니다.
- 3 : modify_date 컬럼을 사용하는 필터 사이드바를 보여주도록 지정합니다.
- 4 : 검색박스를 표시하고, 입력된 단어는 title과 content 컬럼에서 검색하도록 합니다.
- 5 : slug 필드는 title 필드를 사용해 미리 채워지도록 합니다.
- 6 : admin.site.register() 함수를 사용해 Post와 PostAdmin 클래스를 Admin 사이트에 등록합니다.

Post 테이블을 신규로 정의했으므로 신규 테이블을 데이터베이스에 반영합니다.

```
python manage.py makemigrations
python manage.py migrate
```

models.py 파일에 테이블을 정의하고 이를 데이터베이스에 반영하는 명령을 실행했습니다. 또한 테이블을 Admin 사이트에 등록했습니다. Admin 사이트에서 데이터베이스에 테이블이 제대로 등록되었는지 쉽게 확인할 수 있습니다.

![]({{site.url}}/img/post/python/django/book_3_2_2.png)

### 3.2.3 URLconf 코딩하기

앞으로는 ROOT_URLCONF와 APP_URLCONF, 2개의 파일에 코딩합니다. 이번 블로그 앱도 mysite/urls.py와 blog/urls.py 2개의 파일에 코딩합니다.

> #### ROOT_URLCONF vs APP_URLCONF
ROOT_URLCONF와 APP_URLCONF는 이해를 돕기 위한 용어일뿐, 장고 공식 용어는 아닙니다. URLconf를 2계층으로 코딩하는 것이 확장성 측면에서 유리합니다.
- ROOT_URLCONF : URL 패턴에서 보통 첫 단어는 애플리케이션을 식별하는 단어가 옵니다. 첫 단어를 인식하고 해당 애플리케이션의 urls.py 파일을 포함시키기(include) 위한 URLconf입니다. 프로젝트 디렉터리에 있는 urls.py 파일을 의미합니다.
- APP_URLCONF : URL 패턴에서 애플리케이션을 식별하는 첫 단어를 제외한, 그 이후 단어들을 인식해서 해당 뷰를 매핑하기 위한 URLCONF입니다. 각 애플리케이션 디렉터리에 있는 urls.py 파일을 의미합니다.

ROOT_URLCONF인 mysite/urls.py 파일을 코딩합니다.

```python
from django.conf.urls import url, include
from django.contrib import admin

# from bookmark.views import BookmarkLV, BookmarkDV # 1

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bookmark/', include('bookmark.urls', namespace='bookmark')), # 2
    url(r'^blog/', include('blog/urls', namespace='blog')), # 3

    # Class-based views for Bookmark app # 4
    # url(r'^bookmark/$', BookmarkLV.as_view(), name='index'),
    # url(r'^bookmark/(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'),
]
```

- 1 : APP_URLCONF으로 옮길 줄은 삭제(주석) 처리합니다.
- 2 : 북마크 앱의 APP_URLCONF를 포함하고, 이름공간을 'bookmark'라고 지정합니다.
- 3 : 블로그 앱의 APP_URLCONF를 포함하고, 이름공간을 'blog'라고 지정합니다.
- 4 : APP_URLCONF으로 옮길 줄은 삭제(주석) 처리합니다.

다음은 북마크 앱의 APP_URLCONF인 bookmark/urls.py 파일을 코딩합니다.

```python
from django.conf.urls import url
from bookmark.views import BookmarkLV, BookmarkDV # 1

urlpatterns = [
    # Class-based views
    url(r'^$', BookmarkLV.as_view(), name='index'), # 2
    url(r'^(?P<pk>\d+)/$', BookmarkDV.as_view(), name='detail'), # 3
]
```

- 1 : 뷰 모듈의 관련 클래스를 임포트합니다.
- 2 : URL /bookmark/ 요청을 처리할 뷰 클래스를 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'bookmark:index'가 됩니다.
- 3 : URL /bookmark/숫자/ 요청을 처리할 뷰 클래스를 지정합니다. 숫자 자리에는 레코드의 기본 키가 들어갑니다. URL 패턴의 이름은 이름공간을 포함해 'bookmark:detail'이 됩니다.
- URL 패턴의 이름이 변경되었으므로, 관련된 템플릿 파일도 변경해 줘야 합니다.

블로그 앱의 APP_URLCONF인 blog/urls.py 파일을 코딩합니다. 날짜와 관련된 제네릭 뷰를 정의하고 있습니다.

```python
from django.conf.urls import url
from blog.views import *

urlpatterns = [
    # ex: /
    url(r'^$', PostLV.as_view(), name='index'), # 1

    # ex: /post/ (same as /)
    url(r'^post/$', PostLV.as_view(), name='post_list'), # 2

    # ex: /post/ex/
    url(r'^post/(?P<slug>[-\w]+)/$', PostDV.as_view(), name='post_detail'), # 3

    # ex: /archive/
    url(r'^archive/$', PostAV.as_view(), name='post_archive'), # 4

    # ex: /2017/
    url(r'^(?P<year>\d{4})/$', PostYAV.as_view(), name='post_year_archive'), # 5

    # ex: /2017/nov/
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3}/$', PostMAV.as_view(), name='post_month_archive'), # 6

    # ex: /2017/nov/10/
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3}/(?P<day>\d{1,2})/$', PostDAV.as_view(), name='post_day_archive'), # 7

    # ex: /today/
    url(r'^today/$', PostTAV.as_view(), name='post_today_archive'), # 8
]
```

- 1 : URL /blog/ 요청을 처리할 뷰 클래스를 PostLV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:index'가 됩니다.
- 2 : URL /blog/post/ 요청을 처리할 뷰 클래스를 PostLV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:detail'이 됩니다. PostLV 뷰 클래스는 /blog/와 /blog/post/ 2가지 요청을 모두 처리한다는 점을 유의해야 합니다.
- 3 : URL /blog/영단어/ 요청을 처리할 뷰 클래스를 PostDV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:detail'가 됩니다.
- 4 : URL /blog/archive/ 요청을 처리할 뷰 클래스를 PostAV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:archive'가 됩니다.
- 5 : URL /blog/4자리숫자/ 요청을 처리할 뷰 클래스를 PostYAV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:post_year_archive'가 됩니다.
- 6 : URL /blog/4자리숫자/3자리소문자/ 요청을 처리할 뷰 클래스를 PostMAV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:post_month_archive'가 됩니다.
- 7 : URL /blog/4자리숫자/3자리소문자/1~2자리숫자/ 요청을 처리할 뷰 클래스를 PostDAV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:post_day_archive'가 됩니다.
- 8 : URL /blog/today/ 요청을 처리할 뷰 클래스를 PostTAV로 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:post_today_archive'가 됩니다.

### 3.2.4 뷰 코딩하기
