---
layout: post
section-type: post
title: pyDjango - chap6. 가상 환경 사용하기 - virtualenv
category: django
tags: [ 'django' ]
---

독립된 가상환경이 필요한 이유는 인터넷에서 다운로드한 파이썬 라이브러리들이 충돌하는 것을 방지하기 위함입니다. 외부의 라이브러리들은 서로 의존성을 갖고 있는 경우가 많아 버전이 맞지 않는 경우 오작동을 일으킵니다.

## 6.1 virtualenv 설치

**which** 명령으로 virtualenv 명령의 경로를 찾습니다.
```
$ which virtualenv
/usr/local/var/pyenv/shims/virtualenv
```

만일 설치되지 않았다면

```
pip install virtualenv
```

나머지는 생략..

## 6.2 가상 환경 vDjBook 구성

pass

## 6.3 가상 환경에 장고 설치하기

```
pip install django
```
## 6.4 가상 환경에 pytz 설치하기

pytz 는 타임존을 관리하는 패키지입니다.

```
pip install pytz
```

## 6.5 가상 환경에 django-tagging 설치하기

django-tagging 패키지는 태그 기능을 제공합니다.

```
pip install django-tagging
```

## 6.6 가상 환경에 django-disqus 설치하기

django-disqus 패키지는 댓글기능을 제공합니다.

## 6.7 가상 환경에 Pillow 설치하기

Pillow 패키지는 이미지를 처리합니다.

## 6.8 가상 환경의 패키지 설치 툴 업그레이드

가끔 설치 툴의 버전이 낮아 에러가 발생할 수 있습니다.

```
pip install -U pip wheel setuptools
```

## 6.9 가상 환경의 InsecurePlatformWarning 해결하기
