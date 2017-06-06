---
layout: post
section-type: post
title: SSH passwd 없이 접속하기
category: deploy
tags: [ 'deploy' ]
---
TDD 스터디하는중 2부의 내용은 배포와 관련된 내용이 진행됩니다.  
[AUTOMATING DEPLOYMENT WITH FABRIC](https://kimdoky.github.io/tdd/2017/05/31/tdd-newTdd-ch11.html){:target="_blank"}  

진행 도중 SSH로 접속시 패스워드 때문에 진행이 막히게 되었습니다.  

AWS EC2로 진행하였고, EC2는 기본적으로 Keypair를 이용하여 접속하게 됩니다.

fabric으로 접속시 Keypair를 사용할 수 없었기 때문에 EC2 접속에서 패스워드 부분에서 접속이 막혀 더이상 진행되지 못하였습니다.

Python Korea, Googling 등 수 없는 삽질 끝에 해결하여 포스팅합니다.

---

그럼 해결 방안입니다.

클라이언트(로컬)에서 공개키를 서버에 등록하여 접속하는 방법입니다.  
sshpass를 이용하여 접속하는 방법도 있지만 비밀번호가 커맨드라인에 노출되기 때문에 보안상 좋지 않아서 공개키 등록 방식을 채택하였습니다.  

공개키가 이미 있다면 그 공개키를 등록하면 되고 없다면 아래의 명령으로 공개키를 생성합니다.(로컬에서)

```
ssh-keygen -t rsa
```
명령 후 나오는 입력란은 모두 그냥 넘어가도 무관합니다.

생성 후 .ssh 폴더를 보면 공개키가 생성된 것을 확인할 수 있습니다.

```
~ » ls .ssh
id_rsa          id_rsa.pub      known_hosts
```

그럼 이 공개키를 서버에 등록합니다. (로컬에서 실행)

> 구글링하여 나온 자료에는 어디에서 진행하는지에 대해 잘 설명이 안되어 있어서 이 부분에서 삽질이 있었습니다.

```
~ » ssh-copy-id -i ~/.ssh/id_rsa.pub [user]@[host]
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed:
 ...   
Permission denied (publickey).
```
권한 에러가 발생합니다. 멘붕...  
하지반 구글신에게 다시 문의하여 답을 찾았습니다.

서버에서 암호 인증 설정을 해줍니다.
(서버에서)

```
sudo vi /etc/ssh/sshd_config

PasswordAuthentication yes
```

그리고 (서버에서) 재시작합니다.

```
sudo /etc/init.d/ssh restart
```

그리고 다시 로컬에서 공개키를 다시 복사를 시도하면 잘 되는 것을 확인 할 수 있습니다.

(로컬에서)

```
~ » ssh-copy-id -i ~/.ssh/id_rsa.pub [user]@[host]
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed:
...   
Number of key(s) added:        1

Now try logging into the machine, with:   "ssh '[user]@[host]'"
and check to make sure that only the key(s) you wanted were added.
```
이제 다시 패스워드 없이 접속을 시도해보면 잘 됩니다. (fabric을 공부중이라서 fabric으로 접속하였습니다.)

```
~/Git/Study/TDD/superlists/NewVersiondTdd/deploy_tools » fab deploy:host=doky@staging.czarcie.com
[doky@staging.czarcie.com] Executing task 'deploy'
[doky@staging.czarcie.com] run: mkdir -p /home/doky/sites/staging.czarcie.com/database
[doky@staging.czarcie.com] run: mkdir -p /home/doky/sites/staging.czarcie.com/static
[doky@staging.czarcie.com] run: mkdir -p /home/doky/sites/staging.czarcie.com/virtualenv
[doky@staging.czarcie.com] run: mkdir -p /home/doky/sites/staging.czarcie.com/source
[doky@staging.czarcie.com] run: cd /home/doky/sites/staging.czarcie.com/source && git fetch
...
```

이렇게 패스워드 없이 ssh 접속하기 삽질이 완료되었습니다.  


참조  
[serverfault](https://serverfault.com/questions/684346/ssh-copy-id-permission-denied-publickey){:target="_blank"}  
[이 세상에 하나는 남기고 가자](https://blog.asamaru.net/2016/01/26/ssh-login-without-password/){:target="_blank"}  
[신매력](http://marobiana.tistory.com/53#recentTrackback){:target="_blank"}  
