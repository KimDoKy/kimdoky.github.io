---
layout: post
section-type: post
title: Linux - ubuntu에서 pip으로 package 설치 실패 시
category: tip
tags: [ 'tip' ]
---

ubuntu 20.04.2 에서 pip으로 package 설치 실패 시  

구글링하면 `--user` 옵션으로 설치하라고 했지만, 해결이 되지 않는 것으로 보아 제가 만난 에러는 다른 종류인듯 합니다.  

일단 출시일이 급하니까 자세한 원인은 나중에..


### wheel 설치 실패

- apt-get update 확인
- 작업 디렉터리의 권한 확인

### mysqlclient 를 설치하는 중 에러

```
...
error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
...
```

apt-get 으로 mysqlclient를 설치해도 동일한 에러 발생

해결법

```bash
$ sudo apt-get install python3-dev
$ sudo apt-get install build-essential
$ sudo apt-get install libmysqlclient-dev
```

apt로 라이브러리 추가 설치시 마지막에 꼭 한번 더 update를 해야 함.


[stackoverflow](https://stackoverflow.com/questions/33315210/error-command-x86-64-linux-gnu-gcc-when-installing-mysqlclient/33315233)
