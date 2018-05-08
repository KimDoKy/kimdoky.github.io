---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 한 슬라이스에 start, end, stride 를 함께 쓰지 말자
category: python
tags: [ 'python' ]
---

파이썬에는 `somelist[start:end:stride]`처럼 슬라이스의 스트라이트(간격)을 설정하는 문법도 있다.

```python
>>> a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
>>> odds = a[::2]
>>> evens = a[1::2]
>>> print(odds)
['red', 'yellow', 'blue']
>>> print(evens)
['orange', 'green', 'purple']
```

슬라이싱 문법의 stride 부분은 매우 혼란스러울 수 있다. stride가 음수인 경우 특히 그러하다.

```python
>>> a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
>>> a[::2]
['a', 'c', 'e', 'g']
>>> a[::-2]
['h', 'f', 'd', 'b']
>>> a[2::2]
['c', 'e', 'g']
>>> a[-2::-2]
['g', 'e', 'c', 'a']
>>> a[-2:2:-2]
['g', 'e']
>>> a[2:2:-2]
[]
```

이런 문제를 방지하려면 stride를 start, end 인덱스와 함께 사용하지 말아야 한다. stride를 사용해야 한다면 양수 값을 사용하고, start와 end 인덱스는 생략하는 것이 좋다. 함께 꼭 사용해야 한다면 stride를 적용한 결과를 변수에 할당하고, 이 변수를 슬라이스 한 결과를 다른 별수에 할당해서 사용하자.

```python
>>> b = a[::2] # ['a', 'c', 'e', 'g']
>>> c = b[1:-1] # ['c', 'e']
```

슬라이싱부터 하고 스트라이딩을 하면 첫 번째 연산 결과로 얕은 복사본이 나오는데 이 크기를 최대한 줄여야 한다. 프로그램에서 두 과정에 필요한 시간과 메모리가 충분하지 않다면 내장 모듈 `itertools`의 `islice` 메서드를 사용하자. `islice` 메서드는 start, end, stride에 음수 값을 허용하지 않는다.


## 핵심 정리

- 한 슬라이스에 start, end, stride를 지정하면 매우 혼란스러울 수 있다.
- 슬라이스에 start와 end 인덱스 없이 양수 stride 값을 사용하자. 음수 stride 값은 가능하면 피하는게 좋다.
- 한 슬라이스에 start, end, stride를 함께 사용하는 상황은 피하자. 파라미터 3개를 사용해야 한다면 할당 2개(하나는 슬라이스, 다른 하나는 스트라이드)를 사용하거나 내장 모듈 `itertools`의 `islice`를 사용하자.
