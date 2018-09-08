---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 9 - Model creation, OneToOne relations, signals and the Django Admin
category: django
tags: [ 'django' ]
---

# [Model creation, OneToOne relations, signals and the Django Admin](http://www.marinamele.com/taskbuster-django-tutorial/model-creation-onetoone-relationship-signals-django-admin)

이번 파트에서는 TaskBuster 프로젝트의 메인 앱 모델인 TaskManager app을 작성합니다.

먼저 UML 다이어그램을 통해 이 앱의 모델 구조를 보고 이해할 것입니다. 이 유형의 다이어그램을 정의하는 것은 문서화 역할을 할 뿐만 아니라 모델을 어떻게 동작 시킬지에 대한 명확한 구조를 갖는데 도움이 됩니다.

다음으로 `OneToOne` 관계를 통해 User 모델과 관련있는 첫 번째 모델을 만듭니다. 또한 signals, 모델의 Custom attribute, Django Admin 인터페이스, 테스트에 대해서도 다룹니다.

이번 파트의 개요는 다음과 같습니다.

 - UML Diagram of the TaskManager app
 - Create the TaskManager app
 - Profile Model: OneToOne relationship with the User Model
 - Django Signals: create a Profile instance when a new user is created
 - The Django Admin for the Profile Model

## UML Diagram of the TaskManager app
앱을 만들 때 데이터베이스와 모델을 명확하게 구조화하는 것이 중요합니다. 모델을 보여 주거나 개발하는 한 가지 방법은 [UML 다이어그램](http://www.uml.org/)(Unified Modeling Language)을 사용하는 것입니다.

우리가 수행해야 할 다이어그램입니다.

![]({{ site.url }}/img/post/django/TB/uml.png)

작업을 관리하기 위해 4가지 모델을 정의 할 것입니다.

1. Profile Model:
이 모델은 앱의 최상위 모델이 될 것입니다. 각 사용자는 자체 프로필 인스턴스를 가지며 모든 프로젝트, 태그, 작업이 어떻든 이 프로필에 연결됩니다.

속성은 다음와 같습니다.

- **OneToOne relationship** Django Cuctom Model. 각 사용자가 자신의 프로필 인스턴스를 원하기 때문에 Django signals를 사용할 때마다 프로필 인스턴스를 생성합니다.
- 앱과 사용자의 상호 작용의 카운터와 속성입니다. 사용자가 작업을 완료 할 때마다 이 매개 변수는 1씩 증가합니다.

2. , 3. Project, Tag Model:
이 두 모델은 작업을 구성하는 두 가지 다른 방법을 나타냅니다. 둘 다 name 속성을 갖고 프로젝트 모델에도 색상 속성(16진수 문자열)이 있습니다.

4. Task Model
우리 앱의 주요 모델입니다. 속성은 다음과 같습니다.

 - name
 - priority(이 작업이 긴급, 중요인지를 나타내는 문자열)
 - completed(boolean)
 - due date(optional)
 - completed_date(optional)

그리고 다른 모델과의 관계는 다음과 같습니다.

 - 프로젝트 모델에 대한 **ForeignKey relationship**: 각 작업은 프로젝트 인스턴스와 관련이 있으며 각 프로젝트는 둘 이상의 작업을 가질 수 있습니다.
 - 태그 모델에 대한 **ManyToMany relationship**: 각 작업은 0개나 하나 이상의 태그 인스턴스와 관련 될 수 있으며 각 태그틑 0개, 하나 이상의 작업과 관련 될 수 있습니다.
 - ForeignKey 관계가 있더라도 Task Model과의 자체 관계 각 테스크는 여러 테스크와 관련될 수 있습니다. 관계의 방향에 따라 관련 task는 하위 task 또는 상위 task입니다.

## Create the TaskManager app

보통 프로젝트에는 여러 개의 app이 있으며 각 app은 특정 기능을 제공합니다. 깨끗한 구조로 프로젝트를 유지하려면 이러한 모든 app을 apps이라는 공용 폴더에 넣을 수 있습니다.

터미널을 열고 프로젝트의 최상위 폴더(manage.py 레벨)로 이동하여 apps라는 폴더를 만들고 패키지화 합니다.

```
$ mkdir taskbuster/apps
$ touch taskbuster/apps/__init__.py
```

다음으로 taskmanager라고 하는 앱을 만듭니다.

```
$ cd taskbuster/apps
$ python ../../manage.py startapp taskmanager
```

해당 앱에는 다음의 파일들이 있습니다.

 - __init__.py 는 이 폴더가 파이썬 패키지임을 나타냅니다.
 - admin.py는 Django admin을 정의하는데 사용합니다.
 - models.py는 모델을 정의하는 곳입니다.
 - tests.py는 테스트를 저장합니다.
 - views.py는 view가 저장되는 곳입니다.
 - migration은 데이터베이스 마이그레이션이 포함 된 폴더입니다.

 또한 이 폴더 내에 다음 파일을 생성합니다.

```
 $ touch urls.py managers.py
```

마지막으로 settings/base.py 파일에 앱을 추가하세요.

```
INSTALLED_APPS = (
    ...
    # TaskBuster apps
    'taskbuster.apps.taskmanager',
    ...
)
```

이제 models.py에 모델을 만들 준비가 되었습니다. 각 모델에 대해 속성과 메소드를 다음 순서로 정의하는 것이 좋습니다.

```python
class MyModel(models.Model):
    # 관계
    # 속성 - 필수
    # 속성 - 옵션
    # Object Manager
    # 사용자 지정 속성
    # Methods
    # Meta and String
```

이 방법은 다른 속성과 메서드의 가독성을 높여줍니다.

## Profile Model: OneToOne relationship with the User Model

먼저 프로필 모델을 작성합니다. 앞에서 언급했듯이 이 모델은 앱의 최상위 모델이 될 것입니다. 특정 사용자와 관련이 있으며 모든 작업, 태그, 프로젝트가 어떻든간에 이 프로필과 관계가 있습니다.

![]({{ site.url }}/img/post/django/TB/profile.png)

따라서 다음을 정의해야 합니다.

 - User Model과 One To One 관계(각 사용자에 대해 하나의 프로필만 가능)
 - interaction은 사용자 상호작용을 설명하는데 사용할 정수 속성입니다. 사용자가 작업을 완료할 때마다 이 값이 증가합니다.

models.py를 작성합니다.

```python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from . import managers


class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        verbose_name=_("user"),
        on_delete=models.CASCADE
        )
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
        )
    # Attributes - Optional
    # Object Manager
    objects = managers.ProfileManager()

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    # Methods

    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)

    def __str__(self):
        return self.user.username
```

그리고 managers.py에 단순한 ProfileManager를 정의합세요.

```python
# -*- coding: utf-8 -*-
from django.db import models


class ProfileManager(models.Manager):
    pass
```

이 코드를 살펴봅시다.

 - 프로필 모델은 사용자 모델과 일대일 관계를 유지합니다.
  - 사용자 모델은 settings.py에서 `AUTH_USER_MODEL`을 사용하여 가져옵니다. 이는 Custom User Model을 정의하기를 원하기 때문에 프로필은 Django 빌드인 모델 대신 Custom User Model과 일대일 관계를 가져야 합니다.
  - `related_name`은 사용자 모델에서 프로필 인스턴스에 액세스하는 방법을 정의할 때 사용합니다. 예를 들어, myuser가 User 인스턴스인 경우 `myprofile = myuser.profile`를 사용하여 해당 프로필에 액세스할 수 있습니다. 그러나 일대일 관계의 경우 Django는 기본적으로 액세스키(소문자로 된 클래스 이름)를 사용합니다. 하지만 이름을 약간 변경하기 때문에 코드에 명시적으로 작성합니다.
  - `verbose_name`은 쉬운 이름으로 정의할 때 사용합니다. 이 이름은 `ugettext_lazy`함로 감싸고 있습니다. 이 함수는 변환이 가능한 경우 문자열을 변환하는데 사용합니다.([파트5](https://kimdoky.github.io/django/2018/08/30/django-taskbuster-5.html)에서 ugettext_lazy 함수를 다루었습니다.)

 - `interaction` 속성은 기본적으로 0 값을 갖는 양의 정수입니다.
 - object manager는 쿼리를 만들때 사용합니다. MyModel.objects.filter 같은 것들이 친숙하죠? Custom object manager를 정의하면 `MyModel.objects.get_by_start_date()`와 같은 쿼리를 만드는 Custom 기능을 정의할 수 있습니다.
  - 지금까지 ProfileManager는 Manager Django 클래스의 기본 기능만 상속받은 단순한 object manager입니다.(따라서 object manager의 모든 기본 쿼리를 수행할 수 있습니다.)
  - 걱정하지 마세교. 관리자 기능을 확장하여 사용하는 방법을 이해하게 될 것입니다.

 - `username`은 이 모델의 Custom 속성입니다. 즉, profile.username을 사용하여 이 속성을 액세스 할 수 있지만, 데이터베이스 테이블에 row를 생성하지 않습니다.(model 속성이 다름)
  - profile.user.username을 쓰는 대신 사용자가 쉽게 액세스할 수 있도록 username을 정의했습니다.
  - Custom 속성이 데이터베이스를 건드리지 않으므로 코드를 마이그레이션하지 않고도 정의하거나 변경할 수 있습니다.
 - `Meta` 클래스는 모델의 다른 행동을 정의하는데 사용합니다.
  - `verbose_name`과 `verbose_name_plural`은 사용자에게 친숙한 모델 이름입니다.
  - `ordering`은 쿼리 결과의 정렬 순서를 정의합니다. `order_by`를 사용하여 다른 순서를 지정하면 뒤에 정의한 코드로 정렬합니다.

  굿! 모델을 정의햇으므로 이러한 변경 사항을 데이터베이스에 마이그레이션하여 적용합니다.

```
$ python manage.py check
$ python manage.py makemigrations taskmanager
$ python manage.py migrate taskmanager
```

아직 테스트를 못하고 있지만, 그게 다음에 할 일입니다.

## Django Signals: create a Profile instance when a new user is created

앞서 언급했든이 각 사용자는 프로필 인스턴스를 갖게 됩니다. 새로운 사용자가 앱에 등록 할 때마다 프로필 작성을 어떻게 처리할까요?

간단합니다. **Django signals** 를 사용하여 새 사용자가 등록되면 새 프로필 인스턴스를 만드는 함수를 트리거합니다.

하지만 진행하기 전에 이 동작에 대한 테스트를 작성하겠습니다.
'taskbuster/apps/taskmanager/tests.py' 파일에 작성합니다.

```python
# -*- coding: utf-8 -*-
from django.test import TestCase

from django.contrib.auth import get_user_model
from . import models


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.profile, models.Profile)
```

`get_user_model` 함수를 사용하여 사용자 모델을 얻습니다. 다시 말하지만, 때로는 Custom 사용자 모델을 정의하기도 하고, 이 함수는 존재하는 경우 Custom  사용자 모델을 리턴하고 그렇지 않으면 Django default를 리턴합니다.

이 테스트는 다음과 같이 실행하세요.

```
$ python manage.py test taskbuster.apps.taskmanager
```

그럼 다름의 오류가 발생합니다.

```
django.db.models.fields.related.RelatedObjectDoesNotExist: User has no profile.
# Django 버전에 따라 조금 다를 수 있습니다.
django.contrib.auth.models.User.profile.RelatedObjectDoesNotExist: User has no profile.
```

예상대로 새 사용자가 등록되면 프로필이 작성되지 않습니다.

이를 해결하기 위해 **Django signals** 를 정의할 것입니다. 프로필 모델의 정의 바로 아래에 다음을 작성하세요.

```python
from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
```

Note: Django 앱의 시작 부분에서 신호를 읽는 것이 매우 중요합니다. 그렇기 때문에 같은 models.py에 두는 이유입니다. 신호가 많고 별도의 파일에 배치하려는 경우 models.py 파일의 특정 지점에 해당 파일(모든 신호)를 가져옵니다.

그래서 우리는 사용자 모델에 대한 신호를 정의했습니다. 이 신호는 사용자 인스턴스가 저장될 때마다 트리거가 됩니다.

`create_profile_for_new_user`에서 사용되는 인수는 다음과 같습니다.

 - `sender` : 사용자 모델 클래스
 - `created` : 새로운 User가 생성되었는지 나타내는 bool
 - `instance` : 저장 중인 사용자 인스턴스

Note: 이 인수는 작성중인 특정 신호에 따라 다를 수 있습니다. 이 경우에는 `post_save` 신호를 처리한다는 걸 기억하세요. 신호와 인수에 대한 더 자세한 정보는 [공식 문서](https://docs.djangoproject.com/en/1.8/ref/signals/)를 확인하세요.

이제 신호가 무엇인지 이해할 준비가 되었습니다. 사용자 모델의 새 인스턴스가 만들어졋는지 확인하고, true이면 새 사용자 인스턴스를 사용해 프로필 인스턴스를 만듭니다.

테스트를 다시 실행해 봅시다.

```
$ python manage.py test taskbuster.apps.taskmanager
```

잘 작동합니다!!

 Note: **Signals를 남용하지 마세요!** 코드가 모델의 동작을 제어하고 수정하는 신호로 가득하다면 코드를 읽는 사람이 이해할 수 없으며(스스로 관리해야 하니까!) 가능한한 Custom save method를 사용하세요.

## The Django Admin for the Profile Model

마지막으로 Admin 인스턴스를 관리할 수 있도록 manager를 구성할 것입니다.

taskmanager app에서 admin.py 파일을 수정하세요.

```python
# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ("username", "interaction")

    search_fields = ["user__username"]
```

그 다음 <http://127.0.0.1:8000/en/admin>에서 관리자를 열고 프로필 모델에 대한 링크를 볼 수 있습니다.

해당 링크를 클릭하면 아래 이미지처럼 표시됩니다. 목록이 비어 있지 않도록 프로필 인스턴스를 직접 하나 만들어보세요.

![]({{ site.url }}/img/post/django/TB/admin_profile.png)

이것이 admin.py 파일에서 우리가 한 일입니다.

 - 먼저 ProfileAdmin을 ModelAdmin 인스턴스로 정의하세요.
 - admin.register의 데코레이터는 프로필 모델의 ModelAdmin으로 ProfileAdmin을 등록합니다.(여기서 manager 인스턴스르 관리하려는 Model에 연결합니다.)
 - `list_display`는 우리가 프로필 인스턴스를 나열할 때 표시되는 필드를 정의할 수 있습니다.
  - 사용자 이름에 대한 사용자 정의 속성을 정의할 때 `user__username` 대신 `username`을 사용할 수 있습니다.
 - `search_fields`는 검색 박스를 만듭니다. 지정한 필드 리스트는 검색할 필드를 나타냅니다.
  - 검색 필드의 경우 일반 모델 속성을 사용해야하므로 단순히 `username` 대신 `user__username`을 작성해야 합니다.

다음 파트에서는 프로필 모델과 외래키 관계를 갖는 프로젝트 모델을 정의할 것입니다.
