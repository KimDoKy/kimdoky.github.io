---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 4. mock을 이용한 단위 테스트
category: python
tags: [ 'python' ]
---

`unittest.mock`는 소프트웨어 테스트를 위한 mock 객체를 제공합니다.  

`mock`란, 테스트가 의존하고 있는 객체를 인터페이스가 동일한 의사 객체로 대체라는 것입니다.
unittest.mock에 의해 대체된 mock 객체에는 호출할 때의 반환값 지정이나 예외 발생 등을 지정할 수 있습니다. mock를 이용하면 외부 API를 사용하고 있거나 데이터베이스에 접속해야 해서 테스트가 어려울 때에도, 외부에 의존하지 않고 테스트를 실행할 수 있습니다.  

예를 들어, 단위 테스트를 실행하려는 함수 my_processing()이 외부 API인 "OutsideAPI"에 처리를 의존하고 있는 상태입니다.

### 외부 API에 의존하는 상황에서 함수의 단위 테스트를 시행하는 예: sample_processing.py

```python
# 외부 어떤 API
class OutsideAPI:
    def do_something(self):
        return '외부 API로 어떠한 처리를 실행한 결과'

# 단위 테스트를 하려는 처리
def my_processing():
    api = OutsideAPI()
    return api.do_something() + '를 사용하여 무엇인가를 하고 있다.'

if __name__ == "__main__":
    print(my_processing())
```

### sample_processing.py 실행 결과

```
$ python sample_processing.py
외부 API로 어떠한 처리를 실행한 결과를 사용하여 무엇인가를 하고 있다.
```

Python 표준의 mock 기능을 제공하는 unittest.mock을 이용하여 외부 API OutsideAPI에서의 처리를 mock 객체로 대체하여, my_processing() 함수를 단위 테스트라기까지의 흐름을 다루겠습니다.

## mock 객체를 생성하여 반환값고 예외 설정하기 - MagicMock
unittest.mock.MagicMock 클래스를 이용하면 간단하게 mock 객체를 생성할 수 있습니다. 여기서는 외부 API OutsideAPI의 처리를 대체하는 mock 객체를 생성합니다.

### 외부API OutsideAPI의 do_something() 처리를 대체하는 mock 객체 생성하기

```python
>>> from sample_processing import OutsideAPI
>>> from unittest.mock import MagicMock

# 외부 API의 do_something() 함수를 대체하는 mock 객체 생성
>>> api = OutsideAPI()
>>> api.do_something = MagicMock()
>>> api.do_something
<MagicMock id='4546053848'>

# do_something() 함수의 반환값 설정
>>> api.do_something.return_value = 'mock 객체로 대체된 결과'
>>> api.do_something()
'mock 객체로 대체된 결과'

# 함수에 예외를 설정할 수도 있음
>>> api.do_something.side_effect = Exception('예외를 설정합니다.')
>>> api.do_something()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/unittest/mock.py", line 917, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/unittest/mock.py", line 973, in _mock_call
    raise effect
Exception: 예외를 설정합니다.
```

이렇게 외부 API의 처리를 mock 객체로 대체할 수 있습니다.

## 클래스와 메서드를 mock으로 대체하기 - patch
특정 클래스나 메서드를 mock 객체로 대체하려면, parch 장식자/컨텍스트 매니저를 이용합니다. 여기서는 외부 API OutsideAPI의 처리를 대체하는 mock 객체를 생성합니다.

### 장식자 이용하기
patch의 인수에 대체할 대상을 지정하고, 테스트 인수에 대체할 mock 객체를 넘겨줍니다.

### 장식자를 이용하여 외부 API OutsideAPI에 의존하는 처리를 mock으로 대체하기
#### test_sample_processing1.py

```python
from sample_processing import my_processing
from unittest.mock import patch
import unittest

class TestMyClass(unittest.TestCase):
    # 장식자를 이용하여  OutsideAPI를 APIMock으로 대체
    @patch('sample_processing.OutsideAPI')
    def test_my_processing(self, APIMock):
        api = APIMock()
        api.do_something.return_value = 'mock 객체로 대체된 결과'

        # 의존하고 있던 처리를 mock으로 대체하고, my_processing() 처리를 실행
        # assert my_processing() == 'mock 객체로 대체된 결과를 사용하여 무언가를 하고 있다.'

if __name__ == "__main__":
    unittest.main()
```

