---
layout: post
section-type: post
title: django - username에 verbose_name 적용하기
category: django
tags: [ 'django' ]
---

`verbose_name`은 Django 모델을 admin 페이지에서 조회할 때, 필드명 대신 알아보기 쉬운 단어로 지정하는 것이다.

일단적으로 사용법은 아래와 같다.

```python
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20, verbose_name='이름')
```

Custom 모델을 구현할때 `AbstractUser`을 상속받으면, 기본적인 것은 Django가 구현해주고, 추가적인 필드들을 추가할 수 있다.

`username`와 같은 Django가 기본적으로 구현해 주는 필드에 적용하려면, `AbstractBaseUser`을 상속하고 `USERNAME_FIELD`로 해당 필드를 지정해주어야 한다.

```python
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    custom_username = models.CharField(max_length=20, verbose_name='이름')
    USERNAME_FIELD = 'custom_username'
```

위처럼 구현하게 되면 migrate는 정상적으로 진행된다. 하지만 user나 superuser를 생성하려하
`AttributeError: 'Manager' object has no attribute 'get_by_natural_key'` 에러가 발생한다.

해당 모델의 커스텀 매니저를 구현하고, `objects`에 커스텀 매니저를 지정해주면 된다.

```python
from django.contrib.auth.models import UserManager

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractBaseUser):
    objects = CustomUserManager()
    ...
```

이제 superuser를 생성해보자!

```
TypeError: create_superuser() missing 2 required positional arguments: 'username' and 'email'
```

마지막으로 create_user, create_superuser 메서드도 재정의해주면 됩니다.

재정의 방법은 [Django Docs](https://docs.djangoproject.com/ko/2.1/topics/auth/customizing/)으로 대신합니다. 씨익.
