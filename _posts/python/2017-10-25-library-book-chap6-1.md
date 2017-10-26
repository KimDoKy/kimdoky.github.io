---
layout: post
section-type: post
title: Python Library - chap 6. 파일과 디렉터리 접근하기 - 1. 파일 경로 조작하기
category: python
tags: [ 'python' ]
---
파일 경로 조작을 비롯하여 원하는 파일을 찾거나, 파일을 정리하는 기능을 제공하는 다양한 표준 라이브러리를 소개합니다. 같은 명령어를 수작업으로 반복 실행하거나 복잡한 셸 스크립트를 기술할 필요가 없어집니다.  

-

os.path 모듈은 파일 경로와 관련된 기능을 제공합니다.

- 파일 경로 조작하기
- 지정한 파일 경로의 정보 얻기

하지만 다음의 기능은 제공되지 않습니다.

- 파일 읽고 쓰기
- 파일 시스템에 대해 접근하기(파일, 디렉터리 생성과 삭제 등)

### os.path 모듈의 대표적인 함수

함수 이름 | 설명 | 반환값
---|---|---
abspath(path) | 파일 경로 path의 절대 경로를 반환한다. | str/bytes
basename(path) | 파일 경로 path의 맨 끝 파일 이름을 반환한다. | str/bytes
dirname(name) | 파일 경로 path의 파일 이름을 제외한 디렉터리 부분을 반환한다. | str/bytes
exists(paths) | 파일 경로 path가 존재하면 True, 존재하지 않으면 False를 반환한다. |  bool
join(path, \*paths) | 인수로 지정한 여러 개의 파일 경로를 결합한다. | str/bytes
split(path) | 파일 경로를 디렉터리 부분(dirname()과 같음)과 파일 이름 부분(basename()과 같은)으로 분해한 두 요소의 튜플을 반환한다. | tuple

os.path 모듈의 함수는 인수 path에 문자열과 바이트열 중 하나를 지정할 수 있으며, 반환값은 인수와 같은 형으로 반환됩니다.

### os.path의 사용 예

```python
>>> import os.path
>>> os.path.abspath('.')
'/Users/dokyungkim/'

>>> os.path.join('hoge','fuga','piyo')
'hoge/fuga/piyo'

>>> path = _
>>> os.path.basename(path)
'piyo'

>>> os.path.dirname(path.encode())  # 인수로 바이트열을 주면 반환값도 바이트열이 된다.
b'hoge/fuga'

>>> os.path.exists(path)
False

>>> os.path.join('hoge','fuga',b'piyo')  # 문자열과 바이트열을 동시에 지정할 수는 없다.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/posixpath.py", line 89, in join
    genericpath._check_arg_types('join', a, *p)
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/genericpath.py", line 145, in _check_arg_types
    raise TypeError("Can't mix strings and bytes in path components") from None
TypeError: Can't mix strings and bytes in path components

>>> os.path.split(path)
('hoge/fuga', 'piyo')
```

위의 코드는 파일 경로를 구분하는 문자로 UNIX 환경에서 사용하는 슬래시를 사용하고 있습니다. 같은 코드를 Windows 환경에서 실행할 때도 슬래시는 겨로를 구분하는 문자로 인식하므로 정상적으로 동작합니다.

> ### 이식 가능한 코드 작성하기  
파일 경로를 구성하는 요소 중, 디렉터리를 구분하는 문자열은 os에 따라 다릅니다. Windows는 역슬래시(\\)이지만, UNIX계열의 os는 슬래시(/)를 사용합니다.  
**이식성이 없는 코드 예**  
```python
path = ".\\hoge\\hoge"
f = open(path, 'r')
```
os.path 모듈을 사용하면 경로 문자열 작성무문을 Windows와 UNIX 계열 운영체제레어 동작하도록 자시 작성할 수 있습니다.  
**이식성이 있는 코드 예**  
```python
path = os.path.join(".", "hoge", "hoge")
f = open(path, 'r')
```
파일 시스템 이외에도 플랫폼에 따라 달라지는 기능을 이용하면 코드느느 이식성을 갖지 못하게 됩니다. 여러 플랫폼을 실행할 코드를 작성할 때는 플랫폼에 따라 달라지지 않는 기능을 이용하면 됩니다.  
