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

### 7.2.5 템플릿 코딩하기
URL 설계에 따라 2개의 템플릿 파일이 추가로 필요합니다.

또한 화면 UI 설계에 따르면 기존 post_detail.html 파일도 수정이 필요합니다. 화면 UI를 보면 post_detail.html에서 태그를 클릭해 tagging 화면을 보여주는 흐름이므로, post_detail.html 파일을 먼저 코딩합니다.

#### post_detail.html
{% raw %}
- blog/post_detail.html

```python
<div class="body">
    {{ object.content|linebreaks }}
</div>
<div>
    <b>TAGS: </b>
    {% load tagging_tags %} # 1
    {% tags_for_object object as tags %} # 2
    {% for tag in tags %} # 3
    <a href="{% url 'blog:tagged_object_list' tag.name %}">{{ tag.name }}</a> # 4
    {% endfor %}
    <a href="{% url 'blog:tag_cloud' %}"><i>[ TagCloud ]</i></a> # 5
</div>
</div>
{% endblock %}
```

- 1 : tagging 패키지에 정의된 커스텀 태그를 사용하기 위해 tagging_tags 모듈을 로딩합니다.
- 2 : {% tags_for_object %} 커스텀 태그를 사용해 object 객체에 달려 있는 태그들의 리스트를 추출합니다. object 객체는 PostDV 클래스형 뷰에서 넘겨주는 컨텍스트 변수로써, 특정 Post 객체가 담겨 있습니다. 추출한 태그 리스트는 tags 템플릿 변수에 할당합니다.
- 3 : 추출한 태그 리스트의 각 태그를 순회하면서 tag.name을 출력합니다.
- 4 : tag.name에 연결된 링크는 'blog:tagged_object_list' URL 패턴에 tag.name 인자를 넘겨주어 지정합니다.
- 5 : for 루프 이후에, 동일한 줄에 [TagCloud] 텍스트를 출력하고 'blog:tag_cloud' URL 패턴을 `<a href>` 링크로 연결합니다.

#### tagging_cloud.html

태그 클라우드를 보여주는 템플릿 파일을 코딩합니다. 태그 클라우드란, 태그들에게 가중치를 부여해 위치나 글자 크기 등을 강조함으로써 태그들의 리스트를 효과적으로 시각화 한 것입니다.

템플릿 파일은 blog/templates/tagging/ 디렉터리 하위에 둡니다.

```python
{% extends "base.html" %}

{% block title %}tagging_cloud.html{% endblock %} # 1

{% load staticfiles %}
{% block extrastyle %}{% static "tagging/tag.css" %}{% endblock %}


{% block content %}
<div id="content">

    <h1>Blog Tag</h1>

    <dlv class="tag-cloud">
        {% load tagging_tags %} # 2
        {% tag_cloud_for_model blog.Post as tags with steps=6 min_count=1 distribution=log %} # 3
        {% for tag in tags %}
        <span class="tag-{{ tag.font_size }}"> # 4
            <a href="{% url 'blog:tagged_object_list' tag.name %}">{{ tag.name }} ({{ tag.font_size }})</a> # 5
        </span>
        {% endfor %}
    </dlv>
</div>
{% endblock %}
```

- 1 : title 블록을 재정의합니다. 페이지의 제목을 tagging_cloud.html로 지정합니다.
- 2 : tagging 패키지에 정의된 커스텀 태그를 사용하기 위해 tagging_tags 모듈로 로딩합니다.
- 3 : {% tag_cloud_for_model %} 커스텀 태그를 사용해 태그 클라우드 표현 방식을 정의합니다.
  - **blog.Post** : 태그를 추출할 대상은 블로그 앱의 Post 모델입니다.
  - **as tags** : 태그 리스트를 tags 라는 템플릿 변수에 담습니다.
  - **with staps=6 min_count=1** : 태그 폰트 크기 범위를 1~6, 출력용 최소 사용 횟수를 1로 정합니다.
  - **distribution=log** : 태그 폰트 크기를 할당할 때 수학 Logarithmic 알고리즘을 사용합니다.
- 4 : 각 태그별로 디자인을 적용하기 위해 스타일시트 클래스를 .tag-3 형식으로 지정합니다. 스타일시트는 위에서 지정한 tag.css 파일에 정의되어 있습니다.
- 5 : Django 형식으로 태그를 출력하고, 링크는 'blog:tagged_object_list' URL 패턴에 tag.name 인자를 넘겨주어 지정합니다.

#### tagging_post_list.html

태그 클라우드에서 특정 태그를 클릭했을 때, 그 태그가 걸려 있는 포스트의 리스트를 보여주는 템플릿 파일을 코딩합니다.

- blog/templates/tagging/tagging_post_list.html

```python
{% extends "base.html" %}

{% block title %}tagging_post_list.html{% endblock %} # 1

{% block content %}
<div id="content">
    <h1>Posts for tag - {{ tag.name }}</h1> # 2

    {% for post in object_list %} # 3
    <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
    {{ post.modify_date|date:"N d, Y" }} # 4
    <p>{{ post.descriptions }}</p>
    {% endfor %}
</div>
{% endblock %}
```

- 1 : title 블록을 재정의합니다. 페이지의 제목은 tagging_post_list.html로 합니다.
- 2 : Tag 모델의 필드는 id와 name 뿐입니다.
- 3 : object_list 객체는 PostTOL 클래스형 뷰에서 넘겨주는 컨텍스트 변수로써, 특정 tag가 달려 있는 Post 리스트가 담겨 있습니다. object_list 객체의 내용을 순회하면서 Post 객체의 title, modify_date, descriptions 속성을 출력합니다.
- 4 : modify_date 속성값을 "N d, Y" 포멧으로 출력합니다. (ex: July 05, 2017)
{% endraw %}

### 7.2.6 스타일시트 코딩하기
CSS 파일을 코딩합니다. 파일명은 tag_cloud.html에서 지정한 tagging/tag.css 입니다.  

템플릿 파일처럼 CSS 파일 등 static 파일도 적절한 디렉터리에 위치시켜야 장고가 찾을 수 있습니다. 정적 파일의 표준 위치는 템플릿 파일의 원리와 동일합니다. 각 애플리케이션에 소속된 정적 파일은 해당 애플리케이션의 하위 static/애플리케이션명 디렉터리에 위치시키고, 프로젝트 전체에 관련된 정적 파일은 settings.py 파일의 STATICFILES_DIRS 항목으로 지정한 디렉터리에 위치시킵니다.  

- blog/static/tagging/tag.css

```css
.tag-cloud {  # 1
    width: 30%;
    margin-left: 30px;
    text-align: center;
    padding: 5px;
    border: 1px solid orange;
    background-color: #ffc;
}

.tag-1 {font-size: 12px;}  # 2

.tag-2 {font-size: 14px;}

.tag-3 {font-size: 16px;}

.tag-4 {font-size: 18px;}

.tag-5 {font-size: 20px;}

.tag-6 {font-size: 24px;}
```

- 1 : <div class="tag-cloud"> 영역에 대한 너비, 왼쪽 마진, 텍스트 정렬, 안쪽 여백, 테두리선, 배경색 등을 지정합니다.
- 2 : <span class="tag{{tag.font-size}}"> 영역에 대한 폰트 크기를 지정합니다. tag.font_size 값에 따라서 태그의 폰트 크기가 달라집니다.
