---
layout: post
section-type: post
title: new TDD-Chapter 9. Testing Deployment Using a Staging Site
category: tdd
tags: [ 'tdd' ]
---

"제품이 출시되기 전까지는 모든 것이 재미있고 게임과 같다." - Devops Borat

사이트의 첫 번째 버전을 대중에게 공개할 때가 되었습니다.  
과연 이 사이트는 유용할까? 없는 것보다 나을까? 실제 작업 목록을 만들 수 있을까? 당연히 "Yes!"이다.  

"아직 로그인 할 수 없잖아!", "작업을 완료했다는 표시를 할 수 없잖아!" 라고 반대하는 사람도 있을 수 있습니다. 정말 그런 기능들이 필요할까요? 사용자가 어떻게 사용할지는 아무도 모릅니다. 사용자가 사이트를 이용하는 이유가 작업 목록 때문이라고 생각할 수 있지만, 실제로 "날치 잡기 좋은 곳 베스트 10" 같은 목록을 만들기 원할 수도 있습니다. 이런 경우 "작업 완료 체크" 같은 기능은 필요가 없을 것입니다. 사이트를 공개하기 전까지는 아무도 모릅니다.

이번 섹션에서는 사이트를 배포하는 방법과 실제 운영 가능한 진짜 웹 서버에 배포하도록 합니다.

## 9.1. TDD and the Danger Areas of Deployment

배포 시 주의가 필요한 사항입니다.

### Static files (CSS, JavaScript, image, etc.)
이 파일들을 제공하기 위해 웹 서버에 특수한 설정을 해주어야 합니다.

### DataBase
권한이나 경로 문제가 있을 수 있으며 배포 시 테스트 데이터 관리에 유의해야 합니다.

### Dependencies (의존 관계)
개발한 소프트웨어와 연계돼 있는 패키지를 서버에 설치해야 하며, 패키지 버전도 확인해야 합니다.

각각에 대한 해결책입니다.

- 실제 운영 사이트에서 사용하는 환경과 동일한 환경의 *Staging Site* 를 이용합니다. 이를 통해 "실제" 사이트에 배포하기 전에 모든 것이 제대로 동작하는지 테스트할 수 있습니다.
- *Staging Site에 대해 FT를 실행* 할 수 있습니다. 이를 통해 서버상에 있는 코드와 패키지가 제대로 된 것임을 다시 확인할 수 있고, 레이아웃용 "Smoke Test"를 통해 CSS가 정상적으로 로딩되는지 알 수 있습니다.
- *Virtualenv* 라는 유용한 툴을 이용해서 하나 이상의 파이썬 애플리케이션이 동작하고 있는 장비에서 패키지 및 패키지 의존 관계를 관리할 수 있습니다.
- 마지막은 *자동화, 자동화, 자동화* 입니다. 자동화된 스크립트를 이용해서 신규 버전을 배포하고, 이를 스테이징 서버와 운영 서버에 동시에 배포함으로, 운영 서버와 스테이징 서버를 가능한 동일 상태로 유지할 수 있습니다.

### 이번 섹션의 개요
이번 섹션에서는 많은 것을 다루기 때문에 진행하기 전에 대략적인 내용을 정리합니다.

1. 스테이징 서버에서 실행할 수 있도록 FT를 수정합니다.
2. 서버를 구축하고 거기에 필요한 모든 소프트웨어를 설치합니다. 또한 스테이징과 운영 도메인이 이 서버를 가리키도록 설정합니다.
3. Git을 이용해서 코드를 서버에 업로드합니다.
4. Django 개발 서버를 이용해서 Staging Site에서 약식 버전의 사이트를 테스트합니다.
5. Virtualenv 사용법을 배워서 서버에 있는 파이썬 의존 관계를 관리하도록 합니다.
6. 과정을 진행하면서 항시 FT를 실행합니다. 이를 통해 단계별로 무엇이 동작하고, 무엇이 동작하지 않는지 확인합니다.
7. Gunicorn, Upstart, 도메인 소켓 등을 이용해서 사이트를 운영 서버에 배포하기 위한 설정을 합니다.
8. 설정이 정상적으로 동작하면 스크립트를 작성해서 수동으로 했던 작업을 자동화하도록 합니다. 이를 통해 사이트 배포를 자동화할 수 있습니다.
9. 마지막으로, 동일 스크립트를 이용해서 운영 버전의 사이트를 실제 도메인에 배포하도록 합니다.

