---
layout: post
section-type: post
title: AWS - Database Migration Service
category: aws
tags: [ 'aws', 'migration' ]
---

> (target RDS를 생성하고, VPN이 설정되어 있다는 전제하에 진행)

## 0. DB Parameter

DMS를 진행하기에 앞서 DB 파라미터를 셋팅해주어야 한다.

- log_bin = ON
- binlog_format = ROW (8.0 / 5은 FULL)
- binlog_row_image = FULL

확인 방법: `SHOW VARIABLES LIKE 'log_bin';`

## 1. 보안 그룹 설정
DMS 복제 인스턴스가 사용할 SG 셋팅

![]({{ site.url }}/img/post/aws/dms/inbound.png)

![]({{ site.url }}/img/post/aws/dms/outbound.png)

source, target endpoint에 대한 subnet cidr을 inbound, outbound 모두 등록한다.

## 2. 복제 인스턴스 생성
AWS DMS가 데이터 마이그레이션을 수행하는데 사용하는 컴퓨팅 리소스
소스 데이터베이스에서 데이터를 읽고 이를 변환 및 포매팅 후, 대상 데이터베이스로 데이터를 로드하는 작업을 한다.
당연히 복제 인스턴스의 사양에 따라 마이그레이션 작업의 성능에 차이가 있다.

![]({{ site.url }}/img/post/aws/dms/replication_instance.png)

- VPC는 VPN에 셋팅된 VPC 선택
- VPC SecurityGroup은 위에서 셋팅한 RDS SG 선택

## 3. 엔드포인트 생성

### 3.1 소스 엔드포인트

AWS DMS가 데이터베이스 또는 데이터 소스에서 데이터를 읽을 수 있다.

![]({{ site.url }}/img/post/aws/dms/source_endpoint.png)

AZ의 DB 주소로 접속되어야 하나, Private DNS Zone은 Azure에서만 동작하고 VPN 통신으로 인해 private 상태이기 때문에

DB의 IP주소로 설정해야 한다.

DB Domain으로 하는 방법은 추가적인 테스트 필요.

### 3.2 대상 엔드포인트

AWS DMS가 데이터베이스 또는 다른 데이터 소스에 데이터를 쓸 수 있다.

![]({{ site.url }}/img/post/aws/dms/target_endpoint.png)

- RDS 인스턴스를 선택할 수 있다.
- RDS 선택시 자동 입력됨

## 4. 연결 테스트

![]({{ site.url }}/img/post/aws/dms/connection.png)

소스엔드포인트는 스키마를 갱신해주어야,
마이그레이션 테스크의 Mapping rules에서 스키마 리스트가 뜬다.

![]({{ site.url }}/img/post/aws/dms/schema.png)

## 5. 데이터베이스 마이그레이션 테스크

![]({{ site.url }}/img/post/aws/dms/task_conf.png)

Migration Type에서 'Migrate existing data and replicate ongoing changes'를 선택해야

마이그레이션 후 Real Time Sync가 된다.

![]({{ site.url }}/img/post/aws/dms/task_set.png)

Task logs를 꼭 등록하자.

DMS의 오류를 추적할 수 있는 유일한 단서를 제공한다.


#### Task Settings의 각 메뉴 설명

- 소스 트랜잭션에 대한 사용자 지정 CDC 중지 모드
  - 사용자 정의 CDC 중지 모드 비활성화
  - 사용자 정의 CDC 중지 모드 활성화
- Target DB에 복구 테이블 생성
- 대상 테이블 준비 모드
  - 아무것도 하지마
  - 대상에 테이블 삭제
  - 자르기
- 전체 로드가 완료된 후 작업 중지
  - 멈추지마
  - 캐시된 변경 사항을 적용하기 전에 중지
  - 캐시된 변경 사항 적용 후 중지
- LOB 칼럼 설정
  - LOB 열을 포함하지 마
  - 전체 LOB 모드
  - 제한된 LOB 모드
- 데이터 검증

#### LOB(Large Object) 칼럼
대용량 데이터를 저장하기데 사용되는 특별한 유형의 데이터베이스 필드
일반적으로 매우 큰 텍스트나 바이너리 데이터를 저장하는데 적합

##### BLOB(Binary)
바이너리 데이터 저장하는데 사용(이미지, 오디오, 비디오 등)
문자열이나 숫자 데이터와 같은 일반적인 데이터 유형으로 취급할 수 없느 형식의 데이터

##### CLOB(Character)
큰 텍스트 데이터를 저장하는데 사용(긴 문서, 챡의 내용, 큰 XML 파일 등)
문자열 데이터이지만, 일반적인 문자열 필드보다 너무 크기 때문에 별도 처리됨

![]({{ site.url }}/img/post/aws/dms/task_mapping.png)

전 단계의 source endpoint에서 스키마 갱신을 했다면 Table mappings에서 schema를 리스트 형태로 선택할 수 있다.

## 6. DB 싱크 확인

원본 / 대상에 데이터를 추가하여 sync 확인

(좌: source(azure) / 우: target(aws rds))

1. dms task 진행후 target에 task로 지정한 스키마 생성 확인
2. source에서 target에서 지정한 스키마에 새로운 컬럼 추가
3. target에서 해당 스키마에 새로운 컬럼이 실시간으로 추가됨을 확인

![]({{ site.url }}/img/post/aws/dms/db_sync.png)