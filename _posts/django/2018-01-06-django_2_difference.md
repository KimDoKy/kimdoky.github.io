---
layout: post
section-type: post
title: Django 2.0으로 넘어오면서 바뀐 점
category: django
tags: [ 'django' ]
---

## Django 2.0 으로 넘어가면서 바뀐점


### 1. urlpatterns

`urlpatterns`에서 `url`대신 `path`를 사용 (`url`도 사용 가능하지만 `path` 가 너무 편리하여 `path` 사용을 추천)  
`path`를 사용하면 정규식을 사용하지 않아도 됩니다.

```django
 urlpatterns = [
    # 기존
    url(r'^blog/', include('....')),
    # 2.0
    path('blog/', include('...')),
```

인자를 넘겨줄때도 정규식이 필요 없어졌습니다.


```django
 urlpatterns = [
    # 기존
    url(r'^blog/', include('....')),
    url(r'^(?P<id>\d+)/$', views....),
    # 2.0
    path('blog/', include('...')),
    path('<id>/', views...),
```

url을 구현할때 더 이상 정규식에 머리 아파할 필요가 없어졌습니다.

### 2. related
related를 구현할때 필수 인자로 `on_delete`가 추가 되었습니다.  
기존에는 필수 인자는 아니었고, 미리 선언하거나, 모델에서 필수 필드를 추가하고 `makemigratinos`시 지정해주었었는데, 2.0에서는 처음 필수 필드를 선언시 `on_delete`를 지정하지 않으면 에러가 발생합니다.

```django
class User(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

### 3. core의 url경로 변경
`get_absolute_url()`를 사용하려면 `django.core.urlresolvers import reverse` 경로를 통하여 `reverse`를 임포트 하였지만, 경로가 `from django.urls import reverse`으로 수정되었습니다. **[django docu](https://github.com/django/django/blob/2.0/django/urls/base.py)**

```django
def get_absolute_url(self):
    from django.urls import reverse
    return reverse('people.views.details', args=[str(self.id)])

# 사용시
revered_url = resolve_url(post)
# resolve_url은 아래 코드처럼 get_absolute_url()라는 이름의 함수를 찾아서 반환합니다.
```

> `get_absolute_url()`을 사용하면 detail 주소를 쉽게 생성할 수 있습니다.

```
def resolve_url(to, *args, **kwargs):
    ...
    if hasattr(to, 'get_absolute_url'):
        return to.get_absolute_url()
    ...
    try:
        return reverse(to, args=args, kwargs=kwargs)
    ...
```

- [`get_absolute_url()` 코드 참고](https://docs.djangoproject.com/ko/2.0/_modules/django/shortcuts/)
