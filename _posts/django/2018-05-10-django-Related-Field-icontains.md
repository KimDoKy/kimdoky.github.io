---
layout: post
section-type: post
title: Django - Related Field has invalid lookup - contains
category: django
tags: [ 'django' ]
---

django template에서 model을 검색하는 search form을 만들때

model의 field를 contains를 이용해서 지정하게 된다.

```python
q = request.GET.get('q')
if q:
    qs = qs.filter(order__icontains=q)
```

멀티 search form을 구현하려면 아래와 같이 `Q`를 이용하면 된다.

```python
from django.db.models import Q

...

    qs = qs.filter(
        Q(order__icontains=q)|
        Q(order_date__icontains=q)|
        ....)
```

하지만 field가 ForeignKey로 다른 모델과 관계를 맺고 있다면 `Login  Register

Related Field has invalid lookup: icontains` 라는 에러메시지를 만나게 된다.
> 해당 오류는 대부분 어드민에서 많이 접하고는 한다.

에러의 이유는 관계를 맺고 있는 필드는 다른 모델이고,
그 해당 모델에도 여러 필드들이 있기 때문에
관계된 모델의 어떤 필드인지를 지정하지 않았기 때문에 발생한다.

해결법은 당연히 관계 모델의 필드를 지정해주면 된다.

```python
   # field__model's field__icontains=q
   order__icontains=q
```

> related name은 상관없다.

#### 주의점
더블언더바(`__`)는 꼭 지켜줘야 한다. 의외로 이거 때문에 오류나는 경우가 많다.
