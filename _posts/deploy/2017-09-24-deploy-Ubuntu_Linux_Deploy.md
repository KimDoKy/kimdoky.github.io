---
layout: post
section-type: post
title: Deploy - Ubuntu Linux Deploy
category: deploy
tags: [ 'deploy' ]
---

> AWS EC2 + Ubuntu + Nginx + uWSGI + Django

## 개념
### Ubuntu Linux
서버의 OS
### Nginx
웹 서버. 클라이언트로부터의 HTTP 요청을 받아 정적인 페이지/파일을 돌려줍니다.
### Django
웹 애플리케이션. 웹 요청에 대해 동적 데이터를 돌려줍니다.
### uWSGI
웹 서버(Nginx)와 웹 애플리케이션(Django)간의 연결을 중계해줍니다.  
(Nginx에서 받은 요청을 Django에서 처리하기 위한 중계 역할을 합니다.)
### WSGI
Web Server Gateway Interface  
파이썬에서 웹 서버와 웹 애플리케이션 간의 동작을 중계해두는 인터페이스입니다.

## Path 요약(server)
### Nginx 동작
```
/etc/nginx/nginx.conf
```
### Nginx 가상서버 설정 파일
```
/etc/nginx/sites-available/app
```
### uWSIG 사이트 파일
```
/etc/uwsgi/sites/app.ini
```
### uWSGI 서비스 설정 파일
```
/etc/systemd/system/uwsgi.service
```
### Nginx log 파일
```
/var/log/nginx
```
### Socket ,pid
```
/tmp/
```

## Instance 생성
1. AWS에서 KeyPair 다운받은 후 `~/.ssh`으로 복사후 권한 설정  
```
chmod 400 KeyPair.pem
```  
2. 권한 설정 후 pem파일을 통해 AWS에 접속  
```
ssh -i ~/.ssh/KeyPair.pem ubuntu@ec2-13-124....compute.amazonaws.com
```
3. 언어팩 설치  
```
sudo apt-get install language-pack-ko
sudo locale-gen ko_KR.UTF-8
```

## Ubuntu 기본 설정
> 서버에 기본 설치 하기 전에

