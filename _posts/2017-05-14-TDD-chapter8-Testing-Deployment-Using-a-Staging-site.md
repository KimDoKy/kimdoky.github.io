---
layout: post
section-type: post
title: TDD-Chapter 8. 스테이징 사이트를 이용한 배포 테스트
category: tdd
tags: [ 'tdd' ]
---

# Chapter 8. 스테이징 사이트를 이용한 배포 테스트

## TDD와 배포 시 주의가 필요한 사항

[이전 블로그 참조]({{ url.site }}/tdd/2017/05/14/TDD-attention.html)

### 이번 장의 개요###

1. 스테이징 서버에서 실행할 수 있도록 FT를 수정한다.
2. 서버를 구축하고 거기에 필요한 모든 소프트웨어를 설치한다. 또한 스테이징과 운영 도메인이 이 서버를 가리키도록 설정한다.
3. Git을 이용해서 코드를 서버에 업로드한다.
4. Django 개발 서버를 이용해서 스테이징 사이트에서 약식 버전의 사이트를 테스트한다.
5. Virtualenv 사용법을 배워서 서버에 있는 파이썬 의존 관계를 관리하도록 한다.
6. 과정을 진행하면서 항시 FT를 실행한다. 이를 통해 단계별로 무엇이 동작하고, 무엇이 동작하지 않는지 확인한다.
7. Gunicorn, Upstart, 도메인 소켓 등을 이용해서 사이트를 운영 서버에 배포하기 위한 설정을 한다.
8. 설정이 정상적으로 동작하면 스크립트를 작성해서 수동으로 작업을 자동화 하도록 한다. 이를 통해 사이트 배포를 자동화할 수 있다.
9. 마지막으로, 동일 스크립트를 이용해서 운영 버전의 사이트를 실제 도메인에 배포하도록 한다.

## 항상 그렇듯이 테스트부터 시작
기능 테스트를 약간 변경해서 스테이징 사이트에서 실행되도록 한다. 이를 위해 인수 하나를 해킹해서 테스트 임시 서버가 실행되는 주소를 변경한다.


```python
# functional_tests/tests.py

import os
[...]

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')  #1
        if staging_server:
            self.live_server_url = 'http://' + staging_server  #2
```
1. STAGING_SERVER라는 환경 변수를 사용하기로 결정했습니다.
2. 해킹은 다음과 같습니다. self.live_server_url을 "실제"서버의 주소로 대체합니다.

이 해킹이 다른 부분을 망가뜨린 것은 아닌지 FT를 실행해서 확인해본다.

스테이징 서버 URL에 대해 실행해본다. URL 하나 정도 구입해두자.

`STAGING_SERVER=czarcie-staging.com python manage.py test functional_tests`

두 테스트가 모두 실패하는 것을 볼 수 있다. 예상한 실패인데, 아직 스테이징 사이트를 구축하지 않았기 때문이다. 트레이스백을 보면 테스트가 도메인 제공자의 홈페이지에서 끝나는 것을 알 수 있다.

> 실습하는 도중에 파이썬과 Django의 버전이 업그레이드로 인해 책도 업데이트 되었다. 책 그대로 실습하면 `manage.py test: error: unrecognized arguments: --liveserver=czarcie-staging.com` 라는 인식할수 없는 인수 에러가 발생한다.
> 책이 업데이트 되었기 때문에 코드와 명령어 또한 업데이트해야 진행이 가능하다.

어째뜬 FT가 제대로 된 결과를 보여주니 커밋 ㄱㄱ.

## 도메인명 취득

## 수동으로 서버를 호스트 사이트로 프로비저닝하기
> 프로비저닝(provisioning)은 사용자의 요구에 맞게 시스템 자원을 할당, 배치, 배포해 두었다가 필요 시 시스템을 즉시 사용할 수 있는 상태로 미리 준비해 두는 것 - [위키백과](https://ko.wikipedia.org/wiki/%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D){:target="_blank"}

"배포"를 두 단계로 나눌 수 있다.

- 신규 서버를 프로비저닝(provisioning)해서 코드를 호스팅할 수 있도록 한다.
- 신규 버전의 코드를 기존 서버에 배포한다.

배포 시마다 새 서버를 사용할 수 있다. 이것은  PythonAnywhere를 통해 구현할 수 있다. 하지만 규모가 큰 사이트나 기존 사이트의 대규모 업데이트 시에만 필요한 것이다. 간단한 사이트에선 두 단계로 작업을 나누는 것이 좋다. 최종적으로 이 두가지 작업을 자동화하지만, 지금은 수동 프로비저닝 시스템으로 충분하다.

### 사이트를 호스트할 곳 정하기
사이트 호스팅을 위한 다양한 솔루션이 존재하지만, 대략 두 가지 형태로 분류

- 자체 서버(가상도 가능) 운영
- Heroku, DotCloud, OpenShift, PythonAnywhere 같은 PlatForm-As-A-Service(PaaS) 서비스 이용

작은 규모의 사이트에선 PaaS가 많은 이점이 있기 때문에 이를 추천하지만 지금은 사용하지 않는다. PaaS의 서비스 방식이 서로 다 다르기 때문에 배포 절차도 다르다. 즉, 하나를 배우더라도 다른 서비스에 적용할 수 없고, 지금 이순간에도 서비스 프로세스가 변경되거나 폐업될 수도 있다. 그러므로, PaaS 대신 SSH와 웹 서버 설정을 이용한 전통적인 서버 관리 방식으로 진행한다.

여기서 직접 구축하는 서버는 PaaS를 통해 사용할 수 있는 환경과 거의 같기 때문에, 배포 과정 중에 배우는 모든 것을 프로비저닝 솔루션에 상관없이 적용할 수 있다.

### 서버 구축하기
솔루션 선택의 조건만 충족되면 어떤 솔루션이든 상관없다.
나는 AWS EC2로 선택....(아 귀찮....ㅠ)

- 우분투(Ubuntu)(13.04 버전 이상)가 설치돼 있을 것
- 루트 권한이 있을 것
- 인터넷상에 공개돼 있을 것
- SSH로 접속할 수 있을 것

우분투를 추천하는 이유는 파이썬 3.4를 기본으로 탑재하고 있기 때문이다. 또한 Ngnix 설정이 용이하다.


[Ubuntu Linux Deploy](https://github.com/KimDoKy/FastCamp/blob/master/Deploy/01.Ubuntu%20Linux%20Deploy.md)

### 사용자 계정, SSH, 권한




### Nginx 설치
### 스테이징 서버와 운영 서버를 위한 도메인 설정
### FT를 이용해서 도메인 및 Nginx가 동작하는지 확인

## 코드를 수동으로 배포
### 데이터베이스 위치 조정
### Virtualenv 생성
### 간단한 Nginx 설정
### migrate를 이용한 데이터베이스 생성

## 운영 준비 배포 단계
### Gunicorn으로 교체
### Nginx를 통한 정적 파일 제공
### 유닉스 소켓으로 교체하기
### DEBUG를 False로 설정하고 ALLOWED_HOSTS 설정하기
### Upstart를 이용한 부팅 시 Gunicorn 가동
### 변경사항 저장: Gunicorn을 requirements.txt에 추가

## 자동화
### 작업한 것 보호하기
