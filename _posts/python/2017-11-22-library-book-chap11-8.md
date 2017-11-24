---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 8. 스택 트레이스 다루기
category: python
tags: [ 'python' ]
---

`traceback`은 Python의 스택 트레이스(stack trace)를 서식을 맞추어 표시하거나 얻는 기능을 제공합니다. 스택 트레이스는 문제를 지적하거나 기록하기 위해 사용합니다.

traceback 모듈은 프로그램을 정지시키지 않고 스택 트레이스를 표시하거나, 콘솔 이외(로그 파일 등)에 스택 트레이스를 출력합니다.

## 스택 트레이스 표시하기
`print_exc()`는 스택 트레이스를 Python 인터프리터와 같은 서식으로 출력합니다. 기본으로는 콘솔에 출력하지만, 인수 file을 지정하면 파일에도 출력할 수 있습니다.

### print_exc()

형식 | print_exc(limit=None, file=None, chain=True)
---|---
설명 | 발생한 예외로부터 스택 트레이스 정보를 취득하여, 서식에 맞추어 출력한다.
인수 | limit - 지정한 수까지의 스택 트레이스를 출력한다. <br> file - 출력 위치가 될 file-like 객체를 지정한다.(기본값은 sys.stderr) <br> chain - True이면 연쇄적인 예외도 동일하게 출력된다.

### 스택 트레이스 표시하기
발생한 예외의 스택 트레이스를 print_exc()를 사용하여 콘솔에 출력합니다.

```Python
import traceback

def hoge():
    tuple()[0]  # 존재하지 않는 요소에 대한 접근이기 때문에 IndexError가 발생한다.

try:
    hoge()
except IndexError:
    print('--- Exception occurred ---')
    traceback.print_exc(limit=None)
```

### print_exc()의 출력 예
인수 limit에는 기본값과 같은 None을 지정하였기 때문에, 모든 스택 트레이스가 출력됩니다.

```
$ python example.py
--- Exception occurred ---
Traceback (most recent call last):
  File "example.py", line 7, in <module>
    hoge()
  File "example.py", line 4, in hoge
    tuple()[0]
IndexError: tuple index out of range
```

### print_exc의 출력 예 -limit을 지정할 때
limit에 1을 지정하면, 스택 트레이스는 하나만 출력됩니다.

```
$ python example2.py
--- Exception occurred ---
Traceback (most recent call last):
  File "example2.py", line 7, in <module>
    hoge()
IndexError: tuple index out of range
```
이처럼 예외를 포착하여 print_exc()를 이용하면 스택 트레이스를 출력하면서도 프로그햄을 계속 실행시킬 수 있습니다.

## 스택 트레이스를 문자열로 취급하기
`format_exc()`는 스택 트레이스를 Python 인터프리터와 같은 서식으로 맞춘 문자열로 반환합니다.

### format_exc()

형식 | format_exc(limit=None, chain=True)
---|---
설명 | 발생한 예외로부터 스택 트레이스 정보를 취득하고, 서식을 맞춘 문자열로 반환한다.
인수 | limit - 지정한 수까지의 스택 트레이스를 출력한다. <br> chain - True이면 연쇄적인 예외도 동일하게 출력된다.

### 스택 트레이스를 취득하여 로그를 출력하기
발생한 예외의 스택 트레이스를 format_exc()를 사용하여 로그를 출력하는 예입니다.

```python
import traceback
import logging

logging.basicConfig(filename='/tmp/example.log', format='%(asctime)s %(levelname)s %(message)s')

try:
    tuple()[0]
except IndexError:
    logging.error(traceback.format_exc())
    raise
```
샘플 코드에서는 발생한 예외의 스택 트레이스를 로그에 출력하고 있습니다. 예를 들어, 로그의 출력 파일로 설정해 두면 로그 파일에 기록된 예외 내용을 나중에 확인할 수 있습니다. 이것은 데몬이나 정기 실행되는 패치 처리 등, 백그라운드에서 실행되는 프로그램을 이용할 때 유용합니다.

### 스택 트레이스를 로그에 출력하는 스크립트 실행하기
샘플 코드를 example3.py로 실행하여 로그 파일에 출력된 스택 트레이스를 표시해봅니다.

```
$ python example3.py
$ cat /tmp/example.log
2017-11-21 23:06:50,230 ERROR Traceback (most recent call last):
  File "example3.py", line 7, in <module>
    tuple()[0]
IndexError: tuple index out of range
```
