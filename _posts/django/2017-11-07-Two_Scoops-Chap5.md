---
layout: post
section-type: post
title: Two Scoops of Django - chap5. settings와 requirements 파일
category: django
tags: [ 'django' ]
---

장고는 세팅 모듈에서 설정할 수 있는 140여 개가 넘는 항목을 제공하며 대부분의 경우 기본값으로 적용되어 있습니다. 세팅들은 서버가 시작될 때 적용되며 세팅값의 새로운 적용은 서버를 재시작해야만 가능학시 때문에 개발자들이 서비스 운영 중에 임의로 변경할 수 없게 되어 있다.

![]({{site.url}}/img/post/django/two_scoops/5.1.png)
> 프로젝트가 커 감에 따라 장고의 세팅 항목들도 점차 복잡해지기 시작한다.

최선의 장고 설정 방법은 다음과 같다.

- **버전 컨트롤 시스템으로 모든 설정 파일을 관리해야 한다.** 운영 환경에서는 특히 중요하다. 날
짜, 시간 등 세팅 변화에 기록이 반드시 문서화되어야 한다.
- **반복되는 설정들을 없애야 한다.** 여러번 쓰이는 세팅은 기본 세팅 파일로부터 상속을 통해 이용한다.
- **암호나 비밀키 등은 안전하게 보호해야 한다.** 보안 관련 사항은 버전 컨트롤 시스템에서 제외해야 한다.

## 5.1 버전 관리되지 않는 로컬 셋팅은 피하도록 한다.
개발을 위해 개발자에게만 필요한 환경이란 것이 존재한다. 스테이징과 운영 서버에서는 비활성화되어 있거나 아예 설치조차 되어 있지 않은 디버그 도구에 대한 세팅이 그러한 예이다.  
`SECRET_KEY`와 아마존 API, 스트라이프(stripe) API키, 다른 비밀번호 형태의 여러 설정 변수도 보안을 위해 저장소에서 빼야 한다.

> ### 비밀 정보 보호하기!  
SECRET_KEY 세팅은 장고의 암호화 인증 기능에 이용되고 이 세팅값은 다른 프로젝트와는 다른 유일무이한 값이 되어야 하며 버전 컨트롤 시스템에서 제외해야 한다. SECRET_KEY에서 논의된 주의점은 데이터베이스의 비밀번호, AWS 키, OAuth 토큰, 프로젝트를 운영하기 위해 필요한 민감한 자료들 모두에 해당한다.

일반적은 해결 방법으로 local_settings.py라는 모듈을 생성하고 해당 파일을 각 서버나 개발 머신에 위치시켜, 이 파일을 버전 컨트롤 시스템에서 빼 버리는 방법이다. 이로써 버전 컨트롤의 제약 없이 비즈니스 로직을 포함한 개발 환경에 특화된 설정들을 변경할 수 있다. 스테이징 서버와 개발 서버에서는 버전 컨트롤 관리 없이도 해당 위치에 세팅과 로직을 유지할 수 있다. 하지만 문제가 있다.

- 모든 머신에 버전 컨트롤에 기록되지 않은 코드가 존재하게 된다.
- 운영 환경에서만 일어날 수 있는 문제점을 발견하기 어렵다.
- '버그'를 수정했지만 그 원인이 커스터마이징된 local_settings.py 모듈에 기이한 것일 수 있다.
- 여러 팀원이 서로의 local_settings.py를 복사해서 여기저거 쓰면 dry 규칙에 위배된다.

다른 방법은 개발 환경, 스테이징 환경, 테스트 환경, 운영 환경 설정을 공통되는 객체로부터 상속받아 구성된 서로 다른 세팅 파일로 나누어 버전 컨트롤 시스템을 관리하는 것이다. 그런 다음에는 이러한 상태에서 서버의 암호 정보 등을 버전 컨트롤에서 빼서 비밀스럽게 유지하는 것이다.

## 5.2 여러 개의 settins 파일 이용하기
한 개의 settins.py를 이용하기 보다는 settins/ 디렉터리 아래에 여러 개의 셋업 파일을 구성하여 이용한디.

