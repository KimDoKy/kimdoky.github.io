---
layout: post
section-type: post
title: gunicorn service 등록하기
category: deploy
tags: [ 'deploy' ]
---

서버를 재부팅시, 서버에서 실행되던 애플리케이션 서버도 같이 재실행되어야 합니다.  

우분투에서는 service를 등록하면 됩니다.

---

## Service 등록 방법

>
gunicorn 으로 예를 듭니다.
[점프 투 장고](https://wikidocs.net/76904#_3)에서 친절히 설명해주고 있고,  
개인적으로 위 방법을 응용하는 방법을 기술합니다.

### gunicorn 설정

gunicorn의 설정을 작성합니다.

```python
# root of project
# gunicorn.conf.py

bind = "0.0.0.0:8000" # local
workers = 3
accesslog = "./log/gunicorn.access.log"
errorlog = "./log/gunicorn.error.log"
capture_output = True
loglevel = "info"
```

### gunicorn 설정 적용하여 실행하기

service로 등록하지 않고 바로 실행하여 설정이 잘 적용되었는지 확인합니다.

```bash
$ gunicorn conf.wsgi:application -c ./gunicorn.conf.py
```

### service 파일 작성

```bash
# /etc/systemdsystem/myapp.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/srv/Server
ExecStart=gunicorn conf.wsgi-prod:application -c ./gunicorn.conf.py

[Install]
WantedBy=multi-user.target
```

'점프 투 장고'에서 설명하는 방법과 거의 동일하지만, gunicorn의 설정 부분을 따로 분리하여 설정이 약간 깔끔해집니다.  

### service 등록

```bash
// service 시작
$ sudo systemctl start myapp.service

// service가 실행중일때
$ sudo systemctl deamon-reload

// 실행된 service 상태 체크
$ systemctl status myapp.service

// 자동 실행 등록(재부팅시 자동 실행)
$ sudo systemctl enable myapp.service
```

서버를 재부팅해보면 애플리케이션 서버도 같이 재실행이 됨을 확인할 수 있습니다.
