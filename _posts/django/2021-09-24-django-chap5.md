---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap5. Settings and Requirements Files
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

### 최선의 장고 설정 방법

- 버전 컨트롤 시스템으로 모든 설정 파일을 관리해야 한다.(특히 운영환경)
- 반복되는 설정들을 없애야 한다.
- 암호나 비밀키 등은 안전하게 보관해야 한다.

## 5.1 Avoid Non-Versioned Local Settings

운영 환경 외에도 개발자를 위한 로컬 환경이 존재합니다.  
당연히 두 환경은 셋팅이 다릅니다.(ex. `SECRET_KEY`, ..etc)  

일반적으로 `local_settings.py`라는 모듈을 생성하고 해당 파일을 버전 컨트롤에서 제외하는 방법이 있습니다. 해당 방법으로 스테이징 서버와 개발 서버에서는 버전 컨트롤 관리 없이도 세팅과 로직을 유지할 수 있습니다.  
하지만 이 방법은 단점들이 있습니다.

- 모든 머신에 버전 컨트롤에 기록되지 않는 코드가 존재하게 된다.
- 운영 환경의 문제점을 로컬 환경에서 구현해보기 위해 많은 시간을 허비한 후에야 문제의 원인이 오직 운영 환경에서만 일어나는 사실을 발견하게 된다.
- 로컬 환경의 버그를 수정 후 운영 환경에 푸시하면, 해당 버그는 로컬 환경(`local_settings.py`)에 의한 것임을 알아챌 때가 생긴다.
- 여러 팀원이 `local_settings.py`를 복사해서 쓰면 반복하지 말라는 규칙을 위반하는 것이다.

그래서 개발 환경, 스테이징 환경, 테스트 환경, 운영 환경 설정을 공통되는 객체로부터 상속받아 구성된 서로 다른 세팅 파일을 나누어 버전 컨트롤로 관리하는 방법을 사용합니다.

## 5.2 Using Multiple Settings Files

한개의 settings.py 파일을 다음과 같이 환경별로 구성합니다.

```bash
settings/
   ├── __init__.py
   ├── base.py       # 공통 세팅 파일
   ├── local.py      # 로컬 환경(개발 전용 로컬)
   ├── staging.py    # 스테이징서버
   ├── test.py       # 테스트를 위한 세팅
   ├── production.py # 운영 서버
   # 지속적 통합 서버에서 쓰이는 ci.py 가 필요할 수도 있음
```

### 각 환경별 실행 방법

```bash
# 로컬 환경 쉘 실행
$ python3 manage.py shell --settings=twoscoops.settings.local

# 로컬 환경 개발 서버 실행
$ python3 manage.py runserver --settings=twoscoops.settings.local
```

`--settings`의 인자로 실행하려는 환경 설정 파일을 지정하면 됩니다.

### 5.2.1 A Development Settings Example

```python
# settings/local.py

from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'twoscoops',
        'HOST': 'localhost',
    }
}

INSTALLED_APPS += ['debug_toolbar', ]
```

이 파일로 인해 개발자들은 같은 개발 세팅 파일을 공유하게 됩니다.  
각 환경별 `if DEBUG`와 같은 코드를 사용하지 않아도 된다는 장점도 있습니다.

### 5.2.2 Multiple Development Settings

큰 프로젝트의 경우 개발자마다 자기만의 환경이 필요한 경우가 잇습니다.
이런 경우 개발자별로 세팅 파일을 추가 할 수 있습니다.

```
settings/
    __init__.py
    base.py
    local_audreyr.py <-
    local_pydanny.py <-
    local.py
    staging.py
    test.py
    production.py
```

## 5.3 Separate Configuration From Code

코드에서 설정을 분리해야 하는 이유들은 다음과 같습니다.

- 설정은 배포 환경에 따라 다르지만 코드는 그렇지 않다.
- 비밀 키들은 설정값들이지, 코드가 아니다.
- 비밀값들은 반드시 남이 알 수 없어야 한다. 이를 버전 컨트롤 시스템에 추가하면 코드 저장소에 접근할 수 있는 누구에게나 공개된다.
- PaaS 환경에서는 각각의 독립된 서버에서 코드를 수정하도록 허용하지 않고있다. 가능하다 할지라도 독립된 서버에서 직접 코드를 수정하는 것은 매우 위험한 방법이다.

이를 해결하기 위해 **환경 변수**를 이용하면 됩니다. 이 방법의 장점은 다음과 같습니다.

- 환경 변수를 이용하여 비밀 키를 보관함으로써 걱정 없이 세팅 파일을 버전 컨트롤 시스템에 추가할 수 있다.
- 버전 컨트롤로 관리되는 단일한 settings/local.py를 나눠 쓸 수 있다.
- 코드 수정 없이 시스템 관리자들이 프로젝트 코드를 쉽게 배치할 수 있다.
- 대부분 PaaS가 설정을 환경 변수를 통해 이용하기를 추천하고 있고, 이를 워ㅣ한 기능들이 내장되어 있다.

