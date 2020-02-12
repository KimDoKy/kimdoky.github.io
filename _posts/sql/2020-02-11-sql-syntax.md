---
layout: post
section-type: post
title: SQL - Basic Syntax
category: sql
tags: [ 'sql' ]
---

> [모두의 SQL](https://thebook.io/006977/)

## SQL 명령어의 분류

구분 | 명령어 | 설명
---|---|---
DML<br>(Data Manipulation Language) | SELECT<br>INSERT<br>UPDATE<br>DELETE | - DB에서 테이터를 검색(SELECT)<br> - DB 테이블에서 새로운 행을 삽입(INSERT)하고, 기존의 행을 수정(UPDATE)하거나 삭제(DELETE)
DDL<br>(Data Definition Language) | CREATE<br>ALTER<br>DROP<br>RENAME<br>TRUNCATE | 테이블의 데이터를 정의하고 구조를 생성, 수정 제거
DCL<br>(Data Control Language) | GRANT<br>REVOKE | DB에 대해 접근 권한을 부여하거나 제거
TCL<br>(Transaction Control Language) | COMMIT<br>ROLLBACK<br>SAVEPOINT | DML로 실행한 변경 사항을 저장 관리


## 관계형 데이터베이스의 객체

종류 | 설명
---|---
테이블(TABLE) | 행과 열로 구성된 기본적인 데이터의 저장 단위
뷰(VIEW) | 하나 이상의 테이블로부터 데이터를 선택하여 만든 부분 집합이자 가상의 테이블
인덱스(INDEX) | 주소를 사용하여 행을 빠르게 검색
시퀀스(SEQUENCE) | 고유한 번호를 자동으로 생성. 주로 키를 생성할때 사용
동의어(SYNONYM) | 관리 편의성과 보안을 위해 객체에 별칭을 부여

## SQL Basic Syntax

- SELECT ~ FROM

```
SELECT employee_id, first_name, last_name
FROM employees;
```

- ORDER BY
정렬 순서를 지정

```
SELECT employee_id, first_name ,last_name
FROM employees
ORDER BY employee_id DESC;
```

- DISTINCT
중복된 행을 제거후 출력

```
SELECT DISTINCT job_id
FROM employees;
```

- AS
별칭 지정하기

```
SELECT employee_id AS 사원번호, first_name AS 이름, last_name AS 성
FROM employees;
```

- `||`
각 열의 결과를 연결해 하나의 열로 결과를 표현

```
# employees 테이블에서 employee_id를 출력하고 first_name과 last_name를 붙여서 출력
SELECT employee_id, first_name||last_name
FROM employees;
```

```
SELECT employee_id,
       first_name||' '||last_name,
       email||'@'||'company.com'
FROM employees;
```

- WHERE

- SQL 연산자의 종류

연산자 | 의미
---|---
BETWEEN a AND b | a와 b 사이에 값이 있다(a,b 포함)
IN (list) | list 중 어느 값이라도 일치
LIKE '비교문자' | 비교 문자와 형탸가 일치한다(`%`, `_` 사용)
IS NULL | null 값을 갖는다.

- BETWEEN
두 값의 범위에 해당하는 행을 출력

```
SELECT *
FROM employees
WHERE salary BETWEEN 10000 AND 20000;
```

- IN
조회하고자 하는 데이터의 값이 여러 개일 때 사용.

```
# employees 테이블에서 salary가 10000, 17000, 24000인 직원 정보 출력
SELECT *
FROM employees
WHERE salary IN (10000, 17000, 24000);
```

- LIKE
조회 조건 값이 명확하지 않을 때 사용

```
employees 테이블에서 job_id값이 AD를 포함한 모든 데이터를 조회
SELECT *
FROM employees
WHERE job_id LIKE 'AD%';
```

```
SELECT *
FROM employees
WHERE job_id LIKE 'AD___';
```

- IS NULL
데이터 값이 null인 경우를 조회

```
# employees 테이블에서 manager_id가 null 값인 정보를 출력
SELECT *
FROM employees
WHERE manager_id IS NULL;
```

- 논리 연산자의 종류

연산자 | 의미
---|---
AND | 앞의 조건과 뒤의 조건이 True이어야 한다.
OR | 어느 한쪽이라도 True이면 된다.
NOT | 뒤의 조건의 반대결과흫 반환한다.

```
# AND
# employees 테이블에서 salary가 4000을 초과하면서(AND), job_id가 IT_PROG인 값을 조회
SELECT *
FROM employees
WHERE salary > 4000
AND job_id = 'IT_PROG';

# OR
# employees 테이블에서 salary가 4000을 초과하면서(AND), job_id가 IT_PROG이거나(OR) FI_ACCOUNT;
SELECT *
FROM employees
WHERE salary > 4000
AND job_id = 'IT_PROG'
OR job_id = 'FI_ACCOUNT'
```

- 부정 연산자의 종류

연산자 | 의미
---|---
`!=` | 같지 않다.
`<>` | 같지 않다.(ISO 표준)
`NOT 열 이름 =` | ~와 같지 않다.
`NOT 열 이름 >` | ~보다 크지 않다.
`NOT BETWEEN a AND b` | a와 b 사이에 값이 없다.
`NOT IN (list)` | list 값과 일치하지 않는다.
`IS NOT NULL` | null 값을 갖지 않는다.

```
# employees 테이블에서 employee_id가 105가 아닌 직원 조회
SELECT *
FROM employees
WHERE employee_id <> 105;

# employees 테이블에서 manager_id가 null이 아닌 직원 조회
SELECT *
FROM employees
WHERE manager_id IS NOT NULL;
```
