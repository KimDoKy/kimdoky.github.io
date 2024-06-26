---
layout: post
section-type: post
title: MySQL - Storage Engine
category: sql
tags: [ 'sql' ]
---

MySQL은 각 데이터베이스(스키마)를 파일시스템 안의 데이터 디렉터리의 하위 디렉터리로 저장한다.

테이블을 생성하면 `테이블이름.frm` 파일을 만들고 그 안에 테이블 정의를 저장한다.

스토리지 엔진에 따라 테이블 데이터와 인덱스를 저장하는 방식은 다르지만, 테이블 정의는 서버에서 담당한다.

- 특정 테이블이 어떤 스토리지 엔진을 사용하는지 확인
    - SHOW TABLE STATUS
    
    ```sql
    mysql> SHOW TABLE STATUS LIKE 'user' \G
    *************************** 1. row ***************************
               Name: user
             Engine: InnoDB
            Version: 10
         Row_format: Dynamic
               Rows: 7
     Avg_row_length: 2340
        Data_length: 16384
    Max_data_length: 0
       Index_length: 0
          Data_free: 4194304
     Auto_increment: NULL
        Create_time: 2021-11-04 17:30:35
        Update_time: NULL
         Check_time: NULL
          Collation: utf8_bin
           Checksum: NULL
     Create_options: row_format=DYNAMIC stats_persistent=0
            Comment: Users and global privileges
    1 row in set (0.01 sec)
    ```
    
    - `Name`: 테이블 이름
    - `Engine`: 테이블의 스토리지 엔진
    - `Row_format`: 레코드 포맷
        - Dynamic: 동적 크기(VARCHAR, BLOB)
        - Fixed: 항상 같은 크기(CHAR, INTEGER)
        - Compressed: 압축된 테이블에만 존재
    - `Rows`: 테이블 내 행의 개수
    - `Avg_row_length` : 행의 평균 바이트 수
    - `Data_length`: 전체 테이블의 데이터 량(바이트)
    - `Max_data_length`: 테이블이 가질 수 있는 최대 데이터 량
    - `Index_length`: 인덱스 데이터의 디스크 공간 소비량
    - `Data_free`: MyISAM 테이블에 할당되었으나 미사용 공간
    - `Auto_increment`: 다음 AUTO_INCREMENT 값
    - `Create_time`: 테이블이 처음 생성된 시기
    - `Update_time`: 데이터가 마지막으로 갱신된 시기
    - `Check_time`: CHECK TABLE이나 myisamchk를 사용하여 마지막으로 검사된 시기
    - `Collation`: 테이블 내 캐릭터 레코드의 기본 문자 셋과 콜레이션
    - `Checksum`: 테이블 전체 콘텐츠의 유효한 체크섬 값
    - `Create_options`: 테이블 생성 시에 지정된 별도 옵션
    - `Comment`: 부수 정보들
        - MyISAM: 테이블 생성시 설정된 주석
        - InnoDB: InnoDB 테이블스페이스에 있는 빈 공간에 대한 정보
        - View: VIEW 라는 문자가 기록됨

## MyISAM 엔진

- MySQL의 기본 스토리지 엔진
- full-text 인덱싱, 압축, 공간(Geographic Information System, GIS) 함수 등 유용한 기능과 성능 간의 훌륭한 절충안
- 트랜잭션이나 행 수준의 잠금은 미지원

### 스토리지

각 테이블을 데이터 파일(.MYD)와 인덱스 파일(.MYI)에 저장한다.

동적인 행과 정적인 행 모두 가질 수 있고, 테이블 정의를 토대로 포맷을 결정한다.

MyISAM 테이블이 가질 수 있는 행의 개수는 데이터베이스 서버의 사용 가능한 디스크 공간과 OS가 허용하는 최대 파일 크기를 토대로 결정된다.

5.0 기준으로 6바이트 포인터를 사용하여 256TB 데이터를 처리하도록 구현되어 있다.

8바이트 포인터까지 다룰 수 있다.