### 5.3.1 A Caution Before Using Environmant Variable for Secrets

- 저장되는 비밀 전보를 관리할 방법
- 서버에서 bash가 환경 변수와 작용하는 방식에 대한 이해나 PaaS 이용 여부

### 5.3.2 How to Set Environment Variables Locally

`bashrc`, `.bash_profile`, `.profile`에 다음 구문을 추가합니다.

```bash
export SOME_SECRET_KEY=1c3-cr3am-15-yummy
export AUDREY_FREEZER_KEY=y34h-r1ght-d0nt-t0uch-my-1c3-cr34m
```

### 5.3.3 How to Unset Environment Variables Locally

virtualenv를 비활성화하더라도 환경 변수는 그대로 유지됩니다.
환경 변수를 해지하는 방법입니다.

```bash
unset SOME_SECRET_KEY
unset AUDREY_FREEZER_KEY
```

### 5.3.4 How to Set Environment Variables in Production

파이썬에서 환경 변수 접근하는 방법

```python
# Top of settings/production.py
import os
SOME_SECRET_KEY = os.environ['SOME_SECRET_KEY']
```

### 5.3.5 Handling Missing Secret Key Exceptions

환경 변수를 사용할 수 없는 경우, KeyError로 인해 프로젝트를 시작할 수 없을 것입니다.
하지만 KeyError가 문제의 원인을 알려주는 것은 아니기에 디버그가 어렵습니다.  
이런 경우 settings/base.py에 아래와 같은 예외 처리를 해주면 됩니다.

```python
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name] 
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)
```

> ImproperlyConfigured는 장고에서 바르게 설정되지 못한 프로젝트에 대해서 발생시키는 예외처리이다. 에러 메세지에 문제가 되는 세팅 이름을 추가로 나타낼 수 있다.

## 5.4 When You Can't Use Environment Variables

환경 변수를 사용할 수 없는 환경이라면 **비밀 파일 패턴**(secrets file pattern)을 이용할 수 있습니다.

1. JSON, Config, YAML or XML 중 한 가지 포맷을 선택하여 비밀 파일을 생성한다.
2. 비밀 파일을 관리하기 위한 비밀 파일 로더를 추가한다.
3. 파일 이름을 버전관리에서 제외한다.(.gitignore)

### 5.4.1 Using JSON Files

```json
{
    "FILENAME": "secrets.json", 
    "SECRET_KEY": "I've got a secret!", 
    "DATABASES_HOST": "127.0.0.1", 
    "PORT": "5432"
}
```

```python
import json
from django.core.exceptions import ImproperlyConfigured

with open('secrets.json') as f:
    secrets = json.load(f)

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting] 
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret('SECRET_KEY')
```

### 5.4.2 Using .env, Config, YAML, and XML File Formats

다른 포맷으로 작업을 할 수도 있습니다. 
원하는 포멧으로 작업할때 [Section 28.10: Defend Against Python Code Injection Attacks.]()를 참고하세요.

## 5.5 Using Multiple Requirements Files

requirements 파일을 환경 별로 아래와 같이 구성합니다.

```
requirements/
   ├── base.txt
   ├── local.txt
   ├── staging.txt
   ├── production.txt
```

```
# base.txt
# 모든 환경에서 공통으로 이용하는 의존성
Django==3.2.0
psycopg2-binary==2.8.8
djangorestframework==3.11.0
```

```
# local.txt
-r base.txt # includes the base.txt
coverage==5.1
django-debug-toolbar==2.2
```

```
# ci.txt
-r base.txt # includes the base.txt
coverage==5.1
```

```
# production.txt
-r base.txt # includes the base.txt
```

일반적으로 production.txt가 base.txt라고 불리기도 합니다.

### 5.5.1 Installing From Multiple Requirements Files

```
# 로컬 환경
$ pip install -r requirements/local.txt

# 운영 환경
$ pip install -r requirements/production.txt
```

## 5.6 Handling File Paths in Settings

경로는 **하드 코딩**은 절대 피해야 합니다.

### pathlib 으로 세팅하는 방법(Python 3.4 이상)

```python
# settings/base.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'static_root'
STATICFILES_DIRS = [BASE_DIR / 'static']
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
    },
]
```

### os.path 라이브러리만으로 세팅하는 방법

```python
# settings/base.py
from os.path import abspath, dirname, join

def root(*dirs):
    base_dir = join(dirname(__file__), '..', '..') 
    return abspath(join(base_dir, *dirs))

BASE_DIR = root()
MEDIA_ROOT = root('media')
STATIC_ROOT = root('static_root')
STATICFILES_DIRS = [root('static')]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [root('templates')],
    }, 
]
```

`BASE_DIR`에 기반을 둔 경로라면 settings 파일의 경로들은 문제없이 작동할 것입니다.
