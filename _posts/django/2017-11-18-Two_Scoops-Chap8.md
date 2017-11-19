---
layout: post
section-type: post
title: Two Scoops of Django - chap8. 함수 기반 뷰와 클래스 기반 뷰
category: django
tags: [ 'django' ]
---

장고는 함수 기반 뷰(function-based view, FBV)와 클래스 기반 뷰(class-based view, CBV)를 둘 다 지원한다. 이 두가시 타입을 어떻게 이용하는지 다룬다.

## 8.1 함수 기반 뷰와 클래스 기반 뷰를 각각 언제 이용할 것인가?

![]({{site.url}}/img/post/django/two_scoops/8.1.png)

> #### 대안 - FBV 이용  
어떤 개발자들은 대부분의 뷰를 함수 기반 뷰로 처리하기도 한다. 클래스 기반 뷰는 서브클래스가 필요한 경우에 대해 제한적으로 이용한다. 이런 방법 또한 전혀 문제 될 것이 없다.

## 8.2 URLConf로부터 뷰 로직을 분리하기
장고로 오는 요청들은 urls.py라는 모듈 내에서 URLConf를 통해 뷰로 라우팅된다. 장고는 아주 단순하고 명료하게 URL 라우트를 구성하는 방법을 제공한다.

1. 뷰 모듈은 뷰 로직을 포함해야 한다.
2. URL 모듈은 URL 로직을 포함해야 한다.

```python
# 나쁜 예
from django.conf.urls import url
from django.views.generic import DetailView

from tastings.models import Tasting

urlpatterns = [
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Tasting,
            template_name="tastings/detail.html"),
        name="detail"),
    url(r'(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Tasting,
            template_name="tastings/results.html"),
        name="results"),
]
```

이 코드는 문제가 없어 보이지만 장고의 디자인 철학에 어긋난다.

- 뷰와 url, 모델 사이에 상호 **느슨한 결합(loose coupling)** 대신 단단하게 종속적인 결합(tight coupling)이 되어 있다. 다시 말하면 뷰에서 정의된 내용이 재사용되기 어렵다는 의미다.
- 클래스 기반 뷰들 사이에서 같거나 비슷한 인자들이 계속 이용되고 있는데 이는 **DRY** 철학에 위배된다.
- (URL들의) 무한한 확장성이 파괴되어 있다. 클래스 기반 뷰의 최대 장점인 클래스 상속이 안티 패턴을 이용함으로써 불가능하게 되어 버렸다.
- 다른 이슈도 많다. 인증 절차를 추가해야 한다면 어떻게 하겠는가? 권한 처리 문제는 각 URLConf 뷰를 두 개 이상의 데코레이터로 감싸야 할까? 뷰 코드를 URLConf 안으로 밀어 넣는것은 URLConf를 관리할 수 없게 엉망으로 만드는 일이 될 것이다.

URLConf 안에 CBV를 정의하는건 많은 개발자들이 거리는 방법이다.

## 8.3 URLConf에서 느슨한 결합 유지하기

![]({{site.url}}/img/post/django/two_scoops/8.2.png)
> 초콜릿 칩 쿠키와 아이스크림 간의 느슨한 결합

```python
# tastings/views.py
from django.views.generic import ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse

from .models import tasting

class TasteListView(ListView):
    model = Tasting

class TasteDetailView(DetailView):
    model = Tasting

class TasteResultView(TasteDetailView):
    template_name = "tastings/results.html"

class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse("tastings:detail", kwargs={"pk": self.object.pk})
```

```python
# tastings/url.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.TasteListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=views.TasteDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<pk>\d+)/results/$',
        view=views.TasteResultView.as_view(),
        name='results'
    ),
    url(
        regex=r'^(?P<pk>\d+)/update/$',
        view=views.TasteUpdateView.as_view(),
        name='update'
    )
]
```

두 개의 파일로 나뉘었고 코드가 더 늘어났다. 이게 최선인가?  
그렇다. 그 이유는 다음과 같다.

