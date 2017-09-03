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

### 4.2.6 스타일시트 코딩하기 - base.css

### 4.2.7 템플릿 코딩하기 - home.html

#### 테스트용 home.html 작성

#### home.html 완성

### 4.2.8 스타일시트 코딩하기 - home.css

## 4.3 지금까지의 작업 확인하기
