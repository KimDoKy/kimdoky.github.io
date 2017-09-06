---
layout: post
section-type: post
title: pyDjango - chap7. Blog 앱 확장 - Tag 달기
category: django
tags: [ 'django' ]
---
각 포스트마다 태그를 달 수 있는 기능을 개발합니다.  

태그 기능을 제공하는 오픈 소스로, django-tagging 패키지를 사용합니다.  

상용화를 목표로 장고 프로젝트를 개발한다면 오픈 소스를 활용하는 작업은 필수 입니다.

## 7.1 애플리케이션 설계하기
블로그의 각 포스트마다 태그를 보여주고 해당 태그를 클릭하는 경우, 그 태그를 가진 모든 포스트의 리스트를 보여줍니다. 그리고 태그만 모아서 보여주는 태그 클라우드 기능도 개발합니다.

### 7.1.1 화면 UI 설계
기존 포스트 상세 화면은 수정을, 태그와 관련된 2개의 화면은 신규로 추가합니다.

### 7.1.2 테이블 설계
태그 기능을 위해 Post 테이블에 필드 하나를 추가합니다.

필드명 | 타입 | 제약 조건 | 설명
---|---|---|---
tag | TagField | Blank | 포스트에 등록한 태그

### 7.1.3 URL 설계
기존 URL에 태그와 관련된 2개의 URL을 추가합니다 첫 번째는 태그 클라우드를 보기 위한 URL이고, 두 번째는 특정 태그가 달려 있는 포스트들의 리스트를 보여주는 URL입니다.

URL 패턴 | 뷰 이름 | 템플릿 파일명
---|---|---
/blog/tag/ | TagTV(TemplateView) | tagging_cloud.html
/blog/tag/tagname/ | PostTOL(TaggedObjectList) | tagging_post_list.html

### 7.1.4 작업/코딩 순서

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
뼈대 만들기 | startapp <br> settings.py | django-tagging 패키지 설치 <br> tagging 앱을 등록
모델 코딩하기 | models.py <br> makemigrations <br> migrate | tag 필드 추가 <br> 모델이 변경되므로 이를 데이터베이스에 반영
URLconf 코딩하기 | urls.py | URL 정의 추가
뷰 코딩하기 | views.py | 뷰 로직 추가
템플릿 코딩하기 |templates 디렉터리 | 템플릿 파일 추가
그 외 코딩하기 | static 디렉터리 | 태그 클라우드용 tag.css 추가
