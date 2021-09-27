---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap9. Best Practices for Function-Based Views
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

## 9.1 Advantages of FBVs

함수적인(functional) 특징이 장점입니다.

- 뷰 코드는 작을수록 좋다.
- 뷰에서 절대 코드를 반복해서 사용하지 말자.
- 뷰는 프레젠테이션 로직을 처리해야 한다. 비즈니스 로직은 가능한 한 모델 로직에 적용시키고 만약 해야 한다면 폼 안에 내재시켜야 한다.
- 뷰를 가능한 한 단순하게 유지하자.
- 403, 404, 500을 처리하는 커스텀 코드를 쓰는데 이용하라.
- 복잡하게 중첩된 if 블록 구문을 피하자

## 9.2 Passing the HttpRequest Object

middleware나 context processors 같은 글로벌 액션에 연동되지 않은 경우 재사용에 문제가 있습니다.  
프로젝트 전체를 아우르는 유틸리니 팜수를 만들어 사용하는 것을 추천합니다.  

`django.http.HttpRequest` 객체를 요청 함수의 primary argument로 넣음으로써 인자 구성이 단순하게 됩니다.  

```python
from django.core.exceptions import PermissionDenied 
from django.http import HttpRequest

def check_sprinkle_rights(request: HttpRequest) -> HttpRequest: 
    if request.user.can_sprinkle or request.user.is_staff:
        return request

    # Return a HTTP 403 back to the user
    raise PermissionDenied
```

파이썬 언어는 동적 타입 언어이기 때문에 임의의 값이 아닌 HttpRequest 객체를 반환합니다.  

실제 코드에 적용하면 아래와 같습니다.

```python

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Sprinkle
from .utils import check_sprinkles

def sprinkle_list(request: HttpRequest) -> HttpResponse:
    """Standard list view"""
    request = check_sprinkles(request)
    return render(request, 
        "sprinkles/sprinkle_list.html", 
        {"sprinkles": Sprinkle.objects.all()})

def sprinkle_detail(request: HttpRequest, pk: int) -> HttpResponse: 
    """Standard detail view"""
    request = check_sprinkles(request)
    sprinkle = get_object_or_404(Sprinkle, pk=pk)
    return render(request,
        "sprinkles/sprinkle_detail.html", 
        {"sprinkle": sprinkle})

def sprinkle_preview(request: HttpRequest) -> HttpResponse: 
    """
    Preview of new sprinkle, but without the
    check_sprinkles function being used.
    """
    sprinkle = Sprinkle.objects.all() 
    return render(request,
        "sprinkles/sprinkle_preview.html",
        {"sprinkle": sprinkle})
```

CBV으로 통합하기도 쉽습니다.

```python
from django.views.generic import DetailView
from .models import Sprinkle
from .utils import check_sprinkles

class SprinkleDetail(DetailView):
    """Standard detail view"""
    model = Sprinkle

    def dispatch(self, request, *args, **kwargs):
        request = check_sprinkles(request)
        return super().dispatch(request, *args, **kwargs)
```

## 9.3 Decrators Are Sweet

함수의 단순 명료함이라는 장점과 데코레이터의 간편 표기법(syntactic sugar)을 섞으면, 언제든 사용 가능하고, 재사용이 가능한 매우 강력한 도구가 됩니다.

```python
import functools

def decorator(view_func):
    @functools.wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        # You can modify the request (HttpRequest) object here.
        response = view_func(request, *args, **kwargs)
        # You can modify the response (HttpResponse) object here. 
        return response
    return new_view_func
```

아래처럼 활용할 수 있습니다.

```python
from django.shortcuts import get_object_or_404, render
from .decorators import check_sprinkles
from .models import Sprinkle

@check_sprinkles
def sprinkle_detail(request: HttpRequest, pk: int) -> HttpResponse: 
    """Standard detail view"""
    sprinkle = get_object_or_404(Sprinkle, pk=pk)
    return render(request, "sprinkles/sprinkle_detail.html",
        {"sprinkle": sprinkle})
```

### 9.3.1 Be Conservative With Decorators

편하다고 남용하면 오히려 데코레이터 자체를 난해하게 되고, 복잡하게 얽힌 상속 과정을 지닌 뷰보다 복잡해질 수도 있습니다.  
데코레이터가 뷰에 이용될 것인지 정하고, 정해진 수만큼만 사용하세요.

[파이콘의 해당 주제](https://pyvideo.org/pycon-us-2011/pycon-2011--how-to-write-obfuscated-python.html)

> 데코레이터는 여러 곳에 쉽게 추가 할 수 있는 것이 장점이기 때문에, 남용한다는 것은 많이 사용한다는 것이 아니라, 데코레이터의 상속의 깊이와 관련된 문제이다. 

### 9.3.2 Additional Resources on Decorators

- [데코레이터 치트 시트](https://daniel.feldroy.com/posts/python-decorator-cheatsheet)

## 9.4 Passing the HttpResponse Object

HttpRequest와 마찬가지로, HttpResponse 객체도 함수와 함수 사이에서 주고 받을 수 있습니다.  
이 기능은 데코레이터와 같은 곳에서 큰 효과를 볼 수 있습니다.

## 9.5 Additional Resources for Function-Based Views

[spookylukey](https://spookylukey.github.io/django-views-the-right-way/)

여기에 언급돤 CBV의 단점을 동의하지 않지만, FBV에게는 참고할 만한 글입니다.
