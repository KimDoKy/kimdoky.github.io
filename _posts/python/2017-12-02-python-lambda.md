---
layout: post
section-type: post
title: Python - lambda
category: python
tags: [ 'python' ]
---

lambda 함수는 변수를 할당하지 않고 사용하기 때문에, 간단히 사용할 수 있습니다.

## 사용법

```Python
함수명 = lambda 인수 : 로직
```

#### example

```Python
>>> fn = lambda x,y,z: x+y*z  # lambda으로 함수를 정의
>>> fn(2,3,4)
14
```

람다 함수는 iterator와 함께 사용할때 더 빛을 발합니다.

#### map() 함수

```python
map(function, iterable..)
```

```python
>>> list(map(lambda x:x+5, range(5)))
[5, 6, 7, 8, 9]
```

#### filter() 함수

```python
filter(function, iterable)
```

filter()는 function에서 처리되는 요소를 boolean 값으로 판단하여 True를 반환하는 요소만 반환합니다.

```Python
>>> list(filter(lambda x:x%2==0, range(10)))
[0, 2, 4, 6, 8]
```
