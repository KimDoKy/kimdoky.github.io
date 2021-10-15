---
layout: post
section-type: post
title: Deploy - Jenkins 컨테이너에서 Docker 실행하기
category: tech
tags: [ 'tech' ]
---

Jenkins 도입을 위해 이러저러한 시나리오를 시도해 보고 있습니다. (Jenkins도 컨테이너로 돌고 있습니다)

그러던 중 현재 프로젝트를 컨테이너화 시켜서 Jenkins에서 Docker로 돌리면 유지보수에 좋을 것으로 판단하고 진행을 하였습니다.  

---

### 우선 돌려보자!

우선 빌드에서 테스트로 도커를 돌려보기 위해 nginx 를 실행해 보았습니다.

```
docker run -p 8080:80 nginx
```

그리고 빌드를 진행하니...

```
+ docker run -p 8080:80 nginx
/tmp/jenkins15607360083466842074.sh: 3: docker: not found
```

뭐 당연하지만 도커를 찾을 수 없습니다. 

---

### 해결방안..?

[스택오버플로](https://stackoverflow.com/questions/44850565/docker-not-found-when-building-docker-image-using-docker-jenkins-container-pipel
)의 답변입니다.

1. 도커가 설치되어 있는 이미지 사용
2. jenkins 이미지를 빌드하여 호스트에 볼륨을 마운트하고 동일한 볼륨으로 다른 컨테이너를 만들고 bash cmd를 실행하여 도커를 설치한다.
3. jenkins 컨테이너에서 사용할 호스트 시스템의 설치된 도커 경로를 추가

3번의 방법이 가장 간단하기도 하고, 많은 분들이 해결법으로 채택하여서 진행하였습니다.

```
docker run \
--name jenkins --rm \
-u root -p 8080:8080 -p 50000:50000 \
-v $(which docker):/usr/bin/docker\
-v $HOME/.jenkins/:/var/jenkins_home
-v /var/run/docker.sock:/var/run/docker.sock \
jenkins/jenkins:latest
```

```
+ docker run -p 8080:80 nginx
/tmp/jenkins9070985789718332029.sh: 3: docker: Permission denied
```

음... 이번엔 권한이 없다고 하네요.

컨테이너를 root로 실행하여도 똑같이 권한 에러가 발생합니다.

jenkins 컨테이너의 도커 소켓 소유권 및 모드를 바꾸어 보았습니다. 하지만 실패했습니다.  

시간을 너무 많이 잡아 먹는 것 같습니다.

---

### Jenkins를 베이스로 Docker를 설치한 이미지를 빌드하자.

시간이 너무 많이 걸리는 관계로, jenkins 이미지를 베이스로 도커를 설치한 이미지를 생성하는 방법으로 진행하였습니다.

jenkins 이미지는 데비안 os를 사용하고 있습니다.  

[docker doc](https://docs.docker.com/engine/install/debian/)를 참고하여 Dockerfile을 작성하여 빌드합니다.


```
FROM jenkins/jenkins:lts

USER root
# docker
RUN apt-get update
RUN apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN cat /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io
```

이제 빌드를 진행합니다.

```
$ docker build . -t leafunk/jenkins_docker:0.1
```

일단 컨테이너 안에서는 도커가 정상적으로 실행이 됩니다.


```
docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
```

빌드는 실패했지만 끝이 보이네요.

---

### 드디어...!?


일단 주말을 보내고 다음주에 계속...