1. 패키지 인덱스 정보를 업데이트
```
sudo apt-get update
```
2. python-pip 설치
```
sudo apt-get install python-pip
```
3. zsh 설치
```
sudo apt-get install zsh
```
4. oh-my-zsh 설치
```
sudo curl -L http://install.ohmyz.sh | sh
```
5. Default Shell 변경
```
sudo chsh ubuntu -s /usr/bin/zsh
```
6. 서버 종료 후 재 접속
`l` 명령어로 `zsh`이 잘 되어있는지 확인
7. pyenv requirements 설치  
[공식문서](https://github.com/pyenv/pyenv/wiki/Common-build-problems){:target=`_`blank}  
```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils
```
8. pyenv 설치
```
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

9. pyenv 설정 .zshrc 에 기록
```
vi ~/.zshrc
```
```
export PATH="/home/ubuntu/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```
```
source ~/.zshrc
```
`pyenv`를 입력하여 잘 나오는지 확인
10. Pillow 라이브러리 설치 (이미지 처리)
```
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
```

## Django 관련 설정
1. 권한 설정 (서버 루트에서)
```
sudo chown -R ubuntu:ubuntu /srv/
```
> [관련 설명](http://www.thegeekstuff.com/2010/09/linux-file-system-structure/?utm_source=tuicool){:target=`_`blank}

2. AWS 업로드 (서버 : srv안에 app폴더 생성)

- 로컬에서 업로드
```
scp -r -i ~/.ssh/KeyPair.pem . ubuntu@ec2-13-124-46-220.ap-northeast-2.compute.amazonaws.com:/srv/app/
```
> -r :[recursive]. 폴더안쪽까지 모두 전송. :현재폴더

- Git으로 업로드
```
git clone <프로젝트>
```

## 서버 환경 설정
1. pyenv 3.5.2 설치 (서버 /srv/ 에서)
```
pyenv install 3.5.2
```
2. 가상환경 설정 (서버 /srv/app/ 에서)
```
pyenv virtualenv 3.5.2 가상환경명
```

3. requirements 설치
```
pip install -r requirements.txt
```
> 가상환경내에서 설치가 된것인지 반드시 확인해야합니다. 서버에 재접속해서 확인해보면 가상환경에 설치가 되지 않는 버그가 존재합니다.
`/srv/`에는
```
pip (9.0.1)
setuptools (20.7.0)
wheel (0.29.0)
```
위 목록만 설치되어야 합니다.

4. 서버 구동 확인 (서버 내에 프로텍즈 경로에서)
```
python manage.py runserver 0.0.0.0:8000
```

5. AWS Security Groups 8080 Port 추가(AWS에서)  
Security Groups -> Inbound -> Edit -> Custom TCP Rule -> 8000

6. ALLOWED_HOSTS 설정
```
vi mysite/settings.py
```
```
ALLOWED_HOSTS = [
    '<ec2 domain name>',
    또는
    '.amazonaws.com'
]
```
> `DisallowedHost at /` error는 `ALLOWED_HOSTS` 작업을 안하면 발생합니다.

7. 설치된 패키지 업데이트
```
sudo apt-get dist-upgrade
sudo shutdown -r now
```
> 재접속하는게 시간이 꽤 소요됩니다.(의존성을 검사하며 설치)  
error `port 22: Operation timed out`는 서버가 재가동중이라서 timed out error가 발생합니다. 재접속하면 업데이트 할 내용과 재시작해야 한다는 메세지가 없어집니다.

## uWSGI 관련 설정
### 웹 서버 관리용 유저 생성
```
sudo adduser www-data
```
> (default로 'www-data'으로 만들어져 있음)

### uWSGI 설치
`srv/app/`에서
```
pip install uwsgi
```
### uWSGI 정상 동작 확인
```
uwsgi --http :8000 --home ~/.pyenv/versions/(가상환경명) --chdir /srv/app/django_app -w (가상환경).wsgi
```
ex)
```
uwsgi --http :8000 --home ~/.pyenv/versions/czarcie --chdir /srv/app/django_app -w czarcie.wsgi
```
> 실행 후 8000 포트로 접속하여 요청을 잘 받는지 확인해야합니다. 경로를 입력할 때는 tap을 이용해서 자동 완성으로 입력하세요.

### uWSGI 사이트 파일 작성
```
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/sites
sudo vi /etc/uwsgi/sites/app.ini

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

### uWSGI site 파일로 정상 동작 확인
```
sudo /home/ubuntu/.pyenv/versions/czarcie/bin/uwsgi --http :8000 -i /etc/uwsgi/sites/app.ini
```

![](https://github.com/KimDoKy/FastCamp/raw/master/Deploy/images/uwsgi.png)

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

## Nginx 관련 설정
### Nginx 안정화 최신버전 사전셋팅 및 설치
```
sudo apt-get install software-properties-common python-software-properties
sudo add-apt-repository ppa:nginx/stable
sudo apt-get update
sudo apt-get install nginx
nginx -v
```
### Nginx 동작 User 변경
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
### sites-enabled의 default파일 삭제
```
sudo rm /etc/nginx/sites-enabled/default
```
> `/etc/nginx/nginx.conf` 파일에 어떤 폴더에 있는 설정을 가져와서 실행할지 나와있습니다.

### uWSGI, Nginx 재시작
```
sudo systemctl restart uwsgi nginx
```

#### 시스템에서 현재 수행되고 있는 프로세스 확인
```
ps -ax | grep uwsgi
```
#### 파일이나 디렉터리를 삭제 후에는 더 이상 파일을 참조하지 않고 system 복사본을 사용하도록 systemd 프로세스를 다시 로드해야 합니다.
```
sudo systemctl daemon-reload
```

## IAM User 생성
**IAM**(AWS Identity and Access Management) : 사용자를 위해 AWS 리소스에 대한 액서스를 안전하게 제어할 수 있는 웹서비스입니다. IAM을 사용하여 AWS 리소스를 사용할 수 있는 사람(인증)과 이들이 사용할 수 있는 리소스 및 권한을 제어합니다.

AWS - IAM - add User
![](https://github.com/KimDoKy/FastCamp/raw/master/Deploy/images/iam1.png)
![](https://github.com/KimDoKy/FastCamp/raw/master/Deploy/images/iam2.png)
> 권한은 연습이기 때문에 FullAccess로 설정했습니다.

![](https://github.com/KimDoKy/FastCamp/raw/master/Deploy/images/iam3.png)
![](https://github.com/KimDoKy/FastCamp/raw/master/Deploy/images/iam4.png)
> `secret_key`는 다시 볼 수 없기 때문에 반드시 저장해둡니다.

### AWS 명령줄 인터페이스 설치
**CLI** 는 AWS 서비스를 관리하는 통합 도구입니다.  
도구 하나만 다운받아 구성하면 여러 AWS 서비스를 명령중에서 제어하고 스크립트로 자동화 할 수 있습니다.  

(로컬 가상환경에서)  
```
pip install awscli
aws configure
```
```
AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]: ap-northeast-2
Default output format [None]: json
```
> AWS에서 Services - IAM 에서 `Access Key` 확인 가능

`~/.aws` 에서 잘 저장 되었는지 확인 가능합니다.
```
cd ~/.aws
vi config
vi credentials
```

#### 재접속할 때 서버접속 정보 확인을 물어본다면?
![](https://github.com/KimDoKy/FastCamp/raw/master/Deploy/images/finger.png)

(로컬 가상환경에서)
```
aws ec2 get-console-output --instance-id i-instance_id
```
BEGIN SSH HOST KEY FINGERPRINTS 검색  
**SHA256** 으로 시작하는 부분으로 확인이 가능합니다.

### AWS Security Groups 80 Port 추가
Security Groups -> Inbound -> Edit -> HTTP  
**Instance 주소로 접속하여 Hello, World 확인**

## error 찾기
### systemctl restart시 오류 발생 시
```
(오류 발생한 서비스에 따라 아래 명령어 실행)
sudo systemctl status uwsgi.service
sudo systemctl status nginx.service
```
### 502 Bad Gateway
Nginx log 파일 확인
```
➜  nginx pwd
/var/log/nginx
➜  nginx sudo rm *.log
➜  nginx sudo systemctl daemon-reload
➜  nginx sudo systemctl restart nginx
➜  nginx sudo systemctl restart uwsgi
➜  nginx cat error.log
```
### Nginx log파일에서 sock파일 접근 불가시
socket파일 권한 소유자 확인
```
cd /tmp
ls -al
-rw-r--r--  1 nginx  nginx     6 Nov  8 06:58 app.pid
srw-rw-rw-  1 nginx  nginx     0 Nov  8 06:58 app.sock

nginx가 소유자가 아닐 경우,
sudo rm app.pid app.sock으로 삭제 후 서비스 재시작

sudo chown -R username:username filename 으로 권한을 직접 변경후 재시작해도 해결 됨
```

## Cloudflare
### ALLOWED_HOSTS 추가

## SSL
[Nginx에 SSL적용](https://haandol.wordpress.com/2014/03/12/nginx-ssl-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0startssl-com%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%97%AC/){:target=`_`blank}  
[Cloudflare에 Custom SSL적용](https://support.cloudflare.com/hc/en-us/articles/200170466-How-do-I-upload-a-custom-SSL-certificate-Business-or-Enterprise-only-){:target=`_`blank}
