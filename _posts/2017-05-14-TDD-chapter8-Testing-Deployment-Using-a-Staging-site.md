---
layout: post
section-type: post
title: TDD-Chapter 8. 스테이징 사이트를 이용한 배포 테스트
category: tdd
tags: [ 'tdd' ]
---

# Chapter 8. 스테이징 사이트를 이용한 배포 테스트

## TDD와 배포 시 주의가 필요한 사항

[이전 블로그 참조]({{ url.site }}/tdd/2017/05/14/TDD-attention.html)

### 이번 장의 개요###

1. 스테이징 서버에서 실행할 수 있도록 FT를 수정한다.
2. 서버를 구축하고 거기에 필요한 모든 소프트웨어를 설치한다. 또한 스테이징과 운영 도메인이 이 서버를 가리키도록 설정한다.
3. Git을 이용해서 코드를 서버에 업로드한다.
4. Django 개발 서버를 이용해서 스테이징 사이트에서 약식 버전의 사이트를 테스트한다.
5. Virtualenv 사용법을 배워서 서버에 있는 파이썬 의존 관계를 관리하도록 한다.
6. 과정을 진행하면서 항시 FT를 실행한다. 이를 통해 단계별로 무엇이 동작하고, 무엇이 동작하지 않는지 확인한다.
7. Gunicorn, Upstart, 도메인 소켓 등을 이용해서 사이트를 운영 서버에 배포하기 위한 설정을 한다.
8. 설정이 정상적으로 동작하면 스크립트를 작성해서 수동으로 작업을 자동화 하도록 한다. 이를 통해 사이트 배포를 자동화할 수 있다.
9. 마지막으로, 동일 스크립트를 이용해서 운영 버전의 사이트를 실제 도메인에 배포하도록 한다.

## 항상 그렇듯이 테스트부터 시작
기능 테스트를 약간 변경해서 스테이징 사이트에서 실행되도록 한다. 이를 위해 인수 하나를 해킹해서 테스트 임시 서버가 실행되는 주소를 변경한다.


```python
# functional_tests/tests.py

import os
[...]

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')  #1
        if staging_server:
            self.live_server_url = 'http://' + staging_server  #2
```
1. STAGING_SERVER라는 환경 변수를 사용하기로 결정했습니다.
2. 해킹은 다음과 같습니다. self.live_server_url을 "실제"서버의 주소로 대체합니다.

이 해킹이 다른 부분을 망가뜨린 것은 아닌지 FT를 실행해서 확인해본다.

스테이징 서버 URL에 대해 실행해본다. URL 하나 정도 구입해두자.

`STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests`

두 테스트가 모두 실패하는 것을 볼 수 있다. 예상한 실패인데, 아직 스테이징 사이트를 구축하지 않았기 때문이다. 트레이스백을 보면 테스트가 도메인 제공자의 홈페이지에서 끝나는 것을 알 수 있다.

> 실습하는 도중에 파이썬과 Django의 버전이 업그레이드로 인해 책도 업데이트 되었다. 책 그대로 실습하면 `manage.py test: error: unrecognized arguments: --liveserver=staging.czarcie.com` 라는 인식할수 없는 인수 에러가 발생한다.
> 책이 업데이트 되었기 때문에 코드와 명령어 또한 업데이트해야 진행이 가능하다.

어째뜬 FT가 제대로 된 결과를 보여주니 커밋 ㄱㄱ.

## 도메인명 취득

