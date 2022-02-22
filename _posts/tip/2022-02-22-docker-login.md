---
layout: post
section-type: post
title: Docker - permission denined docker daemon socket
category: tip
tags: [ 'tip' ]
---

Docker Compose으로 배포를 진행하고 있었습니다.

Docker 이미지중 private 이미지가 있어서 Docker hub에 로그인을 해야 했습니다.

하지만 로그인이 계속 실패하고, 로그아웃 후 다시 시도해도 아래의 메시지만 나올 뿐이였습니다.


```
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/auth": dial unix /var/run/docker.sock: connect: permission denied
```

답은 이미 메시지에 나와 있었습니다. 도커 소켓의 권한을 변경해주면 해결됩니다.

```bash
$ sudo chmod 666 /var/run/docker.sock
```

---

[NEWBEDEV](https://newbedev.com/got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket-at-unix-var-run-docker-sock-post-http-2fvar-2frun-2fdocker-sock-v1-24-auth-dial-unix-var-run-docker-sock-connect-permission-denied-code-example)
