---
layout: post
section-type: post
title: Python - 기초 다지기 (lambda, comprehension)
category: python
tags: [ 'python' ]
---

## lambda

```python
표현식
(lambda 매개변수1, 매개변수2: 반환값)(인자1, 인자2)

(lambda x, y: x * y)(3,4)
12
```

## map() 활용

```python
list(map(lambda x, y: x * y, [3,4], [5,6]))
[15, 24]
```

## dictionary comprehension

```python
li = [('a',1), ('b',2), ('c',3)]

dict_li = {k : v for k, v in li}
{'a':1, 'b':2, 'c':3}
```

## list comprehension

```python
[n for n in range(3)]
[0,1,2]
```

### 문자열과의 조합으로 활용(구구단)

```python
gugudan = ['{} x {} = {}'.format(i, n, i*n) for i in range(1, 10) for n in range(1, 10)]

gugudan
['1 x 1 = 1',
 '1 x 2 = 2',
 '1 x 3 = 3',
.
.
.
 '9 x 7 = 63',
 '9 x 8 = 72',
 '9 x 9 = 81']
 ```