- 반복되는 작업하지 않기 : 뷰들 사이에서 인자나 속성이 중복 사용되지 않는다.
- 느슨한 결합 : URLConf로부터 모델과 템플릿 이름을 전부 제거했다. 뷰는 뷰여야 하고 URLConf는 URLConf여야 하기 때문이다. 하나 이상의 URLConf에서 뷰들이 호출될 수 있어야 하는데 이를 가능하게 해 주었다.
- URLConf는 한 번에 한 가지씩 업무를 명확하고 매끄럽게 처리해야 한다. URLConf는 URL 라우팅이라는 한 가지 명확한 작업만 처리하는 것을 그 목표로 한다. 뷰의 로직을 찾기 위해 뷰나 URLConf를 둘 다 뒤지지 않아도 된다. 로직은 뷰 안에 다 존재하니기 때문이다.
- 클래스 기반이라는 것에 대한 장점을 살리게 된다. : 뷰 모듈에서 표준화된 정의를 가지게 됨으로써 다른 클래스에서 뷰를 얼마든지 상속해서 쓸 수 있다. 이 말은 인증 절차 추가, 권한 설정 추가 등 비즈니스 로직이 무엇이든 간에 우리의 방법으로 전달되는 것이라면 그 처리가 훨씬 수월해진다는 의미다.
- 무한한 유연성 : 뷰 모델에서 표준화된 정의를 구현함에 따라 뷰는 커스텀 로직이라도 얼마든지 구현할 수 있다.

### 8.3.1 클래스 기반 뷰를 사용하지 않는다면?
같은 방법이 적용된다고 보면 된다.  
`__file__` 속성을 이용하여 디렉터리 워킹(directory walking)과 정규표현식을 혼합하여 자동으로 URLConf를 생성하는 트릭을 이용한 URLConf 확장을 함수 기반 뷰와 함께 사용하는 프로젝트를 다루는 것은 매우 고통스러운 과정이다.  
항상 URLConf로부터 로직을 분리 운영하도록 한다.

## 8.4 URL 이름공간 이용하기
URL 이름공간은 앱 레벨 또는 인스턴스 레벨에서의 구분자를 제공한다.  
tastings_detail이라고 URL 이름을 정의하는 대신 tasting:detail 이라고 정의해 보자.
뷰에서 어떻게 구성되는지 앞의 코드 일부분을 보자.
```python
# tastings/view.py 코드 조각
class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse("tastings:detail", kwargs={"pk": self.object.pk})
```

HTML 템플릿 안에서는 다음과 같다.
{% raw %}
```html
{% extends "base.html" %}

{% block title %}Tastings{% endblock title %}

{% block content %}
<ul>
  {% for taste in tastings %}
  <li>
  <a href="{% url "tastings:detail" taste.pk %}">{{ taste.title }}</a>
  <small>
      (<a href="{% url "tastings:update" taste.pk %}">update</a>)
  </small>
  </li>
  {% endfor %}
</ul>
{% endblock content %}
```
이제 URL 이름공간을 어떻게 구현했는지 보일 것이다. 이것이 왜 유용할까?

### 8.4.1 URL 이름이 짧고, 명확하고, 반복되는 작업을 피해서 작성하는 방법
tastings_detail이나 tastings_results 처럼 모델이나 앱의 이름을 복사한 URL 이름들은 더 이상 볼 수 없다. 대신 'detail'이나 'results' 같은 좀 더 명확한 이름이 보인다.  
'tastings'나 특별한 앱 이름을 입력할 필요가 없기 때문에 시간도 절약된다.

### 8.4.2 서드 파티 라이브러리와 상호 운영성을 높이기
URL 이름을 <myapp>\_detail 등의 방법으로 부를 때 생기는 또 다른 문제는 <myapp> 부분이 서로 겹칠때 발생한다. 이런 경우 URL 이름공간을 통해 간단히 해결할 수 있다. 예를 들어 기존에 contact 앱이 있고 두 번째 contact 앱을 추가해야 한다면 URL 이름공간을 통해 다음과 같이 적용한다.

```python
# 프로젝트 루트에 있는 urls.py
urlpatterns += [
    url(r'^contact/', include('contactmonger.urls', namespace='contactmonger')),
    url(r'^report-problem/', include('contactapp.urls', namespace='contactapp')),
]
```
다음과 같이 템플릿에서 이용이 가능하다.

