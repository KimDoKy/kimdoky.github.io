---
layout: post
section-type: post
title: django - Customizing the Django User Model
category: django
tags: [ 'django' ]
---

> [Options & Objects: Customizing the Django User Model](https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4)의 내용을 일부 번역하였습니다.

[Git repo](https://github.com/eleanorstrib/django-user-model-options)에 아래에서 다룰 3가지 옵션을 각각 간단히 구현해두었습니다.

모든 예제는 Django 1.11과 Python 3.5.2를 사용합니다.

## Django의 인증 기능을 사용하는 경우 모델을 Customizing하는 세 가지 옵션이 있습니다.

#### Option 1. Django의 AbstractBaseUser를 서브 클래싱하여 CustomUser Model을 만듭니다.
모델의 content에 많은 융통성(더 세세한 커스터마이징)이 필요하고 엑서스 방법과 프로젝트 시작시 약간의 작업이 필요하지 않은 경우 유용합니다.

#### Option 2. Django의 AbstractUser를 하위 클래스로 분류하여 기존 User Model을 자신의 필드로 확장합니다.
user model에 기본 필드를 유지하고 권한도 그대로 사용하지만, username을 다른 필드로 변경하거나 인증 필드를 추가하는 경우 유용합니다.

### Option 3. OneToOneField 메서드를 사용하여 기존 User 클래스에 필드를 추가합니다.
이 방법은 username 필드를 변경하려는 경우에는 도움이 되지 않지만, user model을 다른 모델에 연결하여 더 많은 데이터를 저장할 수 있습니다. daisy chains 방식으로 데이터베이스에 두 개의 모델을 연결합니다. 이는 인증과 관련이 없는 user 데이터를 저장하려는 경우나 user가 지정한 일부 서비스가 필요로하는 제 3의 서비스가 필요한 경우에 유용합니다.  

이 세 가지 중에서 대부분의 사용 사례는 옵션 1,2입니다. PyCon에서 Option1, 2는 관심이 있었지만 Option3을 사용했던 사람들은 소수였습니다. 이 경우 데이터베이스 스키마를 근본적으로 변경하기 때문에 데이터를 백업하고 모델과 데이터베이스를 다시 만드는 것이 유일한 방법입니다. 이 포스트는 DJango와 제 3자 인증 서비스 구현, 기존 모델 마이그레이션이나 사용자에게 email 보내기는 다루지 않습니다.

## Three Options, Step by Step

### Option 1.Subclassing AbstractBaseUser[repo](https://github.com/eleanorstrib/django-user-model-options/tree/master/user_models_abstractBaseUser)

이 옵션은 가장 어렵지만 가장 유연한 옵션입니다.(유연하다는 것은 더 세세하게 커스터마이징이 가능하다는 뜻)  

다음과 같은 경우 이 방법을 사용하세요.

- 모델에 대한 모든 것을 커스터마이징하길 원하는 경우
- 데이터 수집을 위한 필드 수를 최소화하고 상자에서 나온 것들(Django에 기본적으로 구현된 것?)을 사용하지 않는 경우
- Django의 권한 모델을 사용하는데 필요한 기본 권한을 작성하는데 시간을 할애하길 원하는 경우

포스트에서 다루는 첫 파트는 custom user model 자체를 작성하는 것입니다.

app 디렉터리에서 models.py에 다음 코드를 추가하세요.

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=6)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FILEDS = ['zip_code']
    USERNAME_FIELD = 'email'

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
```

- `USERNAME_FIELD`로 사용하는 모든 필드에 `unique=True` 매개 변수를 추가해야 합니다.
- `REQUIRED_FILEDS`는 user를 생성하는데 필수적인 필드 목록입니다. 여기에 `USERNAME_FIELD`를 포함하면 오류가 발생합니다. forms.py 파일에 `UserCreationForm`을 가져오고 서브 클래스화하여 양식을 만들기 때문에 `REQUIRED_FILEDS`에 `password`를 추가할 필요가 없습니다.

다음은 app 디렉터리 안에 admin.py 파일 다음을 추가하여 모델을 등록하세요.

```python
from django.contrib import admin
from app.models import CustomUser

