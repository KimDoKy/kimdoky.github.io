---
layout: post
section-type: post
title: map()과 filter(), enumerate()
category: python
tags: [ 'python' ]
---

많이 사용하지만 한번은 정리해야 할 함수들이 있다.

### map()
- map(function, iterable)  
iterable을 함수에 수행한 값들을 리턴한다.

### filter()
- filter(function, iterable)
iterable을 함수에 넣어 True인 값들을 리턴한다.

### enumerate()
- 리스트의 순서와 값을 리턴한다.
- 주로 for문과 같이 시용한다.

```python
>>> def tt(x):
...     return x + 3
...
>>> list(map(tt, [2,4,5,6]))
[5, 7, 8, 9]
>>> list(filter(tt, [2,3,4,5]))
[2, 3, 4, 5]
>>> def yy(x):
...     return x > 0
...
>>> list(filter(yy, [-1,2,4,-5,6,0]))
[2, 4, 6]
>>> def yy(x):
...     return x < 0
...
>>> list(filter(yy, [-1,2,4,-5,6,0]))
[-1, -5]
>>> for i, name in enumerate(['body', 'foo', 'bar']):
...     print(i, name)
...
0 body
1 foo
2 bar
```
