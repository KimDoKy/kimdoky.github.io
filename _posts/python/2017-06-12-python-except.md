---
layout: post
section-type: post
title: Except
category: python
tags: [ 'python' ]
---

예외처리란 에러가 발생했을 경우 어떻게 해야하는지 지정해주는 방법입니다.  
프로그래밍을 할 때 오타 등으로 발생하는 에러는 컴파일 에러라고 하는데 이런 에러는 오타를 수정하여 고치지만, 오타가 아닌 논리적인 에러가 발생하는 경우가 많이 있습니다.  
예를 들어, 사용자에세 1-4까지 숫자를 입력하라고 메시지를 보여주었는데 사용자가 5를 입력한다든지 'y'나 'n'을 입력하라고 했는데 'yes'를 입력하는 경우 등이 논리적인 에러의 예입니다.  
이런 논리적인 에러를 어떻게 대응할 것인지를 지정해 주는 것을 예외 처리라고 합니다.

>
문법
```python
try:
  예외가 발생할 문장
except 예외처리 종류:
  에러가 발생하면 실행할 문장
```
>
ex.
```python
try:
  num = int(input("숫자를 입력해 주세요"))
except ValueError:
  print("숫자가 아닙니다")
```

```python
>>> num = int(input("숫자를 입력하세요: ")) # 정상적인 상황
숫자를 입력하세요: 123
>>>
>>> num = int(input("숫자를 입력하세요: ")) # 에러(예외) 상황
숫자를 입력하세요: abc
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: 'abc'
```
예외처리후
```python
>>> try:
...     num = int(input("숫자를 입력하세요: "))
... except ValueError:
...     print("숫자가 아니네요. 숫자를 입력하세요.")
...
숫자를 입력하세요: abc
숫자가 아니네요. 숫자를 입력하세요.
>>>
```

예외 처리는 에러 유형에 따라 쓰는 문장이 달라집니다.  
바로 위 문장에서 except 뒤에 쓰는 내용이 달라진다는 의미입니다.  

이번에는 나누는 값이 0일 때 발생하는 에러의 경우 예외처리입니다.
```python
>>> no1 = 6
>>> no2 = 0
>>> no1 / no2
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```
맨 마지막 줄에 보면 ZeroDivisionError 이라는 부분을 except 뒤에 적어주면 됩니다.  
```python
SyntaxError: invalid syntax
>>> try:
...     no1 = 6
...     no2 = 0
...     no1 / no2
... except ZeroDivisionError:
...     print("0 으로 나눌수 없습니다!")
...
0 으로 나눌수 없습니다!
>>>
```

위에서 살펴본 예외들은 전부 1개씩 발생하는 경우입니다.  
하지만 실전에서는 여러 가지 예외가 발생할 수도 있기 때문에 모든 예외를 예외처리를 할 때마다 이렇게 `try~except`를 다 사용하기에는 불편합니다.  
그래서 Python에서는 except 뒤에 적는 예외를 여러 개 동시에 적을 수도 있습니다.
```python
>>> try:
...     no1 = 6
...     no2 = 0
...     no1 / no2
... except (ZeroDivisionError, ValueError):
...     print("에러가 발생했습니다!!!")
...
에러가 발생했습니다!!!
```
위와 같이 except 구문 안에 여러 개의 예외 값을 적어 줄 수 있습니다.  
그리고 아해와 같이 여러 개 별도로 사용할 수도 있습니다.