```
setting/
    __init__.py
    base.py
    local.py
    staging.py
    test.py
    production.py
```

세팅 파일 | 설명
---|---
base.py | 프로젝트의 모든 인스턴스에 적용되는 공용 세팅 파일
local.py | 로컬 환경에서 작업할 때 쓰이는 파일이다. 디버그 모드, 로그 레벨, django-debug-toolbar 같은 도구 활성화 등이 설정되어 있는 개발 전용 로컬 파일이다. 때때로 개발자들은 이 파일을 dev.py로 수정해서 이용한다.
staging.py | 운영 환경 서버에서 (반쯤은) 프라이빗 버전을 가지고 구동되는 스테이징 서버를 위한 파일이다. 운영 환경으로 코드가 완전히 이전되기 전에 관리자들은 고객들의 확인을 위한 시스템이다.
test.py | 테스트 러너(test runner), 인메모리 데이터베이스 정의, 로그 세팅 등을 포함한 테스트를 위한 세팅
production.py | 운영 서버에서 실제로 운영되는 세팅 파일이다. 이 파일에는 운영 서버에서만 필요한 설정이 들어 있다. prod.py라고 부르기도 한다.
ratings/ | 이용자가 매긴 점수를 관리하는 앱
static/ | CSS, 자바스크립트, 이미지 등 사용자가 올리는 것 이외의 정적 파일들이 위치시키는 곳이다. 큰 프로젝트의 경우 독립된 서버에 호스팅한다.
templates/ | 시스템 통합 템플릿 파일 저장 장소

shell과 runserver 관리 명령에서 `--settings` 옵션을 통해 적용 및 구동할 수 있다.

settings/local.py 세팅 파일을 이용하고자 하려면 다음과 같이 하면 된다.

#### 셸 이용시
```
python manage.py shell --settings=twoscoops.settings.local
```

#### 개발 서버 구동시
```
python manage.py runserver --settings=twoscoops.settins.local
```

--settings 옵션이나 DJANGO_SETTINGS_MODULE의 환경 변수에 이용 가능한 값들을 다음과 같이 정리할 수 있습니다.

환경 | --settings(또는 DJANGO_SETTINGS_MODULE 값) 옵션값
---|---
로컬 개발 환경 | twoscoops.settings.local
스테이징 서버 | twoscoops.settings.staging
테스트 서버 | twoscoops.settings.test
운영 서버 | twoscoops.settings.production

> ### DJANGO_SETTINGS_MODULE과 PYTHONPATH  
--settins 옵션을 여러 곳에서 이용하는 것에 대한 대안으로 DJANGO_SETTINGS_MODULE과 PYTHONPATH 환경 변수를 조건에 맞는 세팅 모듈 패스로 설정하는 방법이 있다. 이를 위해서는 각 환경별로 DJANGO_SETTINGS_MODULE을 설정해야 한다.  
virtualenv를 좀 더 깊이 이해하고 있다면 다른 대안으로 virtualenv의 postactivate 스크립트에 DJANGO_SETTINGS_MODULE과 PYTHONPATH를 설정하는 방법이 있다. 일단 이렇게 설정한 후 virtualenv 안에서 python 명령어를 입력하는 것만으로 프로젝트의 해당 설정값을 로딩할 수 있다. 또한 이는 django-admin.py를 --settings 옵션 없이 실행해도 자동으로 설정이 적용된다는 의미기도 하다.

### 5.2.1 개발 환경의 settings 파일 예제

```
# settings/local.py
from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "twoscoops",
    "USER": "",
    "PASSWORD": "",
    "HOST": "localhost",
    "PORT": "",
  }
}

INSTALLED_APPS += ("debug_toolbal",)
```

```
python manage.py runser --settings=twoscoops.settings.local
```

