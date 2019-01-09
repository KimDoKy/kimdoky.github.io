---
layout: post
section-type: post
title: algorithm - 기초. 여러가지 기본 정렬 알고리즘
category: algorithm
tags: [ 'algorithm' ]
---

**정렬 알고리즘**? 리스트에 있는 요소들이 일정한 순서대로 나열하는 알고리즘  

정렬 알고리즘은 알고리즘을 설명하기 위해 필요한 핵심 개념을 소개하는데 적합하기 때문에 기초 과정에서 자주 설명이 됩니다.  

선택, 삽입, 버블 정렬은 정렬이라는 과제를 해결하기 위한 알고리즘으로써 최상의 성능과 효율을 발휘하지는 못하지만 개념을 이해하는데 가장 쉽습니다.


## 선택 정렬
선택 정렬은 정렬 알고리즘 중에서 가장 간단한 알고리즘입니다. 선택 정렬은 요소 중에 최솟값을 가장 앞에 위치한 요소와 자리를 바꿔주는 방법으로 구현됩니다.

```python
>>> list1 = [4,2,3,8,7,1]
>>> for i in range(0, len(list1)):
...     min_i = i
...     for j in range(i+1, len(list1)):
...         if list1[min_i] > list1[j]:
...             min_i = j
...     list1[min_i], list1[i] = list1[i], list1[min_i]
...
>>> list1
[1, 2, 3, 4, 7, 8]
>>>
```


## 버블 정렬
탐색 정렬은 탐색 시작위치에 있는 요소의 바로 오른쪽 요소와 값을 비교하고 자리를 이동하는 정렬입니다.

```python
>>> list1 = [4,2,3,8,7,1]
>>> for i in range(0, len(list1)):
...     for j in range(0, len(list1) - 1):
...         if list1[j] > list1[j+1]:
...             list1[j], list1[j+1] = list1[j+1], list1[j]
...
>>> list1
[1, 2, 3, 4, 7, 8]
>>>
```

## 삽입 정렬
정렬된 리스트에 정렬할 리스트의 요소를 삽입하는 방식으로 구현됩니다. 중요한 점은 정렬된 리스트와 정렬할 리스트를 잘 파악하면 쉽게 구현이 가능합니다.

```python
>>> list1 = [4,2,3,8,7,1]
>>> for i in range(1, len(list1)):
...     j = i - 1
...     val = list1[i]
...     while list1[j] > val and j >= 0:
...         list1[j+1] = list1[j]
...         j -= 1
...     list1[j+1] = val
...
>>> list1
[1, 2, 3, 4, 7, 8]
>>>
```