```python
>>> try:
...     no1 = 6
...     no2 = 0
...     no1 / no2
... except ZeroDivisionError:
...     print("0 으로 나눌 순 없어요~")
... except ValueError:
...     print("숫자가 아닙니다.")
...
0 으로 나눌 순 없어요~
```
except를 여러개 사용했을때는 마치 if 문을 사용한 것처럼 해당 에러가 발생한 except만 실행합니다.  
그리고 만약 예외가 발생하지 않았을 경우에는 어떻게 해라고 지정하고 싶을 경우는 예외처리안에서 else 문장을 사용할 수도 있습니다.
```python
>>> try:
...     num = int(input("숫자를 입력하세요"))
... except ValueError:
...     print("숫자가 아닙니다.")
... else:
...     print(num)
...
숫자를 입력하세요123
123

>>> try:
...     num = int(input("숫자를 입력하세요."))
... except ValueError:
...     print("숫자가 아닙니다.")
... else:
...     print(num)
...
숫자를 입력하세요.abc
숫자가 아닙니다.
```
else문을 사용하고 에러가 발생하지 않았을 때는 입력받은 숫자를 그대로 출력하고 예외가 발생한 경우 예외 메시지를 출력하고 있습니다.  

위와 같이 else를 이용해서 에러가 발생하지 않았을 때 원하는 동작을 할 수 있지만 `finally`를 이용하면 에러의 발생여부에 상관없이 원하는 동작을 실행시킬 수 있습니다.
```python
...
숫자를 입력하세요.abc
숫자가 아닙니다.
>>> try:
...     num = int(input("숫자를 입력하세요"))
... except ValueError:
...     print("숫자가 아닙니다.")
... else:
...     print(num)
... finally:
...     print("finally는 무조건 실행됩니다~!")
...
숫자를 입력하세요123
123
finally는 무조건 실행됩니다~!
```
그리고 에러가 발생해도 `finally` 절에 있는 내용은 무조건 실행됩니다.
```python
...
숫자를 입력하세요.abc
숫자가 아닙니다.
>>> try:
...     num = int(input("숫자를 입력하세요"))
... except ValueError:
...     print("숫자가 아닙니다.")
... else:
...     print(num)
... finally:
...     print("finally는 무조건 실행됩니다~!")
...
숫자를 입력하세요abc
숫자가 아닙니다.
finally는 무조건 실행됩니다~!
```
당연히 else를 제외하고 `try~except~finally` 형식으로 사용해도 됩니다.  
`try~except`는 기본적인 문법이지만 else나 finally 같은 경우에는 선택적으로 사용 할 수 있습니다.  

프로그래밍을 하다 보면 의도치 않게 에러가 발생하는 상황도 있지만 경우에 따라서는 에러를 직접 발생시켜야 하는 경우도 있습니다. 그런 상황에서는 `raise` 키워드를 사용해서 원하는 에러를 발생 시킬 수고 있고, 에러를 직접 만들어서 발생시킬 수도 있습니다.

>
문법
```python
raise 에러종류(에러 발생시 나타낼 텍스트)
```
ex.
```python
raise ValueError("값에 대한 에러예요!!")
```

```python
>>> raise ValueError("제가 만든 예외예요~")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: 제가 만든 예외예요~
```
이런 식으로 원할 때 원하는 에러를 발생시킬 수 있습니다.  

실제 문장에 사용해 봅시다.

```python
>>> try:
...     num = int(input("숫자를 입력하세요: "))
...     raise ValueError("0보다 작아요", "0이예요", "0보다 커요")
... except ValueError as e:
...     if num < 0:
...         print(e.args[0])
...     elif num == 0:
...         print(e.args[1])
...     elif num > 0:
...         print(e.args[2])
...
숫자를 입력하세요: 2
0보다 커요
```
3번 라인처럼 미리 발생시킬 에러들을 raise 구문으로 생성한 후 불러서 사용하면 아주 다양한 형태의 예외 메시지를 직접 만들어서 사용할 수 있습니다. 위에서는 ValueError의 값을 사용했지만 다른 형태의 메시지도 사용할 수 있습니다.

- KeyError
```python
>>> raise KeyError
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError
```

- ZeroDivisionError
```python
>>> raise ZeroDivisionError
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError
```

- FileNotFoundError
```python
>>> raise FileNotFoundError
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
FileNotFoundError
```