```sql
# MAX_ROWS, AVG_ROW_LENGTH 옵션으로 테이블 포인터 크기를 조정
CREATE TABLE mytable (
	a INTEGER NOT NULL PRIMARY KEY,
	b CHAR(18) NOT NULL
) MAX_ROWS = 1000000000 AVG_ROW_LENGTH = 32;
```

### 기능

- 잠금과 동시성
    - 헹 단위가 아닌 테이블 전체를 잠금
    - 읽기동작(reader)은 읽어야 할 모든 테이블에 대한 공유된 읽기 권한을
    - 쓰기동작(writer)은 배타적 쓰기 잠금 권한을 얻음
    - select 쿼리 실행 중에도 새 행을 삽입할 수 있음(동시 삽입)
- 자동 복구
- 수동 복구
    - `CHECK TABLE mytable` 과 `REPAIR TABLE mytagle` 으로 테이블 오류 조사 / 복구
    - `Myisamchk` 으로 서버가 오프라인일 때도 조사 / 복구 가능
- 인덱스 기능
    - BLOB, TEXT 칼럼에서 첫 500개의 문자에 대한 인덱스를 만들 수 있음
- 지연된 키 쓰기
    - 생성시 `ELAY_KEY_WRITE` 옵션을 ON으로 설정하면
    - 쿼리 실행 마지막에 변경된 인덱스 데이터를 디스크가 아니라 메모리 상의 키버퍼에 변경 내용을 버퍼링한다.
    - 버퍼를 정리하거나 테이블을 닫을 때 인덱스 블록을 디스크로 flush한다.
    - 이용 빈도수가 높고 데이터 변경이 잦은 테이블의 성능을 높여준다.
    - 서버나 시스템 충돌시 인덱스가 손상됨(복구 필요)

### 압축된 MyISAM 테이블

- `myisampack` 을 사용하여 테이블을 압축
    - 압축 상태에서 직접 수정 불가
- 디스크 공간을 적게 차지하고, 레코드를 찾는데 적은 디스크 공간만 찾기 때문에 작업 속도가 빠름
- 인덱스를 지원하지만 read only 모드만 제공
- CD-ROM, DVD-ROM 기반의 응용프로그램이나 임베디드 환경에 적합
    - 생성된 후 데이터가 채워지고 절대 변하지 않음

## MyISAM 머지 엔진

- 여러 개의 동일한  MyISAM 테이블이 하나의 가상 테이블로 merge
- 로깅과 데이터 워어하우스 응용프로그램에 유용

## InnoDB 엔진

- 트랜잭션을 지원하는 스토리지 엔진 중 가장 유명
    - 대부분의 경우 롤백되지 않고 완료(정상 종료)되는 짧은 트랜잭션이 많은 경우 Good
- 뛰어난 성능과 자동 장애 복구 기능 때문에 트랜잭션이 필요없는 상황에서도 많이 사용
- 데이블스페이스 라는 한 개 이상의 데이터 파일에 데이터를 저장함
    - 각 테이블의 데이터와 인덱스를 개별 파일에 저장도 가능
- MVCC를 이용하여 4가지 격리 수준을 모두 구현함
    - `REPEATABLE READ` 으로 기본 설정
    - Phantom Read를 막는 Next-key locking 전략을 갖고 있음
        - 변경되는 행뿐만 아니라 인덱스 구조 안의 레코드 사이의 갭도 잠궈서 팬텀 레코드 삽입을 방지
- 클러스터 인덱스 기반으로 구성됨
- 인덱스 구조가 다른 스토리지 엔진과 다름
    - 매우신속한 기본키 조회가 가능
    - 기본키 행에 보조 인덱스가 포함되어 있어서, 기본키가 커지면 보조 인덱스도 커짐
    - InnoDB는 인덱스를 압축하지 않음
- 내부적으로 다양한 최적화를 수행
    - predictive read-ahead
        - 디스크에서 필요한 것으로 예측되는 데이터를 미리 가져오는 기능
    - adaptive hash index
        - 조회를 신속하게 하기 위해 hash 인덱스를 메모리 안에 자동으로 만드는 기능
    - Insert Buffer
        - 삽입을 빠르게 하기 위한 기능
