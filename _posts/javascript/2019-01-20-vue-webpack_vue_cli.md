---
layout: post
section-type: post
title: vue.js - Webpack, Vue Cli Commend
category: javascript
tags: [ 'javascript' ]
---

### Webpack Main attribute

attribute | description
---|---
entry | 웹팩으로 빌드할 대상 파일을 지정하는 속성<br> entry로 지정한 파일의 내용에는 전체 애플리케이션 로직과 필요 라이브러리를 로딩하는 로직이 들어감
output | 웹팩으로 빌드한 결과물의 위치와 파일 이름 등 세부 옵션을 설정하는 속성
loader | 웹팩으로 빌드할 때 HTML, CSS, Image 파일 등을 JS로 변환하기 위해 필요한 설정을 정의하는 속성
plugin | 웹팩으로 빌드한 결과물에 추가 기능을 제공하는 속성<br>결과물의 사이즈를 조절하거나 기타 CSS, HTML 파일로 분리하는 등의 기능
resolve | 웹팩으로 빌드할 때 해당 파일이 어떻게 해석되는지 정의하는 속성<br>특정 라이브러리로 로딩할 때의 버전, 파일 경로 지정 등을 정의

### Vue Cli Commend

template | description
---|---
vue init webpack | 고급 웹팩 기능을 활용한 프로젝트 구성 방식. 테스팅, 문법 검사 등을 지원
vue init webpack-simple | 웹팩 최고 기능을 활용한 프로젝트 구성 방식. 빠른 화면 프로토타이핑용
vue init browserify | 고급 브라우저리파이 기능을 활용한 프로젝트 구성 방식. 테스팅, 문법 검사 등을 지원
vue init browserify-simple | 브라우저리파이 최소 기능을 활용한 프로젝트 구성 방식. 빠른 화면 프로토타이핑
vue init simple | 최소 뷰 기능만 들어한 HTML 파일 1개 생성
vue init pwa | 웹팹 기반의 프로그레시브 웹 앱(PWA, Progressive Web App) 기능을 지원하는 뷰 프로젝트


> 출처: [Do it! Vue.js 입문](http://www.yes24.com/24/goods/58206961)
