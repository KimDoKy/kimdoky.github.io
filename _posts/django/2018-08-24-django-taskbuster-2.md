---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 2 - Settings files and Version Control
category: django
tags: [ 'django' ]
---

# [Settings files and Version Control](http://www.marinamele.com/taskbuster-django-tutorial/settings-different-environments-version-control)

이제 테스트, 개발, 프로덕션 환경을 구성하고 다른 Django 설정 파일을 편집합니다.

또한 Django의 SECRET_KEY를 비밀로 유지하기 위해 파일들에서 제거할 것입니다.

원문에서는 Bitbucket을 이용하지만, Git 정원을 꾸미기 위해 github를 사용합니다.

## Virtual Environments and Requirements files

Project에서 작업할 때 중요한 것은 패키지 버전을 제어하는 것입니다. 예를 들어, Django 2.0이 설치된 한 대의 컴퓨터에서 개발중이며 Django의 이전 버전인 한 대의 서버에 배포하고 있다고 가정합니다. 코드는 로컬에서 잘 작동하지만 배포할 때 일부 호환되지 않는 오류가 발생할 수 있습니다. 둘 이상의 개발자가 동일한 프로젝트에서 작업하고 있고 각각이 자체 패키지 버전이 설치된 경우도 마찬가지입니다.

이 문제의 해결책은 모든 패키지를 통합하고 Requirements.txt라는 파일에 사용된 버전을 저장하는 것입니다.

```
# 가상 환경에 설치된 패키지를 볼 수 있습니다.
$ pip freeze
Django==2.1
pytz==2018.5
selenium==3.14.0
urllib3==1.23

# 위 명령의 출력을 파일로 저장합니다.
$ pip freeze > requirements.txt
```

하지만 selenium은 테스트 환경에서만 필요하므로 개발환경이나 프로덕션 환경에는 설치할 필요가 없습니다.

requirements 디렉터리를 생성하고 각 환경에 맞는 파일을 만들어 이 문제를 해결할 수 있습니다.

```
$ mkdir requirements
$ touch requirements/{base.txt,dev.txt,prod.txt,test.txt}
```
> 이전 requirements.txt는 필요하지 않으므로 삭제합니다. 프로덕션 서버에서 사이트의 준 사설 버전을 실행하려는 경우 staging.txt 파일을 만들 수도 있습니다.

먼저 base.txt를 편집합니다. 이 파일에는 모든 환경에 공통적인 모든 패키지가 들어 있습니다.

```
$ cd requirements
# 각자 사용하는 버전을 넣으세요.
$ echo "Django==2.1" >> base.txt
```

공통 패키지를 상속 받도록 3개의 다른 파일도 편집합니다.

```
echo "-r base.txt" | tee -a dev.txt test.txt prod.txt
```

마지막으로 test.txt에 Selenium을 추가합니다.

```
echo "selenium==3.14.0" >> test.txt
```

이제 새로운 프로그래머가 팀에 합류할 때, 테스팅용과 개발용(프로덕션 환경은 배포용)이라는 두 가지 환경을 만들었다고 할 수 있습니다.

다음으로, 그 프로그래머는 각 환경을 활성화하고 각 requirements 파일에 저장된 패키지를 설치하기만 하면 됩니다.

```
$ pyenv local tb_dev
$ pip install -r requirements/dev.txt

$ pyenv local tb_test
$ pip install -r requirements/test.txt
```

## Different settings.py for each environment

각 환경은 다른 용도로 사용되므로 서로 다른 셋팅이 필요합니다. 예를 들어, 프로덕션과 개발을 위한 데이터베이스 구성이 다를 수도 있고, 테스팅 환경이 selenium과 같은 다른 환경에서는 필요 없는 일부 Django 애플리케이션을 사용할 수도 있습니다.

그래서 각 환경마다 다른 설정 파일을 지정합니다. 먼저, teskbuster 디렉터리 안에 설정 파일을 저장할 디렉터리를 만듭니다.