- 외래키 기능
    - MySQL 서버 수준에서는 제공되지 않고 스토리지 엔진 수준에서 지원함
    - 기본 키를 사용하는 쿼리에 대해 InnoDB는 매우 신속한 검색을 제공

## Memory 엔진

- HEAP 테이블은 불변하는 데이터나 재시작 이후 지속되지 않는 데이터에 빠르게 접근하는데 유용
- MyISAM보다 굉장히 빠름
- 모든 데이터가 메모리 안에 저장되므로 쿼리가 디스크 I/O 을 기다릴 필요 없음
- 서버 재시작시 테이블 구조는 지속되지만, 데이터는 지속되지 않음
- 조회 쿼리에 매우 빠른 해시 인덱스를 지원함
- 낮은 쓰기 동시성을 가지는 테이블 잠금을 사용
    - TEXT, BLOB 칼럼 형식 미지원
    - 고정된 레코드만 지원
        - VARCHAR는 CHAR로 저장하기 때문에 메모리 낭비
- MySQL은 메모리 엔진을 사용하여 쿼리 중간 결과를 저장할 임시 테이블로 사용함
    - 중간 결과가 메모리 테이블에 저장하기에 너무 크거나, TEXT / BLOB 칼럼이 포함되면
    - 디스크에 MyISAM 테이블을 만들어서 처리함

## Archive 엔진

- INSERT, SELECT 쿼리만 지원
- 데이터 쓰기를 버퍼링하고 각 행이 삽입될 때마다 zlib으로 압축(MyISAM보다 I/O 이 훨씬 적게 발생)
- 전체 테이블을 수캔하는 분석이나, 복제 마스터에 INSERT 쿼리가 식속히 처리돼야 하는 경우에 이상적
    - SELECT 쿼리는 전체 테이블을 스캔함
- 동시성 향상을 위해 행 수준 잠금과 특별한 버퍼링 시스템을 지원함
- 일관된 읽기 작읍을 위해 SELECT 쿼리 시작시 테이블에 있던 행의 개수만 검색함
- 대량 삽입은 작업이 완결되기 전까지 보이지 않음
    - 트랜잭션 스토리지 엔진이 아니라, 고속 삽입과 압축 저장을 위해 최적화된 스토리지 엔진일 뿐이다.

## CSV 엔진

- csv 파일을 테이블로 처리할 수 있음
- 인덱스 미지원
- 서버 실행하는 동안 데이터베이스 내외로 파일을 복사하게 해줌
    - 스프레드시트에서 csv 파일을 내보내 MySQL 서버의 데이터 디렉터리에 저장하면서, 서버는 바로 읽을수 있음 / csv 테이블에 데이터를 기록하면서 외부 프로그램이 읽을 수도 있음
- 데이터 교환 / 일부 로깅 작업에 유용

## Federated 엔진

- 데이터를 자체 스토리지에 저장하지 않음
- 원격 MySQL 서버 내의 테이블을 참조함
- 복제 등의 트릭을 구현하는데 사용
- 기본키를 이용한 단일 행 조회나 원격 서버에 실행될 INSERT 쿼리에 유용
- 집계 쿼리나 조인 등의 기본적인 작업은 Bad

## Blackhole 엔진

- 저장 메커니즘이 없음(모든 INSERT 구문은 버림)
- 서버는 Blackhole 테이블에 대한 쿼리를 로그에 기록하므로 슬레이브에 복제되거나 로그에 남을 수 있음
- 복잡한 복제 구성과 감사용 로깅에 유용

## NDB 클러스터 엔진

- 아키텍처
    - 아무것도 공유하지 않는 형태의 클러스터링 개념을 기반으로 둠(shared-nothing)
    - 다른 스토리지 엔진에 대한 의존 없음
    - 데이터 노드, 관리 노드, SQL 노드(MySQL 인스턴스) 등을 포함
        - 각 데이터 노드는 클러스터 데이터의 일부를 갖음
        - 일부분들은 복제되어 동일한 데이터 사본들이 다양한 노드에 존재
        - 중복성과 고도의 가용성을 위해 각 노드에 한 애의 서버가 지정됨(RAID와 비슷)
