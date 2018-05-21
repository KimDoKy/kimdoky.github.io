---
layout: post
section-type: post
title: jupyter notebook 원격 접속하기
category: tip
tags: [ 'tip' ]
---

# jupyter notebook 원격 접속하기

나의 pc의 jupyter notebook를 외부에서 접속할때 패스워드만 입력하면 접속이 가능하다.

그전에 설정을 해 주어야 할 것들이 있다.

## 패스워드 설정하기

jupyter notebook을 실행 후 python으로 설정한다.

```python
from notebook.auth import passwd

passwd()

» Enter password: ....
» Verify password: ....
'sha1:...............'
```

## 패스워드 적용하기

```
>> jupyter notebook --generate-config
Writing default config to : PATH\jupyter_notebook_config.py
```

해당 경로의 설정파일에 패스워드를 설정해준다.

```
c.NotebookApp.password = u'sha1:.....'
```

## 외부 접속이 가능하도록 ip와 port트 설정하여 서버 실행하기

```
$ jupyter notebook --ip=0.0.0.0 --port=8001
# 테스트로 8001 포트로 포워딩 해 둠
```

> 일단 외부에서 접속이 가능하도록 포트포워딩등은 설정해주어야 한다.


그럼 셋팅한 도메인으로 접속하면 패스워드 입력하라는 창이 나오게 된다.

패스워드만 입력하면 끗.
