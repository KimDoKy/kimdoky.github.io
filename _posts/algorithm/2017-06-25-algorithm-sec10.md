---
layout: post
section-type: post
title: algorithm - 기초. 입력한 문장에서 원하는 알파벳의 갯수 세기
category: algorithm
tags: [ 'algorithm' ]
---

## 풀이
1. 사용자에게 문장을 입력받아 변수에 저장합니다.
2. 사용자에게 찾기 원하는 알파벳을 입력받아 변수에 저장합니다.
3. 개수를 저장한 count 변수를 선언합니다. 반복문을 이용해서 문자열의 요소를 하나씩 검색하면서 사용자에게 입력받은 알파벳과 같을 경우 count의 값을 1씩 증가시킵니다.

```python
>>> string = str(input("문장을 입력하세요: "))
문장을 입력하세요: chicken
>>> alpha = str(input("개수를 셀 알파벳을 입력하세요: "))
개수를 셀 알파벳을 입력하세요: c
>>>
>>> count = 0
>>> for i in string:
...     if i == alpha:
...         count += 1
...
>>> print(count)
2
>>>
```
