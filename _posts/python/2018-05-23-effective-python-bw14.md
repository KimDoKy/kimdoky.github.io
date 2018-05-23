---
layout: post
section-type: post
title: EFFECTIVE PYTHON - None을 반환하기보다는 예외를 일으키자
category: python
tags: [ 'python' ]
---

# Chapter 2 : 함수
함수를 사용하면 가독성이 높아지고 코드를 더 이해하기 쉬워진다. 재사용이나 리팩토링도 가능하다.  

파이썬에서 제공하는 함수들은 함수의 목적을 더 분명하게 한다. 또한 불필요한 요소를 제거하고 호출자의 의도를 명료하게 보여주며, 찾기 어려운 미묘한 벅그를 상당히 줄여준다.

## None을 반환하기보다는 예외를 일으키자

파이썬에서 유틸리티 함수를 작성시 반환 값 None에는 특별한 의미가 있다. 예를 들어 어떤 숫자를 다른 숫자로 나누는 헬퍼 함수에서, 0으로 나누는 경우에는 결과가 정의되어 있지 않기 때문에 None을 반환하는게 자연스럽다.

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

이 함수를 사용하는 코드는 반환값을 다음과 같이 해석한다.

```python
result = divide(x, y)
if result is None:
    print('Invalid inputs')
```

하지만 분자가 0이라면 반환 값도 0이 되어 버린다. 그러면 if문과 같은 조건에서 결과를 평가할 때 문제가 될 수 있다. 오류인지 확인하려고 None 대신 False에 해당하는 값을 검사할 수도 있다.

```python
x, y = 0, 5
result = divide(x, y)
if not result:
    print('Invalid inputs')  # 잘못됨!
```

위 예는 None에 특별한 의미가 있을때 파이썬 코드에서 흔히 하는 실수이다. 이 점이 함수에서 None을 반환하면 오류가 일어나기 쉬운 이유이다.  

이런 오류가 일어나는 상황을 줄이는 방법은 두 가지가 있다.

1. 반환 값을 두개로 나눠서 튜플에 담는 것이다.  
튜플의 첫 번째 부분은 작업이 성공했는지 실패했는지를 알려준다. 두번째 부분은 계산된 실제 결과다.

```python
def division(a, b):
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None
```
이 함수를 호출하는 쪽에서 튜플로 풀어야 한다. 나눗셈의 결과만 얻는게 아니라 튜플에 들어 있는 상태 부분까지 고려해야 한다.

```python
success, result = divide(x, y)
if not success:
    print('Invalid inputs')
```
문제는 호출자가 (파이썬에선 사용하지 않을 변수에 언더 바(`_`)를 붙이는 관례를 사용해서) 튜플의 첫번째 부분을 쉽게 무시할 수 있다. 얼핏 보기엔 잘못된 것처럼 보이지 않지만, 그냥 None을 반환하는 것만큼 나쁘다.

```python
_, result = divide(x, y)
if not result:
    print('Invalid inputs')
```

2. 절대로 None을 반환하지 않는 것이다.  
대신에 호출하는 쪽에 예외를 일으켜서 호출하는 쪽에서 그 예외를 처리하게 하는 것이다. 여기에서는 입력 값이 잘못됐을을 알리기 위해 ZeroDivisionError 대신에 ValueError로 변경하였다.

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e
```
이제 호출하는 쪽에서는 잘못된 입력에 대한 예외를 처리해야 한다. 호출하는 쪽에서 더는 함수의 반환 값을 조건식으로 검사할 필요가 없다. 함수가 예외를 일으키지 않는다면 반환 값은 문제가 없다.  

예외를 처리하는 코드도 깔끔해진다.

```python
>>> x, y = 5, 2
>>> try:
...     result = divide(x, y)
... except ValueError:
...     print('Invalid inputs')
... else:
...     print('Result is %.1f' % result)
...
Result is 2.5
```

## 핵심 정리

- 특별한 의미를 나타내려고 None을 반환하는 함수가 오류를 일으키기 쉬운 이유는 None이나 다른 값(0이나 빈 문자열)이 조건식에서 False로 평가되기 때문이다.
- 특별한 상황을 알릴 때 None을 반환하는 대신에 예외를 일으키자. 문서화가 되어 있다면 호출하는 코드에서 예외를 적절하게 처리할 것이라고 기대할 수 있다.