해당 설정을 버전 컨트롤 시스템에 추가함으로써 개발자들은 같은 개발 세팅 파일들을 공유하게 된다. 여러 명이 공동 작업을 하는 프로젝트 환경에서 특히 빛을 발하게 된다.  
또 다른 장점은 프로젝트와 프로젝트 사이을 이동하면서 'if DEBUG' 또는 'if not DEBUG' 코드를 붙이지 않아도 된다.  
장고 세팅 파일에 이 파일이 유일하게 `import *` 구문을 이용해도 되는 파일이다. 세팅 파일은 모든 이름 공간을 전부 오버라이드하고 싶은 유일한 경우이다.

### 5.2.2 다중 개발 환경 세팅
때때로 큰 프로젝트를 진행하다 보면 개발자마다 자기만의 환경이 필요한 경우가 있다. 이럴 경우 하나의 dev.py 세팅 파일을 여러 팀원과 함께 사용하는 것이 불가능 할 수도 있다.  
이럴 때는 버전 컨트롤 시스템에서 관리되는 파일들을 구성하여 이용하면 된다. 이를 위해 여러 개의 개발 세팅 파일을 생성하는 것이 좋은데, 예를 들면 dev_audrey.py, dev_pydanny.py 같은 이름을 가진 파일을 생성하여 이용하는 것이다.

```
setings/dev_pydanny.py
from .local import *

# 짧은 캐시 타임아웃 설정
CACHE_TIMEOUT = 30
```

이유는 개발 환경 또는 버전 관리를 하면 더 좋고 팀원 간 서로의 개발 세팅 파일을 참고할 수 있기 때문이다. 일반적으로 이용하는 settings 파일들의 구성이다.

```
settings/
    __init__.py
    base.py
    dev_audrey.py
    dev_pydanny.py
    local.py
    staging.py
    test.py
    production.py
```

## 5.3 코드에서 설정 분리하기

local_settings 안티 패턴을 이용했던 이유 중 하나가 SECRET_KEY, AWS 키, API 키 또는 서버에 따라 특별하게 설정된 값들이 세팅 파일에 위치하게 된다는 것 때문이다.  

- 설정은 배포 환경에 따라 다르지만 코드는 그렇지 않다.
- 비밀 키들은 설정값들이지, 코드가 아니다.
- 비밀값들은 반드시 남이 알 수 없어야 한다. 이를 버전 컨트롤 시스템에 추가하면 코드 저장소에 접근할 수 있는 누구에게나 공개된다.
- PaaS 환경에서는 각각의 독립된 서버에서 코드를 수정하도록 허용하지 않고 있다. 가능하다 할지라도 독립된 서버에서 직접 코드를 수정하는 것은 매우 위험한 방법이다.  

이를 해결하기 위해 **환경 변수** 를 이용하고, 이를 **환경 변수 패턴(environment variables pattern)** 이라고 부른다.  

장고(와 파이썬)은 운영 체제의 환경 변수를 손쉽게 설정할 수 있는 기능을 제공한다.  

환경 변수를 비밀 키를 위해 이용함으로써 다음과 같은 장점을 얻을 수 있다.

- 환경 변수를 이용하여 비밀 키를 보관함으로써 걱정 없이 세팅 파일을 버전 컨트롤 시스템에 추가할 수 있다. 세팅 파일을 포함하여 모든 파이썬 파일은 버전 컨트롤에서 관리해야 한다.
- 개발자 개개인이 문제가 발생하기 쉬운 복사, 붙이기 기반의 local_settings.py.example을 쓰기보다는 버전 컨트롤로 관리되는 단일한 settings/local.py를 나눠 쓸 수 있다.
- 파이썬 코드 수정 없이 시스템 관리자들이 프로젝트 코드를 쉽게 배치할 수 있다.
- 대부분의 PaaS가 설정을 환경 변수를 통해 이용하기를 추천하고 있고 이를 위한 기능들을 내장하고 있다.

### 5.3.1 환경 변수에 비밀 키 등을 넣어 두기 전에 유의할 점

- 저장되는 비밀 정보를 관리한 방법
- 서버에서 배시(bash)가 환경 변수와 작용하는 방식에 대한 이해 또는 PaaS 이용 여부