```html
{% extends "base.html" %}
{% block title %}Contact{% endblock title %}
{% block content %}
<p>
  <a href="{% url "contactmonger:create" %}">Contact Us</a>
</p>
<p>
  <a href="{% url "contactapp:report" %}">Report a Ploblem</a>
</p>
{% endblock content %}
```
{% endraw %}

### 8.4.3 검색, 업그레이드, 리팩터링을 쉽게 하기
장고가 PEP-8에 매우 친화적인 프레임워크이기 때문에 tastings_detail 같은 코드나 이름은 검색에 용이하지 않다. 반면에 tastings:detail 과 같은 이름은 검색 결과를 좀 더 명확하게 해준다. 이는 새로운 서드 파티 라이브러리와 상호 연동 시에 프로젝트를 좀 더 쉽게 업그레이드 및 리팩터링하게 만들어 준다.

### 8.4.4 더 많은 앱과 템플릿 리버스 트릭을 허용하기
꼼수(trick)은 일반적으로 확실한 이득을 주기보다는 프로젝트의 복잡성만 높이는 결과를 가져다 주지만, 몇몇 꼼수는 간단히 짚고 넘어갈 정도의 가치는 있다.

- django-debug-toolbar 같은 디버그 레벨에서 내부적인 검사를 실행하는 개발 도구
- 최종 사용자에게 '모듈'을 추가하게 하여 사용자 계정의 기능을 변경하는 프로젝트

개발자들은 언제든지 이러한 경우에 URL 이름공간을 이용한 창의적인 꼼수를 구현할 수 있지만, 가장 단순 명료한 해결 방안을 먼저 강구하고 시도하는게 옳바르다.

## 8.5 URLConf에서 뷰를 문자열로 지목하지 말자
장고 1.8 이전의 장고 튜토리얼에서는 urls.py에서 뷰를 지목(reference)하는데 문자열을 썼다.

```python
# 나쁜 예
# polls/urls.py
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # 뷰를 문자열로 정의
    url(r'^$', 'polls.views.index', name='index'),
)
```
위 방법은 몇 가지 문제가 있다.

1. 장고가 뷰의 함수, 클래스를 임의로 추가한다. 이런 임의적 기능의 문제점은 뷰에서 에러가 발생한 경우 임의의 작용을 하는 부분에 대해 디버그하기가 어려워진다.
2. 장고를 강사들이 초보자들에게 urlpatterns 변수의 초깃값에서의 공백 문자열에 대해 설명해야 한다.

아래는 urls.py를 올바르게 정의하는 방법이다.

```python
# polls/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    # 뷰를 명시적으로 정의
    url(r'^$', views.index, name='index'),
]
```
#### 참고자료

- 예전 방식 : <http://www.2scoops.co/7E/info/>
- 새로운 방식 : <http://www.2scoops.co/1.8-django-conf-urls-patterns/>

## 8.6 뷰에서 비즈니스 로직 분리하기
상당량의 복잡한 비즈니스 로직을 뷰에 구현했을때 PDF를 생성한다든지, REST API를 추가한다든지, 다른 포맷을 지원해야 하는 등의 경우에 상당량의 로직을 뷰에다 구현한 것은 큰 장애물이 될 것이다.  

이 때문에 모델 메서드, 매니저 메서드 또는 일반적인 유틸리티 헬퍼 함수들을 이용하는 전략을 선호하게 되었다. 비즈니스 로직이 쉽게 재사용 가능한 컴포넌트가 되고 이를 뷰에서 호출하는 경우, 프로젝트에서 해당 컴포넌트를 확장하기가 매우 쉬워진다. 모든 프로젝트에서 초반부터 이렇게 하는 것 자체가 항상 가능한 것이 아니기 때문에, 장고의 뷰에서 표준적으로 이용되는 구조 이외에 덧붗여진 비즈니스 로직을 발견할 때마다 해당 코드를 뷰 밖으로 이동시킨다.

## 8.7 장고의 뷰와 함수
기본적으로 장고의 뷰는 HTTP를 요청하는 객체를 받아서 HTTP를 응답하는 객체로 변경하는 함수다. 수학의 함수와 비슷한 개념이다.

