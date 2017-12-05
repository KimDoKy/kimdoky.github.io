---
layout: post
section-type: post
title: Python - Decorator
category: python
tags: [ 'python' ]
---

기존에 있는 함수의 기능에 추가적인 기능을 추가하여 사용할 수 있습니다.

사용할 함수보더 먼저 데코레이터가 정의되어 있어야 합니다.

parameter로 함수를 받아야 합니다.


### example

```Python
def print_args(fn):
    def inner_fn(a, b):
        print('args: ', a)
        result = fn(a,b)
        return result
    return inner_fn

@print_args
def multi(a,b):
    result = a * b
    print(result)
    return result

multi(3,5)

>>> args: 3
    15
```

### example2

```python
def base_10(fn):
    def wrap(x,y):
        return fn(x,y) + 10
    return wrap

@base_10
def mysum(a,b):
    return a+b

mysum(2,3)

>>> 15
```

### example3

데코레이터 함수자체에 인수를 선언하여 사용할 수도 있습니다.

```Python
def base(i):
    def inner_wrap(fn):
        def i_plus(x,y):
            return fn(x,y) + i
        return i_plus
    return inner_wrap

@base(10)
def mysum(a,b):
    return a+b

mysum(1,2)
>>> 13
```

### askDjango Quiz

<https://gist.github.com/KimDoKy/bf9d4902a9a3a5011ce62ad3e705c3eb>
