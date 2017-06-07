---
layout: post
section-type: post
title: new TDD-Chapter 11. Automating Deployment with Fabric
category: tdd
tags: [ 'tdd' ]
---

배포 자동화는 스테이징 테스트에 있어 핵심이라 할 수 있습니다. 배포 절차를 반복 실행 함으로써 운영 환경에서도 정상적으로 동작하는 사이트를 배포할 수 있습니다.  

페브릭(Fabric)은 서버에서 명령어를 자동으로 실행할 수 있게 해주는 툴입니다. 페브릭은 사이트의 중요 기능이 아니기 때문에 virtualenv나 requirements.txt 에 설치하지 않고, 로컬 PC 시스템에 설치합니다.

```
$ pip install fabric3
```
일반적인 설정은 fabfile.py라는 파일을 이용합니다. 이 파일은 fab 같은 커맨드라인 툴에서 실행할 수 있는 몇몇 함수를 포함하고 있습니다.  

```
fab function_name,host=SERVER_ADDRESS
```
이것은 `function_name`이라는 함수를 호출해서 `SERVER_ADDRESS` 서버에 전달합니다. 사용자명과 패스워드를 지정할 수 있는 다양한 방법이 있습니다. `fab --help`를 통해 확인할 수 있습니다.

## 11.1. Breakdown of a Fabric Script for Our Deployment

패브릭이 어떻게 동작하는지 확인하는 가장 좋은 방법은 예제 파일을 실행해보는 것입니다. 다음은 필자가 예전에 만들었던 예제로, 이후 실습하게 될 모든 배포 과정을 자동화하고 있습니다.  
<http://www.bbc.co.uk/cult/classic/bluepeter/valpetejohn/trivia.shtml>

deploy_tools/fabfile.py (ch09l001)

```python
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/hjwp/book-example.git'  

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}' #1,2
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)  #2
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
```

> #1 : env.host는 커맨드라인에서 지정한 서버 주소를 저장합니다.  
> #2 : env.user는 서버 로그인 시에 사용할 사용자명을 저장합니다.

함수명 자체가 처리 내용을 의미하고 있어서 별도의 설명은 필요 없을 것입니다. `fabfile`에 있는 함수들은 상단부터 차례대로 커맨드라인에서 호출되기 때문에, 밑줄(`_`)을 이용해서 다른 "공용 API"와 섞이지 않도록 했습니다.

### Creating the directory structure
폴더가 이미 존재하더라도 에러가 발생하지 않도록 설정하는 방법입니다.

deploy_tools/fabfile.py (ch09l002)

```python
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}') #1,2
```
> #1 : `run`은 페브릭에서 가장 자주 사용되는 명령어입니다. "이 셸 명령을 서버에서 실행해"라는 의미입니다.  
> #2 : `mkdir -p`는 매우 유용한 mkdir 사용법입니다. 두 가지 의미에서 효율적입니다. 하나는 여러 단계로 이루어진 디랙터리의 경우 상위 디렉터리까지 작성해줍니다. 예흫 들어 `mkdir -p /tmp/foo/bar`는 bar뿐만 아니라 부모 디렉터리인 foo도 생성합니다. 또한 이미 bar 폴더가 있어도 에러가 발생하지 않습니다.[^scala]

[^scala]: 앞에서 본 os.path.join 명령을 사용하지 않고, `%s`를 이용해서 수동으로 경로를 만든 이유는 path.join 을 윈도우에서 실행하면 백슬래시를 이용하기 때문에, 서버에서 필요한 것은 일반 슬래시입니다.

### Pulling down our source code with git
이전 섹션에서 `git pull`과 같은 소스 코드의 최신 버전을 서버에서 다운로드 합니다.

deploy_tools/fabfile.py (ch09l003)

```python
def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):  #1
        run(f'cd {source_folder} && git fetch')   #2,3
    else:
        run(f'git clone {REPO_URL} {source_folder}')  #4
    current_commit = local("git log -n 1 --format=%H", capture=True)  #5
    run(f'cd {source_folder} && git reset --hard {current_commit}')  #6
```