## 수동으로 서버를 호스트 사이트로 프로비저닝하기
> 프로비저닝(provisioning)은 사용자의 요구에 맞게 시스템 자원을 할당, 배치, 배포해 두었다가 필요 시 시스템을 즉시 사용할 수 있는 상태로 미리 준비해 두는 것 - [위키백과](https://ko.wikipedia.org/wiki/%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D){:target="_blank"}

"배포"를 두 단계로 나눌 수 있다.

- 신규 서버를 프로비저닝(provisioning)해서 코드를 호스팅할 수 있도록 한다.
- 신규 버전의 코드를 기존 서버에 배포한다.

배포 시마다 새 서버를 사용할 수 있다. 이것은  PythonAnywhere를 통해 구현할 수 있다. 하지만 규모가 큰 사이트나 기존 사이트의 대규모 업데이트 시에만 필요한 것이다. 간단한 사이트에선 두 단계로 작업을 나누는 것이 좋다. 최종적으로 이 두가지 작업을 자동화하지만, 지금은 수동 프로비저닝 시스템으로 충분하다.

### 사이트를 호스트할 곳 정하기
사이트 호스팅을 위한 다양한 솔루션이 존재하지만, 대략 두 가지 형태로 분류

- 자체 서버(가상도 가능) 운영
- Heroku, DotCloud, OpenShift, PythonAnywhere 같은 PlatForm-As-A-Service(PaaS) 서비스 이용

작은 규모의 사이트에선 PaaS가 많은 이점이 있기 때문에 이를 추천하지만 지금은 사용하지 않는다. PaaS의 서비스 방식이 서로 다 다르기 때문에 배포 절차도 다르다. 즉, 하나를 배우더라도 다른 서비스에 적용할 수 없고, 지금 이순간에도 서비스 프로세스가 변경되거나 폐업될 수도 있다. 그러므로, PaaS 대신 SSH와 웹 서버 설정을 이용한 전통적인 서버 관리 방식으로 진행한다.

여기서 직접 구축하는 서버는 PaaS를 통해 사용할 수 있는 환경과 거의 같기 때문에, 배포 과정 중에 배우는 모든 것을 프로비저닝 솔루션에 상관없이 적용할 수 있다.

### 서버 구축하기
솔루션 선택의 조건만 충족되면 어떤 솔루션이든 상관없다.
나는 AWS EC2로 선택....(아 귀찮....ㅠ)

- 우분투(Ubuntu)(13.04 버전 이상)가 설치돼 있을 것
- 루트 권한이 있을 것
- 인터넷상에 공개돼 있을 것
- SSH로 접속할 수 있을 것

우분투를 추천하는 이유는 파이썬 3.4를 기본으로 탑재하고 있기 때문이다. 또한 Ngnix 설정이 용이하다.


[Ubuntu Linux Deploy](https://github.com/KimDoKy/FastCamp/blob/master/Deploy/01.Ubuntu%20Linux%20Deploy.md)

### 사용자 계정, SSH, 권한

```
➜  / sudo useradd -m -s /bin/bash czarcie
# czarcie라는 사용자 추가
# -m은 home 폴더를 생성
# -s 는 czarcie가 bash를 사용하도록 설정

➜  / sudo usermod -a -G sudo czarcie
# czarcie를 sudoers 그룹에 추가

➜  / sudo passwd czarcie
# czarcie 패스워드 설정
Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully

➜  / su - czarcie
```
SSH 패스워드보다는 개인 키(private key)를 이용한 인증 방법을 배우는 것이 좋다.
로컬 PC에서 공개키(public key)를 가져다가 서버의 `~/.ssh/authorized_key`에 추가하면 된다.

<https://www.linode.com/security/ssh-keys>{:target="_blank"} 에 공개 키 설정 방법이 잘 정리 되어있다.

### Nginx 설치
웹 서버 설치가 필요하다. Nginx 설치는 매우 간단해서 `apt-get` 명령만 실행해 주면 끝이다. 명령 실행 후 바로 "Hello World"를 볼 수 있다.

```
czarcie@ip-172-31-12-**:~$ sudo apt-get install nginx
czarcie@ip-172-31-12-**:~$ sudo systemctl start nginx
```

사이트 IP 주소에 접속해 보면 "Welcome to nginx" 페이지를 볼 수 있다.

![]({{ url.site }}/img/post/tdd/hellonginx.png)

페이지가 보이지 않는다면 방화벽이 포트 80을 막았기 때문일 수도 있다. AWS에선 "security group"을 설정해서 포드 80을 열어주어야 한다.

![]({{ url.site }}/img/post/tdd/security80.png)

루트 권한이 있는 상태에서 시스템에 필요한 필수 소프트웨어들(Python, Git, pip, Virtualenv)를 설치한다.

```
czarcie@ip-172-31-12-**:~$ sudo apt-get install git python3 python3-pip
czarcie@ip-172-31-12-**:~$ sudo pip3 install virtualenv
```

### 스테이징 서버와 운영 서버를 위한 도메인 설정
IP 주소 지정 시마다 혼란스러울 수 있으니, 스테이징과 운영 도메인이 우리가 구축한 서버를 가리키도록 설정한다.

### FT를 이용해서 도메인 및 Nginx가 동작하는지 확인
설정한 것이 정상적으로 동작하는지 확인하기 위해 기능 테스트를 재실행한다.
실패 메세지가 약간 바뀐 것을 알 수 있다(Nginx 내용이 포함 되었다).

```
STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_new_item"]
[...]
AssertionError: 'To-Do' not found in 'Welcome to nginx!'
```
## 코드를 수동으로 배포
스테이징 사이트를 복사해보고 실행해보고, Nginx와 Django가 제대로 상호작용하는지 확인하도록 한다. 이를 통해 프로비저닝이 아닌 실제 "배포" 작업에 들어가게 된다.

> 일반적으로 배포와 프로비저닝을 구분 짓는 한가지 규칙은, 프로비저닝은 루트 권한이 필요하고 배포는 필요 없다는 것이다.

운영 서버의 소스 디렉토리를 준비해야한다.

```
/home/elspeth
├── sites
│   ├── www.live.my-website.com
│   │    ├── database
│   │    │     └── db.sqlite3
│   │    ├── source
│   │    │    ├── manage.py
│   │    │    ├── superlists
│   │    │    ├── etc...
│   │    │
│   │    ├── static
│   │    │    ├── base.css
│   │    │    ├── etc...
│   │    │
│   │    └── virtualenv
│   │         ├── lib
│   │         ├── etc...
│   │
│   ├── www.staging.my-website.com
│   │    ├── database
│   │    ├── etc...
```

각 사이트(스테이징, 운영, 기타 사이트)는 자체 폴더를 가지고 있다. 이 폴더는 다시 소스코드, 데이터베이스, 정적 파일 폴더로 나뉜다. 이런식으로 구성해두면, 예를 들어 소스코드가 신규 버전으로 업데이트 된다해도 데이터베이스를 그대로 유지할 수 있다.

### 데이터베이스 위치 조정
setting.py에 있는 데이터베이스 위치를 변경하고 로컬 PC에서 정상 동작하는지 확인한다. `os.path.abspath`를 이용하는 것이 이후 경로 설정 시 혼란을 줄일 수 있다.

```
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 책에서는 os.path.abspath(os.path.dirname....)으로 나오지만
# 책 출간이후 버젼 업이 있었기 때문에 위의 내용으로 한다.
[...]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
    }
}
```
이제 로컬에서 실행해본다.

```
~/Git/Study/TDD/superlists(master*) » mkdir ../database       
~/Git/Study/TDD/superlists(master*) » ./manage.py migrate --noinput    
[...]
~/Git/Study/TDD/superlists(master*) » ls ../database
db.sqlite3
```
정상적으로 동작한다.

코드를 서버에 올리기 위해서 Git과 코드 공유 사이트를 이용하도록 한다. GitHub이나 BitBucket 등에 업로드한다.

> 서버 배포용 git은 manage.py 파일이 있는곳을 기준으로 gitinit으로 해야한다.

다음과 같이 bash 명령을 이용해서 코드를 옮긴다. export 명령은 bash에서 "로컬 변수"를 설정하는 명령이다.

```
czarcie@ip-172-31-12-**:~$ export SITENAME=staging.czarcie.com
czarcie@ip-172-31-12-**:~$ mkdir -p ~/sites/$SITENAME/database
czarcie@ip-172-31-12-**:~$ mkdir -p ~/sites/$SITANEMT/static
czarcie@ip-172-31-12-**:~$ mkdir -p ~/sites/$SITENAME/virtualenv
czarcie@ip-172-31-12-**:~$ git clone https://github.com/KimDoKy/TDD.git ~/sites/$SITENAME/source
```

> export를 이용해서 정의한 bash 변수는 해당 콘솔이 켜져 있는 동안만 유지된다. 서버에서 로그아웃한 후 다시 로그인하면, 변수는 사라지기 때문에 재설정 해주어야한다. 주의해야 할 것은 변수가 없어도 bash가 에러를 표시하지 않는다는 것이다. 해당 변수를 단순히 빈 문자열로 대체하기 때문에 예측하지 못한 결과가 발생할 수 있다. 의심스럽다면 `echo $SITENAME`을 실행해보자

이제 사이트가 모두 설치됐다. 개발 서버를 실행해보다.(이동한 모든 요소들이 제대로 연결됐는지 확인하기 위한 스모크 테스트라 할 수 있다.)

```
czarcie@ip-172-31-12-**:~$ cd ~/sites/$SITENAME/source
czarcie@ip-172-31-12-**:~/sites/staging.czarcie.com/source/TDD/superlists$ python3 manage.py runserver
```
Django를 설치 하지 않아서 오류가 발생한다.

### requirements.txt 사용하기, Virtualenv 생성

그냥 Django를 설치할 수도 있지만 Django 신규버젼이 나와서 Django를 업데이트하면, 운영 서버와 가른버전의 Django를 가지고 있는 스테이징 사이트를 테스트할 수 없다. 그리고 다른 사용자가 서버상에 있다면 강제적으로 같은 버전의 Django를 사용하도록 해야 한다.

이것을 해결할 수 있는 것이 "virtualenv"이다.

```
(로컬에서)
# virtualenv 설치
$ pip3 install virtualenv
# 서버와 같은 폴더 구조 생성
$ virtualenv --python=python3 ../virtualenv
$ ls ../virtualenv
bin                include            lib                pip-selfcheck.json
```

이것은 ../virtualenv 라는 폴더를 생성해서 여기에 자체 파이썬 및 pip를 저장하고, 파이썬 패키지를 설치하기 위한 위치도 저장한다. 하나의 독립된 "가상 파이썬 환경"이다. 이 환경을 실행하려면 activate라는 스크립트를 실행하면 된다. 이를 통해 시스템 경로 및 파이썬 경로가 virtualenv의 실행 파일 및 패키지 경로로 변경된다.

```
/Git/Study/TDD/superlists(master) » which python3
/usr/local/var/pyenv/versions/3.5.2/envs/TDD/bin/python3
~/Git/Study/TDD/superlists(master) » source ../virtualenv/bin/activate
~/Git/Study/TDD/superlists(master) » which python
python: aliased to python3
~/Git/Study/TDD/superlists(master) » python3 manage.py test lists  
```

> TDD 책은 virtualenv를 모르는 상태로 진행하는 터라 가상환경을 다 만들고 진행을 따라온 나는 여기서 헤매게 되었다...만.. 거두절미하고 가상환경 모두 만들고 진행을 따라왔다면 파일 구조만 서버와 매칭시켜주면 된다.

```
$ git add requirements.txt
$ git commit -m "Add requirements.txt for virtualenv"
```

```
$ git push
```
서버와 로컬의 싱크를 맞춰준다.

```
$ git pull
$ virtualenv --python=python3 ../virtualenv
$ ../virtualenv/bin/pip install -r requirements.txt
$ ../virtualenv/bin/python3 manage.py runserver
```
정상작동이 확인 되었다면 일단 서버를 정지 시킨다.

### 간단한 Nginx 설정

Django를 이용해서 스테이징 서버에 요청을 보낼 수 있도록 Nginx 설정 파일을 생성한다.

server: sudo vi /etc/nginx/sites-available/staging.czarcie.com

```
server {
    listen 80;
    server_name staging.czarcie.com;

    location / {
        proxy_pass http://localhost:8000;
        }
    }
```
이 설정은 스테이징 서버에서만 동작한다는 것을 의미하며, 로컬 포트 8000으로 들어오는 모든 요청을 Django로 보내서 응답하도록 "프록시"한다.
그리고 이것을 symlink를 이용해서 동작 사이트에 추가했다.

```
➜  sites-available echo $SITENAME  # 이 변수가 아직 자신의 사이트를 가리키도 있는지 확인
staging.czarcie.com
➜  sites-available sudo ln -s ../sites-available/$SITENAME /etc/nginx/sites-enabled/#SITENAME
➜  sites-available ls -l /etc/nginx/sites-enabled  # symlink가 있는지 확인
total 0
lrwxrwxrwx 1 root root 34 May 21 09:18 default -> /etc/nginx/sites-available/default
lrwxrwxrwx 1 root root 38 May 21 15:14 #SITENAME -> ../sites-available/staging.czarcie.com
```
진짜 설정 파일은 sites-available에 두고 symlink는 sites-enabled에 두는 것은 Debian/Ubuntu에서 자주 사용되는 Nginx 설정 저장 방법이다. 이 구조는 사이트를 쉽게 시작하고 종료할 수 있도록 한다.

혼란을 막기 위해 기본 "Welcome to Nginx" 설정은 삭제한다.

```
sudo rm /etc/nginx/sites-enabled/default
```
테스트 해보자.

```
sudo service nginx reload
../virtualenv/bin/python3 manage.py runserver
```
>  설정 때문에 디렉토리를 거닐다보면 처음 위치를 잃어버릴수 있다.
> /home/ubuntu/sites/staging.czarcie.com/source  보통은 이 위치에 있다.

사이트가 제대로 동작하는지 접속해보자.

![]({{ site.url }}/img/post/tdd/server1st.png)
> 구입한 도메인으로 접속해야 하지만..
> cloudflare는 너무 처리하는게 느리고 답답하다... SSL 외에는 득이 없는듯..
> 그래서 다른 곳으로 네임서버를 옮겨서 캡쳐에는 적용되지 못하였다.

기능 테스트를 실행해보자.

.....

chromedriver 에서 계속 오류가 난다.  

[Installing Selenium and ChromeDriver on Ubuntu](https://christopher.su/2015/selenium-chromedriver-ubuntu/){:target="_blank"} 을 참고해보자.

그 후에도 error 발생...

[stackoverflow](https://stackoverflow.com/questions/44128139/tdd-djangodeploy-error-selenium-common-exceptions-webdriverexception-messag?noredirect=1#comment75275463_44128139){:target="_blank"}  





### migrate를 이용한 데이터베이스 생성

## 운영 준비 배포 단계
### Gunicorn으로 교체
### Nginx를 통한 정적 파일 제공
### 유닉스 소켓으로 교체하기
### DEBUG를 False로 설정하고 ALLOWED_HOSTS 설정하기
### Upstart를 이용한 부팅 시 Gunicorn 가동
### 변경사항 저장: Gunicorn을 requirements.txt에 추가

## 자동화
### 작업한 것 보호하기