#### test_sample_processing1.py 실행 결과

```
$ python test_sample_processing1.py
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

### 컨텍스트 매니저 이용하기
with 문을 이용하여 특정 클래스나 메서드를 mock으로 대체할 수 있습니다. 이때, patch는 with 문의 블록 내에서만 적용됩니다.

### 컨텍스트 매니저를 이용하여 외부 API OutsideAPI에 의존하는 처리를 mock으로 대체하기
#### test_sample_processing2.py

```python
from sample_processing import my_processing
from unittest.mock import patch
import unittest

class TestMyClass(unittest.TestCase):
    def test_my_processing(self):
        with patch('sample_processing.OutsideAPI') as APIMock:
            api = APIMock()
            api.do_something.return_value = 'mock 객체로 대체된 결과'

            assert my_processing() == 'mock 객체로 대체된 결과를 사용하여 무엇인가를 하고 있다.'

        assert my_processing() == '외부 API로 어떠한 처리를 실행한 결과를 사용하여 무엇인가를 하고 있
다.'

if __name__ == "__main__":
    unittest.main()
```

#### test_sample_processing2.py 실행 결과

```
$ python test_sample_processing2.py
.
----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
```

## mock 객체가 호출되었는지 확인하기 - MagicMock.assert_called_with
`MagicMock.assert_called_with`는 mock 메서드가 실제로 호출되었는지를 확인하고 assertion을 던지는 메서드입니다. 이것은 단위 테스트를 할 때 매우 유용합니다.

### mock 객체가 호출되었는지 확인하기

```python
>>> from unittest.mock import MagicMock
>>> api = OutsideAPI()
>>> api.do_something = MagicMock()
>>> api.do_something.return_value = 'mock 객체로 대체된 결과'

# do_something 메서드가 1회 이상 호출되었는지 확인하다.
# 1회 이상 호출되지 않았으면 AssertionError가 발생한다.
>>> api.do_something.assert_called_with()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/unittest/mock.py", line 783, in assert_called_with
    raise AssertionError('Expected call: %s\nNot called' % (expected,))
AssertionError: Expected call: mock()
Not called

>>> api.do_something()  # 첫 번째 호출
'mock 객체로 대체된 결과'
>>> api.do_something.assert_called_with()
>>>

# 메서드가 한 번만 호출되었는지 확인한다.
>>> api.do_something.assert_called_once_with()
>>>
>>> api.do_something()  # 두 번째 호출
'mock 객체로 대체된 결과'
>>> api.do_something.assert_called_once_with()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/unittest/mock.py", line 802, in assert_called_once_with
    raise AssertionError(msg)
AssertionError: Expected 'mock' to be called once. Called 2 times.
```

> #### MagicMock와 Mock의 차이  
unittest.mock 모듈에는 MagicMock과 Mock, 이 두 가지의 mock 객체가 준비되어 있습니다. MagicMock 클래스는 Mock 클래스의 서브클래스로서 정의되어 있으며, Mock 클래스가 갖는 모든 기능뿐만 아니라 Python이 갖는 모든 특수 메서드를 지원합니다.
e
```python
>>> from unittest.mock import Mock, MagicMock

#########################################
# MagicMock을 이용하는 예

>>> mock = MagicMock()
>>> mock.return_value = 1.0

# 특수 메서드가 기본으로 지원된다.
>>> int(mock)
1

#########################################
# Mock을 이용하는 예

>>> mock = Mock()

# 특수 메서드에 대해서도 Mock을 준비해야 한다.
>>> mock.__float__ = Mock(return_value=1.0)

# __float__만 정의되어 있기 때문에 오류가 발생한다.
>>> int(mock)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: int() argument must be a string, a bytes-like object or a number, not 'Mock'

# int()를 이용하고 싶으면 특수 메서드 __int__도 정의해야 한다.
>>> mock.__int__ = Mock(return_value=1)
>>> int(mock)
1
```
특별한 이유가 없다면 MagicMock을 사용하면 됩니다.