> #1 : `exists`는 서버에 디렉터리나 파일이 존재하는지 확인합니다. `.git`이라는 숨겨진 폴더가 있는지 확인해서 리포지토리가 이미 폴더에 클론(clone)돼 있는지 확인하는 것입니다.  
> #2 : 현재 디렉터리를 설정하기 위해서 많은 명령어가 `cd`로 시작합니다. 페브릭은 상태 정보를 유지하지 않기 때문에, 어떤 디렉터리에서 명령이 실행됐는지 또 실행될 것인지를 기억하지 못합니다.  
> #3 : `git fetch`는 기존 리포지토리 폴더에 가장 최근에 커밋한 것으로 웹으로부터 다운로드합니다.  
> #4 : 기존 리포지토리가 없으면, `git clone`을 이용해서 지정한 리포지토리 URL로부터 폴더 구조를 포함한 전체 내용을 다운로드 합니다.  
> #5 : 페브릭의 `local` 명령은 명령어를 로컬 장비에서 실행합니다. `subprocess.Popen`을 랩핑한 것으로 매우 편리합니다. 여기서는 `git log` 출력 내용을 캡쳐해서 로컬 트리에 있는 현재의 커밋 해쉬를 취득합니다. 이것은 로컬 장비에서 체크아웃한 상태와 동일한 상태로 서버가 종료된다는 것을 의미합니다.(단, 서버에 `push`한 상태여야 합니다.)  
> #6 : `reset --hard`를 이용해서 서버의 코드 디렉터리에 발생한 모든 변경을 초기화합니다.

이 과정의 최종 결과는 새로운 배포인 경우 `git clone`을 수행하거나, 이전 버전의 코드가 이미 존재하는 경우 `git fatch` + `git reset --hard`를 수행합니다. 우리가 수동으로 했을때 사용한 `git pull`과 동등하지만 `reset --hard`를 사용하여 강제로 로컬의 변경 사항을 덮어 씁니다.

> 이 스크립트가 동작하려면, 현재 로컷 커밋을 `git push`해야 합니다. 이를 통해 서버가 이것을 가져오거나 초기화할 수 있습니다. `Could not parse object` 에러가 발생한다면 `git push`를 시도해봅시다.

### Updating settings.py
다음은 settings.py 파일 내에 `ALLOWED_HOSTS`와 `DEBUG`를 설정하고 `SECRET_KEY`를 생성합니다.

deploy_tools/fabfile.py (ch09l004)

