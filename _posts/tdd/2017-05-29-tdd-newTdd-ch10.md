---
layout: post
section-type: post
title: new TDD-Chapter 10. Getting to a Production-Ready Deployment
category: tdd
tags: [ 'tdd' ]
---
ㅎ해킹 된 배포의 문제점은 무엇입니까? 생산을 위해 Django 개발 서버를 사용할 수 없고, "실제" 로딩을 위해 설계되지 않았습니다. Django 코드를 실행하기 위해 Gunicorn이라는 것을 사용할 것이고, Nginx는 정적 파일을 제공할 것입니다.

settings.py는 현재 `DEBUG = True`이며, 프로덕션 환경에 강력히 권장됩니다 (예를 들어, 사이트 오류가 발생했을 때 사용자가 코드의 디버그 추적을 원하지 않는 경우). 또한 보안을 위해 `ALLOWED_HOSTS`를 설정해야합니다.

서버가 재부팅 될 때마다 사이트가 자동으로 시작되기를 바랍니다. 이를 위해 `Systemd` 설정 파일을 작성합니다.

마지막으로, 8000 번 포트를 하드 코딩하면 서버에서 여러 사이트를 실행할 수 없기 때문에 "유닉스 소켓"을 사용하여 nginx와 Django 사이에서 통신합니다.

## 10.1. Switching to Gunicorn
Gunicorn은 "Green Unicorn"을 의미합니다. Django는 ORM, 다양한 미들웨어, 관리 사이트 등등 다양한 요소로 구성되어 있습니다. Django의 마스코트는 조랑말인데 조랑말을 이미 가지고 있다면 다음에 필요한 것은 유니콘입니다.

```
elspeth@server:$ ../virtualenv/bin/pip install gunicorn
```
Gunicorn은 application이라고 하는 함수를 가지고 있는 `WSGI` 서버 경로를 알고 있어야 합니다. Django는 wsgi.py 파일을 통해 이 함수를 제공합니다.

```
elspeth@server:$ ../virtualenv/bin/gunicorn superlists.wsgi:application
2013-05-27 16:22:01 [10592] [INFO] Starting gunicorn 0.19.7.1
2013-05-27 16:22:01 [10592] [INFO] Listening at: http://127.0.0.1:8000 (10592)
[...]
```
이제 사이트를 접속해보면, CSS가 전부 망가져 있는것을 볼 수 있습니다.  
> (캐시가 남아있기 때문에 CSS가 깨지는 것을 늦게 확인될 수도 있다.)

또한 FT를 실행하면 무엇가 잘못됐다는 것을 재차 확인할 수 있습니다. 아이템을 추가하는 테스트는 통과하지만, 레이아웃과 스타일링 테스트는 실패하고 있습니다. (잘했어 테스트!)

```
$ STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests
[...]
AssertionError: 125.0 != 512 within 3 delta
FAILED (failures=1)
```

CSS가 망가진 것은 Django 개발 서버가 정적 차일을 알아서 제공해주지만, Gunicorn은 그렇지 못하기 때문입니다. 이제는 Nginx에게 이것을 대신하도록 얘기해주어야 합니다.

![]({{ site.url }}/img/post/tdd/10_1.png)

## 10.2. Getting Nginx to Serve Static Files
먼저 `collectstatic`을 실행해서 모든 정적 파일을 Nginx가 찾을 수 있는 폴더에 복사합니다.

```
elspeth@server:$ ../virtualenv/bin/python manage.py collectstatic --noinput
elspeth@server:$ ls ../static/
base.css  bootstrap
```
이제 Nginx가 정적 파일을 제공할 수 있도록 설정해줍니다.

server: /etc/nginx/sites-available/staging.czarcie.com

```
server {
    listen 80;
    server_name staging.czarcie.com;

    location /static {
        alias /home/doky/sites/staging.czarcie.com/static;
    }

    location / {
        proxy_pass http://localhost:8000;
    }
}
```
Nginx와 Gunicorn을 재시작합니다.

```
elspeth@server:$ sudo systemctl reload nginx
elspeth@server:$ ../virtualenv/bin/gunicorn superlists.wsgi:application
```
다시 사이트에 접속해보면 훨씬 보기 좋아진 것을 알 수 있습니다. FT를 재실행해봅니다.

```
$ STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests
[...]

...
 ---------------------------------------------------------------------
Ran 3 tests in 10.718s

OK
```

## 10.3. Switching to Using Unix Sockets
스테이징과 운영 서버를 동시에 가동할 때는, 두 서버가 동시에 포트 8000을 사용할 수 없습니다. 서로 다른 포트를 사용하도록 설정할 수 있지만, 이 방식은 약간 자의적입니다. 또한 쉽게 스테이징 서버를 실제 운영 포트에서 가동한다던가, 그 반대의 경우도 발생할 수 있어서 위험하다고 할 수도 있습니다.

더 나은 해결책은 유닉스의 도메인 소켓을 이용하는 것입니다. 이것은 디스크상에 파일 형태로 존재하며, Nginx와 Gunicorn이 이 파일을 이용해서 서로 커뮤니케이션 할 수 있습니다.