```python
# 함수로서의 장고 함수 기반 뷰
HttpResponse = view(HttpResponse)

# 기본 수학식의 형태로 풀이해 봄(수학에서 이용한 함수식)
y = f(x)

# ... 그리고 이를 CBV 예로 변형해 보면 다음과 같다.
HttpResponse = View.as_view()(HttpResponse)
```

이런 일련의 과정을 거치는 변환 개념은 함수 또는 클래스 기반 뷰 모두를 통틀어 똑같이 일어난다.

> #### 클래스 기반 뷰의 경우 실제로 함수로 호출된다.
장고의 클래스 기반 뷰의 경우 함수 기반 뷰와 비교하면 사뭇 다른 모습을 보여준다. 하지만 사실 URLConf에서 View.as_view()라는 클래스 메서드는 실제로 호출 가능한 뷰 인스턴스를 반환하다. 다시 말하면 요청/응답 과정을 처리하는 콜백 함수 자체가 함수 기반 뷰와 동일하게 작동한다는 것이다.

### 8.7.2 뷰의 기본 형태들

장고에서 이용되는 뷰의 기본 형태는 기억해 두자.

```python
# simplest_views.py
from django.http import HttpResponse
from django.views.generic import View

# 함수 기반 뷰의 기본 형태
def simplest_view(request):
    # 비즈니스 로직이 여기에 위치한다.
    return HttpResponse("FBV")

# 클래스 기반 뷰의 기본 형태
class SimplestView(View):
    def get(self, request, *args, **kwargs):
        # 비즈니스 로직이 여기에 위치한다.
    return HttpResponse("CBV")
```

기본 형태가 왜 중요한가?

- 종종 우리에겐 한 기능만 따로 떼어 놓은 관점이 필요할 때가 있다.
- 가장 단순한 형태로 된 기본 장고의 뷰를 이해했다는 것은 장고 뷰의 역할을 명확히 이해했다는 것이다.
- 장고의 함수 기반 뷰는 HTTP 메서드에 중립적이지만, 클래스 기반 뷰의 경우 HTTP 메서드의 선언이 필요하다는 것을 설명해 준다.

## 8.8 locals()를 뷰 콘텍스트에 이용하지 말자
`locals()`를 호출형(callble)으로 반환하는 것은 안티 패턴이다. 시간을 단축하는 것 같지만 실제론 시간을 허비하게 된다.

```python
# 나쁜 예
def ice_cream_store_display(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    date = timezone.now()
    return render(request, 'melted_ice_cream_report.html', locals())
```

명시적이었던 디자인이 암시적 형태의 안티 패턴 형식이 됨으로쎠 유지보수가 복잡한 형태가 되었다. 특히 뷰가 어떤 걸 반환하려고 했는지 알 수가 없다. 뷰가 반환하는 변수들을 어떤 식으로 변환해야 할지 명확하지 않아 문제가 된다.

```python
# 나쁜 예
def ice_cream_store_display(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    now = timezone.now()
    return render(request, 'melted_ice_cream_report.html', locals())
```

단순한 예임에도 불구하고, 큰 템플릿을 가진 복잡한 코드라면 어떨까? 이런 이유로 뷰에서 명시적인 콘텐츠를 이용해야 한다.

```python
def ice_cream_store_display(request, store_id):
    return render(request, 'melted_ice_cream_report.html', dict{
        'store': get_object_or_404(Store, id=store_id,
        'now': timezone.now()
        })
```

## 8.9 요약
우선 함수 기반 뷰 또는 클래스 기반 뷰를 언제 이용해야하는지, 그에 따른 선호하는 패턴을 다루었다.  
그리고 URLConf에서 뷰 로직을 분리하는 기법을 다루었다. 뷰 코드는 앱의 views.py 모듈에, URLConf 코드는 앱의 urls.py 모듈에 소속되어야한다. 또한 클래스 기반 뷰를 이용할 때 객체 상속을 이용함으로써 코드를 재사용하기 쉬워지고 디자인을 좀 더 유연하게 할 수 있다.
