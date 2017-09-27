---
layout: post
section-type: post
title: pyDjango - chap4. 프로젝트 첫 페이지 만들기
category: django
tags: [ 'django' ]
---
첫 페이지는 사이트 전체의 이미지를 대표하므로, 개성있는 UI와 일관성있는 룩앤필이 강조됩니다. 따라서 기능보다는 디자인 측면이 중요하기 때문에 HTML, 자바스크립트, 스타일시트 등의 지식이 필요한 부분입니다.

## 4.1 첫 페이지 설계하기

첫 페이지를 개발하는 것이므로 화면 UI를 설계하는 템플릿 파일 설계가 주된 작업이고, URL 설계는 아주 간단합니다. 물론 테이블 설계는 필요하지 않습니다.

### 4.1.1 화면 UI 설계

만드려는 첫 페이지 화면은 제목(header), 메뉴(menu), 본문(content), 바닥글(footer) 으로 이루어져 있습니다.  
본문에는 이 사이트에서 제공하는 앱을 설명하고, 해당 앱에 대해 콘텐츠를 추가(add) 및 수정(change) 할 수 있는 링크를 추가합니다.

![]({{site.url}}/img/post/python/django/book_4_1.png)

### 4.1.2 테이블 설계
테이블은 변경 사항이 없습니다.

### 4.1.3 URL 설계
프로젝트의 첫 페이지는 루트(/) URL에 대한 로직을 개발하는 것입니다.

URL 패턴 | 뷰 이름 | 뷰가 처리하는 내용
---|---|---
/ | HomeView(TemplateView) | home.html 템플릿을 보여줍니다.
/bookmark/ | | 기존관 동일함
/blog/ | | 기존관 동일함
/admin/ | | 기존관 동일함

### 4.1.4 작업/코딩 순서

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | (이번 과정엔 필요 없음) | (이번 과정엔 필요 없음)
모델 코딩하기 | (이번 과정엔 필요 없음) | (이번 과정엔 필요 없음)
URLconf | urls.py | 루트(/) URL 정의
뷰 코딩하기 | views.py | HomeView 작성
템플릿 코딩하기 | templates 디렉터리 | home.html 작성, 상속 기능 적용
그 외 코딩하기 | static 디렉터리 | 화면 디자인을 위해 css 작성

## 4.2 개발 코딩하기

### 4.2.1 뼈대 만들기
이번 과정에서는 작업이 없습니다.

### 4.2.2 모델 코딩하기
이번 과정에서는 작업이 없습니다.

### 4.2.3 URLconf 코딩하기
뷰 클래스는 HomeView, URL 패턴명은 'home'이라고 정의했습니다.

- mysite/urls.py

```python
from django.conf.urls import url, include
from django.contrib import admin

from mysite.views import HomeView # 추가

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomeView.as_view(), name='home'), # 추가
    url(r'^bookmark/', include('bookmark.urls', namespace='bookmark')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
]
```

### 4.2.4 뷰 코딩하기
HomeView는 특별한 처리 로직 없이 단순히 템플릿만 보여주는 로직이므로, TemplateView 제네릭 뷰를 상속받아 코딩합니다.  

- mysite/views.py

```python
from django.views.generic.base import TemplateView

#--- TemplateView
class HomeView(TemplateView): # 1
    template_name = 'home.html' # 2
```

- 1 : TemplateView 제네릭 뷰를 상속받아 사용합니다. TemplateView를 사용하는 경우에는 필수적으로 template_name 클래스 변수를 오버라이딩으로 지정해줘야 합니다.
- 2 : mysite 프로젝트의 첫 화면을 보여주기 위한 템플릿 파일은 home.html으로 지정합니다. 템플릿 파일이 위치하는 디렉터리는 settings.py 파일의 TEMPLATE_DIRS 항목으로 지정되어 있습니다.  

프로젝트 화면의 전체 윤관을 잡고, 애플리케이션별로 바로가기 링크 및 메뉴를 만들어야 하며, 템플릿 상속 기능도 구현해야 하기 때문에 템플릿 코딩은 좀 복잡한 편입니다. 또한 실전에 사용할 수 있을 정도로 화면 룩앤필을 보여주기 위해 CSS 코딩도 필요합니다.


### 4.2.5 템플릿 코딩하기 - base.html

템플릿 상속은 보통 3단계로 구성합니다. 여기서는 복자반 편이 아니므로 2단계로 구성합니다. 최상위 템플릿은 사이트 전체의 룩앤필을 정의하는 것으로 보통은 파일명을 base.html로 합니다. 파일의 위치는 배결 애플리케이션 템플릿이 아니라 공통 템플릿이므로, 프로젝트 템플릿 디렉터리에 생성합니다.  

