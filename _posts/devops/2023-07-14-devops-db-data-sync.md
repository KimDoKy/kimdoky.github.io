---
layout: post
section-type: post
title: DB(MySQL) Data Sync in MultiCloud
category: deploy
tags: [ 'mysql' ]
---

## Introduction

MultiCloud로 인프라를 구성시 각각 인프라에서의 DB의 Sync를 맞추어야 합니다.
이때 MySQL의 Replication 기능을 사용할 수 있습니다. (VPN 작업이 선행되어야 합니다.)

Replication은 2대 이상의 DBMS를 나눠서 데이터를 저장하는 방식으로 Master / Slave 로 구성됩니다.

- Master: 웹서버로부터 데이터 등록/수정/삭제 요청시 바이너리로그를 생성하여 Slave 서버로 전달합니다.
- Slave: Master로부터 전달받은 바이너리로그를 릴레이 로그에 기록하고 데이터를 반영합니다.


![]({{ site.url }}/img/post/deploy/230714/DB_Replication.png)

---

## solution

### 진행전 확인

Source DB Server(RDS)에서 이진 로깅의 활성화 여부 확인이 필요합니다.

```sql
SHOW VARIABLES LIKE 'log_bin';
```

MySQL 8.0 에서는 활성화가 기본값입니다.

### DB dump, Recovery

#### Dump

```bash
mysqldump -h hostname -u username -p --single-transaction \
--set-gtid-purged=OFF --databases dbnames --order-by-primary > dump.sql
```

dump 진행시 원본(AWS) DB를 read-only로 지정해야 하지만, RDS는 해당 기능을 막아두었고,
읽기 전용 DB를 생성해도 FLUSH 관련 권한들이 막혀있기 때문에 `--set-gtid-purged=OFF` 옵션이 필요합니다.
해당 옵션은 덤프 파일에 기록되는 GTID 정보(`SET @@GLOBAL.gtid_purged`)를 제어하는데, 해당 문법을 추가하지 않고 진행합니다.

> RDS는 SUPER 권한을 부여하지 않고, `FLUSH TABLES WITH READ LOCK` 명령을 실행할 권한을 허용하지 않습니다.

> 해당 내용은 MySQL 8.0.32 버전의 버그로 보고되어 있고, 8.0.33 버전에서 해결되었습니다. 하지만 현재 사용하는 RDS의 버전은 8.0.32 이기 때문에 위 방법으로 진행해야 합니다. - [mysql bugs](https://bugs.mysql.com/bug.php?id=109685)

> 주의사항. 덤프파일이 기록되고 replication 설정이 완료되기 전에 DB쪽에 어떠한 업데이트가 일어난다면 `Cannot modify @@session.sql_log_bin inside a transaction` 에러가 발생하기 때문에 Position 정보를 다시 맞추는 작업이 필요합니다. Position 정보는 뒤쪽에서 다시 설명합니다.

#### Recovery

```bash
mysql -h hostname -u username -p < dump.sql
```

> 주의사항. 원본서버의 마스터 작업자(RDS)와 복원을 진행하는 작업자(Azure)의 이름이 동일해야 합니다.

### Set Replication

#### Create User for SyncData

```sql
CREATE USER 'syncuser'@'%' IDENTIFIED BY 'userpassword';
GRANT REPLICATION SLAVE, REPLICATION CLIENT on *.* to 'syncuser'@'%';

Mysql> SHOW GRANTS FOR syncuser@'%';
```
생성하는 유저는 보안상 최소한의 권한(Replication)만 주어저야 합니다.

> 주의사항. password는 32자 내로만 가능합니다.

#### Get Posion Info

RDS에서 바이너리 로그의 포지션 정보를 가져옵니다.
Master DB와 Slave DB의 Sync를 맞추기 위한 정보입니다.

```sql
mysql> show master status\G
*************************** 1. row ***************************
             File: mysql-bin-changelog.020557
         Position: 157
     Binlog_Do_DB:
 Binlog_Ignore_DB:
Executed_Gtid_Set:
1 row in set (0.01 sec)
```

#### Link Source DB Server(Master), Replication DB Server(Slave)

위에서 얻은 포지션정보를 기반으로 Replication DB Server을 설정합니다.

```sql
CALL mysql.az_replication_change_master('master_host', 'master_user', 'master_password', master_port, 'master_log_file', master_log_pos, '');

# ex
CALL mysql.az_replication_change_master('sdp.us-east-1.rds.amazonaws.com', 'syncuser', 'userpassword', 3306, 'mysql-bin-changelog. 020557', 157, '');

# 설정 적용
CALL mysql.az_replication_start;

# 설정 확인
## Master(RDS)
mysql> show full processlist\G
...
*************************** 11. row ***************************
     Id: 6135
   User: syncuser
   Host: 192.*.*.*:3306
     db: NULL
Command: Binlog Dump
   Time: 11433
  State: Master has sent all binlog to slave; waiting for more updates
   Info: NULL
...

## Slave(Azure)
mysql> show slave status\G
Slave_IO_Running, Slave_SQL_Running 값이 Yes
Slave_IO_State: Waiting for source to send event 확인
만약 Error 관련된 부분에 내용이 있다면 해당 에러 메시지를 확인하고 해결이 필요합니다.

# 그외 옵션
## 복제 중지
CALL mysql.az_replication_stop;

## 복제 관계 제거
CALL mysql.az_replication_remove_master;
```

![]({{ site.url }}/img/post/deploy/230714/DB_Replication_Slave.png)