```
$ mkdir taskbuster/settings
```

이 폴더에는 다음 내용이 포함됩니다.

- 이 폴더를 파이썬 패키지로 만들기 위한 __init__.py 파일
- base.py : 모든 환경에서 공통적인 모든 설정을 포함. 다른 설정 파일은 이 파일을 상속합니다.
- dev.py : 로컬 개발용입니다.
- test.py : 테스트용입니다.
- prod.py : 프로덕션 환경에서 사용됩니다.
- 프로젝트의 프로덕션 서버에서 스테이징 버전을 실행하려면 staging.py를 사용하세요.

이 파일들을 모두 taskbuster/settings 디렉터리에 생성하세요.

```
$ cd taskbuster/settings
$ touch __init__.py dev.py test.py prod.py staging.py
```

그리고 각각을 편집하여 base.py 파일을 상속받게 합니다.

```
$ echo "# -*- coding: utf-8 -*-" | tee -a dev.py test.py prod.py staging.py
$ echo "from .base import *" | tee -a dev.py test.py prod.py staging.py
```

마지막으로 Django의 settings.py 파일을 settigns 디렉터리의 base.py파일로 이동하고 이름을 바꿉니다.

```
$ mv ../settings.py base.py
```
이러한 파일을 만든 후에는 올바른 설정 파일을 사용하도록 가상 환경을 지정해야 합니다.

원문에서는 virtualenvwrapper를 이용하지만, 개인적으로 이용해본 결과 그냥 virtualenv를 사용하는 것이 편하여, 제가 사용하는 방법으로 바꾸어 소개합니다.

**(세팅하려는 가상환경으로 들어간 다음에)**  

개발자 가상환경인 tb_dev 에서는

```
# $VIRTUAL_ENV/bin/activate애 입력합니다.
export DJANGO_SETTINGS_MODULE='taskbuster.settings.dev'
```

테스트 가상환경인 tb_test에서는

```
# $VIRTUAL_ENV/bin/activate애 입력합니다.
export DJANGO_SETTINGS_MODULE='taskbuster.settings.test'
```

이런식으로 셋팅을 해줍니다. source 적용은 각 사용하고 있는 쉡에 alias로 단축키를 지정하면 간단히 사용 가능합니다.

- 현재 사용하고 있는 쉡 확인 : `echo $SHELL`
- zsh이라면 '~/.zshrc'에 `alias sv='source $VIRTUAL_ENV/bin/activate'`으로 단축키를 지정한다.
- 이제 해당 가상환경으로 들어가서 단축키만 누르면 각 가상환경별로 환경이 적용 된다.
- python manage.py runserver를 해보면 `Django version 2.1, using settings 'taskbuster.settings.test'`를 확인할 수 있습니다.

다른 탭을 열고 테스트를 실행해봅니다.

```
$ python functional_tests/all_user.py
```

당연히 테스트를 통과합니다.

## Production Settings – Debug False
기억해야 할 중요한 점은 프로덕션 settings 파일에 `DEBUG`를 False로 설정해야 합니다.

Note: Django 1.8 이전 버전에서는 'TEMPLATE_DEBUG'도 False로 설정해야 합니다.

먼저 'base.py' 설정 파일에서 DEBUG 변수를 잘라와서 'dev.py', 'test.py' 설정 파일이 붙여넣습니다. 그리고 'prod.py'에는 `DEBUG=False`로 설정합니다.

```
# base.py에서는 삭제
# dev.py, test.py에는 추가
DEBUG = True

# prod.py
DEBUG = False
```

이 방법으로 각 환셩은 변수의 올바른 값을 갖게 됩니다. staging.py 파일이 있는 경우도 마찬가지로 설정합니다.

## Django security and the Secret Key

