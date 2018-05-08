---
layout: post
section-type: post
title: EFFECTIVE PYTHON - map과 filter 대신 리스트 컴프리헨션을 사용하자
category: python
tags: [ 'python' ]
---

### 리스트 컴프리헨션(list comprehensioin: 리스트 함축 표현식)

```python
# 리스트에 있는 각 숫자의 제곱을 계산
>>> a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> squares = [x**2 for x in a]
>>> print(squares)
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

인수가 하나뿐인 함수를 적용하는 것이 아니라면, 간단한 연산에는 리스트 컴프리헨션이 내장 함수 `map` 보다 명확하다. `map`을 쓰려면 계산에 필요한 `lambda` 함수까지 사용해야 해서 깔끔하지 못하다.

```python
>>> squares = map(lambda x: x ** 2, a)
```

리스트 컴프리헨션을 사용하면 입력 리스트에 있는 아이템을 간편하게 걸러내서 그에 대응하는 출력을 결과에서 삭제할 수 있다.

```python
# 2로 나누어 떨어지는 숫자의 제곱만 계산
>>> even_squres = [x**2 for x in a if x % 2 == 0]
>>> print(even_squres)
[4, 16, 36, 64, 100]
```

내장 함수 `filter`를 `map`과 연계해서 사용해도 같은 결과를 얻을 수는 있지만 읽기 어렵다.

```python
>>> alt = map(lambda x: x**2, filter(lambda x: x % 2 == 0, a))
>>> assert even_squres == list(alt)
```

딕셔너리와 세트에도 리스트 컴프리헨션에 해당하는 문법이 있다. 컴프리헨션 문법을 사용하면 알고리즘을 작성할 때 파생되는 자료 구조를 쉽게 생성할 수 있다.

```python
>>> chile_ranks = {'ghost': 1, 'habanero': 2, 'cayenne': 3}
>>> rank_dict = {rank: name for name, rank in chile_ranks.items()}
>>> chile_len_set = {len(name) for name in rank_dict.values()}
>>> print(rank_dict)
{1: 'ghost', 2: 'habanero', 3: 'cayenne'}
>>> print(chile_len_set)
{8, 5, 7}
```

## 핵심 정리

- 리스트 컴프리헨션은 추가적인 `lambda` 표현식이 필요 없어서 내장 함수인 `map`이나 `filter`를 사용하는 것보다 명확하다.
- 리스트 컴프리헨션을 사용하면 입력 리스트에서 아이템을 간단히 건너 뛸 수 있다. `map`으로는 `filter`르 사용하지 않고서는 이런 작업을 못한다.
- 딕셔너리와 세트도 컴프리헨션 표현식을 지원한다.
