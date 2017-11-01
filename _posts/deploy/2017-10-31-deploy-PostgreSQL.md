---
layout: post
section-type: post
title: Deploy - Mac에서 PostgreSQL 사용하기
category: deploy
tags: [ 'deploy' ]
---

PostgreSQL 사용법을 검색하면 우분투는 많이 나오지만 Mac은 자료가 적습니다.

그래서 삽질한 것들을 다시 정리합니다.

Brew로 PostgreSQL를 설치합니다.

```
brew install postgresql
```

psql 를 실행합니다.

그냥 실행하면 인증 에러가 발생하여 그냥 실행하면 안됩니다.

```
Postgresql: password authentication failed for user “postgres”
```

역시나 StackOverFlow에서 해답을 찾습니다.  
<https://stackoverflow.com/questions/7695962/postgresql-password-authentication-failed-for-user-postgres>


10번의 해결책으로 정상 작동을 확인했습니다.

```
/ » su - postgres
Password:
MacBook-Pro:~ postgres$ psql
Password:
psql (10.0, server 9.6.5)
Type "help" for help.

postgres=# create database snapmemo;  # DB 생성
CREATE DATABASE

postgres=# create user kim with password '1q2w3e4r';  # 유저 생성
CREATE ROLE

postgres=# grant all privileges on database snapmemo to kim;  # 데이터베이스에 사용자 권한 등록
GRANT

postgres-# \l  # 권한이 잘 적용되었는지 확인
                             List of databases
   Name    |  Owner   | Encoding | Collate | Ctype |   Access privileges
-----------+----------+----------+---------+-------+-----------------------
 postgres  | postgres | UTF8     | C       | C     |
 snapmemo  | postgres | UTF8     | C       | C     | =Tc/postgres         +
           |          |          |         |       | postgres=CTc/postgres+
           |          |          |         |       | park=CTc/postgres
 template0 | postgres | UTF8     | C       | C     | =c/postgres          +
           |          |          |         |       | postgres=CTc/postgres
 template1 | postgres | UTF8     | C       | C     | =c/postgres          +
           |          |          |         |       | postgres=CTc/postgres
(4 rows)

postgres-# \connect snapmemo  # 데이터베이스 변경
psql (10.0, server 9.6.5)
You are now connected to database "snapmemo" as user "postgres".

MacBook-Pro:~   # ctrl + d
MacBook-Pro:~ postgres$ logout
------------------------------------------------------------
/ »
```
