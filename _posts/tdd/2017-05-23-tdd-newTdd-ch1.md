---
layout: post
section-type: post
title: new TDD-Chapter 1. Getting Django Set Up Using a Functional Test
category: tdd
tags: [ 'tdd' ]
---

## Required Software Installations <a id="chapter-1"></a>

python = 3.6.0

Django = 1.11.1

Firefox web browser
> <https://www.mozilla.org/firefox/>  

Git version control system

Selenium
> `pip install "selenium>3"``

Geckodriver
> MacOS : `brew install geckodriver`  
> 설치확인 : `geckodriver --version`  

## 1.1 Obey the Testing Goat! Do Nothing Until You Have a Test

테스팅 고트님은 파이썬 테스팅 커뮤니티의 비공식적 TDD 마스코트입니다. 만화에서 귓속말로 지시를 내리는 천사와 악마 같다고 보시면 됩니다.  

아직 무얼 할지 모르지만 일단 웹 사이트 하나를 만드려고 합니다. 일반적으로 웹 개발의 첫 번째 단계는 웹 프레임워크를 설치하는 것입니다. "이것을 다운로드해서 설치한 후, 이것을 설정하고 스크립트를 실행한다"라는 식입니다. 하지만 TDD에서는 다른 접근법이 필요합니다. TDD를 할 때에는 내면에 있는 테스팅 고크님을 항상 생각하고 있어야 합니다. *"테스트를 먼저 해! 테스트를 먼저 하라고!"*

TDD에서 가장 먼저 해야하는 것은 "테스트를 작성"하는 것입니다.

먼저 테스트를 작성한 후 실행합니다. 그리고 테스트가 예상대로 실패하는지 확인합니다. 이 과정을 끝내고 나서야 다음 과정인 웹 구축 단계로 넘어갈 수 있습니다. 이것을 염소 같은 목소리로 반복해서 되뇌어야 합니다.

염소는 한 번에 한가지만 합니다. 이 때문에 염소는 산에서 떨어지거나 하는 일이 거의 없습니다.

![]({{ site.url }}/img/post/tdd/1_2.png)

단계를 작게 나누어 진행해 봅시다. 먼저 유명한 파이썬 웹 프레임워크인 Django를 이용해서 애플리케이션을 개발하는 과정을 봅니다.

첫 번째 단계는 Django가 제대로 설치됐는지, 사용할 준비가 됐는지 확인하는 것입니다. 이것을 확인하기 위해서, Django 개발 서버를 가동해서 이 서버에 있는 웹 페이지를 로컬 PC상의 브라우저로 접속해야 합니다. *셀레늄* 브라우저 자동화 툴을 이용해서 이 동작을 구현하도록 합니다.

코드를 저장할 프로젝트 폴더를 하나 만들고 거기에 `functional_tests.py`라는 파이썬 파일을 생성합니다.

functional_tests.py

```python
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
```
처음 만든 첫 번째 *기능 테스트(functional test:FT)* 입니다. 여기서는 이 코드가 어떤 역할을 하는지만 이해하고 넘어 갑니다.

- 파이어폭스 브라우저 창을 실행하기 위해 셀레늄의 webdriver를 가동합니다.
- 브라우저를 통해 로컬 PC상의 웹 페이지를 엽니다.
- 웹 페이지 타이틀에 "Django"라는 단어가 있는지 확인(테스트 어설션(assertion) 생성)합니다.

코드를 실행해 봅니다.

```
$ python functional_tests.py
```
브라우저 창이 실행되고 `localhost:8000`에 접속하려고 하는 것을 확인할 수 있습니다. 그리고 파이썬 코드의 실행 결과를 보면 에러 메세지가 뜨는 것을 알 수 있습니다.

> import selenium 부분이나 "geckodriver" 관련 에러가 발생한다면 '[Required Software Installations](#chapter-1)' 부분을 다시 확인해야 합니다.


## 1.2 Getting Django Up and Running
"전제조건 및 가정"을 일고 지시대로 프로그램을 설치했다면, 이미 Django가 설치되어 있을 것입니다. 첫 번째 단계는 웹 사이트의 메인 컨테이너가 될 프로젝트를 만들기 위해 Django를 가동하고 실행하는 것입니다. 이를 위해 Django에서 커맨드라인 툴을 제공합니다.

```
django-admin.py startproject superlists
```
정상적으로 실행된다면, 다음과 같은 서브 폴더와 파일로 구성된 'superlists' 폴더가 생성됩니다.

```
.
├── functional_tests.py
├── geckodriver.log
└── superlists
    ├── manage.py
    └── superlists
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```
manage.py 파일은 Django의 맥가이버칼고 같은 것으로, 개발 서버르 ㄹ가동하는 역할도 합니다. `cd superlists` 명령을 실행하여 superlists 상위 폴더로 이동한 후에 다음 명령을 실행합니다.

```
$ python manage.py runserver
```

수동으로 웹 브라우저를 열어서 개발 서버(http://localhost:8000)에 접속해보면 다음과 같은 화면을 볼 수 있을 것입니다.

![]({{ site.url }}/img/post/tdd/1_1.png)

## 1.3 Starting a Git Repository
이번 섹션을 마치기 전에 마지막으로 해야 할 것은 앞서 작업한 것들을 *버전 관리 시스템(Version Control System,VCS)* 에 커밋(commit)하는 것입니다.

제일 먼저 할 것은 커밋입니다. VCS로 Git을 사용합니다. 왜냐하면 Git이 최고의 VCS이기 때문입니다.

`functional_tests.py` 파일을 superlists 폴더로 옮기고 `git init`을 실행해서 리포지토리(repository)를 가동하도록 합니다.

```
$ mv functional_tests.py superlists/
$ cd superlists
$ git init .
$ ls
superlists  functional_tests.py db.sqlite3  manage.py
```

db.sqlite3는 데이터베이스 파일입니다. 이 파일은 버전 관리가 필요 없기 때문에 `.gitignore`라는 특수한 파일에 추가합니다. `.gitignore`는 명칭 그대로 Git이 무시해도 되는 파일을 정의 합니다. ".pyc" 파일들은 의미 없는 파일들로 커밋 할 필요가 없기 때문에 같이 추가해줍니다.

```
$ echo "db.sqlite3" >> .gitignore
$ echo "geckodriver.log" >> .gitignore
$ echo "__pycache__" >> .gitignore
$ echo "*.pyc" >> .gitignore
```
다음은 현재 폴더의 나머지 파일들을 "."애 추가합니다.

```
$ git add .
$ git status
On branch master

Initial commit

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   .gitignore
        new file:   functional_tests.py
        new file:   manage.py
        new file:   superlists/__init__.py
        new file:   superlists/settings.py
        new file:   superlists/urls.py
        new file:   superlists/wsgi.py
        new file:   .gitignore

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)
```
(`git status` 명령을 자주 사용할 것이기 때문에 `git st`라는 별칭을 이용하도록 합니다. 별칭을 사용하는 방법은 "Git aliases"에 대해 공부하면 됩니다.)

문제가 없어 보입니다. 첫 커밋을 실행합니다.

```
$ git commit -m "first commit: First FT and basic Django config"
```

> git을 처음 실행하는 경우 사용자명과 사용자 이메일 등록이 필요합니다.

```
$git config --global user.email "개인 이메일주소"
$git config --global user.name "임의 사용자ID"
```

이것으로 VCS, 셀레늄을 이용해서 기능 테스트를 작성했고 Django 설치 및 실행까지 끝냈습니다. 고트님이 인증한 테스트 우선 TDD 방법을 구현한 것입니다.
