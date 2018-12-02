---
layout: post
section-type: post
title: Python - MySql 다루기
category: python
tags: [ 'python' ]
---

파이썬으로 데이터베이스를 다루려면 SQL(Structured Query Language)이나 MySql 같은 구현 방식을 알아야 CLI나 파이썬 프로그램을 사용해서 관계형 데이터베이스에 접근할 수 있다.


### MySql 실행

```sql
> mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.

...

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

### 새 데이터베이스 사용자와 패스워드 생성

```sql
mysql> CREATE USER 'doky'@'localhost' IDENTIFIED BY 'badpassw0rd';
```

아래와 같은 패스워드 정책으로 인한 에러가 발생할 수 있다.
```
ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
```

```sql
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

```sql
mysql> CREATE USER 'doky'@'localhost' IDENTIFIED BY 'MidPassw0rd!';
```

### 프로젝트용 새 데이터베이스 생성

```sql
mysql> CREATE DATABASE pjdb;
Query OK, 1 row affected (0.17 sec)
```

### 사용자에게 데이터베이스 접근 권한을 부여

```sql
mysql> GRANT ALL ON pjdb.* TO 'doky'@'localhost';
Query OK, 0 rows affected (0.03 sec)
```

### 기존 데이터베이스에 새 테이블 만들기

```sql
# 생성한 유저로 다시 로그인
> mysql -u doky -p pjdb
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.

...

# employee 테이블 생성, emapname(가변길이 텍스트), salary(실수), hired(날짜) 열 생성
mysql> USE dsdb;
Database changed
mysql> CREATE TABLE employee (empname TINYTEXT, salary FLOAT, hired DATE);
Query OK, 0 rows affected (0.10 sec)
```

### 데이터베이스 삭제

```sql
mysql> DROP TABLE employee;
Query OK, 0 rows affected (0.13 sec)
```

### 기본 키(primary key)

언어 표준에 따라 다르긴 하지만, 각 레코드에 자동으로 생성되는 기본 키(primary key)와 자동으로 업데이트되는 최종 수정 시점의 타임 스탬프를 추가해야 한다. 기본 키는 고유한 레코드를 식별하여 검색 속도를 높이고, 최종 수정 시점은 수정 현황을 파악할 수 있게 한다. `NOT NULL`은 `NULL`이 아닌 값을 갖도록 강제한다.

```sql
mysql> CREATE TABLE employee (id INT PRIMARY KEY AUTO_INCREMENT,
  -> updated TIMESTAMP, empname TINYTEXT NOT NULL, salary FLOAT NOT NULL,
  -> hired DATE);
Query OK, 0 rows affected (0.02 sec)
```

### 인덱스(INDEX)

정렬, 추출, 결함 등에 열을 사용하려면 인덱스에 해당 열을 추가해야 한다.

```sql
mysql> ALTER TABLE employee ADD INDEX(hired);
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

인덱스는 검색 시간을 단축시켜주지만, 데이터의 입출력에 걸리는 시간을 늘린다. 테이블에 상당 분량의 데이터를 입력 후 데이터를 생성해야 한다. 일정 분량 이상의 데이터를 새로 입력하려면 기존 인덱스를 지워야 한다.

```sql
mysql> DROP INDEX hired ON employee;
Query OK, 0 rows affected (0.05 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

그 후에 데이터를 입력한 후 인덱스를 추가한다.

### 고유값(UNIQUE)

데이터가 고유값이라면 `UNIQUE` 조건을 붙여야 한다. 데이터의 폭(width)가 가변적이라면 엔트리가 얼마나 고유한지 길이를 지정해야 한다.

```sql
mysql> ALTER TABLE employee ADD UNIQUE(empname(255));
```

### 입력(INSERT)

```sql
mysql> INSERT INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());
Query OK, 1 row affected, 1 warning (0.12 sec)
```

두 개의 `NULL`은 인덱스와 타임스탬프에 대한 플레이스 홀더이다. 서버는 자동으로 이들을 인식한다.  
`NOW()`는 현재 날짜와 시간을 반환하여 '날짜'만 레코드에 입력한다. 이 쿼리는 하나의 경로를 발생시키는데, 시간 부분이 잘렸기 때문이다.

```sql
# 경고 자세히 보기

mysql> SHOW WARNINGS;
+-------+------+-------------------------------------------------------------------------+
| Level | Code | Message                                                                 |
+-------+------+-------------------------------------------------------------------------+
| Note  | 1292 | Incorrect date value: '2018-12-02 21:53:19' for column 'hired' at row 1 |
+-------+------+-------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

데이버 입력 중 `UNIQUE` 제약 조건을 위반하면 서버는 입력 명령을 취소한다.

```sql
mysql> INSERT INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());
ERROR 1062 (23000): Duplicate entry 'John Smith' for key 'empname'
```

`IGNORE` 키워드를 지정하여 해당 내용을 무시하고 입력할 수 있다.

```sql
mysql> INSERT IGNORE INTO employee VALUES(NULL,NULL,"John Smith",35000,NOW());
Query OK, 0 rows affected, 2 warnings (0.02 sec)
```

### 삭제(DELETE)

```sql
# 이름이 John Smith이고, 소득이 11000 이하인 레코드를 삭제

