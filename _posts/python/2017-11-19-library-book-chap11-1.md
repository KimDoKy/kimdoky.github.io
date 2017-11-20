---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 1. 문서 생성과 온라인 도움말 시스템
category: python
tags: [ 'python' ]
---

테스트를 통해 프로그램 품질을 검증하거나 버그가 숨어 있을 때 그 원인을 찾아내는(디버깅) 것은 소프트웨어 개발에 있어서 매우 중요한 기술입니다.

# 문서 생성과 온라인 도움말 시스템

`pydoc`은 소스 코드에 작성한 주석으로부터 문서를 자동으로 생성해줍니다. 생성된 문서는 텍스트 형식으로 콘솔에 표시하거나 HTML 파일로 저장할 수 있습니다. HTTP 서버를 구동해 웹브라우저에서 열람 할 수도 있습니다.

## 모듈의 문서 확인하기
Python 인터프리터에서 `help()`를 입력하면 대화 모드 인터프리터에서 온라인 도움말을 실행할 수 있습니다.

### Python 인터프리터에서 문서 확인

```python
>>> help()

Welcome to Python 3.5's help utility!

If this is your first time using Python, you should definitely check out
the tutorial on the Internet at http://docs.python.org/3.5/tutorial/.

Enter the name of any module, keyword, or topic to get help on writing
Python programs and using Python modules.  To quit this help utility and
return to the interpreter, just type "quit".

To get a list of available modules, keywords, symbols, or topics, type
"modules", "keywords", "symbols", or "topics".  Each module also comes
with a one-line summary of what it does; to list the modules whose name
or summary contain a given string such as "spam", type "modules spam".

# 문서를 확인하고 싶은 모듈 이름을 입력한다.
help> string

Help on module string:

NAME
    string - A collection of string constants.

MODULE REFERENCE
    https://docs.python.org/3.5/library/string.html
    ...
# q를 입력하면 help 모드에서 빠져나온다.
help> q

You are now leaving help and returning to the Python interpreter.
If you want to ask for help on a particular object directly from the
interpreter, you can type "help(object)".  Executing "help('string')"
has the same effect as typing a particular string at the help> prompt.
>>>
```

### pydoc 명령어 실행 예

`pydoc` 명령어를 이용하면 같은 기능을 명령줄에서 사용할 수 있습니다.

```python
$ python -m pydoc string
$ python -m pydoc string.Formatter  # doc "."로 구분함으로써 클래스, 메서드, 함수의 help 정보도 참조할 수 있다.
```
> -m : 라이브러리 모듈을 스크립트로 실행합니다.

## 모듈의 문서 작성하기

`pydoc`은 Python의 소스 코드에 적힌 정보로부터 자동으로 문서를 생성합니다.

### 문서 작성 대상 파일: sample_module.py

```Python
"""
 모듈에 관한 주석을 작성합니다.
"""

__author__ = "Python Freelec <sample@sample.com>"
__version__ = "0.0.1"

class SampleClass(object):
    """
    클래스에 관한 주석을 작성합니다.
    """
    def sample_method(self, sample_params):
        """
        메서드에 관한 주석을 작성합니다.

        :params str sample_param: 인수에 관한 주석을 작성합니다.
        """
        pass
```

\__author__나 \__version__ 등의 작성은 모듈의 메타 정보를 나타내는 것입니다.  

sample_module.py를 pydoc 명령어로 실행하면 다음과 같은 문서가 생성됩니다. Python 인터프리터에서 help() 명령어를 이용할 수도 있습니다.

### sample_module.py에 대해 pydoc 실행

```
$ python -m pydoc sample_module


Help on module sample_module:

NAME
    sample_module - 모듈에 관한 주석을 작성합니다.

CLASSES
    builtins.object
        SampleClass

    class SampleClass(builtins.object)
     |  클래스에 관한 주석을 작성합니다.
     |
     |  Methods defined here:
     |
     |  sample_method(self, sample_params)
     |      메서드에 관한 주석을 작성합니다.
     |
     |      :params str sample_param: 인수에 관한 주석을 작성합니다.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

VERSION
    0.0.1
```

## 모듈의 문서를 HTML 형식으로 생성하기
`pydoc` 명령어의 인수에 -w 옵션을 지정하면 현재 디렉터리에 HTML 문서가 생성됩니다.

### html 출력

```
$ python -m pydoc -w sample_module
wrote sample_module.html
```

### Python의 HTML 문서

![]({{site.url}}/img/post/python/library/11.1.png)

## HTML 서버를 구동하여 웹브라우저에서 문서 확인하기
`pydoc` 명령어에 -p 옵션으로 포트 번호를 지정하면 로컬 머신에 문서 열람용 HTTP 서버를 구동할 수 있습니다.

### 1234번 포트에 HTTP 서버 구동하기

```
$ python -m pydoc -p 1234
Server ready at http://localhost:1234/
Server commands: [b]rowser, [q]uit
server>
```

http://localhost:1234/ 으로 접속하면 문서를 열람할 수 있습니다.

### Python 문서

![]({{site.url}}/img/post/python/library/11.2.png)