프로젝트 템플릿 디렉터리는 settings.py 파일에 다음과 같이 정의해 두었습니다.

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
```

base.html에 모든 페이지에서 공통을 사용하는 제목과 메뉴, 이런 페이지 구성요소들을 배치하는 내용으로 코딩합니다.

![]({{site.url}}/img/post/python/django/book_4_2.png)

- templates/base.html
{% raw %}
```html
<!doctype html> # 1
<html lang="ko">
<head>
    <title>{% block title %} Django Web Programming {% endblock %}</title>
    {% load staticfiles %} # 2
    <link rel="stylesheet" href="{% static "css/base.css" %}" type="text/css"> # 3
    <link rel="stylesheet" href="{% block extrastyle %}{% endblock %}">
</head>

<body>
<div id="header"> # 4
    <h2 class="maintitle">Easy&amp;Fast Django Web Programming</h2>
    <h4 class="welcome">Welcome, <a href="#">makingfunk</a>
        <a href="#">Change Password</a>
        <a href="#">Logout</a>
    </h4>
</div>

<div id="menu"> # 5
    <li><a href="#">Home</a></li>
    <li><a href="#">Bookmark</a></li>
    <li><a href="#">Blog</a></li>
    <li><a href="#">Photo</a></li>
    <li><a href="#">Add&bigtriangledown;</a>
        <ul>
            <li><a href="#">Bookmark</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Photo</a></li>
        </ul>
    </li>
    <li><a href="#">Change&bigtriangledown;</a>
        <ul>
            <li><a href="#">Bookmark</a></li>
            <li><a href="#">Blog</a></li>
            <li><a href="#">Photo</a></li>
        </ul>
    </li>
    <li><a href="#">Archive</a></li>
    <li><a href="#">Search</a></li>
    <li><a href="#">Admin</a></li>
</div>
{% block content %}{% endblock %} # 6
{% block footer %}{% endblock %} # 7
</body>
</html>
```

- 1 : HTML5 스팩을 준수하는 파일임을 나타냅니다.
- 2 : {% static %} 템플릿 태그를 사용하기 위해서는 {% load staticfiles %} 문장으로 커스텀 태그 파일 staticfiles 를 로딩해야 합니다.
- 3 : 이 파일에 스타일을 적용하기 위해 css/base.css 파일을 코딩합니다.
- 4 : header 영역에는 사이트의 제목과 로그인 관련 기능이 들어 있습니다. makingfunk 자리는 로그인 아이디가 채워지는 자리입니다. `&amp;`는 HTML 특수문자(&)를 의미합니다.
- 5 : menu 영역에는 사이트의 메뉴가 위치합니다. `<ul><li>`는 가로 메뉴와 드롭다운 메뉴를 구성합니다.
- 6 : content 영역은 빈칸으로 하고, 각 앱에서 만드는 페이지로 채워집니다. 이 영역은 {% block %} 태그를 사용함으로써, 실제 내용은 전적으로 하위 템플릿 파일에서 결정됩니다.
- 7 : footer 영역은 사이트의 꼬리말이 위치합니다. 이 영역 역시 {% block %} 태그를 사용함으로써, 실제 내용은 하위 템플릿에서 결정됩니다.

이번 base.html 템플릿 파일에는 하위 템플릿 파일에서 재정의 할 수 있도록 다음 4가지 블록을 정의하고 있습니다.

- **{% block title %}** : 하위 페이지마다 페이지 제목을 다르게 정의할 수 있습니다.
- **{% block extrastyle %}** : base.html 에서 사용하는 base.css 파일 이외에, 하위 페이지에서 필요한 CSS 파일을 정의할 수 있습니다.
- **{% block content %}** : 하위 페이지마다 실제 본문 내용을 정의할 수 있습니다.
- ** {% block footer %}** : 하위 페이지마다 꼬리말을 다르게 정의할 수 있습니다.

> #### {% block %} 정의 참고사항
`{% block content %}{% endblock %}`을 `<div id="content">{% block content %}{% endblock %}</div>` 이라고 코딩한다면?  
2 가지 방법 모두 사용 가능합니다. `<div>` 태그를 상위에 둘 것인지 하위에 둘 것인지의 차이인데, 이는 개발자의 취향에 따라 선택하면 됩니다.
{% endraw %}

### 4.2.6 스타일시트 코딩하기 - base.css
CSS 파일명은 base.html 에서 지정한 base.css 입니다.  

프로젝트 템플릿 디렉터리처럼 CSS 파일 등의 정적(static) 파일도 특정 디렉터리에 위치시켜야 장고가 찾을 수 있습니다.

```python
STATICFILES_DIRS =  [os.path.join(BASE_DIR, 'static')]
```

- static/css/base.css

```css
body {
    font-family: "Lucida Grande", Verdana, Arial, sans-serif;
    font-size: 12px;
}

