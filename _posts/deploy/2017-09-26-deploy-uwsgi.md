---
layout: post
section-type: post
title: Deploy - uWSGI + Nginx settings
category: deploy
tags: [ 'deploy' ]
---

## uWSGI

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
`chown` : 파일의 소유권을 바꿉니다.
`enable-threads` : uWSGI는 processes를 통해 worker의 수를 지정할 수 있고, `threads`를 통해 worker당 동작할 thread 수를 지정할 수 있습니다. 이 옵션은 thread로 동작을 활성화 하는 옵셥입니다.  
`vacuum` : 서버가 멈추면 자동으로 소켓 파일이 삭제하는 옵션  
`pidfile` : 서버가 동작할 때 생기는 프로세스의 PID를 기록하는 파일 위치를 지정합니다. (`pid`는 각 프로세스/스레드를 구분해주는 번호입니다.)

### uWSGI 서비스 설정파일 작성

```
sudo vi /etc/systemd/system/uwsgi.service

[Unit]
Description=uWSGI Emperor service
After=syslog.target

[Service]
ExecPre=/bin/sh -c 'mkdir -p /run/uwsgi; chown username:username /run/uwsgi'
ExecStart=/home/ubuntu/.pyenv/versions/mysite/bin/uwsgi --uid www-data --gid www-data --master --emperor /etc/uwsgi/sites

Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```


## Nginx

### Nginx 안전화 최신버전 사전 셋팅 및 설치

```
sudo apt-get install software-properties-common python-software-properties
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update
sudo apt-get install nginx
nginx -v
```

### Nginx 동작 user 변경

```
sudo vi /etc/nginx/nginx.conf
user www-data
```

### Nginx 가상서버 설정 파일 작성

```
sudo vi /etc/nginx/sites-available/app

server {
    listen 80;
    server_name localhost;
    charset utf-8;
    client_max_body_size 128M;


    location / {
        uwsgi_pass    unix:///tmp/app.sock;
        include       uwsgi_params;
    }
}
```

### 설정파일 심볼릭 링크 생성

```
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/app
```

### SITES-ENABLED의 DEFAULT파일 삭제

```
sudo rm /etc/nginx/sites-enabled/default
```

## uWSGI, Nginx 재시작

```
sudo systemctl restart uwsgi nginx
```

#### 시스템에서 현재 수행되고 있는 프로세스 확인

```
ps -ax | grep uwsgi
```

> 파일이나 디렉터리를 삭제 후에는 더 이상 파일을 참조하지 않고 system 복사본을 사용하도록 systemd 프로세스를 다시 로드해야 합니다.
```
sudo systemctl daemon-reload
```

그냥 날 잡아서 uWSGI 문서 번역이나 해봐야겠네요.