> Staging Server를 다른 곳에서는 "개발"(Development) 서버나 "사전 운영"(Pre production) 서버라고 부르는 경우도 있습니다. 명칭이 어떠하든 중요한 것은 실제 운영 서버와 동일한 환경을 갖춘 서버를 가리킨다는 것입니다.

## 9.2. As Always, Start with a Test
FT를 약간 변경해서 Staging Site에서 실행되도록 합니다. 이를 위해 인수 하나를 해킹해서 테스트 임시 서버가 실행되는 주소를 변경하도록 합니다.

functional_tests/tests.py (ch08l001)

```python
import os
[...]

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER') # 1
        if staging_server:
            self.live_server_url = 'http://' + staging_server # 2  
```
`LiveServerTestCase`는 특정 제약사항이 있습니다. 이 제약사항 중 하나가 자체 테스트 서버에서 사용된다고 가정하는 것입니다. 때로는 필요한 제약이긴 하지만, 선택적으로 실제 운영 서버에서 실행할 수 있으면 좋을 것입니다.  

> #1 : `STAGING_SERVER`라는 환경 변수를 사용하기록 결정했습니다.  
> #2 : 'self.live_server_url'을 "실제" 서버의 주소로 대체합니다. (해킹과정)

이 해킹이 다른 부분을 망가뜨린 것은 아닌지 FT를 실행해봅니다.

```
$ python manage.py test functional_tests
[...]
Ran 3 tests in 8.544s

OK
```
이제는 Staging Server URL에 대해 실행해봅니다.

```
$ STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests

======================================================================
FAIL: test_can_start_a_list_for_one_user
(functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/functional_tests/tests.py", line 49, in
test_can_start_a_list_and_retrieve_it_later
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'Domain name registration | Domain names
| Web Hosting | 123-reg'
[...]


======================================================================
FAIL: test_multiple_users_can_start_lists_at_different_urls
(functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File
"/.../superlists/functional_tests/tests.py", line 86, in
test_layout_and_styling
    inputbox = self.browser.find_element_by_id('id_new_item')
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_new_item"]
[...]


======================================================================
FAIL: test_layout_and_styling (functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_new_item"]
[...]

Ran 3 tests in 19.480s:

FAILED (failures=3)
```
아직 실제 도메인을 설정하지 않았기 때문에 두 테스트가 예상대로 실패하였습니다. 첫 번째 트레이스백을 보면 테스트가 도메인 제공자의 홈페이지에서 끝나는 것을 알 수 있습니다.

FT가 제대로 된 결과를 보여주는 것 같으니 커밋합니다.

```
$ git diff # functional_tests.py 변경 내용 표시
$ git commit -am "Hack FT runner to be able to test staging"
```

## 9.3. Getting a Domain Name

몇 개의 도메인명이 필요합니다. 메인 도메인의 서브 도메인이라도 상관없습니다. 저는 czarcie.com과 staging.czarcie.com이라는 도메인을 사용합니다.

## 9.4. Manually Provisioning a Server to Host Our Site
"배포"를 두 단계로 나눌 수 있습니다.

- 신규 서버를 프로비저닝(Provisioning)해서 코드를 호스팅할 수 있도록 합니다.
- 신규 버전의 코드를 기존 서버에 배포합니다.

어떤 사람은 배포 할때마다 새 서버를 사용하는 것을 좋아할 수 있습니다. 이것은 PythonAnywhere를 통해 구현할 수 있긴 합니다. 하지만 큐모가 큰 사이트나 기존 사이트의 대규모 업데이트 시에만 필요한 것입니다. 지금 공부하는 사이트에선 두 단계로 작업을 나누는 것이 좋습니다. 최종적으로 이 두 가지 작업을 자동화하겠지만, 지금은 수동 프로비저닝 시스템으로 충분합니다.

이번 섹션을 진행하면서 프로비저닝 종류가 매우 다양하다는 것과 몇 가지 최적의 배포 솔루션이 있다는 것을 알게 될 것입니다. 따라서 여기서 작업하는 것을 기억하려하지 말고, 이해하려고 노력해야합니다. 이를 통해 이후 다른 환경에서 개발을 하더라도 같은 원리를 적용할 수 있습니다.