/* PAGE STRUCTURE */
div#header {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 30px;
    width: 100%;
    display: table;
    background: orange;
}

div#menu {
    position: absolute;
    top: 30px;
    left: 0px;
    height: 20px;
    width: 100%;
    display: table;
    table-layout: fixed;
    border-spacing: 40px 0px;
    background: #ffa;
    font-size: 8px;
}

div#content {
    position: absolute;
    top: 70px;
    left: 50px;
    right: 50px;
}

div#footer {
    position: absolute;
    bottom: 20px;
    left: 50px;
    right: 50px;
    height: 30px;
    border-top: 1px solid #ccc;
}

/* HEADER */
.maintitle {
    display: table-cell;
    vertical-align: middle;
    padding-left: 20px;
    color: #ffc;
    font-weight: bold;
    font-size: 16px;
}

.welcome {
    display: table-cell;
    vertical-align: middle;
    text-align: right;
    padding-right: 20px;
    color: #ffc;
    font-weight: normal;
    font-size: 12px;
}

.welcome a:link, .welcome a:visited {
    color: white;
}

/* MENU */
div#menu a:link, div#menu a:visited {
    color: #36c;
}

div#menu > li {
    display: table-cell;
    vertical-align: middle;
    border: 2px solid #bbb;
    border-radius: 25px;
    text-align: center;
    font-weight: bold;
}

/* pulldown menu */
div#menu li ul {
    display: none;
    position: absolute;
    margin: 0;
    padding: 10px 10px 5px 10px;
    list-style: none;
    border-right: 1px solid #ccc;
    border-left: 1px solid #ccc;
    border-bottom: 1px  solid #ccc;
    background: white;
    z-index: 1;
}

div#menu li:hover ul {
    display: block;
}

