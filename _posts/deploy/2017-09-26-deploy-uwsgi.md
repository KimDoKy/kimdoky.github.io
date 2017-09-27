---
layout: post
section-type: post
title: Deploy - uWSGI + Nginx + Ubuntu 14.04
category: deploy
tags: [ 'deploy' ]
---

Django 애플리케이션을 배포하기 위해서는 uWSGI와 Nginx에 대한 이해가 필요합니다.  
Django 애플리케이션을 위한 uWSGI 애플리케이션 컨테이너 서버에 대해서 설정하고, uWSGI와의 역프록시를 위한 Nginx를 설치해서 Django 애플리케이션의 보안과 성능을 높일 수 있습니다.

- WSGI(Web Server Gateway Interface) : 파이썬에서 애플리케이션이 웹 서버와 통신하기 위한 명세입니다. WSGI는 서버와 얍 양단으로 나누어져 있는데, WSGI request를 처리하면 서버에서 환경정보와 콜백함수를 앱에 제공해야 합니다. 앱은 그 요청을 처리하고 콜백함수를 통해 서버에 응답합니다.

- Nginx : Apache 다음으로 차세대 웹서버로 불립니다. Apache는 많은 기능을 갖고 있지만 대신 무겁습니다. Nginx는 자주 사용하는 기능만 사용하기 때문에 더 작은 자원으로 더 빠르게 데이터를 서비스 할 수 있습니다.

## uWSGI 애플리케이션 서버 설정하기

uWSGI는 Django 애플리케이션과 WSGI라는 표준 인터페이스로 통신하는 애플리케이션 서버입니다.

### uWSGI 설치하기
설치하기에 앞서 uWSGI와 의존성이 있는 Python Development 파일을 먼저 설치합니다.
```
sudo apt-get install python-dev
```

development 파일이 설치되면, pip를 통해 uWSGI를 설치합니다.

```
sudo pip install uwsgi
```

설치 후 uWSGI를 간단하게 테스트해 볼 수 있습니다.
```
uwsgi --http :8000 --home ~/.pyenv/versions/(가상환경명) --chdir /srv/app/(장고앱) -w (가상환경).wsgi
```

### 설정파일 생성하기
전체 시스템에 적용되어야 하기 때문에 `/etc/uwsgi/sites/` 폴더를 생성하고 설정파일을 작성합니다.

```
sudo mkdir -p /etc/uwsgi/sites
cd /etc/uwsgi/sites
```
```
vi app.ini

[uwsgi]
chdir = /srv/app/django_app # Django application folder
module = czarcie.wsgi:application # Django project name.wsgi
home = /home/ubuntu/.pyenv/versions/czarcie # VirtualEnv location

uid = www-data
gid = www-data

socket = /tmp/app.sock
chmod-socket = 666
chown-socket = www-data:www-data

enable-threads = true
master = true
pidfile = /tmp/app.pid
```
설정파일의 시작은 `[uwsgi]`으로 시작해야하고 모든 설정은 이 섹션아래에 기술되어야 합니다.  
`chdir` : 프로젝트 경로
`module` : 프로젝트와 어떻게 상호 작용할지를 설정합니다.(프로젝트에 있는 wsgi.py에서 'application'을 임포트합니다.)  
`home` : 가상환경의 경로를 설정합니다.  
`uid` : user id . 사용자 식별자. 리눅스에서는 사용자를 식별하는데 유저 아이디로 구분합니다.
`gid` : group id . 그룹 식별자. 리눅스에서는 그룹을 통해서 사용자를 묶을 수도 있습니다.
`socket` : 모든 모듈이 하나의 서버에서 동작하기 때문에, 네트워크 포트 대신 유닉스소켓을 사용합니다.  
`vacuum` : 서버가 멈추면 자동으로 소켓 파일이 삭제하는 옵션

가이드 따라해보기

https://www.digitalocean.com/community/tutorials/how-to-set-up-uwsgi-and-nginx-to-serve-python-apps-on-ubuntu-14-04#definitions-and-concepts