server: /etc/nginx/sites-available/staging.czarcie.com

```
[...]
    location / {
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/staging.czarcie.com.socket;
    }
}
```
`proxy_set_header`는 Django와 Gunicorn이 어떤 도메인상에서 실행되고 있는지 알게 합니다. 이 설정 뒤에서 할 `ALLOWED_HOSTS` 보안 설정에도 사용됩니다.

Gunicorn을 재시작해보면 기본 포트가 아닌 소켓을 사용하고 있는 것을 알 수 있습니다.

```
elspeth@server:$ sudo systemctl reload nginx
elspeth@server:$ ../virtualenv/bin/gunicorn --bind \
    unix:/tmp/staging.czarcie.com.socket superlists.wsgi:application
```
FT를 실행해서 통과하는지 확인합니다.

```
$ STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests
[...]
OK
```

## 10.4. Switching DEBUG to False and Setting ALLOWED_HOSTS
Django의 DEBUG 모드는 서버를 해킹하기에 좋은 정보를 공개해버립니다. 하지만 이렇게 트레이스백 정보로 가득 찬 페이지를 그대로 공개하는 것은 보안상 좋지 않습니다.  

DEBUG 설정은 settings.py에서 할 수 있습니다. 이 항목을 False로 설정할 때는 `ALLOWED_HOSTS`라는 항목도 같이 설정해야 합니다.

server: superlists/settings.py

```
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

# Needed when DEBUG=False
ALLOWED_HOSTS = ['staging.czarcie.com']
[...]
```
Gunicorn을 재시작한 후 FT를 실행해서 동작 여부를 확인합니다.

> 이 작업은 서버에 커밋하지 않습니다. 현 시점에선 테스트 통과를 위한 임시 처방이기 때문에 굳이 리포지토리로 관리할 필요가 없습니다. 과정을 간단히 하기 위해, 로컬 PC 내용을 서버와 동기화하기 위해서만 Git 커밋을 하도록 합니다.(git push, pull)

## 10.5. Using Systemd to Make Sure Gunicorn Starts on Boot
마지막 과정은 서버 부팅 시 Gunicorn을 자동으로 가동시키는 것입니다. 또한 Gunicorn이 어떤 문제로 다운된 경우도 자동으로 재시작할 수 있도록 설정이 필요합니다. 우분투에서는 Upstart를 이용해서 이것을 구현할 수 있습니다.

server: /etc/systemd/system/gunicorn-staging.czarcie.com.service

```
[Unit]
Description=Gunicorn server for staging.czarcie.com

[Service]
Restart=on-failure  #1
User=doky  #2
WorkingDirectory=/home/elspeth/sites/staging.czarcie.com/source  #3
ExecStart=/home/elspeth/sites/staging.czarcie.com/virtualenv/bin/gunicorn \
    --bind unix:/tmp/staging.czarcie.com.socket \
    superlists.wsgi:application  #4

[Install]
WantedBy=multi-user.target #5
```
Upstart는 설정이 쉽고(특히 init.d 스크립트를 편집해본 경험이 있는 사람은 더 그렇게 느낄 것입니다.), 구문만 보고도 어떤 처리를 하고 있는지 이해할 수 있습니다.

> #1 : `Restart=on-failure`시 충돌이 발생하면 자동으로 프로세스가 시작됩니다.  
> #2 : `User=doky`는 프로세스를 'doky' 사용자로 실행합니다.
> #3 : `WorkingDirectory`는 현재 작업 디렉토리를 설정합니다.
> #4 : `ExecStart`는 실행할 실제 프로세스입니다. `\`줄 연속 문자를 사용하여 가독성을 위해 여러 줄로 전체 명령을 분할하지만 모두 한 줄로 나갈 수 있습니다.
> #5 : `[install]`섹션 안의 `WantedBy`은 `Systemd`가 부팅 할 때 이 서비스를 시작하도록 알려줍니다.

`Systemd` 스크립트는 `/etc/systemd/system`에 있으며 이름은 `.service`로 끝나야합니다.  

이제 `systemd` 명령으로 Gunicorn을 시작하도록 `Systemd`에 지시합니다.

```
# 이 명령은 새로운 설정 파일을 로드하도록 Systemd에게 알려줍니다.
elspeth@server:$ sudo systemctl daemon-reload
# 이 명령은 부팅시 항상 서비스를 로드하도록 Systemd에게 지시합니다.
elspeth@server:$ sudo systemctl enable gunicorn-staging.czarcie.com
# 이 명령은 실제로 서비스를 시작합니다.
elspeth@server:$ sudo systemctl start gunicorn-staging.czarcie.com
```
(systemctl 명령이 서비스 이름을 포함하여 탭 완성에 응답함을 발견해야 합니다.)

FT를 다시 실행하여 모든 것이 여전히 작동하는지 확인 할 수 있습니다. 서버를 재부팅하면 사이트가 다시 작동하는지 테스트 할 수도 있습니다.



### More Debugging Tips