/* LINK */
a:link, a:visited {
    color: #369;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* TABLE */
table {
    border-collapse: collapse;
}

td, th {
    line-height: 18px;
    border-bottom: 1px solid #eee;
    vertical-align: top;
    padding: 5px 15px;
    font-family: "Lucida Grande", Verdana, Arial, sans-serif;
}
```

HomeView 클래스 뷰에서 template_name 을 home.html으로 지정했기 때문에 home.html 파일이 존재해야 합니다.

### 4.2.7 템플릿 코딩하기 - home.html

#### 테스트용 home.html 작성
완전한 home.html을 구현하기 위해서는 home.html뿐만 아니라 home.css 파일도 코딩해야 합니다. 하지만 앞에서 구현한 파일들이 정상으로 동작하는지 확인하기 위해 간단한 임시 home.html을 먼저 만듭니다.  

home.html 템플릿도 개별 애플리케이션 템플릿이 아니므로, base.html과 동일하게 프로젝트 템플릿 디렉터리에 생성합니다.

- templates/home.html
{% raw %}
```html
{% extends "base.html" %}

{% block title %}home.html{% endblock %} # 1

{% block content %} # 2
<div id="content"> # 3
This is CONTENT area.
</div>
{% endblock content %}

{% block footer %} # 4
<div id="footer">
    This is FOOTER area.
</div>
{% endblock footer %}
```
{% endraw %}
- 1 : title 블록을 재정의합니다. 즉, 페이지 title을 home.html이라고 정의합니다.
- 2 : content 블록을 재정의합니다.
- 3 : `<div>` 태그로 content 영역을 정의합니다. 참고로 이 영역에 대한 스타일은 base.css에서 정의하고 있습니다.
- 4 : footer 블록을 재정의합니다.

![]({{site.url}}/img/post/python/django/book_4_3.png)

페이지의 제목과 우측의 로그인 관련 항목들, 메뉴 항목들이 정상 출력되고 있습니다. 메뉴의 Add, Change 메뉴의 드롭다운 메뉴도 제대로 출력되는지 확인해야합니다.

#### home.html 완성

- templates/home.html
{% raw %}
```html
{% extends "base.html" %}

{% block title %}home.html{% endblock %}

{% load staticfiles %} # 1
{% block extrastyle %}{% static "css/home.css" %}{% endblock %} # 2

{% block content %}
<div id="content"_home>
    <div id="homeimg"> # 3
        <a href="/"><img src="{% static 'img/django-actor-big.jpg' %}" style="height:256px;"/></a>
        <h4 style="margin: 0;">This is Django powered web site.</h4>
    </div>

    <hr style="margin: 5px 0;">

    <h2>Select Application</h2>

    <table id="applist"> # 4
        <tr>
            <td><b><i><a href="#">Bookmark</a></i></b></td>
            <td>You can write your own post and share to others. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo</td>
            <td class="Edit"><i><a href="#">Add</a></i></td>
            <td class="Edit"><i><a href="#">Change</a></i></td>
        </tr>
        <tr>
            <td><b><i><a href="#">Blog</a></i></b></td>
            <td>You can write your own post and share to others. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo</td>
            <td class="Edit"><i><a href="#">Add</a></i></td>
            <td class="Edit"><i><a href="#">Change</a></i></td>
        </tr>
        <tr>
            <td><b><i><a href="#">Photo</a></i></b></td>
            <td>You can write your own post and share to others. Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo</td>
            <td class="Edit"><i><a href="#">Add</a></i></td>
            <td class="Edit"><i><a href="#">Change</a></i></td>
        </tr>
    </table>
</div>
{% endblock content %}

{% block footer %}
<div id="footer">
    &copy; makingfunk 2017 # 5
</div>
{% endblock footer %}
```

- 1 : {% static %} 템플릿 태그를 사용하기 위해서는 {% load staticfiles %} 문장으로 커스텀 태그 파일 staticfiles를 로딩해야 합니다.
- 2 : extrastyle 블록을 재정의합니다. 즉, base.css 스타일시트 파일 외에 추가적으로 home.css 스타일시트를 지정합니다. home.css 파일은 home.html 템플릿에 사용되는 스타일을 정의하기 위한 스타일시트 파일로 다음절에 코딩합니다.
- 3 : 이미지 영역의 id를 homeimg라고 설정하고, `<img>` 태그를 사용해 그림을 넣었습니다. {% static %} 템플릿 태그 기능에 의해 STATICFILES_DIRS 디렉터리 하위에서 img/django-actor-big.jpg 파일을 찾습니다.(static/img/이미지파일)
- 4 : `<i>` 는 이텔릭체로 출력하는 HTML 태그입니다.
- 5 : `&copy`는 copyright 마크를 표시하는 HTML 특수문자입니다.
{% endraw %}
### 4.2.8 스타일시트 코딩하기 - home.css
home.html 템플릿 파일에서 스타일 적용이 필요한 항목 `<div id="content_home">,<div id="homeimg">` 2개입니다.

- static/css/home.css

```css
div#content_home {
    position: absolute;
    top: 80px;
    left: 110px;
    right: 110px;
}

div#homeimg {
    background: #ddd;
    padding: 5px 0 1px 0;
    text-align: center;
}
```

## 4.3 지금까지의 작업 확인하기

![]({{site.url}}/img/post/python/django/book_4_4.png)

> #### 서버 사이드 vs 클라이언트 사이드 프로그래밍  
웹 프로그래밍은 서버 사이드와 클라이언트 사이드(프론트엔드) 프로그래밍으로 구분하고 있습니다. 프로젝트의 기능 개발, 로직의 처리 성능 향상, 데이터베이스 연동 등을 다루는 서버 기술과 디자인 요소 및 사용 편의성을 다루는 클라이언트 기술이 다르게 발전해 왔기 때문입니다. 이 이면에는 클라이언트를 대표하는 웹 브라우저 기술이 빠르고 다양하게 발전하고 있다는 점도 한 요인입니다.  
프론트엔트 프로그래밍은 HTML, CSS, 자바스크립트 기술을 잘 이해하고 있어야만 합니다.

> #### 부트스트랩 라이브러리  
부트스트랩(Bootstrap)은 UI 화면 디자인이 필요한 CSS와 자바스크립트를 미리 만들어서 제공해주느 ㄴ라이브러리입니다. 부트스트랩은 2011년에 트위터에서 처음 만들어졌으며 현재는 웹 디자인의 필수 라이브러리로 자리잡았습니다.  
부트스트랩은 웹 페이지에 사용되는 거의 모든 요소에 대해 라이브러리로 미리 정의해 놓았기 때문에, 아주 쉽고 빠르게 웹 사이트를 만들 수 있다는 장점을 가지고 있습니다. 그래서 전문 디자이너가 아니더라도 부트스트랩에서 제공하는 요소들을 가져다 쓰거나, 필요하면 직접 수정을 해서 고급스러운 웹 페이지를 만들 수 있습니다.