mysql> DELETE FROM employee WHERE salary<11000 AND empname="John Smith";
Query OK, 0 rows affected (0.00 sec)

# 전체 레코드를 삭제

mysql> DELETE FROM employee;
Query OK, 1 row affected (0.07 sec)

# 고유 키나 다른 식별 조던을 사용하여 특정한 레코드 하나만 삭제

DELETE FROM employee WHERE id=387513;
```

### 변형(UPDATE)

```sql
# 최근 입사한 사람의 임금을 리셋
mysql> UPDATE employee SET salary=35000 WHERE hired=CURDATE();
Query OK, 0 rows affected (0.01 sec)
Rows matched: 0  Changed: 0  Warnings: 0

# John Smith의 임금을 인상

mysql> UPDATE employee SET salary=salary+1000 WHERE empname="John Smith";
Query OK, 0 rows affected (0.00 sec)
Rows matched: 0  Changed: 0  Warnings: 0
```

### 추출(SELECT)

```sql
mysql> SELECT empname,salary FROM employee WHERE empname="John Smith";
+------------+--------+
| empname    | salary |
+------------+--------+
| John Smith |  35000 |
+------------+--------+
1 row in set (0.00 sec)

mysql> SELECT empname,salary FROM employee;
+-------------+--------+
| empname     | salary |
+-------------+--------+
| John Smith  |  35000 |
| DK Kim      |  70000 |
| James Brown | 170000 |
| Jamiroquai  |  20000 |
+-------------+--------+
4 rows in set (0.00 sec)
```

정렬, 그룹핑, 집계, 필터링을 사용해서 추출 작업을 고도화할 수 있다.

`ORDER BY` : 내림차순과 오름차순으로 정렬

```sql
mysql> SELECT * FROM employee WHERE hired>='2000-01-01' ORDER BY salary DESC;
+----+---------+-------------+--------+------------+
| id | updated | empname     | salary | hired      |
+----+---------+-------------+--------+------------+
|  6 | NULL    | James Brown | 170000 | 2018-12-02 |
|  5 | NULL    | DK Kim      |  70000 | 2018-12-02 |
|  4 | NULL    | John Smith  |  35000 | 2018-12-02 |
|  7 | NULL    | Jamiroquai  |  20000 | 2018-12-02 |
+----+---------+-------------+--------+------------+
4 rows in set (0.00 sec)
```

`GROUP BY`와 집계 함수(`COUNT()`, `MIN()`, `MAX()`, `SUM()`, `AVG()`)를 사용여 데이터를 그룹핑하고 집계 할 수 있다.

```sql
# 2001년 1월 1일을 기준으로 이전과 이후에 고용된 직원들의 평균 임금과 고용 기간 카테고리를 산출

mysql> SELECT (hired>'2001-01-01') AS Recent, AVG (salary) FROM employee
    -> GROUP BY (hired>'2001-01-01');
+--------+--------------+
| Recent | AVG (salary) |
+--------+--------------+
|      1 |        73750 |
+--------+--------------+
1 row in set (0.01 sec)
```

`WHERE`과 `HAVING` 키워드는 추출한 결과를 필터링하는데, `WHERE`는 그룹핑하기 전에 실행하고, `HAVING`은 그룹핑한 후에 실행한다.

```sql
# 2001년 1월 1일 이후에 고용한 직원들을 고용연도를 기준으로 묶고, 각 그룹의 평균 임금과 최고,최신 고용일자를 집계

