---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 7. 더 높은 수준의 unittest 기능 이용하기
category: python
tags: [ 'python' ]
---

`pytest`는 더 높은 수준의 기능을 제공하는 테스트 프레임워크입니다.

## pytest 설치

```
$ pip install pytest
```

## 테스트를 작성하여 실행하기
기댓값과 실제 값을 검증할 때에는 Python 표준인 assert 문을 이용합니다.

### 테스트 케이스 작성 예: test_sample.py

```python
import pytest

def test_upper():
    assert 'foo'.upper() == 'FOO'
```

### test_sample.py 테스트 결과

```
$ py.test test_sample.py
======================================== test session starts ========================================
platform darwin -- Python 3.5.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /path/chap11/7_pytest, inifile:
collected 1 item

test_sample.py .

===================================== 1 passed in 0.02 seconds ======================================
```

pytest는 테스트가 실패할 때는 함수 호출 반환값을 표시합니다.

### 실패하는 테스트 케이스 예: test_sample2.py

```python
import pytest

def test_upper():
    assert 'foo'.upper() == 'Foo'
```

### test_sample2.py 테스트 결과

```
$ py.test test_sample2.py
======================================== test session starts ========================================
platform darwin -- Python 3.5.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /path/chap11/7_pytest, inifile:
collected 1 item

test_sample2.py F

============================================= FAILURES ==============================================
____________________________________________ test_upper _____________________________________________

    def test_upper():
>       assert 'foo'.upper() == 'Foo'
E       AssertionError: assert 'FOO' == 'Foo'
E         - FOO
E         + Foo

test_sample2.py:4: AssertionError
===================================== 1 failed in 0.05 seconds ======================================
```

## 자동으로 테스트를 찾아 실행하기

pytest는 테스트를 실행할 때, 지정한 디렉터리 아래의 테스트를 자동으로 탐색하여 실행합니다.(지정하지 않으면 현재 디렉터리 아래의 테스트를 탐색합니다.) 탐색 대사은 Python 패키지 아래의 `test_*` 또는 `*_test`등의 이름으로 정의되어 있는 모듈입니다. 이 조건이 충족되면, unittest로 작성된 테스트도 실행됩니다.

```
$ py.test [테스트가 지정된 디렉터리]
```

### 여러 개의 입출력 패턴에 대한 테스트(Parameterized test)
pytest는 PHPUnit 등에서 지원하는 테이터 제공자의 기능을 기본으로 지원합니다. 데이터 제공자란 하나의 테스트에 대한 입력과 이에 대응하는 출력을 여러 개 부여할 수 있게 해 주는 기능으로, 이를 통해 하나의 메서드에 대한 테스트를 매개변수화할 수 있습니다.  

### Parameterized test의 예: test_sample3.py

```python
import pytest

@pytest.mark.parametrize("obj", ['1', '2', 'Foo'])
def test_indigit(obj):
    assert obj.isdigit()
```

### test_sample3.py 테스트 결과

```
$ py.test test_sample3.py
======================================== test session starts ========================================
platform darwin -- Python 3.5.2, pytest-3.2.5, py-1.5.2, pluggy-0.4.0
rootdir: /path/chap11/7_pytest, inifile:
collected 3 items

test_sample3.py ..F

============================================= FAILURES ==============================================
_________________________________________ test_indigit[Foo] _________________________________________

obj = 'Foo'

    @pytest.mark.parametrize("obj", ['1', '2', 'Foo'])
    def test_indigit(obj):
>       assert obj.isdigit()
E       AssertionError: assert False
E        +  where False = <built-in method isdigit of str object at 0x10468ec38>()
E        +    where <built-in method isdigit of str object at 0x10468ec38> = 'Foo'.isdigit

test_sample3.py:5: AssertionError
================================ 1 failed, 2 passed in 0.06 seconds =================================
```
입력이 1 또는 2일 때는 테스트가 성공하였으나, Foo를 주면 테스트가 실패하는 것을 알 수 있습니다.
