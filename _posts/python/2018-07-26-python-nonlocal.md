---
layout: post
section-type: post
title: Python - 변수의 유효범위(global, nonlocal)
category: python
tags: [ 'python' ]
---

## 변수의 유효범위(global, nonlocal)


```python
In [1]: def first():
    ...:     a = 1
    ...:     print('first a: ', a, id(a))
    ...:     def second():
    ...:         print('second a', a, id(a))
    ...:         b =2
    ...:         print('second b', id(b))
    ...:         def third():
    ...:             global a
    ...:             print('third before global a ', a, id(a))
    ...:             nonlocal b
    ...:             a = a + 3
    ...:             print('third after global a ', a, id(a))
    ...:             print('third before nonlocal b' , b, id(b))
    ...:             b = b + 3
    ...:             print('third after nonlocal b ', b, id(b))
    ...:         third()
    ...:     second()
    ...:

In [2]: a = 1000

In [3]: b = 2000

In [4]: print('before a : ', a, id(a))
before a :  1000 56601440

In [5]: print('before b : ', b, id(b))
before b :  2000 56601664

In [6]: first()
first a:  1 1705629488
second a 1 1705629488
second b 1705629504
third before global a  1000 56601440
third after global a  1003 56602608
third before nonlocal b 2 1705629504
third after nonlocal b  5 1705629552

In [7]: print('after a :', a, id(a))
after a : 1003 56602608  # first() 함수안에서 global 로 선언하여 조작하였기 때문에 값이 변경되었다.

In [8]: print('after b :', b, id(b)) # nonlocal 선언으로 함수안의 상위 함수의 지역 변수를 조작하였기 때문에 함수 밖에 있는 지역 변수는 아무런 변화가 없다.
after b : 2000 56601664
```

> 함수 안에 정의된 지역 변수는 함수안의 함수에서 호출(참조)하면 정상 작동한다.  
하지만 함수안의 하위 함수에서 상위 함수의 지역 변수를 조작하려하면 `UnboundLovalError` 가 발생한다.


### 정리

- global : 함수 내에서 지역 변수 조작
- nonlocal : 하위 함수가 상위 함수의 변수를 조작