> ### 환경 변수를 아파치와 같이 이용해서는 안 된다.  
운영 환경이 아파치를 이용하고 있다면 운영 체제의 환경 변수 세팅이 아파치에서는 정상으로 작동하지 않는다. 이는 아파치가 스스로 독립적인 환경 변수 시스템을 가지고 있기 때문이다.

### 5.3.2 로컬 환경에서 환경 변수 세팅하기
배시를 이용하는 맥과 리눅스의 경우, 다음 구문을 bashrc, bash_profile, 또는 .profile의 뒷부분에 추가하면 된다. 또는 같은 API를 이용하는 여러 개의 프로젝트를 서로 다른 API 키를 이용하여 작업한다고 하면 다음 구문을 virtualenv의 /bin/activate 스크립트의 맨 마지막 부분에 넣어주면 된다.

```
$ export SOME_SECRET_KEY=1c3-cr3am-15-yummy
$ export AUDREY_FREEZER_KEY=u34h-r1ght-d0nt-t0uch-my-1c3-cr34m
```

> ### virtualenvwrapper를 통해 좀 더 쉽게 처리해 보자  
virtualenvwrapper는 각각의 virtualenv 환경 설정을 더욱 단순화해주는 매우 좋은 도구다. 물론 설정을 하려면 맥 OS X, 리눅스를 일정 수준 이상 이해해야 한다.

### 5.3.3 운영 환경에서 환경 변수를 세팅하는 방법
자체 서버를 운영하는 경우, 사용하는 도구와 자체 서버 설정의 복잡도에 따라 각기 다른 방법을 적용하게 된다. 가장 간단하게는 테스트 프로젝트를 위한 한대의 서버 환경을 구성한 후 환경 변수들을 수작업으로 설정하는 것이다. 하지만 스크립트나 서버 프로비저닝 또는 배포를 위한 도구들을 이용 중이라면 방법은 더 복잡해진다.  
장고 프로젝트가 PaaS를 통해 배포된다면 해당 문서를 확인해야 한다. 여기서는 허로쿠(Heroku) 기반으로 한 설정을 예로 든다. PaaS 옵션을 이용하는 경우 비슷한 예가 될 것이다.  

허로쿠에서는 다음과 같은 명령어를 통해 개발 환경의 환경 변수들을 지정하게 된다.

```
$ heroku config:set SOME_SECRET_KEY=1c3-cr3am-15-yummy
```
파이썬에서 어떻게 환경 변수에 접근하게 되는지를 보려면, 파이썬 프롬포트를 열고 다음과 같이 입력한다.

```
>>> import os
>>> os.environ["SOME_SECRET_KEY"]
"1c3-cr3am-15-yummy"
```

세팅 파일에서 환경 변수들에 접근하려면 다음과 같이 한다.

```
# settings/production.py의 윗부분
import os
SOME_SECRET_KEY = os.environ["SOME_SECRET_KEY"]
```

이 코드는 SOME_SECRET_KEY라는 환경 변수의 값을 운영 체제로부터 받아와서 SOME_SECRET_KEY라는 파이썬 변수로 저장하고 있다.  
이런 패턴을 이용함으로써 모든 코드가 버전 컨트롤 시스템으로 들어갈 수 있으며 또한 모든 비밀 설정들도 안전하게 유지될 수 있다.

### 5.3.4 비밀 키다 존재하지 않을 때 예외 처리하기
앞에서 쓴 코드에서 SECRET_KEY를 환경 변수로부터 가져오는 것이 여의치 않거나 값이 존재하지 않을때, 해당 코드는 KeyError를 일으키고 프로젝트를 시작할 수 없을 것이다. 이 것 자체가 문제는 아니지만, 발생한 KeyError가 문제의 원인을 가르쳐 주지 않는게 문제가 된다.  
환경 변수가 존재하지 않을 때 원인을 좀 더 쉽게 알기 위해 settings.base.py에 다음의 코드를 추가한다.