- sudo journalctl -u gunicorn-staging.czarcie.com을 사용하기 위해 Systemd 로그를 확인하세요.
- Systemd에 서비스 구성의 유효성을 확인하도록 요청할 수 있습니다. : systemd-analyze verify /path/to/my.service
- 변경 사항이있을 때마다 두 서비스를 다시 시작해야합니다.
- Systemd 설정 파일을 변경하면 systemctl을 재시작하기 전에 daemon-reload를 실행하여 변경 사항의 영향을 확인해야합니다.


### Saving Our Changes: Adding Gunicorn to Our requirements.txt
로컬 리포지토리로 돌아와서 Gunicorn을 virtualenv의 패키지 리스트에 추가하도록 합니다.

```
$ pip install gunicorn
$ pip freeze | grep gunicorn >> requirements.txt
$ git commit -am "Add gunicorn to virtualenv requirements"
$ git push
```

## 10.6. Thinking about Automating
프로비저닝 및 배포 절차를 다시 정리합니다.

*Provisioning*  
 1. 사용자 계정과 홈 폴더가 있다고 가정합니다.
 2. `add-apt-repository ppa:fkrull/deadsnakes`
 3. `apt-get install nginx git python3.6 python3.6-venv`
 4. 가상 호스트를 위한 Nginx 설정을 추가합니다.
 5. Gunicorn을 위한 Upstart 처리를 추가합니다.

*Deployment*  
 1. `~/sites`에 디렉터리 구조를 생성합니다.
 2. `source` 폴더에 소스 코드를 저장합니다.
 3. `../virtualenv`에 있는 virtualenv를 시작합니다.
 4. `pip install -r requirements.txt`
 5. 데이터베이스를 위한 `manage.py migrate`를 실행합니다.
 6. 정적 파일을 위한 `collectstatic`
 7. settings.py 파일의 `DEBUG = False` 및 `ALLOWED_HOSTS`를 설정합니다.
 8. Gunicorn을 재시작합니다.
 9. FT를 실행해서 정상적으로 동작하는지 확인합니다.

아직 전체프로비저닝 처리를 자동화할 준비가 돼있지 않은 상태에서 지금까지 한 작업을 어떻게 저장할 수 있을까요? Nginx와 Upstart 설정 파일을 어딘가에 저장해서 이후에 재사용할 수 있도록 해두는 것이 필요합니다. 리포지토리의 서브 폴더에 저장해둡니다.

### Saving templates for our provisioning config files

```
$ mkdir deploy_tools
```

deploy_tools/nginx.template.conf

```
server {
    listen 80;
    server_name SITENAME;

    location /static {
        alias /home/elspeth/sites/SITENAME/static;
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/SITENAME.socket;
    }
}
```

deploy_tools/gunicorn-systemd.template.service

```
[Unit]
Description=Gunicorn server for SITENAME

[Service]
Restart=on-failure
User=elspeth
WorkingDirectory=/home/elspeth/sites/SITENAME/source
ExecStart=/home/elspeth/sites/SITENAME/virtualenv/bin/gunicorn \
    --bind unix:/tmp/SITENAME.socket \
    superlists.wsgi:application

[Install]
WantedBy=multi-user.target
```
이후에 신규로 사이트를 생성할 때는 이 설정 파일의 `SITENAME` 부분만 찾아서 수정해주면 됩니다.

나머지 작업 과정은 메모로 남겨두기만 해도 충분합니다. 작업 과정을 텍스트 파일로 기록해둔 후 리포지토리에 보관합니다.


deploy_tools/provisioning_notes.md

```
Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

ex. Ubuntu에서 실행하는 방법:

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual Host config

* nginx.template.conf 참고
* SITENAME 부분을 다음과 같이 수정 staging.my-domain.com

## Systemd service(Upstart)

* gunicorn-systemd.template.service 참고
* SITENAME 부분을 다음과 같이 수정 staging.my-domain.com

## Folder structure:
사용자 계정의 홈 폴더가 /home/username 이라고 가정

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
```

작업 및 메모한 것을 커밋합니다.

```
$ git add deploy_tools
$ git status # see three new files
$ git commit -m "Notes and template config files for provisioning"
```
여기까지의 폴더 구조는 다음과 같습니다.

```
.
├── deploy_tools
│   ├── gunicorn-systemd.template.service
│   ├── nginx.template.conf
│   └── provisioning_notes.md
├── functional_tests
│   ├── [...]
├── lists
│   ├── __init__.py
│   ├── models.py
│   ├── [...]
│   ├── static
│   │   ├── base.css
│   │   └── bootstrap
│   │       ├── [...]
│   ├── templates
│   │   ├── base.html
│   │   ├── [...]
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── superlists
    ├── [...]
```

## 10.7. Saving our Progress

스테이징 서버에서 FT를 실행해서 정상 동작 여부를 확인할 수 있습니다. 하지만 대부분의 경우, "진짜" 서버에서 FT 실행을 원하지 않을 것입니다. "작업한 것을 보호"하고, 운영 서버가 스테이징 서버만큼 제대로 동작하는지 확인하기 위해서는 배포과정을 반복해서 실시할 수 있는 구조가 필요합니다.

자동화는 다음 섹션에서 다룹니다.
