---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.8 반복자와 조합하여 처리하기
category: python
tags: [ 'python' ]
---
itertools는 반복자와 조합하여 다양한 처리를 구현할 수 있도록 각종 도구를 제공합니다.  

Python에서는 연속된 일련의 데이터를 반복자를 사용하여 표현합니다. 반복자는 단순한 인터페이스 객체로, 반복자의 __next__() 메서드를 호출하면 반복자의 다음 값을 반환하고 반환할 값이 존재하지 않을 때에는 StopIteration 예외가 발생합니다. Python에서는 반복문이나 데이터 전달 등에서 반복자를 이용합니다.

### 반복자 값을 합치기
iterable 객체의 모든 값을 더한 결과를 구할 등, 모든 요소를 합쳐 결과를 구할 때는 itertools.accumulate()를 사용합니다.

### accumulate() 함수

형식 | itertools.accumulate(iterable func=operator.add)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> func - 두 개의 인수를 취하는 함수를 지정한다. 생략하면 operator.add()가 되어, 요소를 맨 앞부터 순서대로 더한다.
반환값 | accumulate 반복자

다음 예에서는 함수로 두 개 인수의 곲을 반환하는 spam()을 지정하고 있으며, 리스트의 맨 앞 요소인 1이 처음 값이 되고, 다음 값은 spam(1,2), 마지막 값은 spam(2,3)이 반환됩니다.

### itertools.accumulate() 샘플 코드

```python
>>> import itertools
>>> def spam(left, right):
...     return left * right
...

>>> for v in itertools.accumulate([1,2,3], spam):
...     print(v)
...
1
2
6
```

itertools.accumulate()는 지정한 iterable 객체의 처음 값을 초깃값으로 하며, 이어서 초깃값과 iterable 객체 다음 값을 인수로서 함수를 호출하여 그 결과값을 반환합니다. 이 후의 값은 앞에서 함수를 호출한 결과값과 iterable 객체의 다음 값을 인수로서 다시 함수를 호출한 결과값이 됩니다.

### itertools.accumulate()의 동작

```python
>>> it = itertools.accumulate([1,2,3,4], spam)
>>> next(it)  # 처음 값은 iterable 객체의 맨 앞 값
1
>>> next(it)  # left:1 right:2 처음 값(=1) * 2 = 2
2
>>> next(it)  # left:2 right:3 처음 값(=2) * 3 = 6
6
>>> next(it)  # left:6 right:4 처음 값(=6) * 4 = 24
24

>>> next(it)  # iterable 객체 종료
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

## iterable 객체 연결하기
itertools.chain()은 여러 개의 iterable 객체를 연결한 반복자를 만듭니다.

### chain() 함수

형식 | itertools.chain(\*iterable)
---|---
인수 | iterable - iterable 객체를 지정한다.
반환값 | chain 반복자

### itertools.chain() 샘플 코드

```python
>>> it = itertools.chain([1,2,3], {'a','b','c'})  # 리스트와 집합을 열결
>>> for v in it:
...     print(v)
...
1
2
3
b
c
a
```

itertools.chain.from_iterable()은 연결할 iterable 객체들을 하나의 iterable 객체로 지정합니다.

### from_iterable() 함수

형식 | itertools.chain.from_iterable(iterable)
---|---
인수 | iterable - 연결할 대상을 반환하는 iterable 객체를 지정한다.
반환값 | chain 반복자

### itertools.chain.from_iterable() 샘플 코드

```python
>>> iters = ([1,2,3], {'a', 'b', 'c'})
>>> for c in itertools.chain.from_iterable(iters):
...     print(c)
...
1
2
3
b
c
a
```

## 값의 순열, 조합, 지적 구하기
