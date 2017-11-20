---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 3. 단위 테스트 프레임워크 이용하기
category: python
tags: [ 'python' ]
---

`unittest`는 테스트의 자동화, 초기 설정과 종료 처리 공유, 테스트 분류, 테스트 실행과 결과 리포트 분리 등의 기능을 제공합니다.

## 테스트를 작성하여 실행하기
테스트 케이스는 unittest.TestCase의 서브 클래스로 작성합니다. 메서드 이름이 test로 시작하는 것이 테스트하는 메서드입니다. 테스트 러너는 명명 규칙(Naming conventions)에 따라 테스트를 수행하는 메서드를 검색합니다.

### 테스트 케이스의 작성 예: sample_unittest.py

```python
import unittest

class TestSample(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__=='__main__':
    unittest.main()
```

### sample_unittest.py 실행

```
$ python sample_unittest.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
앞선 코드를 수정하여 테스트 실패하는 예를 확인해봅니다.

### 테스트 케이스 실패 예: sample_unittest.py

```python
import unittest

class TestSample(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'Foo')

if __name__=='__main__':
    unittest.main()
```

### sample_unittest.py 실행

```
$ python sample_unittest.py
F
======================================================================
FAIL: test_upper (__main__.TestSample)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "sample_unittest.py", line 5, in test_upper
    self.assertEqual('foo'.upper(), 'Foo')
AssertionError: 'FOO' != 'Foo'
- FOO
+ Foo


----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
```

테스트에 실패한 것을 확인할 수 있습니다.

## 다양한 조건이나 실패를 작성하기
unittest.TestCase 클래스에서는 테스트 러너가 테스트를 실행하는 인터페이스뿐만 아니라, 각종 검사 및 테스트 실패를 보고하는 메서드를 지원합니다.  

다음 메서드를 이용하면 테스트를 실행하는 전후 처리(setUp/tearDown)를 작성할 수 있습니다.

### 테스트를 실행하는 전후 처리의 정의

형식 | 설명
---|---
setUp() | 테스트 픽스처(test fixture)를 준비하는 메서드. 테스트 메서드를 실행하기 직전에 호출된다.
tearDown() | 테스트 메서드를 실행하고 나서 호출된다. 이 메서드는 테스트 결과에 상관없이 setUp()이 성공한 경우에만 호출된다.
setUpClass() | 클래스 내에 정의된 테스트를 실행하기 전에 호출되는 클래스 메서드. 클래스를 유일한 인수로 가지며, classmethod()로 장식되어(decorate) 있어야 한다.
tearDownClass() | 클래스 내에 정의된 테스트를 실행하고 나서 호출되는 클래스 메서드. 클래스를 유일한 인수로 가지며, classmethod()로 장식되어 있어야 한다.

예를 들어 setUp() 메서드를 이용하면 다음과 같이 초기화 처리를 작성할 수 있습니다.

### 초기화 처리

```python
class TestSample(unittest.TestCase):
    def setUp(self):
        self.target = 'foo'

    def test_upper(self):
        self.assertEqual(self.target.upper(), 'Foo')
```

### 대표적인 assert 메서드

메서드 | 테스트 내용
---|---
assertEqual(a,b) | a == b
assertNotEqual(a,b) | a != b
assertTrue(x) | bool(x) is True
assertFalse(x) | bool(x) is False
assertIs(a,b) | a is b
assertIsNot(a,b) | a is not b
assertInNone(x) | x is None
assertIsNotNone(x) | x is not None
assertIn(a,b) | a in b
assertNotIn(a,b) | a not in b
assertIsInstance(a,b) | isinstance(a,b)
assertNotIsInstance(a,b) | not isinstance(a,b)

## 테스트를 건너뛰거나 의도적으로 실패하기
Python의 decorator를 이용하여 장식한 테스트를 건너뛰거나 의도적으로 실패하는 처리를 작성할 수 있습니다.

### 건너뛰거나 의도적 실패를 작성할 때 사용하는 작성자

장식자 | 설명
---|---
@unittest.skip(reason) | 테스트를 무조건 건너뛴다. reason에는 테스트를 건너뛰는 이유를 적는다.
@unittest.skipIf(condition, reason) | condition이 참이면 테스트를 건너뛴다.
@unittest.skipUnless(condition, reason) | condition이 거짓이면 테스트를 건너뛴다.
@unittest.expectedFailure | 테스트 실패가 의도적이라는 것을 나타낸다. 해당 테스트에 실패해도 이 테스트는 실패로 세지 않는다.

### 테스트 건너뛰기

```python
class TestSample(unittest.TestCase):
    @unittest.skip("이 테스트를 건너뜁니다.")
    def test_upper(self):
        self.assertEqual(self.target.upper(), 'Foo')

if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSample)
    unittest.TextTestRunner(verbosity=2).run(suite)
```

앞선 코드에서 테스트를 건너뛰기 처리를 알기 쉽게 표시하기 위해 unittest.main()을 수정하여 더 자세한 테스트 결과를 표시하였습니다.

### 자세한 테스트 결과 출력

```
$ python sample_unittest.py
test_upper (__main__.TestSample) ... skipped '이 테스트를 건너뜁니다.'

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK (skipped=1)
```

## 명령줄 인터페이스 이용하기
`unittest`는 명령줄에서도 사용할 수 있습니다.

### 명령줄에서 unittest 사용

```
python -m unittest test_module1 test_module2  # 특정 모듈로 정의된 테스트를 실행한다.
python -m unittest test_module.TestClass  # 특정 클래스로 정의된 테스트를 실행한다.
python -m unittest test_module.TestClass.test_method  # 특정 메서드로 정의된 테스트를 실행한다.
```

### unittest 명령줄 옵션

옵션 | 설명
---|---
-b, --buffer | 표준 출력과 표준 오류 출력의 스트림을 테스트를 실행하는 동안 버퍼링한다.
-c, --catch | control-C를 실행 중인 테스트가 종료될 때까지 지연시키고, 그때까지의 결과를 출력한다. 두 번째 control-C는 원래대로 KeyboardInterrupt 예외를 발생시킨다.
-f, --failfast | 맨 처음 오류 또는 실패 시 테스트를 중지한다.
