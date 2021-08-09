---
layout: post
section-type: post
title: Linux - Process
category: tip
tags: [ 'tip' ]
---

## Process

- 실행중인 프로그램
- 실행시에 PID(Process Identity)가 할당되어 관리
- Background Process: 사용자의 입력과 관계없이 실행
- Foreground Process: 명령 입력 후 수행 종료까지 기다려야 함

## Process 생성

- fork: 새로운 프로세스를 위해 메모리를 할당받아 복사본 형태의 프로세스를 실행 (기존 프로세스는 그대로 실행)
- exec: 호출한 프로세스의 메모리에 새로운 프로세스의 코드로 덮어씌워 실행

리눅스가 부팅하면 커널이 init 프로세스를 최초의 프로세스로 실행하고 PID는 1번을 할당  
후에 시스템 운영에 필요한 데몬 등의 다른 프로세스들은 init 프로세스를 fork 방식으로 자식 프로세스로 생성된다.

## Foreground / Background 전환

### Foreground

cli 입력시 마지막에 `&`를 입력하면 포어그라운드로 실행한다.

```bash
$ find / -name '*.*' > find_list.txt &
```

포어그라운드로 실행하면 Job Number와 PID를 출력한다.  

### Foreground -> Background

- Foreground -> suspend -> Background
- 작업중에 Ctrl + z 를 누르면 suspend(대기) 변경(일시정지)
- jobs 으로 대기 중인 작업들의 상태를 확인
- `bg` 으로 suspend 상태의 프로세스를 Background로 전환

### Background -> Foreground

- `jobs`으로 확인되는 작업번호로 변환할 프로세스를 확인 및 `fg [작업번호]`으로 지정하여 변환
- `+`는 주로 처리되는 프로세스로, 보통 가장 나중에 실행한 프로세스. 작업번호 없이 `fg`를 하면 이 작업이 Foreground로 전환됨
- `-`는 `+`의 다음 우선순위

## Signal

- 특정 프로세스가 다른 프로세스에게 보내는 신호
- `kill -l`으로 시그널들을 확인 가능

num | name | desc
---|---|---
1 | SIGHUP (HUP) | 터미널에서 접속이 끊김 시그널 <br/> 데몬 관련 환경 설정 파일을 변경후 적용을 위해 재시작시 사용
2 | SIGINT (INT) | ctrl + c <br/> 키보드 인터럽트 시그널
3 | SIGQUIT (QUIT) | ctrl + \ <br/> 키보드로부터 오는 실행 중지 시그널
9 | SIGKILL (KILL) | 프로세스 강제 종료 시그널
15 | SIGTERM (TERM) | 가능한 정상 종료 시그널
18 | SIGCOUNT (CONT) | STOP 시그널 등에 의해 정지된 프로세스를 다시 실행
19 | SIGSTOP (STOP) | 터미널에서 입력된 정지 시그널
20 | SIGTSTP (TSTP) | ctrl + z <br/> 실행 정지후 다시 실행을 계속하기 위해 대기시키는 시그널

## daemon

- 주기적, 지속적인 서비스 요청을 처리하기 위해 계속 실행되는 프로세스(Background)
- 이름 뒤에 d를 붙임
- standalone / inetd
- standalone: 부팅 시에 실행되어 해당 프로세스가 메모리에 계속 상주하면서 클라이언트의 서비스 요청을 처리
- inetd: 클라이언트의 서비스 요청이 있을때만 프로세스를 종료하고 종료하면 프로세스도 자동 종료
 - 유닉스 시절 부족한 메모리를 효율적으로 관리하기 위함이었고, xinetd으로 대체 되었지만, 최근에는 메모리 용량이 커져서 대부분 standalone으로 실행

- 부팅과 관련된 정보는 /etc/rc.d 에 모아두고, 관련 데몬들은 init.d와 rc0.d ~ rc.6.d 를 이용하여 데몬의 실행을 조절 (각 번호는 런 레벨)
