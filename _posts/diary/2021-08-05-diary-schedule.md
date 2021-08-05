---
layout: post
section-type: post
title: 개발 고민 - 스케쥴러, crontab
category: diary
tags: [ 'diary' ]
---

## 개요

이번 프로젝트에서 객체가 시간에 흐름에 따라 상태를 변경하고 FCM을 발송하고 포인트를 계산하는 등의 비동기 작업이 필요하게 되었다.  

처음 생각한 구상은 Redis나 RabbitMQ에 Queue로 처리해야 할 객체를 추가하고, Queue가 추가되면 Celery으로 비동기 작업을 수행하는 것이였다.  

하지만 위 구성은 기능에 비해 오버 스팩이라 판단하여 좀 더 작게 구성하려고 고민하였고, python으로 스크립트로 처리하기로 하였다.

## 진행

해당 작업을 30초마다 반복하고, 비동기로 처리하기 위해 `schedule`과 `Thread`를 사용하기로 하였다.

```python
from threading import Thread
import schedule

class Command(BaseCommand):
     def handle(self, *args, **options):
         try:
             schedule.every(30).seconds.do(self.thread_run)
             schedule.run_pending()
             while True:
                 schedule.run_pending()
             self.thread_run()
         except:
             print(sys.exc_info())
```

해당 객체의 상태에 따라 잘 동작하고, DB에도 잘 적용되었다.  

하지만 해당 스크립트를 실행하면 맥북이 뜨거워짐을 느꼈고, 테스트 서버에 배포후 cpu 상태를 점검해보니 99% 까지 사용량이 치솟았다.  

## 개선

그래서 더 가벼운 방법을 고민하였고, crontab 으로 처리하기로 하였다.  

crontab 의 최소 실행주기는 1분이였다. 그래서 crontab에 바로 등록하는게 아니라, 간단한 쉘 스크립트를 작성하여 crontab에 등록하기로 하였다.


```bash
#!/bin/bash
SLEEP=30
SHELL_PATH=`pwd -P`

for i in $(seq $((60/$SLEEP))); do
    python3 ${SHELL_PATH}/manage.py reserv_thread
    sleep ${SLEEP};
done
```

> python3 의 명령어는 가상환경때문에 세부 경로를 지정하였었는데 정상 동작하지 않았다. python3 으로 그냥 입력하면... 정상동작.. 음.. 

#### crontab의 간단 사용법

##### 서비스 등록

```bash
# /etc/crontab

# 추가할 작업 추가
# 분 - 시 - 일 - 월 - 요일 - 사용자 - 실행명령
* * * * * zen /bin/sh /home/zen/Documents/Server/thread.sh
```

```bash
# crontab 실행
$ service cron start

# crontab 이 실행중이라면 리로드
$ systemctl daemon-reload

# crontab 상태 체크
$ systemctl status cron.service
$ service cron status  (같은 명령)
```

> service는 Centos 6 이전, systemctl은 Centos 7 이후에서 제어한다. 어떤걸 사용해도 무방

## 결과

모니터링은 아이패드의 ServerCat 이라는 어플을 사용하고 있는데, 인터페이스도 심플해서 애용하고 있다.

![]({{ site.url }}/img/post/diary/other/servercat.jpg)

위 사진처림 cpu 사용량이 2% 까지 내려가게 되었다.  

crontab 애용하자....ㅋㅋ
