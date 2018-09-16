---
layout: post
section-type: post
title: pyDjango - chap8. Blog 앱 확장 - 댓글 달기
category: django
tags: [ 'django' ]
published: false
---
장고 1.7 버전까지는 django.contrib.comments 패키지를 통해 자체 댓글 기능을 제공했었습니다. 장고 1.8 버전 이후부터는 comments 기능을 제외하고, 이보다 좀 더 유연하고 확장성이 높은 오픈소스 패키지인 django-disqus 패키지를 사용하는 것을 권장합니다.  

django-disqus 패키지는 다음과 같은 기능을 제공합니다.

- 기존읜 django.contrib.comments 앱을 이용해 작성한 댓글을 DISQUS로 옮기기
- DISQUS로 만든 댓글을 JSON 파일로 덤프하기
- DISQUS로 만든 댓글을 WXR 파일로 내보내기
- 댓글에 필요한 템플릿 태그 제공

django-disqus 패키지를 사용하려면 DISQUS 홈페이지에서 앱에 대한 설정을 해줘야 합니다.

## 8.1 애플리케이션 설계하기

### 8.1.1 화면 UI 설계
댓글의 화면 디자인은 DISQUS에서 디폴트로 제공해줍니다. 댓글에 대한 수정, 답글, 페이스북 등 공유하는 기능도 제공합니다.

### 8.1.2 테이블 설계
pass
### 8.1.3 URL 설계
pass
### 8.1.4 작업/코딩 순서

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | settings.py | disqus 앱 및 관련 항목을 등록
모델 코딩하기 | migrate | disqus 앱에서는 불필요하나, site 앱에서 이 명령이 필요함
템플릿 코딩하기 | templates 디렉터리 | 템플릿 파일 추가
그 외 작업하기 | DISQUS 홈페이지 | 계정 생성 및 댓글 앱 설정하기


## 8.2 DISQUS 홈페이지 설정하기
[DISQUS](https://disqus.com){:target="`_`blank"}

![]({{site.url}}/img/post/python/django/book_8_1.png)

페이스북, 트위터, 구글 계정을 연동해 계정을 만들 수도 있고, 신규로 가입도 가능합니다. [Name] 은 한글도 가능합니다.

> #### Shortname 찾는 방법
첫 페이지 > 우측 상단의 설정 아이콘 > Admin > 상단 메뉴 [Settings] > 좌측 메뉴 [Basic] (사이트 개편에 따라 위치가 다를 수 있음)

## 8.3 개발 코딩하기
오픈 소스로부터 설치한 disqus 앱을 등록하고, disqus 앱에서 제공하는 기능을 사용하기 위해 관련 파일들을 수정합니다. 템플릿 파일 코딩이 주된 작업입니다.

### 8.3.1 뼈대 만들기
django-disqus 패키지를 settings.py 파일에 등록합니다.  
django-disqus 패키지의 소스 디렉터리를 살펴보면, 앱 설정 파일인 apps.py 파일이 정의되어 있지 않습니다. 이런 경우는 앱 디렉터리명인 'disqus'를 등록해주면 됩니다. 또한 django-disqus 패키지를 사용하기 위해서 몇 가지 더 추가로 등록해주어야 합니다.

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
    'tagging.apps.TaggingConfig',
    'disqus',
    'django.contrib.sites',
]

DISQUS_WEBSITE_SHORTNAME = DISQUS에서 설정한 Shortname
SITE_ID = 1
```
django-disqus 패키지를 사용하는 모든 사이트들을 구별할 수 있어야 하므로, django-disqus를 사용하는 장고의 각 사이트는 사이트 구별자를 갖고 있어야 합니다. 이를 위해 장고의 기본 애플리케이션 django.contrib.sites 를 등록하고 SITE_ID 값을 임의로 지정합니다.

### 8.3.2 모델 코딩하기

테이블 정의를 딱히 하지 않기 때문에 변경사항이 없습니다. 하지만 disqus 앱을 사용하기 위해서 필수적으로 등록해야 하는 django.contrib.sites 앱에는 테이블이 있으므로, migrate 과정이 필요합니다.

```
~/Git/Book_Study/pyDjango/2nd(master*) » python manage.py makemigrations
No changes detected
(pyDjango) ------------------------------------------------------------
~/Git/Book_Study/pyDjango/2nd(master*) » python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, bookmark, contenttypes, sessions, sites, tagging
Running migrations:
  Applying sites.0001_initial... OK
  Applying sites.0002_alter_domain_unique... OK
```

### 8.3.3 URLconf 코딩하기
pass
### 8.3.4 뷰 코딩하기
pass
### 8.3.5 템플릿 코딩하기
disqus 댓글 앱은 모델이나 뷰 작업은 없고, 템플릿 작업만 해주면 됩니다. DISQUS 애플리케이션이 로컬 서버에 댓글을 저장하는 것이 아니라, DISQUS 서버에 저장된 댓글을 가져와서 브라우저 화면에 보여주는 기능이 주된 역할이기 떄문입니다. 화면에 보여주는 역할은 커스텀 태그로 구현되어 django-disqus 패키지에 들어 있어서, 해당 커스텀 태그를 잘 사용하기만 하면 됩니다.

- blog/post_detail.html
{% raw %}
```python
<a href="{% url 'blog:tag_cloud' %}"><i>[ TagCloud ]</i></a>
</div> # 기존 동일
<br> # 여기서부터 추가
<div>
{% load disqus_tags %} # 1
{% disqus_show_comments %}
</div>
```
{% endraw %}
- 1 : disqus 앱에 정의된 커스텀 태그를 사용하기 위해 disqus_tags 모듈을 로딩합니다.

참고로, disqus 앱에서 보여주는 댓들은 글자 크기를 조정할 수 있습니다. 그래서 본문과 댓글 간에 글자 크기가 서로 어울리지 않는다면 본문의 글자 크기를 변경해야 합니다. disqus 댓글과 어울리는 글자 크기는 14~16pt가 적당합니다. 그래서 본문의 글자 크기를 14pt로 변경합니다.

- static/css/base.css

```css
body {
    font-family: "Lucida Grande", Verdana, Arial, sans-serif;
    font-size: 14px;
}
```

## 8.4 지금까지의 작업 확인하기
포스트 하나를 선택해 댓글 영역을 확인합니다.
![]({{site.url}}/img/post/python/django/book_8_2.png)