```python
# settings/base.py
import os

# 일반적으로 장고로부터 직접 무언가를 설정 파일로 임포츠해 올 일은
# 없을 것이며 또한 해서도 안 된다. 단 ImproperyConfigured는 예외다.
from django.core.exceptions import ImproperyConfigured

def get_env_variable(var_name):
    """환경 변수를 가져오거나 예외를 반환한다."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperyConfigured(erro.r_msg)
```
이제 세팅 파일 어디에서라도 다음과 같은 방법으로 환경 변수에서 비밀 키를 가져올 수 있다.

```
SOME_SECRET_KEY = get_env_variable("SOME_SECRET_KEY")
```

SOME_SECRET_KEY가 환경 변수로 존재하지 않는 경우 다음과 같은 유용한 에러 메시지를 볼 수 있다.

```
django.core.exceptions.ImproperyConfigured: Set the SOME_SECRET_KEY
environment variable.
```
>
### 세팅 모듈 안에서 장고 컴포넌트 임포트는 금물이다.
세팅 모듈 안에서 장고 컴포넌트를 임포트하면 예기치 못한 부작용을 일으킬 수 있다. 따라서 세팅 파일 어디에서라도 장고 컴포넌트를 임포트하는 일은 삼가해야한다. ImproperyConfigured는 장고에서 바르게 설정되지 못한 프로젝트에 대해서 발생시키는 예외처리이다. 이 ImproperyConfigured에 덧붙여 문제시 발생되는 에러 메세지에 문제가 되는 세팅 이름을 추가로 나타냄으로써 좀 더 도움이 될 수 있다.

>
### manage.py 대신 django-admin.py 이용하기
장고 공식 문서에 따르면 여러 개의 settings 파일을 이용할 때는 manage.py가 아니라 django-admin.py를 이용하라고 나오있다. django-admin.py 이용에 어려움이 있다면 그냥 manage.py를 이용하여 개발해도 무방하다.

## 5.4 환경 변수를 이용할 수 없을 때
환경 변수를 이용할 때 문제점은 경우에 따라 이런 방식이 적용되지 않을 수도 있다는 것이다. 가장 일반적인 경우가 아파치를 웹(HTTP) 서버로 이용하는 경우다. 아파치 뿐만 아니라 Nginx 기반 환경에서도 특정 경우에 한해 환경 변수를 이용하는 방법이 작동되지 않는다. 이럴 경우 다시 local_settings 안티 패턴 방법으로 돌아가기 보다는 **비밀 파일 패턴(secret file)** 방법을 이용할 수 있다. 이는 장고에서 실행되지 않는 형식의 파일을 버전 컨트롤 시스템에 추가하지 않고 사용하는 방법이다.  

다음 3 단계로 비밀 파일 패턴을 구현할 수 있다.

1. JSON, Config, YAML 또는 XML 중 한 가지 포맷을 선택하여 비밀 파일을 생성한다.
2. 비밀 파일을 관리하기 위한 비밀 파일 로더를 간단하게 추가한다.
3. 비밀 파일의 이름을 .gitignore에 추가한다.

### 5.4.1 JSON 파일 이용하기
JSON 포맷의 장점은 파이썬을 비롯한 다른 언어에서도 다양하게 이용할 수 있다.  
secrets.json 파일을 생성한다.

```json
{
    "FILENAME": "secrets.json",
    "SECRET_KEY": "I've got a secret!",
    "DATABASES_HOST": "127.0.0.1",
    "PORT": "5432"
}
```
이렇게 만든 secrets.json 파일을 이용하기 위해 다음 코드를 기본 베이스 settings 모듈에 추가한다.

```python
# settings/base.py
import json

# 일반적으로 장고로부터 직접 무언가를 설정 파일로 임포츠해 올 일은
# 없을 것이며 또한 해서도 안 된다. 단 ImproperyConfigured는 예외다.
from django.core.exceptions import ImproperyConfigured

# JSON 기반 비밀 모듈
with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적으로 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
```