- 중복성과 부하 분산 기능, 빠른 속도를 내도록 만들어짐
- 메모리에 모든 데이터를 저장하며 기본키 조회를 위해 최적화됨
- 스토리지 엔진 수준이 아닌 MySQL 서버 수준에서 조인을 실행함
    - 복잡한 조인은 매우 느리나, 단일 테이블 조회는 매우 빠름
- NDB 클러스터는 매우 크고 복잡함(대부분의 전형적인 응용프로그램엔 부적합)

## 적합한 엔진 선택하기

기본 엔진은 트랜잭션 등의 필요한 기능을 제공하지 않거나, 응용프로그램이 생성하는 읽기와 쓰기 쿼리에 MyISAM의 테이블 잠금보다 더 세분화된 잠금 기능이 필요할 수도 있음

테이블별로 스토리지 엔진을 선택할 수 있기 때문에, 각 테이블이 어떻게 사용되고 저장되는지 이해해야 하며, 응용 프로그램을 전체적으로 이해하고 확장 가능성을 알아야 한다.

테이블별로 다른 스토리지 엔진을 사용하는 것이 반드시 좋은 것은 아니다.

### 트랜잭션

- 트랜잭션이 필요하다면 InnoDB
- 트랜잭션이 필요없거나, SELECT, INSERT 쿼리를 많이 사용한다면 MyISAM(로깅)

### 동시성

- 삽입과 읽기만 동시에 한다면 MyISAM
- 여러 작업이 서로 인터럽트 없이 동시에 실행되려면 행 수준 잠김 기능이 있는 엔진

### 백업

- 서버가 백업의 시행 주기에 맞추어 셧다운 가능 여부에 따라 달라짐
- 온라인 백업을 수행해야 한다면 InnoDB
- 데이터가 많다면(데이터 수집 시간이 길다면) InnoDB
    - MyISAM은 복구 시간이 오래 걸림

### 특수 기능

- 일부 스토리지 엔진에서만 제공하는 기능들
    - 클러스터 인덱스 최적화: InnoDB, SolidDB
    - MySQL 내에서 전문 검색 지원: MyISAM

## 실용 예제

### 로깅하기

- MyISAM, Archive: 오버헤드가 매우 낮고, 초당 수천개의 레코드 삽입이 가능함
- 로깅된 데이터의 요약보고서를 만들어야 한다면?
    - MySQL의 내장 복제 기능을 사용하여 데이터를 슬레이브에 복제하여, 슬레이브에 있는 데이터에 자원을 많이 쓰는 작업을 실행
        - 응용 프로그램이 커지면 이 전략도 불가능
    - 머지 테이블을 사용 (필요할 때 자세히 살펴보자)

### read-only 또는 read-mostly 테이블

- MyISAM: 쓰기보다는 읽기가 자주 일어나고, 테이블이 깨져도 문제가 되지 않는다면
- InnoDB: 클러스터 인덱스가 유용하게 쓰이틑 환경이나 메모리에 데이터가 충분히 들어갈 수 있는 경우

### 주문처리

- InnoDB: 트랜잭션이 꼭 필요, 외래키 요구조건을 만족하는지 여부

### 주식시세

- MyISAM: 실시간 시게를 제공하며, 사용자가 수천명이고 트래픽이 많다.
    - 여러 클라이언트가 읽기/쓰기 권한을 동시에 테이블에 요청(행수준 잠금을 사용하거나 데이터 갱신을 최고화 설계해야 함)

### 게시판

- MyISAM: 카운터를 갱신하는 등의 쿼리(`SELECT COUNT(*) FROM table;`)를 빨리 실행함

### CD-ROM 응용 프로그램

- MyISAM, 압축 MyISAM: MySQL에서 분리가 되고, 다른 미디어에 복사 될 수 있음
    - 읽기 전용 미디어

---

참조
- MySQL 성능 최적화