### Choosing Where to Host Our Site
사이트 호스팅을 위해 다양한 솔루션이 존재하지만, 대략 두 가지 형태로 분류할 수 있습니다.

- 자체 서버(가상도 가능) 운영
- Heroku, OpenShift, PythonAnywhere 같은 Platform-As-A-Service(PaaS) 서비스 이용

특히 작은 규모의 사이트에선 PaaS가 많은 이점이 있기 때문에 이를 추천합니다. 하지만 이번 섹션에서는 PaaS를 사용하지 않습니다. 모든 PaaS의 서비스 방식이 다르기 때문에 배포 절차도 모두 다릅니다. 하나의 PaaS 서비스에서 배포하는 방법을 배운다고 해도 다른 서비스에 적용할 수 없습니다.

PaaS 대신에 SSH와 웹 서버 설정을 이용한 전통적인 서버 관리 방식을 배우도록 합니다. 이 방식은 당분간 계속 될 것이며, 배워주면 현장에서 일하고 있는 백발의 개발자들에 대한 존경심도 생길 것입니다.

여기서 구축하는 서버는 PaaS를 통해 사용할 수 있는 환경과 거의 같습니다. 따라서 배포 과정 중에 배우는 모든 것을 프로비저닝 솔루션에 상관없이 적용할 수 있을 것입니다.

