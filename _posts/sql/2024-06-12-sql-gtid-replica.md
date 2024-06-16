---
layout: post
section-type: post
title: MySQL - MySQL Replica with GTID
category: sql
tags: [ 'sql' ]
---

I simply ran MySQL as a container and implemented replicas.

## 1. Write Docker Compose File

```yaml
version: '3.1'

services:
  master:
    image: mysql:8.0
    container_name: mysql_master
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: testdb
    ports:
      - "3306:3306"
    command: --server-id=1 --gtid-mode=ON --enforce-gtid-consistency=ON --log-bin=mysql-bin --binlog-format=ROW --default-authentication-plugin=mysql_native_password

  slave:
    image: mysql:8.0
    container_name: mysql_slave
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: testdb
    ports:
      - "3307:3306"
    command: --server-id=2 --gtid-mode=ON --enforce-gtid-consistency=ON --log-bin=mysql-bin --binlog-format=ROW --default-authentication-plugin=mysql_native_password
```

## 2. Run Docker Container

```bash
docker-compose up -d
```

## 3. Set Master(Source)

connect master db.

```bash
docker exec -it mysql_master mysql -uroot -prootpassword
```
create replication user and grant permission

```sql
CREATE USER 'replica_user'@'%' IDENTIFIED WITH mysql_native_password BY 'replica_password';
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';
FLUSH PRIVILEGES;

-- check Master status
SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+------------------------------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
+------------------+----------+--------------+------------------+------------------------------------------+
| mysql-bin.000003 |      883 |              |                  | ebf8005f-292f-11ef-9015-0242c0a8a703:1-9 |
+------------------+----------+--------------+------------------+------------------------------------------+
1 row in set (0.00 sec)
```

remenber file(mysql-bin.000003) and position(883).

## 4. Set Slave(replica)

connect slave db.

```bash
docker exec -it mysql_slave mysql -uroot -prootpassword
```
master settings in slave.
```sql
CHANGE MASTER TO MASTER_HOST='mysql_master', MASTER_USER='replica_user', MASTER_PASSWORD='replica_password', MASTER_AUTO_POSITION=1;
START SLAVE;

-- check Slave status
SHOW SLAVE STATUS\G;

*************************** 1. row ***************************
               Slave_IO_State: Waiting for source to send event
                  Master_Host: mysql_master
                  Master_User: replica_user
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.000003  <--- master file
          Read_Master_Log_Pos: 1444
               Relay_Log_File: d41561b21952-relay-bin.000003
                Relay_Log_Pos: 1660
        Relay_Master_Log_File: mysql-bin.000003
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 1444
              Relay_Log_Space: 3042467
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: ebf8005f-292f-11ef-9015-0242c0a8a703
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Replica has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set: ebf8005f-292f-11ef-9015-0242c0a8a703:1-11
            Executed_Gtid_Set: ebf8005b-292f-11ef-ae61-0242c0a8a702:1-6,
ebf8005f-292f-11ef-9015-0242c0a8a703:1-11
                Auto_Position: 1
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
       Master_public_key_path:
        Get_master_public_key: 0
            Network_Namespace:
1 row in set, 1 warning (0.00 sec)
```

## 5. Test

```sql
# on Master
USE testdb;
CREATE TABLE test_table (id INT PRIMARY KEY, data VARCHAR(100));
INSERT INTO test_table (id, data) VALUES (1, 'Hello World'), (2, 'Replication Test');

mysql> show tables;
+------------------+
| Tables_in_testdb |
+------------------+
| test_table       |
+------------------+
1 row in set (0.00 sec)

mysql> SELECT * FROM test_table;
+----+------------------+
| id | data             |
+----+------------------+
|  1 | Hello World      |
|  2 | Replication Test |
+----+------------------+
2 rows in set (0.00 sec)
```

```sql
# on Slave
USE testdb;
SELECT * FROM test_table;

mysql> SELECT * FROM test_table;
+----+------------------+
| id | data             |
+----+------------------+
|  1 | Hello World      |
|  2 | Replication Test |
+----+------------------+
2 rows in set (0.00 sec)
```

---

### Issue
```
Last_IO_Error: Error connecting to source 'replica_user@master:3306'. This was attempt 2/86400, with a delay of 60 seconds between attempts. Message: Authentication plugin 'caching_sha2_password' reported error: Authentication requires secure connection.`

- MySQL 8.0에서 기본 인증 플러그인 'caching_sha2_password'를 사용시 보안 연결을 요구하여 발생  
- SSL을 사용한 보안 연결을 설정하여 해결
- 여기서는 로컬에서 간단한 실습을 위해 `mysql_native_password`를 사용
```

```
Last_IO_Error: Fatal error: The replica I/O thread stops because source and replica have equal MySQL server ids; these ids must be different for replication to work (or the --replicate-same-server-id option must be used on replica but this does not always make sense; please check the manual before using it).`

- Master와 Slave의 MySQL 서버 ID가 동일하여 발생
- 각 서버가 고유한 서버 ID를 가져야 함
- docker compose에서 각 서버에 고유한 서버ID를 할당
```

- Master의 Postion 정보를 사용하지 않는 이유
`MASTER_AUTO_POSITION`을 활성화하면 GTID를 사용하여 자동으로 위치를 추적하고 복제를 설정한다. 그러면 file과 position을 수동으로 설정할 필요가 없다.  
binlog position 기반이라면 file과 position을 명시적으로 설정해주어야 한다.
