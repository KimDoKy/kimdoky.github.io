---
layout: post
section-type: post
title: TemplateView / urls.py에서 템플릿 지정하기
category: django
tags: [ 'django' ]
---

때로는 urls.py에서 view를 지정하지 않고 template을 바로 지정해야 할 경우가 있다.

이때 사용하는 것이 `TemplateView`이다.

### 사용법

```python
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('foo/', TemplateView.as_view(template_name='foo.html'))
]
```
