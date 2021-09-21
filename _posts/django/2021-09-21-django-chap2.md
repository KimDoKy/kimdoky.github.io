---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap2. The Optimal Django Environment Setup
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

## 2.1 Use the Same Database Engine Everywhere

로컬 개발 환경과 실제 운영 환경의 데이터베이스 엔진을 일치시키세요.

### 2.1.1 You Can't Examine an Exact Copy of Production Data Locally

개발 환경과 운영 환경이 다를 경우, 운영 데이터베이스에서 SQL 덤프하여 개발환겨에 임포트한다고 해도 두 개의 데이터베이스가 완전히 같은 데이터를 가지고 있다고는 할 수 없습니다.

### 2.1.2 Different Databases Have Different Field Types/Constraints

데이터베이스들 마다 각 필드 데이터 타입에 대해 다르게 작동하지만, ORM은 어느 정도 그 차이를 커버해줍니다만 완벽하지 않습니다.  

개발 환경에서는 보통 SQLite3를 많이 사용하는데, 이는 동적이고 느슨한 타이핑을 지원하기 때문에, 운영 환경의 엄격한 타이핑 동작 데이터베이스에서는 조건 에러(constraint error)등을 발생시킵니다. 그리고 이러한 에러는 재현 및 발견하기가 어렵습니다.  

추천 조합은 Django + PostgreSQL 입니다.  
[Django QuerySet API](https://kimdoky.github.io/django/2020/02/03/django-queryset-api/)  
[Django Database Functions](https://kimdoky.github.io/django/2020/01/31/django-db-functions/) 참고

### 2.1.3 Fixtures Are Not a Magic Solution

픽스터는 단순히 하드코딩된 간단한 데이터 셋을 생성하는 데는 좋은 도구입니다. 하지만 큰 크기의 데이터 셋을 이전할 때에는 신뢰성을 가지지 못합니다. 애초에 그런 목적의 도구가 아닙니다.

## 2.2 Use Pip and (Virtualenv or venv)

- pip: 파이썬 패키지 인덱스(Python Package Index)와 그 미러 사이트에서 파이썬 패키지를 가져오는 도구
- virtualenv: 파이썬 패키지 의존성을 유지할 수 있게 독립된 파이썬 환경을 제공하는 도구

> 개인적으로는 Python의 기본 가상환경 구성인 `python3 -m env`도 좋다고 생각합니다.

### 2.2.1 virtualenvwrapper

virtualenv 활성화와 같은 명령어를 줄여줍니다. 필수는 아님

## 2.3 Install Django and Other Dependencies via Pip

requirments.txt 를 활용하세요.

## 2.4 Use Git For Version Control

Git 쓰세요. 두 번 쓰세요.

## 2.5 Optional: Identical Environments

'내 컴퓨터에서는 잘되는데요?'라는 문제들이 종종 발생합니다. 

- 서로 다른 운영 체제
- 서로 다른 파이선 셋업
- 개발자와 개발자 간의 차이

이러한 문제를 해결하기 위해 **가능한 똑같은** 환경을 구성할 필요가 있습니다.

### 2.5.1 Docker

도커 쓰세요. 두 번 쓰세요.
