---
layout: post
section-type: post
title: Python - MySql 다루기
category: python
tags: [ 'python' ]
---

파이썬으로 데이터베이스를 다루려면 SQL(Structured Query Language)이나 MySql 같은 구현 방식을 알아야 CLI나 파이썬 프로그램을 사용해서 관계형 데이터베이스에 접근할 수 있다.


MySql 실행

```
> mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.

...

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

새 데이터베이스 사용자와 패스워드 생성

```
mysql> CREATE USER 'doky'@'localhost' IDENTIFIED BY 'badpassw0rd';
```

아래와 같은 패스워드 정책으로 인한 에러가 발생할 수 있다.
```
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

```
# 패스워드 정책 확인하기

mysql> show variables like 'validate_password%';
+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |
| validate_password.dictionary_file    |        |
| validate_password.length             | 8      |
| validate_password.mixed_case_count   | 1      |
| validate_password.number_count       | 1      |
| validate_password.policy             | MEDIUM |  # 요기
| validate_password.special_char_count | 1      |
+--------------------------------------+--------+
7 rows in set (0.06 sec)
```

```
validate_password_policy=LOW   (기본 8자 이상)
validate_password_policy=MEDIUM  (기본8자이상,숫자,소문자,대문자,특수문자를 포함)
validate_password_policy=STRONG  (기본8자이상,숫자,소문자,대문자,특수문자,사전단어 포함)
```

```
mysql> create user 'doky'@'localhost' identified by 'MidPassw0rd!';
```

프로젝트용 새 데이터베이스 생성

```
mysql> CREATE DATABASE pjdb;
Query OK, 1 row affected (0.17 sec)
```

사용자에게 데이터베이스 접근 권한을 부여

```
mysql> GRANT ALL ON pjdb.* TO 'doky'@'localhost';
Query OK, 0 rows affected (0.03 sec)
```



> 출처 [모두의 데이터과학 with 파이썬](https://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9791160502152&orderClick=JAj)  

[시골청년의 엔지니어이야기](https://xinet.kr/?p=974)  
[MySql](https://dev.mysql.com/doc/refman/5.6/en/validate-password.html)
