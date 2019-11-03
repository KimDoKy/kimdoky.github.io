---
layout: post
section-type: post
title: django - Django Admin 계정 자동 생성
category: django
tags: [ 'django' ]
---

django로 개발시 DB를 반복적으로 지우고 생성하는 작업을 하게 되는데,
그때마다 관리자 계정을 만들어 주어야 한다.  

하지만, 같은 일을 반복한다는 것은 자동화를 할 수 있다는것!!

### path

```
proj/app/management/commands/[지정할 명령어].py
```

### script

```python
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser(
            username='admin',
            email='',
            password='autoadmin',
        )
```
