---
layout: post
section-type: post
title: Docker Tutorial
category: deploy
tags: [ 'deploy' ]
---

![]({{ site.url }}/img/post/docker/logo.png)

Prakhar Srivastav가 작성한 Docker for beginners 입니다.

> 출처 [docker-curriculum](https://docker-curriculum.com/)

---

## What is Docker?

Wikipedia defines Docker as "an open-source project that automates the deployment of software applications inside containers by providing an additional layer of abstraction and automation of OS-level virtualization on Linux."


## Hello World

`pull` 명령으로 Docker registry에서 busybox라는 이미지를 다운받습니다.

```
$ docker pull busybox
```

`images` 명령으로 다운받은 이미지를 확인합니다.

```
$ docker images
REPOSITORY              TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
busybox                 latest              59788edf1f3e        2 months ago         1.15 MB
```

## Docker run

`run` 명령으로 이미지를 기반으로 컨테이너를 실행합니다.
```
$ docker run busybox
```

그냥 `run`만 실행하면 docker 클라이언트는 이미지를 찾고(없으면 Docker registry에서 찾아서 다운 받습니다.) 컨테이너를 로드한 후 해당 컨테이너에서 명령을 실행합니다. 위 명령은 실행후 명령이 제공되지 않아서 컨테이너가 부팅되고 빈 명령이 실행 된 후 종료됩니다.

```
$ docker run busybox echo "hello from busybox"
hello from busybox
```

위 명령은 컨테이너에서 echo 명령을 실행한 후 종료합니다. 주목 할 점은 실행된 시간입니다. virtual machine으로 위 액션을 취하는 것과 큰 차이가 있습니다.

`ps` 명령으로 현재 실행중인 모든 컨테이너를 확인합니다.

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

현재 컨테이너가 실행되고 있지 않기 때문에 빈 행만 표시됩니다.

`ps` 명령에  `-a` 플래그를 사용합니다.

```
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
305297d7a235        busybox             "uptime"            11 minutes ago      Exited (0) 11 minutes ago                       distracted_goldstine
ff0a5c3750b9        busybox             "sh"                12 minutes ago      Exited (0) 12 minutes ago                       elated_ramanujan
14e5bd11d164        hello-world         "/hello"            2 minutes ago       Exited (0) 2 minutes ago                        thirsty_euclid
```

컨테이너에서 하나 이상의 명령을 실행해봅니다.

```
$ docker run -it busybox sh
/ # ls
bin   dev   etc   home  proc  root  sys   tmp   usr   var
/ # uptime
 05:45:21 up  5:58,  0 users,  load average: 0.00, 0.01, 0.04
```

`-it` 플래그는 컨테이너의 cli가 실행됩니다.

`docker run -help` 명령으로 지원하는 모든 플래그 리스트를 확인 할 수 있습니다.

`docker ps -a`를 실행하면 컨테이너 종료 후에도 컨테이너 잔재들을 확인 할 수 있습니다. docker를 여러번 실행하고 종료하면 디스크 공간을 많이 소모하기 됩니다. `docker rm` 명령으로 잔재들을 삭제 할 수 있습니다.

```
$ docker rm 305297d7a235 ff0a5c3750b9
305297d7a235
ff0a5c3750b9
```

삭제 할 컨테이너가 많을 경우 중지된 컨테이너를 `docker container prune`으로 한번에 삭제 할 수 있습니다.

```
$ docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
4a7f7eebae0f63178aff7eb0aa39f0627a203ab2df258c1a00b456cf20063
f98f9c2aa1eaf727e4ec9c0283bcaa4762fbdba7f26191f26c97f64090360

Total reclaimed space: 212 B
```

`docker rmi` 명령으로 이미지를 삭제 할 수 있습니다.

## Terminology

- Images : 컨테이너의 기초를 형성하는 Docker 이미지.
- Containers : Docker 이미지에서 생성되고 실제 응용 프로그램을 실행합니다.
- Docker Daemon : Docker 컨테이너 빌드, 실행, 배포 등을 관리하는 호스트에서 실행되는 백그라운드 서비스. 클라이언트가 통신하는 운영 체제애서 실행되는 프로세스입니다.
- Docker Client : 사용자가 Daemon과 상호 작용 할 수 있는 cli.
- Docker Hub : Docker 이미지의 레지스트리.

## Webapps with Docker

### Static Sites

Docker Hub에서 Docker 이미지를 가져와 컨테이너를 실행하고 웹서버를 실행하여 정적 웹사이트를 운영합니다.

이 예제는 레지스트리(prakhar1989/static-site)의 이미지를 데모로 사용합니다.
`-rm` 플래그는 컨테이너가 종료될 때 컨테이너를 자동으로 제거합니다.

```
$ docker run --rm prakhar1989/static-site
Nginx is running...
```

로컬에 해당 이미지가 없는 경우 레지스트리에서 이미지를 가져온 후 실행됩니다.
`Ctrl + c`으로 컨테이너를 중지시킬 수 있습니다.

위 경우 클라이언트는 포트를 공개하지 않기 때문에 포트를 게시하는 플래그를 조합하여 다시 실행해야 합니다.

```
$ docker run -d -P --name static-site prakhar1989/static-site
04bf7fba4e532ddeb41f9a6b45b585e0d904811706ffdf8ec183a83739292bd8
```

`-d`는 분리모드(컨테이너가 실행되고 터미널은 컨테이너와 분리된 상태)이고, `-P`(대소문자 주의)는 모든 노출된 포트를 임의의 포트에 게시하고, `--name`은 컨테이너의 이름을 정의합니다. `--name` 플래그를 사용하지 않으면 임의의 이름으로 생성됩니다.

`docker port [CONTAINER]` 명령으로 포트를 확인 할 수 있습니다.

```
$ docker port static-site
443/tcp -> 0.0.0.0:32770
80/tcp -> 0.0.0.0:32771
```

브라우저를 사용해 'http://localhost:32771/'으로 접속 할 수 있습니다.

컨테이너에 연결 할 포트를 직접 지정 할 수도 있습니다.

```
$ docker run -p 8888:80 prakhar1989/static-site
Nginx is running...
```

![]({{ site.url }}/img/post/docker/static.png)

분리모드의 컨테이너를 중지하려면 `docker stop [CONTAINER]`를 실행합니다.

```
$ docker stop static-site
static-site
```

## Docker Images

`docker images` 명령으로 로컬에서 사용 할 수 있는 이미지 목록을 확인할 수 있습니다.

```
$ docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
prac/docker_test          latest              67c5e884558e        18 hours ago        700MB
nginx                     latest              568c4670fa80        2 weeks ago         109MB
ubuntu                    16.04               a51debf7e1eb        3 weeks ago         116MB
ubuntu                    latest              93fd78260bd1        3 weeks ago         86.2MB
busybox                   latest              59788edf1f3e        2 months ago        1.15MB
python                    3-onbuild           292ed8dee366        5 months ago        691MB
prakhar1989/static-site   latest              f01030e1dcf3        2 years ago         134MB
```

'TAG'는 이미지의 특정 스냅샷을 나타내고, 'IMAGE ID'는 해당 이미지의 고유 식별자입니다.

GIT과 비슷한 관점으로 생각해 볼 수 있습니다. 이미지는 변경 사항을 커밋한 여러 버전이 있을 수 있습니다. 특정 버전 번호를 제공하지 않으면 클라이언트는 기본값으로 최신 버전을 가져옵니다.

```
$ docker pull ubuntu:12.04
```

Docker Hub에는 수만 개의 이미지가 있습니다. `docker search`를 통해 cli에서 직접 이미지를 검색 할 수 있습니다.

이미지의 중요한 점은 **Base images** 와 **Child images** 입니다.

- Base images : 부모 이미지가 없는 일반 이미지. 일반적으로 ubuntu와 같은 OS 이미지입니다.
- Child images : Base images를 기반으로 추가 기능을 추가한 이미지입니다.

Base images, Child images로 사용할 수 있는 Official images와 User images가 있습니다.

- Official images : Docker에서 공식적으로 유지 관리 및 지원하는 이미지입니다. 일반적으로 한 단어로 이루어저 있고, 'python', 'ubuntu', 'busybox', 'hello-world' 등이 공식 이미지입니다.
- User images : 사용자가 만들고 공유한 이미지입니다. Base images를 바탕으로 추가 기능이 추가되었습니다. 일반적으로 user/image-name 형식을 취합니다.


## Our First Image

이제 도커 이미지를 직접 빌드해봅니다. 이번에 사용할 예제는 접속할 때마다 임의의 고양이 GIF를 표시하는 Flask 앱입니다. 아래 명령으로 git에서 클론해옵니다.

```
$ git clone https://github.com/prakhar1989/docker-curriculum
$ cd docker-curriculum/flask-app
```

우리가 만들 이미지는 Base images를 기반으로 합니다. 위 플라스크앱은 파이썬으로 작성되었기 때문에 Base images는 Python3(python:3-onbuild)가 될 것입니다.

> 이러한 이미지는 'onbuild' 트리거가 여러개 포함되어 있어 대부분의 응용 프로그램을 부트 스트랩하는데 필요합니다. 빌드는 requirements.txt 파일을 복사하고, 상기 파일에서 `pip install`를 하고, 현재 디렉토리를 '/usr/src/app'에 복사합니다.

즉 'onbuild' 버전은 앱을 실행하는 지루한 부분을 자동화하는 helper가 포함됩니다. 이러한 작업은 수동으로 수행하거나 이러한 작업을 스크립팅하는 작업을 대체해줍니다.

## Dockerfile

Dockerfile은 이미지를 만드는 동안 Docker 클라이언트가 호출하는 명령 목록을 포함하는 텍스트 파일입니다. 이미지 생성 프로세스를 자동화하는 간단한 방법입니다. Dockerfile에 작성한 명령은 Linux 명령과 거의 동일합니다. 자신만의 도커 파일을 만들려면 Linux 구문을 숙지해야 합니다.

플라스크 앱과 동등한 위치의 디렉토리에 Dockerfile라는 이름의 텍스트 파일을 만듭니다.


```
# 기본 이미지를 지정하는 것으로 시작합니다.
FROM python:3-onbuild
```

```
# 다음은 파일을 복사하고 종속성을 설치하는 명령을 작성하지만
# onbuild 버전이 알아서 처리합니다.
# 실행할 포트 번호를 설정합니다.
EXPOSE 5000
```

```
# 마지막으로 응용 프로그램을 실행하기 위한 명령을 작성합니다.
# 즉 `python ./app.py`를 수행합니다.
CMD ["python", "./app.py"]
# CMD의 주 목적은 시작될 때 어떤 명령을 실행해야 하는지 컨테이너에 알리는 것입니다.
```

위 명령들을 정리된 최종 Dockerfile 입니다.

```
# our base image
FROM python:3-onbuild

# specify the port number the container should expose
EXPOSE 5000

# run the application
CMD ["python", "./app.py"]
```

이제 Dockerfile을 작성하였으므로 이미지를 만들 수 있습니다. `docker build` 명령은 Dockerfile에서 Docker 이미지를 생성하는 작업을 수행합니다. 명령할때 마지막에 . 을 잊지 말아야 합니다. user는 Docker Hub에 등록할때 생성한 사용자 이름과 동일해야 합니다. `-t` 옵션과 함께 태그 이름과 Dockerfile이 들어 있는 디렉토리 위치를 지정합니다.

```
$ docker build -t prac/docker_test .
Sending build context to Docker daemon 8.704 kB
Step 1 : FROM python:3-onbuild
# Executing 3 build triggers...
Step 1 : COPY requirements.txt /usr/src/app/
 ---> Using cache
Step 1 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Using cache
Step 1 : COPY . /usr/src/app
 ---> 1d61f639ef9e
Removing intermediate container 4de6ddf5528c
Step 2 : EXPOSE 5000
 ---> Running in 12cfcf6d67ee
 ---> f423c2f179d1
Removing intermediate container 12cfcf6d67ee
Step 3 : CMD python ./app.py
 ---> Running in f01401a5ace9
 ---> 13e87ed1fbc2
Removing intermediate container f01401a5ace9
Successfully built 13e87ed1fbc2
```

'python:3-onbuld' 이미지가 없다면 클라이언트는 먼저 이미지를 가져온 다음 이미지를 생성합니다.  

마지막으로 이미지를 실행하고 실제 작동하는지 확인합니다.

```
$ docker run -p 8888:5000 prac/docker_test
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

방금 실행한 명령은 컨테이너 내부의 서버에 대해 5000 포트를 사용하고, 8888 포트에서 외부로 노출했습니다. 8888 포트로 접속해봅니다.

![]({{ site.url }}/img/post/docker/cat.png)

성공적으로 도커 이미지를 만들었습니다.