mysql> SELECT AVG(salary), MIN(hired), MAX(hired) FROM employee
    -> GROUP BY YEAR(hired)
    -> HAVING MIN(hired) > '2001-01-01';
+-------------+------------+------------+
| AVG(salary) | MIN(hired) | MAX(hired) |
+-------------+------------+------------+
|       73750 | 2018-12-02 | 2018-12-02 |
+-------------+------------+------------+
1 row in set (0.01 sec)
```

### 결합(JOIN)

MySQL은 inner, left, right, outer, natural 등 다섯 가지 결합 타입을 지원한다.

- `inner` : 두 테이블 모두에서 하나 이상의 공통 항목이 있는 행을 반환
- `left`, `right` : 반대편 테이블에 매칭되는 행이 하나도 없더라도 left/right 테이블의 모든 행을 결합
- `outer` : 두 테이블 중 한 테이블에만 행이 있어도 이를 반환. 없으면 NULL을 반환
- `natural` : `outer`처럼 행동하지만, 이름이 같은 열은 제외한다.

```sql
# 테이블을 만들고 데이터를 입력

mysql> CREATE TABLE position (eid INT, description TEXT);
Query OK, 0 rows affected (0.16 sec)

mysql> INSERT INTO position (eid, description) VALUES (6,'Imposter'),
    -> (1,'Accountant'),(4,'Programmer'),(5,'President');
Query OK, 4 rows affected (0.08 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ALTER TABLE position ADD INDEX(eid);
Query OK, 0 rows affected (0.02 sec)
Records: 0  Duplicates: 0  Warnings: 0


# 결합한 데이터를 불러온다.

mysql> SELECT employee.empname,position.description
    -> FROM employee,position WHERE employee.id=position.eid
    -> ORDER BY position.description;
+-------------+-------------+
| empname     | description |
+-------------+-------------+
| James Brown | Imposter    |
| DK Kim      | President   |
| John Smith  | Programmer  |
+-------------+-------------+
3 rows in set (0.00 sec)
```

## pymysql을 이용하여 Python으로 MySql 사용하기

파이썬은 'pymysql'과 같은 데이터베이스 드라이버 모듈을 사용해서 MySQL을 사용할 수 있다.
'pymysql'은 데이터베이스 서버에 연결한 후 데이터베이스 쿼리로 파이썬 함수를 변환하고, 파이썬 데이터 구조로 데이터베이스 조회 결과를 변환한다.

```python
In [1]: import pymysql
# connect() 함수는 데이터베이스정보(DB이름), 데이터베이스 서버의 위치(호스트,포트번호), 데이터베이스 사용자(사용자 이름,비밀번호)가 필요
In [2]: conn = pymysql.connect(host='localhost', port=3306,
   ...:         user='doky', passwd='MidPassw0rd!', db='pjdb')

In [3]: cur = conn.cursor()

In [4]: query = '''
   ...: SELECT employee.empname, position.description
   ...: FROM employee, position WHERE employee.id=position.eid
   ...: ORDER BY position.description
   ...: '''
# execute()함수는 실행할 쿼리를 전달하고, 처리된 행의 개수를 반환한다.
In [5]: n_rows = cur.execute(query)

# 변형을 하지 많은 쿼리를 전달할 때는 fetchall()을 사용하여 모든 레코드를 가져올 수 있다.
# fetchall() 함수는 튜플로 된 열의 리스트로 변환할 수 있는 제네레이터를 반환한다.
In [6]: results = list(cur.fetchall())

In [7]: results
Out[7]:
[('James Brown', 'Imposter'),
 ('DK Kim', 'President'),
 ('John Smith', 'Programmer')]

# 변형을 가하는 쿼리는 커밋을 해야한다. 커서가 아니라 커넥션이 제공하는 함수다.
In [8]: conn.commit()
````


> 출처  
- [모두의 데이터과학 with 파이썬](https://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9791160502152&orderClick=JAj)  
전체 내용은 위 서적에서 발췌하였으며, 미리보고로 제공되는 선까지만 다루었습니다. :)  
- [시골청년의 엔지니어이야기](https://xinet.kr/?p=974)  
- [MySql](https://dev.mysql.com/doc/refman/5.6/en/validate-password.html)