admin.site.register('CustomUser')
```

다음 코드를 settings.py에 추가하여 CustomUser를 사용자 인증에 사용하도록 설정합니다.

```python
AUTH_USER_MODEL = 'app.CustomUser'
```

그런 다음 프로젝트 루트에서 데이터베이스를 마이그레이션 하세요.

큰 유연성은 설정에 많은 프로그래밍 오버 헤드가 발생합니다.  

localhost에서 이 앱을 실행하면, 표면상으로는 정상 동작하는 것처럼 보이지만 admin에 엑세스하거나 user를 추가할 수 없습니다. user manager를 통해 이 기능을 정의해야 하며, `CustomUserManager` 클래스가 제공됩니다.  

이 기능을 만들려면 `django.contrib.auth.models`에서 `BaseUserManager`를 가져온 다음 `CustomUserManager` 클래스를 만들때 상속받습니다. 최소한 `create_user`, `create_superuser`, `get_by_natural_key`에 대한 메소드를 정의하지 않으면 오류가 발생합니다. 보다 구체적인 사용 권한 그룹을 만들려면 여기에서 사용 권한 그룹을 정의해야 합니다.

```python
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, zip_code, password):
        user = self.model(email=email, zip_code=zip_code, password=password)
        user.set_password(password
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db
        return user

    def create_superuser(self, email, zip_code, password):
        user = self.create_user(email=email, zip_code=zip_code, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db
        return user

    def get_by_natural_key(self, email):
        print(email_)
        return self.get(email=email)
```

- `user.is_staff` : admin 사이트에 대한 엑세스를 제어합니다.
- `user.is_superuser` : True이면 user에게 사용할 수 있는 모든 권한을 줍니다.
- `user.save()` : 데이터베이스에 저장합니다.

`get_by_natural_key` 메소드는 ID 자격증명이 무엇이든간에, 실제 username이나 그 값을 바꿀 값으로 설정해야 합니다. 이 경우는 email입니다.

아직 완료되지 않았습니다. CustomUser를 약간 더 수정해야 합니다.  

`PermissionsMixin`를 임포트하였는데, 이걸로 최소한의 노력으로 Django의 권한 모듈로 작업하는데 필요한 메소드를 제공받을 수 있습니다.
`AbstractBaseUser`와 `BaseUserManager`보다 먼저 임포트하지 않으면 오류가 발생합니다. 그 후에 CustomUser 모델의 인수에 추가하세요.

```python
class CustomUser(AbstractBaseUser, PermissionsMixin):  # 추가
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=6)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FILEDS = ['zip_code']
    USERNAME_FIELD = 'email'

    objects = CustomAccountManager()  # 추가

    def get_short_name(self):
        return self.email

    def natural_key(self):
        return self.email

    def __str__(self):
        return self.email
```

Django는 각 user가 짧은 이름을 사용할 것을 기대하기 때문에 'get_short_name' 메소드도 추가해야 합니다.  

또한, email을 반환하는 natural_key 필드(위와 같이 사용자가 로그인해야하는 자격 증명)와 계정을 나타내는 문자열로 email을 반환하는 간단한 메서드를 추가했습니다.

마지막으로, `CustomAccountManager` object를 인스턴스화를 통해 `CustomAccountManager` 클래스를 만들 때 사용 권한 관리와 데이터 엑세스를 위해 작성한 method에 엑세스할 수 있습니다.  

모든 변경 작업을 수행 한 후에는 반드시 베이터베이스를 마이그레이션해야 합니다.

우리는 `first_name`, `last_name` 등과 같은 표준 Django User 필드를 많이 가지고 있지 않다는 것에 주의해야 합니다.


### Option 2. Subclassing AbstractUser[repo](https://github.com/eleanorstrib/django-user-model-options/tree/master/user_models_abstractUser)

이 옵션은 다음과 같은 경우에 유용합니다.

- Django User model의 기본 필드 사용
- 최소한의 오버 헤드로 username 변수를 제어
- custom user manager 작성을 건너뛰고 Django의 내장 된 메소드를 활용

하지만, 이 옵션은 username을 커스텀하는 것과 관련하여 몇 가지 제한이 있습니다.

첫 단계는 모델을 작성하는 것입니다.

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=6)

    USERNAME_FIELD = 'email'
    REQUIRED_FILEDS = ['zip_code']

    def __str__(self):
        return self.email
```

이번에는 `AbstractUser`를 상속받지만, `is_staff` 필드는 필요하지 않습니다. 왜냐하면 이미 이 속성을 가진 기본 User 모델에 효과적으로 추가하고 있기 때문입니다.  

`USERNAME_FIELD`는 username을 email로 재설정하므로 로그인할 때 필요합니다. 모델에는 이미 email 필드가 있지만 `unique=True` 매개 변수를 추가하려면 여기에 추가해야 합니다.

> 또 다른 중요한 메모. username field와 password가 필요하기 때문에 `REQUIRED_FILEDS`에 이동할 필요가 없습니다. 실제로 `USERNAME_FIELD`를 재설정하면 앱에서 오류가 발생합니다.  

`AUTH_USER_MODEL` 변수를 settings.py에 추가하여 이 프로젝트가 user를 알 수 있도록 하세요.

```python
AUTH_USER_MODEL = 'app.CustomUser'
```

모델을 프로젝트의 admin.py 파일에 등록하면 admin 화면에 모델이 표시됩니다.

```python
from django.contrib import admin
from app.models import CustomUser

admin.site.register(CustomUser)
```

이 시점에서 마이그레이션을 실행합니다.

그 후 superuser를 생성하여 테스트를 합니다. username으로 email을 사용하려고 하지만, 실제로 로그인 할 때 실제 username이 필요하지 않은 경우 문제가 발생합니다. `AbstractUser` 모델의 소스 코드에는 email, password, username이 필요합니다.

이것은 다음을 의미합니다.

- superuser를 만든 때 `REQUIRED_FILEDS`에 username을 추가하지 않으면 'TypeError: create_superuser() missing 1 required positional argument: ‘username’' 오류가 발생하는데, `USERNAME_FIELD = 'email'`로 설정했더라도 `AbstractUser` 모델에서 해당 인수를 기대합니다.

- 브라우저에서 username을 포함하지 않는 양식을 통해 user를 생성하려고 하면 다음과 같은 오류가 발생합니다 : `NOT NULL constraint failed: abstract_user_sample_customuser.username`

요구 사항에 따라 몇 가지 옵션이 있습니다.

1. 옵션1을 사용하고 custom model에 `AbstractBaseUser`를 상속받으세요. 더 많은 코드가 필요하지만 어떤 면에서는 더 깨끗합니다. 예를 들어, 응용 프로그램이 이해가 되지 않는 경우 username을 완전히 건너 뛸 수 있습니다.

2. 필드를 유지하면서 새 user를 만들 때 email 매개 변수를 필요로 하지 않으려면 email 매개 변수를 덮어 쓰는 방법을 models.py 파일에서 username 필드 매개 변수를 재정의하세요. 바로 사용할 수 있는 예로, helper text, error message 등은 지우지만 해당 필드를 비워 두거나 `null`로 설정할 수 있습니다.

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    zip_code = models.CharField(max_length=6
    username = model.CharField(blank=True, null=True, max_length=150)
    REQUIRED_FILEDS = ['zip_code', 'username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
```

`REQUIRED_FILEDS`에 username을 추가했으면 명령행에 superuser를 만들 때 표시되지만, forms.py 파일에 필드를 지정할 수 있으므로 최종 user가 username을 등록하면 완전히 삭제할 수 있으며 데이터베이스의 빈 username 필드에도 불구하고 프로세스를 완료할 수 있습니다.

테스트를 하기 전에 마이그레이션을 실행하세요.  

admin 패널에 로그인하고 새 user를 만들면 옵션 1과 달리 모델에 명시적으로 없는 기본 Django 필드와 우리가 추가한 `zip_code` 필드가 나옵니다. username이 나타나지만 필수는 아닙니다.

### Option 3. The OneToOneField [repo](https://github.com/eleanorstrib/django-user-model-options/tree/master/user_models_oneToOne)

이 옵션은 email을 암호로 사인하는 기존의 사용 사례와 실제로 일치하진 않지만 인증과 직접적으로 관련이 없는 user 데이터를 저장하는 경우 많은 의미를 갖습니다. 이건 여전히 user model에 연결되어 있습니다.  

구현하기 매우 간단합니다. 앱의 models.py에 User 모델을 임포트하고 `OneToOneField` 메소드가 있는 모델에 연결 합니다.

```python
from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username
```

이 경우, Django User 모델을 사용하기 때문에 settings.py에 아무 것도 추가할 필요가 없지만, admin.py에 모델은 등록해야 합니다.  

`User`모델과 `CustomUser`모델이 연결된 방식은 Admin에서 매우 명확합니다. Admin을 보면 `User`와 `CustomUser`가 별도로 나열되어 있음을 알 수 있습니다.

![]({{ site.url }}/img/post/django/other/custom_1.png)

user를 만들때는 평소와 같지만 custom user를 추가하려면 관지자가 custom user 모델을 연결할 레코드의 username을 묻는 메시지를 표시하고 추가한 `zip_code` 필드를 표시합니다.

![]({{ site.url }}/img/post/django/other/custom_2.png)
