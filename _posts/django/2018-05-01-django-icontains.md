---
layout: post
section-type: post
title: Django - contains and icontains
category: django
tags: [ 'django' ]
---

[django doc](https://docs.djangoproject.com/en/2.0/ref/models/querysets/#contains)

장고 문서에 따르면 `contains`는 대소문자를 구분하고 `icontains`는 대소문자를 구별하지 않는다고 한다.

```python
if q:
    qs = qs.filter(title__contains=q)
```

하지만 테스트 서버에서는 제대로 대소문자 구별이 제대로 적용이 안되었다. SQLite는 대소문자를 구별하는 LIKE 문을 지원하지 않기 때문이다.
