---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 2. 대화형 실행 예 테스트하기
category: python
tags: [ 'python' ]
---

`doctest`는 함수나 메서드에 있는 맨 처음 주석(docstring) 내에 작성한 테스트 코드를 실행하는 기능을 제공합니다.  

테스트 코드는 Python의 대화 모드와 비슷한 형식으로, 실행 내용과 기대하는 결과가 적습니다. docstring에 기능 설명과 테스트 코드가 함께 적혀 있으면 사용자는 구체적인 동작을 이해하고 함수나 메서드를 이용할 수 있습니다.  
또한 docstring이 아니라 외부 텍스트 파일에 테스트 코드를 적는 사용 방법도 다룹니다.

## doctest 작성하기
doctest는 doctest 모듈을 import하고 doctest.testmod()를 실행하기만 하면 됩니다. doctest를 실행하면 코드 안에 주석으로 작성된 Python의 대화형 실행 예처럼 보이는 텍스트가 모두 실행되고, 대화형 실행 예대로 동작하는지 여부를 테스트합니다. 구체적으로 ">>>"나 "..."으로 시작하는 부분은 Python 코드를 적고, 그 바로 아래에 기대하는 출력 결과를 작성합니다(다음 ">>>" 행이나 빈 행까지를 출력 결과로 인식합니다.). 출력 결과에 빈 행이 들어갈 때에는 <BLANKLINE>을 삽입합니다.

### Python 코드 안에 doctest를 포함한 예: sample_doctest.py

```python


"""
 주어진 인수에 대해 a / b를 실행하는 함수입니다.
>>> div(5,2)
2.5
"""

def div(a, b):
    """
    답은 소수로 반환됩니다.
    >>> [div(n, 2) for n in range(5)]
    [0.0, 0.5, 1.0, 1.5, 2.0]
    """

    return a / b

if __name__=="__main__":
    import doctest
    doctest.testmod()
```

### 명령줄에서 sample_doctest.py 실행

```
$ python sample_doctest.py
$
```

아무것도 출력되지 않아야 바르게 동작한다는 의미입니다. 스크립트에 -v를 부여하면 자세한 로그를 확인할 수 있습니다.

### 자세한 로그 출력

```
$ python sample_doctest.py -v
Trying:
    div(5,2)
Expecting:
    2.5
ok
Trying:
    [div(n, 2) for n in range(5)]
Expecting:
    [0.0, 0.5, 1.0, 1.5, 2.0]
ok
2 items passed all tests:
   1 tests in __main__
   1 tests in __main__.div
2 tests in 2 items.
2 passed and 0 failed.
Test passed.
```

doctest에서 예외를 다룰 수도 있습니다. 예외가 발생할 떄 원하는 출력은 트레이스백 헤더인  "Traceback (most recent call last):" 또는 "Traceback (innermost last):" 로 시작해야 합니다

### doctest에서 예외를 작성하는 예

```python
def div(a, b):
    """
    ...

    두 번째 인수가 0이면, ZeroDivisionError가 발생합니다.
    >>> div(1, 0)
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<stdin>", line 2, in div
    ZeroDivisionError: division by zero
    """
    ...
```

이처럼 트레이스백 헤더 뒤에 트레이스백 스택이 이어져고 문제는 없으나, doctest는 이 내용을 무시합니다. 문서를 읽는 데 명확한 가치가 있는 정보가 아니면 트레이스백 스택은 생략해도 상관없습니다.

### 트레이스백 스택을 생략하는 예

```python
def div(a, b):
    """
    ...

    두 번째 인수가 0이면, ZeroDivisionError가 발생합니다.
    >>> div(1, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: division by zero
    """
    ...
```

또한 Python 인터프리터에서 다음과 같이 실행하면 doctest 모듈을 표준 라이브러리로부터 직접 실행할 수 있습니다.

### doctest를 표준 라이브러리로부터 직접 실행

```
$ python -m doctest -v sample_doctest.py
```

## 텍스트 파일 안의 실행 예 테스트하기
`doctest`를 이용하여 Python 코드와는 독립된 텍스트 파일 안에 있는 테스트 코드를 실행할 수 있습니다. 장석법은 docstring과 같습니다.

### sample_doctest.txt

```txt
div 모듈
===========================
div 모듈을 import합니다.

    >>> from sample_doctest import div

함수 테스트 부분은 다음과 같이 작성합니다.

    >>> div(6, 2)
    4.0
```
단위 테스트를 실행하려면 testfile() 함수를 이용합니다.

### sample_pydoc2.py

```python
import doctest
doctest.testfile("sample_doctest.txt")
```

### sample_pydoc2.py 실행

```
$ python sample_pydoc2.py
**********************************************************************
File "sample_doctest.txt", line 9, in sample_doctest.txt
Failed example:
    div(6, 2)
Expected:
    4.0
Got:
    3.0
**********************************************************************
1 items had failures:
   1 of   2 in sample_doctest.txt
***Test Failed*** 1 failures.
```
sample_doctest.txt에 작성한 기댓값과 실행 결과가 다르므로, 한 곳의 테스트 실패가 검출됩니다.
