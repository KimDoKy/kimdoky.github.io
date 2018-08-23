---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 1
category: django
tags: [ 'django' ]
---

[TaskBuster Django Tutorial](http://www.marinamele.com/taskbuster-django-tutorial)을 진행하지만, 버전의 차이가 있습니다. django 2.1, python 3.6 기준으로 진행합니다.

# [Part I – 작업 환경과 Django 프로젝트 시작하기](http://www.marinamele.com/taskbuster-django-tutorial/taskbuster-working-environment-and-start-django-project)

좋은 작업 환경을 구축하는 것은 생산성 향상에 매우 중요합니다. 구성하는데 시간이 걸릴 수도 있지만, 잘 수행되면 충분히 가치있는 일입니다.

예를 들어, 가상 환경은 패키지를 체계적으로 관리 및 제어할 수 있게 해주며, 훌륭한 에디터는 변수 이름, 패키지 방법, 구문 강조를 도와줍니다.

## 작업 환경 구축

[python setting for MacOS](https://github.com/KimDoKy/FastCamp/blob/master/python/2017-01-25%20(python%20setting).md)를 참고하세요.

텍스트 에디터는 그냥 편한거 쓰세요. 저는 vi와 파이참을 사용합니다.(주는 vi)

Git도 다룹니다.

## Django 설치

```
$ pip install django
```
이후 진행은 원문에서는 sublime text로 진행하지만, 전 그냥 vi를 사용합니다. 손에 편한게 좋은 겁니다.

## 테스트 고트님에세 복종하십시오.

TDD(Test-Driven Development)에서는 '어떤 코드를 작성하기 전에 테스트를 작성하라는 당신의 머리 속에 있는 작은 목소리'를 따라야 한다고 말합니다. **테스트!!**

테스트를 위해 브라우저를 시뮬레이션할 'Selenium' 패키지를 설치합니다.(Firefox나 Chrome도 있어야 합니다.)

```
$ pip install selenium
```

tasknuster_project 폴더로 이동하여 **기능 테스트** 를 위한 폴더를 만듭니다. 이 폴더에는 **사용자 관점에서 프로젝트 기능** 을 테스트하는 모든 파일이 포함됩니다.

```
$ mkdir -p taskbuster_project/functional_tests
$ vi taskbuster_project/functional_tests/all_users.py
```

다음 테스트를 작성하세요.

```python
# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # 원문과 다르게 Chrome을 사용하기 때문에 chromedriver를 다운받아두고
        # 패스를 설정해주어야 합니다.
        chromedriver = '../../../../../driver/chromedriver'
        self.browser = webdriver.Chrome(chromedriver)
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_it_worked(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django: the Web framework for perfectionists with deadlines.', self.browser.title)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
```

- 첫 줄은 파일의 코딩을 나타냅니다.
- 테스트용 python 라이브러리인 selenium과 unittest를 가져옵니다.
- NewVisitorTest라는 TestCase 클래스를 만듭니다.
 - 테스트를 초기화하는 'setUp' 메소드. 브라우저를 열면 필요에 따라 3초동안 대기합니다.(페이지가 로드되지 않은 경우)
 - 각 테스트 후에 실행되는 'tearDown'메서드. 브라우저를 닫습니다.
 - 테스트로 시작하고 웹페이지의 제목에 'Django: the Web framework for perfectionists with deadlines.'를 포함하고 있다 주장하는 메서드(Django 2.0에서 메세지가 바뀌었다.)
- 'setUp'과 'tearDown'메서드는 각 테스트 방법(단어 테스트로 시작하는 방법)의 시작과 끝에 실행됩니다.
- 마지막 라인은 Python이 파일을 직접 실행하는 경우에만 `unittest.main()` 함수를 실행할 것임을 의미합니다. 이 함수는 test로 시작하는 메서드을 찾음으로써 정의된 다른 테스트를 식별합니다.
- ResourceWarning 메시지를 피하기 위해 선택적 매개 변수 `warnings='ignore'`로 unittest.main() 함수를 호출합니다.

이 스크립트를 실행합니다.

```
$ python all_users.py
```

결과 출력은 테스트가 분명히 실패하는 방법을 보여줍니다.

```
FAIL: test_it_worked (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "all_users.py", line 18, in test_it_worked
    self.assertIn('Django: the Web framework for perfectionists with deadlines.', self.browser.title)
AssertionError: 'Django: the Web framework for perfectionists with deadlines.' not found in 'localhost'
```

이제 Django 프로젝트를 만들고 이 테스트를 통과시킵니다.

## Django Project 만들기

```
$ django-admin startproject taskbuster .
```
명령의 끝에 .이 표시되면 추가 디렉터리를 만들지 않고 프로젝트를 생성합니다. 현재 디렉터리 구조입니다.

```
.
├── functional_tests
│   ├── all_users.py
│   └── geckodriver.log
├── manage.py
└── taskbuster
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

- manage.py는 마이그레이션, 커스텀스크립트 등 개발 서버를 관리하는데 사용됩니다.
- taskbuster 폴더에는 다음 내용이 들어 있습니다.
 - 이 폴더가 Python 패키지임을 나타내는 `__init__.py` 파일
 - settings.py
 - urls.py
 - Django의 배포를 구성하는 wsgi.py

이 튜토리얼 뒷 부분엔 프로젝트와 관련된 모든 애플리케이션, 템플릿, static 파일 및 기타 파일이 포함됩니다.


## 개발 서버 시작

```
$ python manage.py runserver
```
마이그레이션에 대한 경고가 뜨지만 무시합니다. 뒤에 할꺼니까..

```
Starting development server at http://127.0.0.1:8000/
```

브라우저를 열고 URL을 확인할 수 있습니다. 다른 터미널 탭을 열어서 테스트를 실행합니다.

```
$ python functional_tests/all_users.py
----------------------------------------------------------------------
Ran 1 test in 2.047s

OK
```

테스트가 통과되었습니다.

---

- 아직 파트1이라 내용이 쉽습니다. 쉬운 내용들은 스킵하면서 진행합니다.
- 원문에서는 firefox를 사용하지만 전 chrome이 더 편해서 chrome으로 바꾸었습니다.