```python
def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")  #1
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'  #2
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):  #3
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')  #4,5
```
> #1 : 페브릭 `sed` 명령은 파일 내에 있는 문자열을 특정 문자열로 변경합니다. 여기서는 `DEBUG`의 `True`를 `False`로 변경하고 있습니다.  
> #2 : 마찬가지 방법으로 `ALLOWED_HOSTS`를 변경합니다. 여기서는 `regrex`를 이용해서 해당 문져열을 찾습니다.  
> #3 : Django에선 암호화(쿠키와 CSRF 보호)를 위해서 `SECRET_KEY`를 이용합니다. 키를 이용할 때는 공개 중인 소스 코드 리포지토리에 있는 비밀 키와 다른 키를 이용해야 합니다. 이 코드는 비밀 키가 존재하지 않으면 새로운 키를 만들어서 설정 파일에 임포드합니다. 더 자세한 내용은 [Django 문서](https://docs.djangoproject.com/en/1.11/topics/signing/){:target="_blank"}를 참고합니다.  
> #4 : `append` 명령은 파일 끝에 새로운 줄을 추가합니다.(파일 끝에 이미 빈 줄이 있다면 여기에 다시 한 줄을 추가한다고 해도 문자가 없습니다. 빈 줄이 없다면 파일 끝에 내용을 추가해버리기 때문에 문제가 될 수 있습니다. 따라서 '\ㅜ'(줄바꿈 문자)을 항상 붙여주는게 좋습니다.)  
> #5 : 상대 임포트(relative import)를 이용해서(`secret_key`가 아닌 `.secret_key`로부터 임포트) `sys.path`에 있는 것이 아닌 로컬 모듈에서 임포트하도록 합니다.  
>> 이와 같이 설정 파일을 해킹하는 것은 서버의 구성을 변경하는 방법 중 하나 입니다. 또 다른 공통 패턴은 환경 변수를 사용하는 것입니다. [chapter_server_side_debugging](https://www.obeythetestinggoat.com/book/chapter_server_side_debugging.html){:target="_blank"}에서 확인 할 수 있습니다.

### Updating the virtualenv
virtualenv를 생성하거나 업데이트합니다.

deploy_tools/fabfile.py (ch09l005)

```python
def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):  #1
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')  #2
```

> #1 : virtualenv 폴더 내부에 실행 가능한 pip가 있는지 확인합니다.  
> #2 : 이전에 했던 것처럼 `pip install -r`을 실행합니다.

정적 파일 업데이트는 명령어 하나로 가능합니다.

deploy_tools/fabfile.py (ch09l006)

```python
def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'  #1
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'  #2
    )
```

> #1 : 파이썬에서는 긴 문자열을 여러 줄로 나눌 수 있으며, 하나의 문자열에 연결합니다. 실제로 원하는 것은 문자열 목록이었지만 버그는 보통 쉽표는 빼먹었을 때 일어납니다.  
> #2 : Django의 manage.py를 실행할 때는 virtualenv의 바이너리 폴더를 이용합니다. 이것은 시스템 자체 Django가 아닌 virtualenv Django를 실행하기 위한 것입니다.  

### Migrating the database if necessary

마지막으로 manage.py migrate 를 이용해서 테이텁[이스를 업데이트 합니다.

deploy_tools/fabfile.py (ch09l007)

```python
def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
```

`--noinput`은 패브릭이 처리하기 어려운 커맨드라인의 예/아니오 확인을 제거합니다.  

이 스크립트는 신규 사이트뿐만 아니라 기존 사이트에서도 동작합니다. 라틴어 어원을 가진 단어를 좋아한다면, 이것을 idenpotent(멱등성:몇 번을 실행해도 같은 결과를 같는다.)라고 표현할 수 있을 것입니다.

## 11.2. Trying It Out
스테이징 사이트에서 이 스크립트를 실행해봅시다.

```
$ cd deploy_tools
$ fab deploy:host=doky@staging.czarcie.com
```

....

---

```
~/Git/Study/TDD/superlists/NewVersiondTdd/superlists/deploy_tools(master*) » fab deploy:host=doky@staging.czarcie.com --disable-known-hosts
[doky@staging.czarcie.com] Executing task 'deploy'
[doky@staging.czarcie.com] run: mkdir -p /home/doky/sites/staging.czarcie.com/database
[doky@staging.czarcie.com] Login password for 'doky':
[doky@staging.czarcie.com] Login password for 'doky':
```

할 수록 멘붕......  
TDD 끝낼 수 있을까.. 배포에 오면서부터 한 단계 한 단계....  
일단 SSH를 먼저 공부하고 이어가야 할 듯....

> 삽질 끝에 해결하였습니다.
[ssh 패스워드 없이 접속하기 삽질기](https://kimdoky.github.io/deploy/2017/06/06/ssh-nonpass-connect.html){:target="_blank"}

```
~/Git/Study/TDD/superlists/NewVersiondTdd/superlists/deploy_tools(master*) » fab deploy:host=doky@staging.czarcie.com
[doky@staging.czarcie.com] Executing task 'deploy'
...
Done.
Disconnecting from doky@staging.czarcie.com... done.
```
메시지를 잘 보면 우리가 정의한 작업을 진행하고 있는 것을 알 수 있습니다. `mkdir -p` 명령은 디렉터리가 이미 존재함에도 불구하고 에러 없이 잘 동작합니다. 다름은 `git`이 앞서 커밋한 처리를 다운로드합니다. `sed`와 `echo >>`는 settings.py를 수정합니다. 그리고 `pip3 install -r requirements.txt`가 완료됩니다. 기존 `virtualenv`가 필요한 패키지를 이미 보유하고 있는 것에 주목해야합니다. `collectstatic` 또한 정적 파일이 이미 존재한다고 인식하며, 마지막으로 `migrate`가 완료됩니다.

> **패브릭 설정**  
SSH 키를 사용해서 로그인한다면, SSH 키가 기본 위에 있고 서버와 동일 사용자명을 사용하는 한 페브릭이 정상 동작해야 합니다. 그렇지 않으면 `fab` 명령이 제대로 실행되도록 몇가지 사항을 확인해야 합니다. 보통은 사용자명, SSH 키 위치, 패스워드 등이 문제가 됩니다.  
>
이 값들을 인수로 해서 페브릭을 커맨드라인상에서 실행할 수 있습니다.  
>
```
$ fab --help
```
또는 페브릭 문서를 참고합니다. <http://docs.fabfile.org/en/1.13/>  
(본인도 오류를 만나서 위에 문제 해결내용을 기술하였습니다.)

### Deploying to Live
실제 운영 서버에 적용해봅니다. (스테이징이 아닌 메인용 서버가 하나 더 필요합니다. 서브 도메인과 하나의 ec2로 독립적인 사이트를 운영할 수 있는지 먼저 테스트를 진행하였습니다.)

```
~/Git/Study/TDD/superlists/NewVersiondTdd/superlists/deploy_tools(master*) » fab deploy:host=doky@deploy.czarcie.com  
[doky@deploy.czarcie.com] Executing task 'deploy'
[doky@deploy.czarcie.com] run: mkdir -p /home/doky/sites/deploy.czarcie.com/database
[doky@deploy.czarcie.com] run: mkdir -p /home/doky/sites/deploy.czarcie.com/static
[doky@deploy.czarcie.com] run: mkdir -p /home/doky/sites/deploy.czarcie.com/virtualenv
[doky@deploy.czarcie.com] run: mkdir -p /home/doky/sites/deploy.czarcie.com/source
[doky@deploy.czarcie.com] run: git clone https://github.com/KimDoKy/TDD.git /home/doky/sites/deploy.czarcie.com/source
[doky@deploy.czarcie.com] out: Cloning into '/home/doky/sites/deploy.czarcie.com/source'...
[doky@deploy.czarcie.com] out: remote: Counting objects: 321, done.
[doky@deploy.czarcie.com] out: Receiving objects:   0% (1/321)   
...
[doky@deploy.czarcie.com] out: Resolving deltas: 100% (156/156), done.
[doky@deploy.czarcie.com] out: Checking connectivity... done.
[doky@deploy.czarcie.com] out:

[localhost] local: git log -n 1 --format=%H
[doky@deploy.czarcie.com] run: cd /home/doky/sites/deploy.czarcie.com/source && git reset --hard 863028f87f44ba1a73fb2720a03ef48c6e1af79e
[doky@deploy.czarcie.com] out: HEAD is now at 863028f Notes and template config files for provisioning
[doky@deploy.czarcie.com] out:

[doky@deploy.czarcie.com] run: sed -i.bak -r -e 's/DEBUG = True/DEBUG = False/g' "$(echo /home/doky/sites/deploy.czarcie.com/source/superlists/settings.py)"
[doky@deploy.czarcie.com] run: sed -i.bak -r -e 's/ALLOWED_HOSTS =.+$/ALLOWED_HOSTS = ["deploy.czarcie.com"]/g' "$(echo /home/doky/sites/deploy.czarcie.com/source/superlists/settings.py)"
[doky@deploy.czarcie.com] run: echo 'SECRET_KEY = "go$y$f9!-2%3v#(2v*l0*&t21%$^#u(p)m=8_&ad#qs"' >> "$(echo /home/doky/sites/deploy.czarcie.com/source/superlists/secret_key.py)"
[doky@deploy.czarcie.com] run: echo '
from .secret_key import SECRET_KEY' >> "$(echo /home/doky/sites/deploy.czarcie.com/source/superlists/settings.py)"
[doky@deploy.czarcie.com] run: python3.6 -m venv /home/doky/sites/deploy.czarcie.com/source/../virtualenv
[doky@deploy.czarcie.com] run: /home/doky/sites/deploy.czarcie.com/source/../virtualenv/bin/pip install -r /home/doky/sites/deploy.czarcie.com/source/requirements.txt
[doky@deploy.czarcie.com] out: Collecting django==1.11rc1 (from -r /home/doky/sites/deploy.czarcie.com/source/requirements.txt (line 1))
...
[doky@deploy.czarcie.com] out: Successfully installed django-1.11rc1 gunicorn-19.7.1 pytz-2017.2
[doky@deploy.czarcie.com] out:

[doky@deploy.czarcie.com] run: cd /home/doky/sites/deploy.czarcie.com/source && ../virtualenv/bin/python manage.py collectstatic --noinput
[doky@deploy.czarcie.com] out: Copying '/home/doky/sites/deploy.czarcie.com/source/lists/static/base.css'
...
[doky@deploy.czarcie.com] out: 15 static files copied to '/home/doky/sites/deploy.czarcie.com/static'.
[doky@deploy.czarcie.com] out:

[doky@deploy.czarcie.com] run: cd /home/doky/sites/deploy.czarcie.com/source && ../virtualenv/bin/python manage.py migrate --noinput
...
[doky@deploy.czarcie.com] out:   Applying sessions.0001_initial... OK
[doky@deploy.czarcie.com] out:


Done.
Disconnecting from doky@deploy.czarcie.com... done.
```

스크립트가 약간 다른 경로를 따라가고 있는 것을 볼 수 있습니다. `git pull` 대신에  `git clone`을 이용해서 신규 리포지토리를 다운로드하고 있기 때문입니다. 또한 `pip`와 `Django` 설치를 포함한 신규 `virtualenv`를 생성하고 있습니다. `collectstatic`은 이번에는 새 파일을 생성하고 있으며 `migrate`가 정상적으로 처리되었습니다.

### Nginx and Gunicorn Config Using sed
운영 서버 배포를 위해 남은 작업은 무엇이 있을까요? 프로비저닝 설정사항을 메모해둔 것을 보면, 템플릿 파일을 이용해서 Nginx 가상 호스트와 Upstart 스크립트를 생성해야 된다는 것을 알 수 있습니다. 유닉스의 커맨드라인에서 마법의 명령어를 실행해주면 이 문제가 해결됩니다.

(/home/doky/sites/deploy.czarcie.com 에서 실행)

```
doky@server:$ sed "s/SITENAME/deploy.czarcie.com/g" \
    source/deploy_tools/nginx.template.conf \
    | sudo tee /etc/nginx/sites-available/deploy.czarcie.com
```
`sed("stream editor")`는 문자열을 스트림해서 편집합니다. 페브릭의 문자열 대체 명령이 같은 이름을 가지고 있는 것은 우연이 아닙니다. 여기서는 `SITENAME`을 사이트 주소로 변경하고 있습니다. `s/나를 교체해/이걸로/g` 형식으로 사용합니다. 또한 파이프문자(|)를 이용해서 이 결과를 루트 사용자 처리(sudo)에 건넵니다. `sudo`는 이 결과를 받아서 Nginx의 sites-available 가상 호스트 설정 파일로 저장합니다.

이제 이 설정 파일을 활성화할 수 있습니다.

```
doky@server:$ sudo ln -s ../sites-available/deploy.czarcie.com \
    /etc/nginx/sites-enabled/deploy.czarcie.com
```
다음은 Upstart 스크립트 파일을 작성합니다.

```
doky@server: sed "s/SITENAME/deploy.czarcie.com/g" \
    source/deploy_tools/gunicorn-systemd.template.service \
    | sudo tee /etc/systemd/system/gunicorn-deploy.czarcie.com
```
마지막으로 두 서비스를 가동합니다.

```
doky@server:$ sudo systemctl daemon-reload
doky@server:$ sudo systemctl reload nginx
doky@server:$ sudo systemctl enable gunicorn-deploy.czarcie.com
doky@server:$ sudo systemctl start gunicorn-deploy.czarcie.com
```
이제 사이트가 동작하는지 확인해 봅니다.

---

>
현재 여기서 막힘 (복수의 gunicorn이 설정 가능한지.)  
해결 중입니다... 능력자님들 도와주세요.
---

fabfile을 리포지토리에 등록합니다.

```
$ git add deploy_tools/fabfile.py
$ git commit -m "Add a fabfile for automated deploys"

```

## 11.3. Git Tag the Release
마지막으로 관리 목적의 작업이 남았습니다. 현재 운영 서버에서 동작하고 있는 코드 상태를 저장하기 위해 `Git tag`를 실행해줍니다.

```
$ git tag LIVE
$ export TAG=$(date +DEPLOYED-%F/%H%M)  # 타임스탬프 생성
$ echo $TAG # "DEPLOYED-" + 타임스탬프(시간정보)를 보여준다
$ git tag $TAG
$ git push origin LIVE $TAG # 태그를 푸쉬한다
```
이것으로 운영 서버의 코드와 현재 코드 상태를 쉽게 비교할 수 있습니다. 이 기능은 특히 뒤에서 다룰 데이터베이스 마이그레이션 시에 유용합니다. tag 기록을 살펴봅시다.

```
$ git log --graph --oneline --decorate
[...]
```
이제 인터넷상에 공개된 웹 사이트를 가지게 되었습니다.

## 11.4. Further Reading
배포에는 "이것이 정답"이라고 하는 것은 없습니다. 배포에는 다양한 방법이 존재합니다. 다음은 TDD 필자가 참고한 자료들입니다.

- [Solid Python Deployments for Everybody](https://hynek.me/talks/python-deployments/){:target="_blank"} by Hynek Schlawack
- [Git-based fabric deployments are awesome](http://dan.bravender.net/2012/5/11/git-based_fabric_deploys_are_awesome.html){:target="_blank"} by Dan Bravender
- The deployment chapter of [Two Scoops of Django](https://www.obeythetestinggoat.com/book/bibliography.html#twoscoops){:target="_blank"} by Dan Greenfeld and Audrey Roy
- [The 12-factor App](https://12factor.net/){:target="_blank"} by the Heroku team

프로비저닝 자동화와, 페브릭을 대체할 수 있는 Ansible에 대해서는 [appendix3](https://www.obeythetestinggoat.com/book/appendix_III_provisioning_with_ansible.html){:target="_blank"}에서 설명하고 있으니 참고하면 됩니다.

## 배포 자동화
### Fabric
페브릭은 파이썬 스크립트를 이용해서 서버상에서 명령어를 실행하게 해줍니다. 서버 관리 자동화를 위한 훌륭한 툴입니다.
### 멱등성(Idempotency)
기존 서버에 배포 스크립트를 실행한다면, 스크립트 설계 시 두 가지 측면을 고려해야 합니다. 서버에 신규로 설치하는 경우와 이미 설치 버전이 있는 경우입니다.
### 설정 파일 버전 관리
설정 파일이 서버에만 존재하는 일은 없어야 합니다. 애플리케이션 핵심 파일이기 때문에 다른 코드와 같이 버전 관리해야 합니다.
### 프로비저닝 자동화
신규 서버 가동과 필요 소프트웨어 설치까지 모두 자동화돼야 합니다. 또한 호스팅 제공자의 API 연계성도 확인해야 합니다.
### 관리 툴 설정
페브릭은 매우 유연한 툴이긴 하지만 그 로직이 스크립트에 기반하고 있습니다. "선언적인" 작성이 가능해서 작업을 더 쉽게 해주는 툴들도 있습니다. Ansible과 Vagrant가 그것으로 참고할 가치가 있습니다. 이외에도 많은 툴이 있습니다.(Chef, Puppet, Salt, juju ...)
