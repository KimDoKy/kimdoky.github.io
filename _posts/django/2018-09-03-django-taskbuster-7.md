---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 7
category: django
tags: [ 'django' ]
---

# [Install and Configure PostgreSQL](http://www.marinamele.com/taskbuster-django-tutorial/install-and-configure-posgresql-for-django)

이제 프로젝트의 데이터베이스픞 구성할 차례입니다. 이번 파트에서는 PostgreSQL에 대해 다룹니다.

이 튜토리얼의 뒷부분에서는 Heroku에 앱을 배포할 것이고 PostgreSQL를 사용할 것입니다. 따가서 어떤 데이터베이스를 구성해야 할지 모른다면 PostgreSQL를 권장합니다.

이 번 파트의 개요입니다.
 - Install PostgreSQL
 - Create a PostgreSQL Database
 - Install the PostgreSQL Django adapter, psycopg2
 - Configure the Django Database Settings

## Install PostgreSQL

[PostgreSQL](https://www.postgresql.org/download/macosx/)에서 다운받을 수 있습니다.

설치 프로세스 중에 PostgreSQL의 데이터베이스 슈퍼 유저 계정에 대한 비밀번호를 설정해야 합니다.

```
$ pg_config
```

만약 찾을 수 없는 오류가 발생한다면 먼저 다음 명령을 사용하여 이 명령의 경로를 찾아야 합니다.

```
$ sudo find / -name pg_config
```

이건 '/Librry/PostgreSQL/9.3/bin'과 같아야 합니다. `$PATH` 변수에 추가해야 하므로 '.bash_profile' 파일을 열고 다음 행을 추가하세요.

```bash
export PATH=/Library/PostgreSQL/9.3/bin:$PATH
```

터미널을 다시 실행하여 'pg_config'을 입력하면 잘 작동하게 됩니다.

## Create a PostgreSQL Database

맥에서는 아래의 명령을 합니다.

```
$ which psql
```

PostgreSQL 앱을 가리켜야 합니다. 그리고 다른 명령은 PostgreSQL command line 유틸리티를 시작해야 합니다.

```
$ psql -h localhost
```

이 명령으로 "**psql: FATAL: password authentication falied for user “username”**"와 같은 오류가 발생하고 암호를 올바르게 입력했으면 PostgreSQL 사용자를 사용하여 psql을 입력해야 합니다.

```
$sudo -u postgres psql
```

반면에 "**psql: FATAL: database <user> does not exist**"와 같은 오류가 발생하면 패키지 관리자가 적절한 데이터베이스를 만들지 못했을 수 있습니다. 자세한 내용은 [post](http://stackoverflow.com/a/17936043)를 참조하세요. 이 문제를 해결하려면 다음을 시도하세요.

```
$ createdb
$ psql -h localhost
(or $ sudo -u postgres psql)
```

이제 PostgreSQL의 command line에 있어야 합니다. 다음을 입력하여 이 환경을 종료할 수 있습니다.

```
\q
```

마찬가지로, 더 많은 도움말을 보려면 `\?`를 입력할 수 있습니다. 데이터베이스를 나열하려면 `\list`를 입력하고, 사용자를 나열하려면 `\du`를 입력하세요.


**프로젝트를 위한 새 데이터베이스** 와 데이터베이스에 대한 액세스 권한을 부여할 새 사용자를 만듭니다.

```
$ createdb taskbuster_db
(or $ sudo -u postgres createdb taskbuster_db)
$ psql
(or $ sudo -u postgres psql)
CREATE ROLE myusername WITH LOGIN PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE taskbuster_db TO myusername;
ALTER USER myusername CREATEDB;
```

원하는 사용자 이름으로 myusername을 변경하고, 원하는 비밀번호로 mypassword를 변경하세요. 그리고 각 명령의 끝에 `;`를 잊지 마세요.

## Install the PostgreSQL Django adapter, psycopg2

다음으로 Python용 PostgreSQL 데이터베이스 어댑터인 '[psycopg2](https://pypi.org/project/psycopg2/)' 패키지를 설치해야 합니다.

```
$ pip install psycopg2
```

마지막으로 'requirements/base.txt' 파일에 추가하고, 작업환경(테스트, 개발)에 설치하세요.

## Configure the Django Database Settings

다음으로, PostgreSQL를 데이터베이스로 지정해야 합니다. 이것은 로컬 데이터베이스이므로 테스트와 개발의 설정 파일에서 `DATABASES` 변수를 다시 정의해야 합니다. 'settings/dev.py'와 'settings/test.py'를 수정합니다.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}
```

이 파일들은 `get_env_variable` 함수를 정의한 'settings/base.py' 파일을 임포트합니다.

```python
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)
```

그리고 각 환경의  `postactivate` 파일을 편집하세요.

```
$ vi $VIRTUAL_ENV/bin/activate
```

데이터베이스 설정을 추가하세요.

```
export DATABASE_NAME='taskbuster_db'
export DATABASE_USER='myusername'
export DATABASE_PASSWORD='mypassword'
```

이러한 변경 사항을 효과적으로 적용하려면 환경을 비활성화하고 활성화해야 합니다.

이제 데이터베이스를 확인하고 동기화하고 마이그레이션 할 준비가 되었습니다.

```
$ python manage.py check
$ python manage.py migrate
```

하나의 환경(개발이나 테스트)에서만 데이터베이스를 마이그레이션하면 됩니다. 마이그레이션이 두 데이터베이스 모두에서 동일한 데이터베이스에 적용되기 때문입니다.

Django의 슈퍼유저를 생성하라는 메시지가 표시됩니다. 아니면.. 다음 명령으로 생성하세요.

```
$ python manage.py createsuperuser
```

> 저는 아무런 오류가 일어나지 않아서 해보지는 못했습니다..

Mac에서 작업하면 다음과 같은 오류가 일어납니다.

```
django.core.exceptions.ImproperyConfigured: Error loading psycop2 module
Library not loaded: libssl.1.0.0.dylib
Referenced from: .../psycopg2/_psycopg.so
Reason: image not found
```

다음을 실행해야 합니다.

```
$ sudo ln -s /Library/PosgreSQL/9.4/lib/libssl.1.0.0.dylib /usr/lib
$ sudo ln -s /Library/PosgreSQL/9.4/lib/libcrypto.1.0.0.dylib /usr/lib
```

확인하고 마이그레이션하세요. 그래도 작동하지 않고 오류가 발생한다면 '.bash_profile'에 다음을 추가하세요.

```
export DYLD_FALLBACK_LIBRARY_PATH=/Library/PostgreSQL/9.4/lib:$DYLD_LIBRARY_PATH
```

Mac에서 다음과 같은 오류가 있는 경우

```
django.db.utils.OperationalError: could not connect to server: No such file or directory
Is the server running locally and accepting connections on Unix domain socke
```

'~/.bash_profile' 파일에 다음을 추가하세요.

```
export PGHOST=localhost
```

확인하고 다시 마이그레이션하세요.

다음과 같은 또 다른 오류가 있을 수 있습니다.

```
raise ImproperlyConfigured("Error loading psycopg2 module: %s" % e)
django.core.exceptions.ImproperlyConfigured: Error loading psycopg2 module: dlopen(/Users/user/.virtualenvs/tb_dev/lib/python3.4/site-packages/psycopg2/_psycopg.so, 2): Symbol not found: _lo_lseek64
  Referenced from: /Users/user/.virtualenvs/tb_dev/lib/python3.4/site-packages/psycopg2/_psycopg.so
  Expected in: /usr/lib/libpq.5.dylib
  in /Users/user/.virtualenvs/tb_dev/lib/python3.4/site-packages/psycopg2/_psycopg.so
```

PostgreSQL 디렉터리 내에 최신 libpq.5.dylib 파일에 대한 symlink를 생성해야 합니다.

```
$ sudo ln -fs /Library/PostgreSQL/9.4/lib/libpq.5.6.dylib /usr/lib/libpq.5.dylib
```

Mac이나 다른 버전의 PostgreSQL를 사용하지 않는 경우 폴더 경로가 다를 수 있습니다.

확인하고 다시 마이그레이션 하세요.

마지막으로 모든 것이 예상대로 작동하는지 테스트합니다.

```
$ python manage.py test
```

테스트가 얼마나 유용한지 알겠나요? 이제 데이터베이스를 변경한 후 모든 기능이 이전과 동일하게 작동합니다.

다음 튜토리얼에서는 Google이나 Twitter와 같은 소셜 계정을 사용하여 사용자 인증을 할 것입니다.
