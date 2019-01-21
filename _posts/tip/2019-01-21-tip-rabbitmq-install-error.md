---
layout: post
section-type: post
title: tip. RabbitMQ 설치시 sbin 디렉토리가 없다?
category: tip
tags: [ 'tip' ]
---


## RabbitMQ를 설치해보자.

MacOS에서 RabbitMQ의 설치와 관련된 글(공식 사이트 포함)을 보면 brew로 설치하고, .bash_profile 을 설정하는 것만 나와있다.

#### 설치

```
$ brew install rabbitmq
```

#### PATH 설정
```
PATH=$PATH:/usr/local/sbin
```

#### 실행

```
rabbitmq-server
```

## 하지만 에러를 만났다.

rabbitmq 명령어가 없다는 에러가 발생한다.

PATH 설정의 sbin 디렉터리의 유무를 보니... 없다.

MacOS 시에라 이상 버전에서는 sbin 디렉토리가 없는 것 같다.  
(시에라 이하 버전에서는 확인을 못했기 때문에 그렇게 추측된다.)

그래서 brew를 삭제하고 재설치한다고 하여도 해결되지 않는다.

```
Error: The `brew link` step did not complete successfully
The formula built, but is not symlinked into /usr/local
Could not symlink sbin/cuttlefish
/usr/local/sbin is not writable.

You can try again using:
  brew link rabbitmq
  ...
```

## 해결법

다행히 [STACK OVERFLOW
](https://stackoverflow.com/questions/23050120/rabbitmq-command-doesnt-exist)에서 해결법을 찾을 수 있다.

#### 일단 다시 설치

```
$ brew install rabbitmq
```

#### 설치 버전 확인

```
ls /usr/local/Cellar/rabbitmq/
```
위 경로에서 알 수 있듯이 설치 경로가 다르다!! 이것이 오류의 원인.

#### PATH 설정

```
export PATH=/usr/local/Cellar/rabbitmq/<version>/sbin:$PATH
```

## 이제 실행해보자!

```
$ rabbitmq-server

  ##  ##
  ##  ##      RabbitMQ 3.7.10. Copyright (C) 2007-2018 Pivotal Software, Inc.
  ##########  Licensed under the MPL.  See http://www.rabbitmq.com/
  ######  ##
  ##########  Logs: /usr/local/var/log/rabbitmq/rabbit@localhost.log
                    /usr/local/var/log/rabbitmq/rabbit@localhost_upgrade.log

              Starting broker...
 completed with 6 plugins.
^CStopping and halting node rabbit@localhost ...
```

굳!!