### Spinning Up a Server
어떻게 서버를 구축하는지는 여기서는 설명하지 않습니다. Amazon AWS, Rackspace, Digital Ocean 등의 서비스를 이용해도 되고, 자체 서버를 사용해도 됩니다. 다음 조건만 충족하면 됩니다. [참조 포스팅](https://kimdoky.github.io/deploy/2017/05/14/AWS-key-pairs.html){:target="_blank"}

- 우분투(Ubuntu) 16.04 (aka "Xenial/LTS")
- 루트 권한이 있을 것
- 인터넷상에 공개 돼 있을 것
- SSH로 접속할 수 있을 것

우분투 배포판을 추천합니다. 파이썬 3.6을 설치하기 쉽고, Nginx 설정이 용이합니다. 서버 작업이 익숙한 사함은 우분투 외에 다른 것을 사용해도 됩니다. 하지만 문제는 스스로 해결해야합니다.  
이전에 리눅스 서버를 사용해 본적이 없고, 어떻게 시작해야 할지 모른다면 다음 [링크](https://github.com/hjwp/Book-TDD-Web-Dev-Python/blob/master/server-quickstart.md){:target="_blank"}를 참조하세요.

### User Accounts, SSH, and Privileges
이번 섹션에선 "sudo" 권한이 있는 비루트 사용자 계정을 가지고 있다고 가정하고 진행합니다. 따라서 루트 권한이 필요할 때마다 sudo를 이용해서 작업을 진행할 것입니다. 만약 비루트 계정이 없다면 아래 방법을 따라하세요.

```
# 아래 명령들은 root 사용자로 실행해야 합니다.
root@server:$ useradd -m -s /bin/bash doky # doky라는 사용자 추가
# -m은 home 폴더를 생성합니다. -s는 doky가 bash를 사용하도록 설정합니다.
root@server:$ usermod -a -G sudo doky # doky를 sudoers 그룹에 추가
root@server:$ passwd doky # doky 패스워드 설정
root@server:$ su - doky # doky로 사용자 변경
doky@server:$
```

SSH 패스워드보다 개인 키(Private key)를 이용한 인증 방법을 배우는 것이 좋습니다. 로컬 PC에서 공개 키(Public key)를 가져다가 서버의 `~/.ssh/authorized_key`에 추가하면 됩니다.

> 커맨드라인 리스트에 나오는 doky@server에 주의해야합니다. 이것은 로컬 PC에서 실행하는 명령어가 아닌 서버에서 실행해야 하는 명령어를 가리킵니다.

### Installing Nginx
웹 서버 설치가 필요합니다. 좀 안다고 하는 사람들은 요즘 Nginx를 사용하기 때문에 이것을 사용하도록 합니다. 아파치와 수년간 싸운 결과, (적어도) 설정 파일 가독성 측면에선 훨씬 좋다.

Nginx 설치는 매우 간단하다. 명령어 실행 후 바로 "Hello World" 화면을 볼 수 있습니다.

```
(먼저 apt-get update 나 apt-get upgrade 가 필요할 수 있습니다.)
elspeth@server:$ sudo apt-get install nginx
elspeth@server:$ sudo systemctl start nginx
```
사이트 IP 주소에 접속하면 "Welcome to nginx" 페이지를 볼 수 있습니다.

![]({{ site.url }}/img/post/tdd/9_1.png)
> 페이지가 보이지 않으면 방화벽이 포트 80을 막았기 때문일 수 있습니다. 예를 들어 AWS에선 "security group"을 설정해서 포트 80을 열어주어야 합니다.

### Installing Python 3.6
파이썬 3.6은 작성 시점에 우분투의 표준 저장소에서 사용할 수 없었지만, user-contributed인 "[deadsnakes PPA](https://launchpad.net/~fkrull/+archive/ubuntu/deadsnakes){:target="_blank"}"에서 사용할 수 있습니다.

루트 권한이 있는 상태에서 시스템에 필요한 필수 소프트웨어(Python, Git, pip, Virtualenv)를 설치합니다.

```
elspeth@server:$ sudo add-apt-repository ppa:fkrull/deadsnakes
elspeth@server:$ sudo apt-get update
elspeth@server:$ sudo apt-get install python3.6 python3.6-venv
elspeth@server:$ sudo apt-get install git
```

### Configuring Domains for Staging and Live
IP 주소 지정 시마다 혼란스러울 수 있으니, 여기서 스테이징과 운영 도메인이 우리가 구축한 서버를 가리키도록 설정합니다.  
DNS 시스템에서 하나의 도메인이 특정 IP 주소를 가리키는 것을 "A-Record"라고 부릅니다. 도메인 서비스마다 약간씩 다를 수 있지만, 몇 번 클릭하다 보면 찾을 수 있습니다.
![]({{ site.url }}/img/post/tdd/9_2.png)

### Using the FT to Confirm the Domain Works and Nginx Is Running
설정한 것이 정상적으로 동작하는지 확인하기 위해 FT를 재실행합니다. 실패 메세지가 약간 바뀐 것을 알 수 있습니다.(Nginx에 대한 내용이 포함됩니다.)

```
$ STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_new_item"]
[...]
AssertionError: 'To-Do' not found in 'Welcome to nginx!'
```
진전이 있습니다!

## 9.5. Deploying Our Code Manually
다음은 Staging site를 복사해서 실행해보고, Nginx와 Django가 제대로 상호작용 하는지 확인하도록 합니다. 이를 통해 프로비저닝이 아닌 실제 "배포" 작업에 들어가게 됩니다. 진행하면서 어떻게 프로세스를 자동화할 수 있는지 생각해봅니다.

> 일반적으로 배포와 프로비저닝을 구분 짓는 한 가지 규칙은, 프로비저닝은 푸트 권한이 필요하고 배포는 없다는 것입니다.
운영 서버의 소스 디렉터리를 준비해야 합니다. 비루트 사용자의 홈 리렉터리가 있다고 가정합니다. 여기서는 /home/doky(대부분의 공유 호스팅 서비스에서는 이런식으로 설정됩니다. 하지만 웹 어플리케이션을 실행할 때는 항상 비루트 사용자로 실행해야 합니다.)

TDD 저자는 다음과 같이 사이트를 구축했습니다.

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

각 사이트(스테이징, 운영, 기타 사이트)는 자체 폴더를 가지고 있습니다. 이 폴더는 다시 소스 코드, 데이터베이스, 정적 파일 폴더로 나뉩니다. 이런 식으로 구성해두면, 예를 들어 소스 코드가 신규 버전으로 업데이트된다고 해도 데이터베이스는 그대로 유지할 수 있습니다. 정적 파일 폴더는 앞 섹션에서 설정한 것과 같이 상대 경로인 `../static`에 존재합니다. 마지막으로 `virtualenv`도 자체 폴더를 가집니다.

### Adjusting the Database Location
먼저 settings.py에 잇는 데이터베이스 위치를 변경하고 로컬 PC에서 정상 동작하는지 확인합니다.

superlists/settings.py (ch08l003)

```python
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
[...]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
    }
}
```
> 항상 `abspath`를 먼저(가장 안쪽) 실행하도록 합니다. 이렇게 하지 않으면 파일 임포드 방법에 따라서 문제가 발생할 수 있습니다.

이제 로컬에서 실행해봅니다.

```
$ mkdir ../database
$ python manage.py migrate --noinput
Operations to perform:
Apply all migrations: auth, contenttypes, lists, sessions
Running migrations:
[...]
$ ls ../database/
db.sqlite3
```
정상적으로 동작합니다. 커밋합니다.

```
$ git diff # settings.py 변경 내역
$ git commit -am "move sqlite database outside of main source tree"
```
코드를 서버에 올리기 위해서 Git과 코드 공유 사이트를 이용하도록 합니다.

다음과 같이 bash 명령을 이용해서 코드를 옮깁니다. 명령어 익숙하지 않은 사람들 위해 서명하자면, export 명령은 bash에서 "로컬 변수"를 설정하는 명령입니다.

```
elspeth@server:$ export SITENAME=staging.czarcie.com
elspeth@server:$ mkdir -p ~/sites/$SITENAME/database
elspeth@server:$ mkdir -p ~/sites/$SITENAME/static
elspeth@server:$ mkdir -p ~/sites/$SITENAME/virtualenv
# 다음 줄에 있는 URL을 각자의 코드 리포지토리 URL으로 변경해야 합니다.
elspeth@server:$ git clone https://github.com/KimDoKy/TDD.git \
~/sites/$SITENAME/source
Resolving deltas: 100% [...]
```
> export를 이용해서 정의한 bash 변수는 해당 콘솔이 켜져 있는 동안만 유지됩니다. 서버에서 로그아웃한 후 다시 로그인하면, 변수는 사라지기 때문에 재설정해주어야 합니다. 주의해야 할 것은 변수가 없어도 bash가 에러를 표시하지 않는다는 것입니다. 해당 변수를 단순히 빈 문자열로 대체하기 때문에 예측하지 못한 결과가 발생할 수 있습니다. 의심스럽다면 `echo $SITENAME`을 실행해보면 됩니다.

이제 사이트가 모두 설치되었습니다. 개발 서버를 실행해 봅니다.(이동한 모든 요소들이 제대로 연결됐는지 확인하기 위한 Smoke Test라 할 수 있습니다.)

```
elspeth@server:$ $ cd ~/sites/$SITENAME/source
$ python manage.py runserver
Traceback (most recent call last):
  File "manage.py", line 8, in <module>
    from django.core.management import execute_from_command_line
ImportError: No module named django.core.management
```
이런, Django가 설치돼 있지 않다.

### Creating a Virtualenv manually, and using requirements.txt
`Virtualenv`에 필요한 패키지 목록을 "저장"하고 서버에서 다시 만들려면 requirements.txt 파일을 만듭니다.

```
$ echo "django==1.11rc1" > requirements.txt
$ git add requirements.txt
$ git commit -m "Add requirements.txt for virtualenv"
```
이제 코드 공유 사이트로 업데이트를 보냅니다.

```
$ git push
```
그리고 업데이트 된 내용을 서버에 적용합니다.

```
elspeth@server:$ git pull  # may ask you to do some git config first
```
virtualenv를 "수동으로"생성하려면 (즉, virtualenvwraper없이) 표준 라이브러리 "venv"모듈을 사용하고 virtualenv가 들어갈 경로를 지정해야합니다.

```
elspeth@server:$ pwd
/home/espeth/sites/staging.superlists.com/source
elspeth@server:$ python3.6 -m venv ../virtualenv
elspeth@server:$ ls ../virtualenv/bin
activate      activate.fish  easy_install-3.6  pip3    python
activate.csh  easy_install   pip               pip3.6  python3
```
`virtualenv`를 활성화하려면 `source ../virtualenv/bin/activate`를 사용해야하지만, 그렇게 할 필요는 없습니다. virtualenv의 bin 디렉터리에 있는 Python, pip 및 다른 실행 파일의 버전을 호출하여 실제로 원하는 모든 작업을 수행 할 수 있습니다.

필수 소프트웨어를 virtualenv에 설치하기 위해 virtualenv pip를 사용합니다.

```
elspeth@server:$ ../virtualenv/bin/pip install -r requirements.txt
Downloading/unpacking Django==1.11rc1 (from -r requirements.txt (line 1))
[...]
Successfully installed Django
```
그리고 virtualenv에서 파이썬을 실행하기 위해 virtualenv 파이썬 바이너리를 사용합니다.

```
elspeth@server:$ ../virtualenv/bin/python manage.py runserver
Validating models...
0 errors found
[...]
```
> 방화벽 구성에 따라 http://your.domain.com:8000 으로 이동하여 현재 수동으로 사이트를 방문 할 수도 있습니다.

행복하게도 모든 게 정상 동작하는 듯합니다. 일단 서버를 정지시킵니다.

이제 코드를 서버와 주고 받는 시스템을 갖게 되었습니다.(git push, pull) localenv와 로컬 파일을 일치시키는 virtualenv와 하나의 파일 requirements.txt가 동기화 되었습니다.

다음으로 Django와 대화하고 표준 포트 80에서 사이트를 얻을 수 있도록 Nginx 웹 서버를 구성할 것입니다.

### Simple Nginx Configuration

Django를 이용해서 스테이징 서버에 요청을 보낼 수 있도록 Nginx 설정 파일을 생성합니다.

server: /etc/nginx/sites-available/staging.czarcie.com

```nginx
server {
    listen 80;
    server_name staging.czarcie.com;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```
이 설정은 스테이징 서버에서만 동작한다는 것을 의미하며, 로컬 포트 8000으로 들어오는 모든 요청을 Django로 보내서 응답하도록 "프록시"합니다.  

이 설정은 `/etc/nginx/sites-available` 폴더에 `staging.czarcie.com`라는 파일을 저장했습니다. 그리고 이것을 symlink를 이용해서 동작 사이트에 추가합니다.

```
elspeth@server:$ echo $SITENAME # 변수가 아직 자신의 사이트를 가리키는지 확인
staging.czarcie.com
elspeth@server:$ sudo ln -s ../sites-available/$SITENAME /etc/nginx/sites-enabled/$SITENAME
elspeth@server:$ ls -l /etc/nginx/sites-enabled # symlink가 있는지 확인
```
진짜 설정 파일은 `sites-available`에 두고 `symlink`는 `sites-enabled`에 두는 것은 `Debian/Ubuntu`에서 자주 사용되는 Nginx 설정 저장 방법입니다. 이 구조는 사이트를 쉽게 시작하고 종료할 수 있도록 합니다.

혼란을 막기 위해 기본 "Welcome to Ngnix" 설정은 삭제합니다.

```
elspeth@server:$ sudo rm /etc/nginx/sites-enabled/default
```

그리고 테스트 해봅니다.

```
elspeth@server:$ sudo systemctl reload nginx
elspeth@server:$ ../virtualenv/bin/python manage.py runserver
```
> 길이가 긴 도메인이 제대로 동작하도록 하려면 `/etc/nginx/ngnix.conf`파일의 `server_names_hash_bucket_size 64;`를 주석 처리해야 합니다. 도메인명이 길지 않다면 작업할 필요가 없습니다. 설정 파일을 다시 로딩할 때 문제가 있으면 Nginx가 경고를 줍니다.

그러면 사이트가 제대로 동작하는지 확인해봅니다.

![]({{ site.url }}/img/post/tdd/9_3.png)
> Nginx가 예상한대로 동작하지 않는다면 `sudo nginx -t` 명령을 시도해봅니다. 설정 파일이 정상인지 테스트해서 문제가 있으면 경고 메세지를 표시해 줍니다.

FT를 실행해서 결과를 확인해봅니다.

```
$ STAGING_SERVER=czarcie.com python manage.py test functional_tests
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
[...]
AssertionError: 0.0 != 512 within 3 delta
```
데이터베이스를 아직 설정하지 않았기 때문에 신규 아이템을 전송하자마자 에러가 발생합니다. 또한 Django의 노란색 디버그 페이지를 통해 어느 정도 테스트가 진행됐는지 확인할 수 있습니다.

> 테스트 때문에 창피할 수 있는 상황을 모면하게 됐습니다. 메인 페이지를 로딩했을 때는 사이트가 괜찮은 것처럼 보였습니다. 우리가 성급했더라면 작업이 끝났다고 생각하고 배보했을 수도 있습니다. 그랬다면 지저분한 Django 디버그 페이지를 처음 발견한 것은 우리가 아닌 사용자가 됐을 것입니다. 약간 상황을 과장되게 표현하긴 했지만, 사이트 규모가 더 크고 복잡했다면 어떤 문제가 발생했을까요? 우리는 모든 것을 체크할 수는 없지만 테스트는 할 수 있습니다!

![]({{ site.url }}/img/post/tdd/9_4.png)
> Database Error가 일어나야 하는데 나는 Operational Error가 일어났다..

### Creating the Database with migrate
"확실해?"라고 묻는 프롬포트를 생략하기 위해 `--noinput` 옵션을 이용해서 `migrate`를 실행합니다.

```
elspeth@server:$ ../virtualenv/bin/python manage.py migrate --noinput
Creating tables ...
[...]
elspeth@server:$ ls ../database/
db.sqlite3
elspeth@server:$ ../virtualenv/bin/python manage.py runserver
```
FT를 다시 실행합니다.

```
$ STAGING_SERVER=staging.czarcie.com python manage.py test functional_tests
[...]

...
 ---------------------------------------------------------------------
Ran 3 tests in 10.718s

OK
```
사이트가 다시 동작하기 시작했습니다.
> "502 - Bad Gateway" 메세지가 뜬다면, migrate 후에 서버를 재시작(manage.py runserver)하지 않았기 때문입니다.


### Server Debugging Tips
>
배포는 까다롭습니다. 일들이 예상대로 수행되지 않으면 주의해야 할 몇가지 팁들이 있습니다.
>
- 각각의 파일이 올바른 내용들을 가지고 있어야 합니다. 오타가 모든 차이를 만들 수 있습니다.
- Nginx 오류 로그는 /var/log/nginx/error.log로 이동합니다.
- Nginx에게 `-t` 플래그를 사용하여 설정을 "체크"하도록 요청할 수 있습니다. (`nginx -t`)
- 브라우저가 오래된 응답을 캐싱하지 않았는지 확인하세요. Ctrl + Refresh 을 사용하거나 새 비공개 브라우저 창으로 시작하세요.
- 간혹 서버를 재부팅해야만 문제가 해결될 때도 있습니다.
>
혹시 전혀 해결될 기미가 보이지 않으면, 서버를 날려 버리고 처음부터 다시 시작할 수도 있습니다만.. 빠른 시간에 진행해야 합니다.

## 9.6. Success! Our hack deployment works
최소한의 기본 파이프가 작동하는 것을 보았습니다. 하지만 실제로 Django 개발 서버를 프로덕션 환경에서 사용할 수 없습니다. 또한 `runserver`를 사용하여 수동으로 시작하는데 의존할 수도 없습니다. 다음 섹션에서 이러한 부분을 다룹니다.


### 테스트 주도 서버 설정 및 배포
>
*테스트는 배포 시에 발생할 수 있는 불확실성을 제거해 줍니다.*
>
개발자로서 서버 관리는 매우 재미있는 작업입니다. 왜냐하면 다양한 불확실성과 놀라움으로 가득 차 있기 때문입니다. 이번 섹션의 목표 중 하나는 FT가 처리 과정 중 발생할 수 있는 불확실성을 어떻게 발견할 수 있는지 보여주는 것이었습니다.
>
*배포가 까다로운 전형적인 요소들 - 데이터베이스, 정적 파일, 의존 관계, 사용자 지정 설정*
>
배포 시에 항상 주의해야 할 것은 데이터베이스 설정, 정적 파일, 소프트웨어 의존 관계, 사용자 지정 설정 등입니다. 이것들은 스테이징과 배포 서버에서 구성이 다릅니다. 각각에 대해 배포 과정을 잘 검토해야 합니다.
>
*테스트에선 실험이 가능합니다.*
>
서버 설정을 바꿀 때마다 테스트를 실행해서 이전과 같은 상태로 동작하는지 확인할 수 있습니다. 이것은 두려움 없이 설정을 시도할 수 있도록 합니다.