'taskbuster/settings/base.py' 파일을 보면 `SECRET_KEY`라는 변수가 있습니다. 이 변수는 **비밀로 유지되어야** 하므로 **버전 제어에서 제외** 됩니다.

하나의 방법은 'base.py'를 '.gitignore'에 추가하는 것입니다. 하지만 프로젝트를 개발하는 동안 이 파일은 많은 변화가 있습니다. 특히 동료와 공유하려는 경우 유용하기 때문에 버전 관리에 포함시키는 것이 좋습니다. 따라서 더 나은 방법이 필요한데, 비밀 키 변수를 제거하고 다른 곳에서 가져오는 방법이 있습니다.그리고 다른 곳은 버전 제어에서 벗어나야 합니다.

여기서 다루는 접근법은 가상 황견 설정에 비밀 키를 넣고 'base.py' 파일에 가져와서 환경에서 키를 얻는 것입니다.

> Note: Apache에서는 동작하지 않습니다. 가장 좋은 방법은 비밀키를 파일에 저장하고 base.py로 가져오는 것입니다. 키 파일을 '.gitignore'에 포함시켜 버전 관리에서 제거합니다.(저는 이 방법을 애용하지만, 튜토리얼이니까.. 일단 따라해봅시다.)

가상 환경에 비밀 키를 포함시키기 위해 activate hook을 사용합니다.

'tb_dev' 환경을 활성화하고 'bin/activate'에 비밀키를 입력합니다.

```
$ vi %VIRTUAL_ENV/bin/activate
# '=' 기로 주위에 공백을 넣지 마세요.
export SECRET_KEY="your_secret_django_key"
```

이렇게 하고 다음을 입력하여 확인합니다.

```
$ pyenv local tb_dev
$ echo $SECRET_KEY
                     # 없음을 의미
$ sv                 # alias로 지정해둔 source 단축키
$ echo $SECRET_KEY
your_secret_django_key
```

'tb_test' 가상 환경에도 동일하게 적용하세요.

마지막으로 base.py에 `SECRET_KEY`를 제거하고, 다음 코드를 추가하세요.

```python
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_env_variable('SECRET_KEY')
```
`get_env_variable` 함수는 환경 변수 `var_name`을 얻으려고 시도하고, 찾지 못하면 `ImproperlyConfigured` 오류를 발생시킵니다.

```
django.core.exceptions.ImproperlyConfigured: Set the SECRET_KEY environment variable
```
이렇게하면 앱을 실행하려고 할때 `SECRET_KEY` 변수를 찾을 수 없으므로 프로젝트가 실패한 이유를 나타내는 메세지를 확인 할 수 있습니다.

이제 예상대로 작동하는지 확인합니다.

'tb_dev' 환경에서 개발서버를 실행합니다.

```
$ pyenv local tb_dev
$ sv      # alias로 source 적용한 단축키
$ python manage.py runserver
```

다른 터미널을 열어 'tb_test' 환경에서 기능 테스트를 실행합니다.

```
$ pyenv local tb_test
$ python functional_tests/all_user.py
```

```
Ran 1 test in 2.104s

OK
```

참고: 앱을 배포할 때 서버에 `SECRET_KEY`를 지정해야 합니다. 예를 들어, Heroku를 사용하는 경우 다음을 사용할 수 있습니다.

```
$ heroku config:set SECRET_KEY="your_secret_django_key"
```

튜토리얼 후반에 Heroku 진행을 다룰 것입니다.

## Initialize a Git Repository and Commit
쿨하게 패스.

`git add` 이후 커밋하고 싶지 않은 파일 제거하기

```
$ git rm --cached path_of_file
```

---
버전관리에 대해 좋은 내용이 많은 파트입니다. two scoops에 나오는 내용들이 적용되어 있습니다.
다만, 가상환경별 환경변수적용 부분은 따로 파일을 만들어서 적용하는게 협업에 더 잘 맞지 않나 생각합니다.
