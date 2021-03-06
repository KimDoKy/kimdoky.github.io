---
layout: post
section-type: post
title: Deploy - 미들웨어에 대한 기초 지식
category: deploy
tags: [ 'deploy' ]
---

애플리케이션을 구동하기 위해서는 네트워크, 하드웨어, OS에 대한 지식은 물론, 미들웨어 지식도 있어야합니다.

- 미들웨어 : OS와 업무 처리를 수행하는 애플리케이션 사이에 있는 소프트웨어
- OS가 가진 기능을 확장하는 것으로 애플리케이션에서 사용하는 공통적인 기능을 제공하는것, 각종 서버 기능을 제공하는 것, 상용 SW 등 많은 종류가 있습니다.

## 웹 서버 및 웹 애플리케이션

- 웹서버 : 클라이언트 브라우저에서 HTTP request를 받아 웹 콘텐츠(HTML, CSS 등)을 response하거나 다른 서버 프로그램을 호출하는 기능을 가니 서버

이름 | 설명
---|---
Apache HTTP Server | 오픈소스 웹 서버. 소규모부터 대규모 업무 시스템까지 널리 사용되고 있다.
Internet Information Services(IIS) | MS가 제공하는 웹 서버. Windows Server 시리즈 등 OS 제품에 포함되어 있다. 업무 시스템 등에서 자주 사용되며 GUI 관리 툴로 설정 및 관리할 수 있다.
nginix | 오픈소스 웹 서버. 메모리 사용량이 작고 리버스 프록시 기능과 로드밸런스 기능까지 갖고 있다.
GlassFish | Oracle을 중심으로 한 오픈소스 커뮤니티에서 개발되고 있는 웹 애플리케이션 서버. Jave EE의 레퍼런스 구현이다.
Apache Tomcat | 오픈소스 Java Servlet과 JavaServer Pages(JSP)를 실행하기 위한 웹 애플리케이션 서버
IBM WebSphere Application Server | IBM이 제공하는 JAVA EE 대응 웹 애플리케이션 서버(WAS라고 줄여 부른다)

## 데이터베이스 서버

이름 | 설명
---|---
MySQL | Oracle이 제공하는 오픈소스 RDBMS. 세계에서 가장 많이 보급되어 있는 오픈소스 RDBMS.
PostgreSQL | 오픈소스 RDBMS. MySQL과 함께 업무 시스템으로 자주 사용되는 데이터베이스
Oracle Database | Oracle이 개발한 상용 RDBMS. 업무 시스템으로 가장 많이 사용되고 있는 RDBMS. UNIX, Linux/Windows Server 등 서버 OS뿐만 아니라 메인프레임에서부터 클라이언트 PC까지 여러 플랫폼을 지원하는 것이 특징
DB2 | IBM이 개방한 RDBMS. 메인프레임용으로 개발되었기 때문에 금융기관 등 대규모 시스템에서 많이 사용
MongoDB | 오픈소스 NoSQL. 'document'라는 데이터 집합을 'collection'으로 관리한다. collection을 사용하기 위해서 'query'를 실행하여 데이터를 조작한다.

> NoSQL  
RDBMS 이외의 데이터베이스 관리 시스템. 고정된 스키마에 얽매이지 않고 Key-Value 형 데이터베이스 등이 있다.  
NoSQL은 데이터 저장 및 호출에 최적화되어 있으므로 대량 데이터를 고속으로 주고받을 수 있는 것이 특징.  
대규모 데이터를 통계 분석하거나 늘어나는 정보를 실시간으로 분석할 때 사용된다.

## 시스템 통합 운영 모니터링 툴

시스템을 안정적으로 준영하기 위해서 시스템 관리자는 시스템이 어떤 상태인지 전체적인 관점에서 모니터링해야 합니다.  
'통합 운영 관리 툴'은 시스템 모니터링 대상인 서버와 장비 상태를 모니터링하고 미리 설정한 임계치를 넘었을 때 정해진 액션을 수행한다.

이름 | 설명
---|---
Zabbix | Zabbix SIA로 개발된 통합 운영 관리 툴. 여러 서버 상태를 모니터링 및 추적하기 위한 오픈소스 소프트웨어. 수집한 데이터를 저장하기 위해 MySQL, PostgreSQL, Oracle Database, DB2 등을 사용한다
Mackerel | 하테나에서 개발한 SaaS형 서버 통합 모니터링. SaaS라서 통합 모니터링 서버를 별도로 도입하지 않고 웹 브라우저에서 통합 모니터링을 할 수 있는 서비스. 클라우드상의 서버와 호환이 잘 되며 모니터링 대상 서버에 Agent를 설치하기만 하면 손쉽게 모니터링할 수 있다.
Datadog | Datadog에서 개발한 SaaS형 서버 통합 모니터링. Mackerel과 같이 통합 모니터링 서버를 별도로 도입하지 않고 웹 브라우저에서 통합 모니터링을 할 수 있는 서비스. 클라우드 및 온프레미스가 함께 있는 환경에서도 모니터링이 가능한 것이 특징.
Hinemos | NTT데이터에서 개발한 오픈소스 통합 운영 관리 툴. 일반 서버 모니터링과 alert 등을 뮤료로 사용할 수 있지만, 가상환경과 클러스터 환경을 사용할 경우 유료 옵션이 필요.
Senju | 노무라종합연구소에서 개발한 통합 운영 관리 툴. 일본 내 대규모 금융 시스템 등에서 도입된 사례가 많다.

이 밖에도 HTTP로 통신 트랜잭션과 처리 트랜잭션을 관리하는 트랜잭션 모니터 등의 미들웨어가 있습니다. 인프라를 구축할 때 이러한 미들웨어의 특징과 기능을 잘 파악하여 상황에 맞게 조합하는 기술이 중요합니다.
