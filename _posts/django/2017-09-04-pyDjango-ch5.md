---
layout: post
section-type: post
title: pyDjango - chap5. 기존 앱 개선하기 - Bookmark 앱, Blog 앱
category: django
tags: [ 'django' ]
---
첫 페이지가 완성되고, 북마크 앱과 블로그 앱을 첫 페이지에 맞춘다면 이번 과정은 필요 없을 수도 있습니다.  
하지만 일반적으로 디자인 요소가 중요시되는 첫 페이지 개발이 늦어지고, 고객의 요청에 따라 첫 페이지가 변경되는 경우가 자주 발생하기 때문에, 이미 개발된 북마크 앱과 블로그 앱을 개선하는 과정을 다룹니다.
{% raw %}
## 5.1 기존 앱 개선 설계하기
첫 페이지의 메뉴에서 애플리케이션을 클릭해 해당 애플리케이션의 첫 페이지로 이동하는 기능과, 첫 페이지의 룩앤필에 맞추기 위해 base.html 템플릿을 상속받아 각 애플리케이션의 페이지들을 개발합니다.

### 5.1.1 화면 UI 설계
### 5.1.2 테이블 설계
테이블 변경 사항이 없습니다.
### 5.1.3 URL 설계
URL 변경사항 없습니다.
### 5.1.4 작업/코딩 순서
작업순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
템플릿 코딩하기 | templates 디렉터리 | base.html 파일의 메뉴 링크 수정 <br> home.html 파일의 링크 수정 <br> 북마크 앱의 템플릿 파일들 수정 <br> 블로그 앱의 템플릿 파일들 수정

## 5.2 개발 코딩하기

### 5.2.1 뼈대 만들기
신규 앱을 만드는 것이 아니기 때문에 뼈대 작업이 없습니다.
### 5.2.2 모델 코딩하기
테이블 변경 사항 없습니다.
### 5.2.3 URLconf 코딩하기
URL 변경사항 없습니다.
### 5.2.4 뷰 코딩하기
뷰 코딩 없습니다.
### 5.2.5 템플릿 코딩하기
#### base.html 수정

- templates/base.html

```python
<div id="menu">
    <li><a href="{% url 'home' %}">Home</a></li>
    <li><a href="{% url 'bookmark:index' %}">Bookmark</a></li>
    <li><a href="{% url 'blog:index' %}">Blog</a></li>
    # 중략
    <li><a href="{% url 'blog:post_archive' %}">Archive</a></li>
    <li><a href="#">Search</a></li>
    <li><a href="{% url 'admin:index' %}">Admin</a></li>
</div>
```

메뉴 버튼명 | URL 패턴명 | {% url %} 반환값
---|---|---
Home | 'home' | /
Bookmark | 'bookmark:index' | /bookmark/
Blog | 'blog:index' | /blog/
Archive | 'blog:post_archive' | /blog/archive/
Admin | 'admin:index' | /admin/

#### home.html 수정

- templates/home.html

```python
<table id="applist">
    <tr>
        <td><b><i><a href="{% url 'bookmark:index' %}">Bookmark</a></i></b></td>
        # 중략
        </tr>
        <tr>
            <td><b><i><a href="{% url 'blog:index' %}">Blog</a></i></b></td>
```

링크 텍스트 | URL 패턴명 | {% url %} 반환값
---|---|---
Bookmark | 'bookmark:index' | /bookmark/
Blog | 'blog:index' | /blog/

#### bookmark_list.html 수정

- bookmark/templates/bookmark/bookmark_list.html

```python
{% extends "base.html" %}

{% block title %}Django Bookmark List{% endblock %}

{% block content %}
<div id="content">
    <h1>Bookmark LIst</h1>

    <ul>
        {% for bookmark in object_list %}
            <li><a href="{% url 'bookmark:detail' bookmark.id %}">{{ bookmark }}</a></li> # 1
        {% endfor %}
    </ul>
</div>
{% endblock %}
```

- 1 : 북마크 제목에 연결된 URL 링크를 표현할 때 사용하는 URL 패턴명을 'detail' 대신 이름공간을 포함한 'bookmark:detail' 으로 수정했습니다.

#### bookmark_detail.html 수정

- bookmark/templates/bookmark/bookmark_detail.html

```python
{% extends "base.html" %}

{% block title %}Django Bookmark Detail{% endblock %}

{% block content %}
<div id="content">

    <h1>{{  object.title }}</h1>

    <ul>
        <li>URL: <a href="{{ object.url }}">{{ object.url }}</a></li>
    </ul>
</div>
{% endblock %}
```

#### post_all.html 수정

- blog/templates/blog/post_all.html

```python
{% extends "base.html" %}

{% block title %}post_all.html{% endblock %}

{% block content %}
<div id="content">

<h1>Blog List</h1>
# 중략
</div>
{% endblock %}
```

#### post_detail.html 수정

- blog/templates/blog/post_detail.html

```python
{% extends "base.html" %}

{% block title %}post_detail.html{% endblock %}

{% block content %}
<div id="content">

<h2>{{ object.title }}</h2>
# 중략
</div>
{% endblock %}
```

#### post_archive_*.html 수정

- blog/templates/blog/post_archive.html

```python
{% extends "base.html" %}

{% block title %}post_archive.html{% endblock %}

{% block content %}
<div id="content">

<h1>Post Archives until {% now "N d, Y" %}</h1>
# 중략
</div>
{% endblock %}
```

- blog/templates/blog/post_archive_year.html

```python
{% extends "base.html" %}

{% block title %}post_archive_year.html{% endblock %}

{% block content %}
<div id="content">

<h1>Post Archives for {{ year|date:"Y" }}</h1>
# 중략
</div>
{% endblock %}
```

- blog/templates/blog/post_archive_month.html

```python
{% extends "base.html" %}

{% block title %}post_archive_month.html{% endblock %}

{% block content %}
<div id="content">

<h1>POST Archives for {{ month|date:"N, Y" }}</h1>
# 중략
</div>
{% endblock %}
```

- blog/templates/blog/post_archive_day.html

```python
{% extends "base.html" %}

{% block title %}post_archive_day.html{% endblock %}

{% block content %}
<div id="content">

<h1>Post Archives for {{ day|date:"N d, Y" }}</h1>
# 중략
</div>
{% endblock %}
```
{% endraw %}
## 5.3 지금까지의 작업 확인하기
브라우저로 확인해봅니다.  

첫 페이지에 [Home], [Bookmark], [Blog], [Archives], [Admin] 버튼들을 클릭해 나오는 각 페이지들을 확인합니다. 각 화면마다 base.html 템플릿이 반영되어 있으면 정상입니다.  

프로젝트 첫 페이지
![]({{site.url}}/img/post/python/django/book_5_1.png)
Bookmark 클릭
![]({{site.url}}/img/post/python/django/book_5_2.png)
Bookmark 상세 페이지
![]({{site.url}}/img/post/python/django/book_5_3.png)
Blog 클릭
![]({{site.url}}/img/post/python/django/book_5_4.png)
Blog 상세 페이지
![]({{site.url}}/img/post/python/django/book_5_5.png)
Admin 클릭
![]({{site.url}}/img/post/python/django/book_5_6.png)
