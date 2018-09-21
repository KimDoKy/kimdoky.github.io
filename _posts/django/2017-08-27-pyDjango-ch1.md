---
layout: post
section-type: post
title: pyDjango - chap 1. 장고 개발의 기본 사항
category: django
tags: [ 'django' ]
---
두 번째 실습이라서 요점만 포스팅합니다.

> Django 1.11.1 / Python 3.5.2 버전으로 실습 진행하였습니다.
실습 당시와 지금은 버전 차이가 있기 때문에 오류들을 만나시게 될 겁니다.
하나하나 해결해 나가셔도 되겠지만, 이 글을 보신다면 파이썬에 익숙하지 않으실 가능성이 높으므로,
최신 버전으로 개정된 [파이썬 웹 프로그래밍(개정판)](http://www.hanbit.co.kr/store/books/look.php?p_code=B4329597070)을 구매시는 걸 추천 드립니다. 이 포스팅은 개정되기 전 버전의 [파이썬 웹 프로그래밍](http://www.hanbit.co.kr/store/books/look.php?p_code=B7703021280)을 실습한 내용입니다.

## 1.1 MTV 개발 방식

### MTV
- Model : `models.py`
- Template : `templates/*.html`
- View : `views.py`)\
장점 : 모델, 템플릿, 뷰 모듈 간에 독립성을 유지, 디자이너, 응용 개발자, DB 설계자 간에 협업이 쉬워짐
`startproject`, `startapp` 명령으로 디렉터리와 파일을 만듬.

## 1.2 MTV 코딩 순서
MTV 방식에 따르면 화면 설계는 뷰와 템플릿 코딩으로 연결되고, 테이블 설계는 모델 코딩에 반영  
그렇기 때문에 독립적으로 개발할 수 있는 모델을 먼저하고, 뷰와 템플릿은 서로 영향을 미치므로 같이 코딩하는 것이 일반적  

UI 화면을 생각하면서 로직을 풀어나가는 것이 쉽기 때문에  보통은 템플릿을 먼저 코딩
클래스형 뷰(CBV)처럼 뷰의 코딩이 매우 간단한 경우는 뷰를 먼저 코딩

### 실습에서의 순서
실습에서는 대부분 CBV이기 때문에 모델, 뷰, 템플릿 순서를 기준으로 진행하며, 그 외에도 프로젝트 설정 파일인 URLconf 파일까지 포함해 다음 순서로 코딩합니다.

- **프로젝트 뼈대 만들기** : 프로젝트 및 앱 개발에 필요한 디렉터리와 파일 생성
- **모델 코딩하기** : 테이블 관련 사항을 개발(models.py, admin.py)
- **URLconf 코딩하기** : URL 및 뷰 매핑 관계를 정의(urls.py)
- **뷰 코딩하기** : 애플리케이션 로직 개발(views.py)
- **템플릿 코딩하기** : 화면 UI 개발(templates/)

## 1.3 settings.py 주요 사항
settings.py는 프로젝트 설정 파일

- **데이터베이스 설정** : 디폴트로 `SQLite3`
- **템플릿 항목 설정** : `TEMPLATES`
- **정적 파일 항목 설정** : `STATIC_URL`
- **애플리케이션 등록**
- **타임존 지정** : 한국 시간으로 변경해야 합니다.

settings.py는 루트 디렉터리를 포함한 각종 디렉터리의 위치, 로그의 형식, 디버그 모드, 보안 관련 사항 등 프로젝트의 전반적인 사항들을 설정

## 1.4 models.py 주요 사항
데이터베이스 처리는 ORM(Object Relation Mapping)을 사용  
테이블을 클래스로 매핑해서 테이블에 대한 CRUD(Create, Read, Update, Delete) 기능을 클래스 객체에 대해 수행하면, 장고가 내부적으로 데이터베이스에 반영  

테이블 클래스는 django.db.models.Model 클래스를 상속받아 정의  
각 클래스 변수의 타입도 장고에서 미리 정의해 놓은 필드 클래스를 사용  

models.py 파일에서 데이터베이스 변경 사항이 발생하면, 마이그레이션(migrations)을 해야함.
장고에서는 `makemigrations` 및 `migrate` 명령으로 실제 데이터베이스에 적용합.

## 1.5 URLconf 주요 사항
URLconf는 URL과 뷰(함수 또는 메소드)를 매핑해주는 urls.py파일입니다.

프로젝트 전체 URL을 정의하는 **프로젝트 URL** 과 앱마다 정의하는 **앱 URL** , 2계층으로 나눠서 코딩하는 방식을 추천.

URL 패턴별로 이름을 지정할 수 있고, 패턴 그룹에 대해 이름공간(namespace)을 지정할 수도 있음.

## 1.6 views.py 주요 사항

가독성과 유지보수 편리, 재활용 등을 고려해야 함.(프로젝트가 커질 것을 대비)

**함수형 뷰(Function-based-view)** 와 **클래스형 뷰(Class-based-view)** 로 구분

클래스형 뷰를 사용하는 것이 장고가 제공하는 제네릭 뷰를 사용할 수 있고 재활용 및 확장성 측면에서 유리하기 때문에, 클래스형 뷰를 더 활용하기를 권장.

## 1.7 templates 주요 사항

웹 페이지 별로 템플릿 파일(`*.html`)이 하나씩 필요

템플릿 디렉터리는 프로젝트 템플릿 디렉터리와 앱 템플릿 디렉터리를 구분해서 사용(프로젝트 템플릿 디렉터리는`TEMPLATES` 설정의 `DIRS` 항목에 지정된 디렉터리)

프로젝트 템플릿 디렉터리에는 base.html 등 전체 프로젝트의 룩앤필(Look and feel)에 관련된 파일들을 모아두고, 각 앱에서 사용하는 템플릿 파일들은 앱 템플릿 디렉터리에 위치

예를 들어, mysite 프로젝트에서 bookmark 앱을 개발한다면, 일반적인 경우 템플릿 디렉터리의 구조는 다음과 같습니다.

- **프로젝트 베이스(루트) 디렉터리** : /home/user/pyDjango/2nd/
- **프로젝트 디렉터리** : /home/user/pyDjango/2nd/mysite/
- **프로젝트 템플릿 디렉터리** : /home/user/pyDjango/2nd/templates/
- **앱 템플릿 디렉터리** : /home/user/pyDjango/2nd/bookmark/templates/

앱 템플릿이 여러개라면 `INSTALED_APPS` 설정 항목에 등록된 순서대로 검색합니다.

## 1.8 Admin 사이트

Admin 사이트에서 User와 Group 테이블을 포함해, 테이블에 대한 데이터의 입력, 수정, 삭제 등의 작업을 할 수 있음.
Admin 화면에서 기본적으로 User와 Group 테이블이 보이는 것은 이미 settings.py 파일에 django.contrib.auth 애플리케이션이 등록되어 있기 때문.(굿)

SQL 없이도 테이블의 모습 및 내용을 확인하고 테이블에 레코드를 입력하고 수정할 수 있음.

## 1.9 개발용 웹 서버 - runserver

장고에서는 `runserver`라는 테스트용 웹 서버를 제공.  

프로젝트를 상용화를 고려한다면, runserver 대신 Apache 또는 Nginx 등의 상용 웹 서버를 사용해야 함.
