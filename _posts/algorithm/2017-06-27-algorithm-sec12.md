---
layout: post
section-type: post
title: algorithm - 기초. 입력한 문장에서 존재하는 알파벳 모두 골라내내서 갯수 세기
category: algorithm
tags: [ 'algorithm' ]
---

### 풀이
1. 사용자에게 문장을 입력받습니다.
2. 알파벳을 저장할 때 사용할 리스트를 생성합니다.
3. 반복문을 이용해서 문자열의 요소를 한 개씩 검사합니다.
4. 요소를 한개씩 검사할때 마다 반복문을 이용해서 알파벳을 저장하는 리스트의 요소를 검색하면서 같은 요소가 있을 경우에는 변수를 True로 바꾸고 반복문을 멈춥니다.
5. 만약에 같은 요소가 존재하지 않을때에는 알파벳을 저장하는 리스트에 요소를 추가시켜 줍니다.

```python
>>> string = str(input("문장을 입력하세요: "))
문장을 입력하세요: chicken
>>>
>>> alphas = { }
>>> for i in string:
...     exist = False
...     for j in alphas.keys():
...         if i == j:
...             exist = True
...             alphas[j] += 1
...             break
...     if not exist:
...         alphas[i] = 1
...
>>> alphas
{'c': 2, 'n': 1, 'e': 1, 'h': 1, 'i': 1, 'k': 1}
>>>
```
