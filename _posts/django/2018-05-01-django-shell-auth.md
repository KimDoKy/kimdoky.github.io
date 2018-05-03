---
layout: post
section-type: post
title: Django - shell에서 login하기
category: django
tags: [ 'django' ]
---

장고에서 작업 진행 내용을 확인하려면 로그인을 해야하는 경우들이 필수적으로 발생한다.


```python
>>> from django.contrib.auth import authenticate
>>> user = authenticate(username='id', password='password')
>>> user.username
```

제대로 로그인이 된다면 해당 username을 반환하고, 로그인 정보가 틀렸다면 속성 오류(None)을 반환합니다.
