---
layout: post
section-type: post
title: new TDD-Chapter 1. Getting Django Set Up Using a Functional Test
category: tdd
tags: [ 'tdd' ]
---

## Required Software Installations

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

functional_tests.py

```python
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title
```

```
$ python functional_tests.py
```

## 1.2 Getting Django Up and Running

```
django-admin.py startproject superlists
```

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

```
$ python manage.py runserver
```

![]({{ site.url }}/img/post/tdd/1_1.png)

## 1.3 Starting a Git Repository

```
$ ls
superlists  functional_tests.py  geckodriver.log
$ mv functional_tests.py superlists/
$ cd superlists
$ git init .
```

```
$ echo "db.sqlite3" >> .gitignore
$ echo "geckodriver.log" >> .gitignore
$ echo "__pycache__" >> .gitignore
$ echo "*.pyc" >> .gitignore
```

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

```
$ git commit -m "first commit: First FT and basic Django config"
```
