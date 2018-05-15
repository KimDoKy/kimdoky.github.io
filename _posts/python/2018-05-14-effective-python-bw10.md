---
layout: post
section-type: post
title: EFFECTIVE PYTHON - range보다는 enumerate를 사용하자
category: python
tags: [ 'python' ]
---

내장 함수 `range`는 정수 집합을 순회(iterate)하는 루프를 실행할 때 유용하다.

```python
>>> random_bits = 0
>>> for i in range(64):
...     if randint(0, 1):
...         random_bits |= 1 << i
...
>>> random_bits
13560444895797892850
```

종종 리스트를 순회하거나 리스트의 현재 아이템의 인덱스를 알고 싶은 경우가 있다.

```python
for i in range(len(flavor_list)):
    flavor = flavor_list[i]
    print('%d: %s' % (i + 1, flavor))
```

위의 코드는 리스트의 길이를 알아내야 하고, 배열을 인덱스로 접근해야 하며, 읽기 불편하다.

파이썬은 이런 경우를 처리하기 위해 내장 함수 `enumerate`를 제공한다. `enumerate`는 지연 제너레이터(lazy generator)로 이터레이터를 감싼다. 이 제너레이터는 이터레이터에서 루프 인덱스와 담음 값을 한 쌍으로 가져와 넘겨준다.

```python
>>> flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
>>> for i, flavor in enumerate(flavor_list):
...     print('%d: %s' % (i + 1, flavor))
...
1: vanilla
2: chocolate
3: pecan
4: strawberry
```

`enumerate`에 세기 시작할 숫자를 지정할 수도 있다.

```python
for i, flavor in enumerate(flavor_list, 1):
    print('%d: %s' % (i, flavor))
```

## 핵심 정리

- `enumerate`는 이터레이터를 순회하면서 이터레이터에서 각 아이템의 인덱스를 얻어오는 간결한 문법을 제공한다.
- `range`로 루프를 실행하고 시퀀스에 인덱스로 접근하기보다는 `enumerate`를 사용하는게 좋다.
- `enumerate`에 두 번째 파라미터를 사용하면 세기 시작할 숫자를 지정할 수 있다(기본값은 0이다).