### 5.4.2 Config, YAML, XML 파일 이용하기
다른 개발자들은 다른 형태의 포맷을 선호할 수 있다. 이에 대해서는 스스로 원하는 포맷에 적합한 get_secret()을 추가하면 된다.

## 5.5 여러 개의 requirements 파일 이용하기
각 세팅 파일에 대해 각각에 해당하는 requirements 파일을 이용해야 한다. 이는 각 서버에서 그 환경에 필요한 컴포넌트만 설치하자는 의미다.  

우선 <repository_root> 아래에 requirements/ 디렉터리를 만들고 디렉터리 안에 파일들의 이름을 똑같은 '.txt' 파일들을 생성한다.

```
requirements/
    base.txt
    local.txt
    staging.txt
    production.txt
```

base.txt 파일 안에는 모든 환경에 걸쳐 공통으로 이용한 의존성을 넣어준다.

```
Django==1.8.0
psycopg2=2.6
djangorestframework==3.1.1
```

local.txt 파일에는 개발 환경에서 필요한 다음과 같은 패키지들이 존재하게 된다.

```
-r base.txt # base.txt requirements 파일 포함
coverage=3.7.1
django-debug-toolbar=1.3.0
```

지속적 통합 서버가 이용하는 ci.txt는 다음과 같은 내용을 담게 된다.

```
-r base.txt # base.txt requirements 파일 포함
coverage=3.7.1
django-jenkins=0.16.4
```

운영 환경에서 요구되는 것들은 앞의 local.txt, ci.txt의 경우를 제외한 나머지 구성 요소들과 비슷하다. 일반적으로 production.txt가 base.txt라고 불리기도 한다.

```
-r base.txt # base.txt requirements 파일 포함
```

### 5.5.1 여러 개의 requirements 파일로부터 설치하기
```
$ pip install -r requirements/local.txt
```
뒤에 경로만 변경하여 각 환경에 맞게 설치하면 된다.

### 5.5.2 여러 개의 requirements 파일을 PaaS 환경에서 이용하기
추후에 다룰 예정

## 5.6 setting에서 파일 경로 처리하기
장고 세팅 파일에 파드 코딩된 파일 경로는 절대 금지이다.

```python
# settins/base.py
# 나쁜 예

# MEDIA_ROOT 설정
MEDIA_ROOT = "/User/pydanny/twoscoops_project/media"
```

`Unipath`나 `os.path` 라이브러리를 이용해 `BASE_DIR`을 세팅하면 된다.

```python
# Unipath 이용 예
from unipath import Path

BASE_DIR = Path(__file__).ancestor(3)
MEDIA_ROOT = BASE_DIR.child("media")
STATIC_ROOT = BASE_DIR.child("static")
STATICFILES_DIRS = (
    BASE_DIR.child("assets"),
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIR = (BASE_DIR.child("templates"),)
    }
]
```

```python
# os.path 이용 예
from os.path import join. abspath, dirname
here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)

# MEDIA_ROOT 설정
MEDIA_ROOT = root("media")

# STATIC_ROOT 설정
STATIC_ROOT = root("collected_static")

# 정적 파일의 추가 위치
STATICFILES_DIRS = (
    root("assets")
)

# TEMPLATE_DIR 설정
TEAMPLTES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        DIR = (root("templates"),)
    }
]
```

`BASE_DIR`에 기반을 둔 경로라면 settings 파일의 경로들을 문제없이 작동할 것이다. 즉 쳄플릿과 미디어들이 서로 문제없이 잘 로딩된다.

> ### 장고의 기본 세팅이 얼마나 변경되었는지..  
`diffsettings` 라는 명령으로 비교할 수 있다.

## 5.7 요약

특별히 보안에 관계된 사항들을 제외한 모든 요소를 버전 컨트롤로 관리해야 한다. 실제로 상용 운영 환경에서 구현될 프로젝트라면 다수의 settings 파일과 requirements 파일을 필요로 하게 될 것이다. 심지어 처음 개발을 시작했던 기기로부터 코드가 다른 기기로 이전된다면 settings/requirements 파일이 큰 도움이 될 것이다.
