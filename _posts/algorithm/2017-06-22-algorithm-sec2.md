---
layout: post
section-type: post
title: algorithm - 기초. 약수 구하기
category: algorithm
tags: [ 'algorithm' ]
---

### 풀이
1. 사용자로부터 약수를 구할 값을 입력받아 변수에 저장합니다.
2. 약수를 저장할 리스트를 생성해두고, 모든 수의 약수들을 자기 자신을 반으로 나눈 값을 넘지 않기 때문에 입력받은 값을 2로 나눕니다. 그리고 홀수를 입력받았을 경우를 대비해서 int로 변환시켜서 소수점을 없애줍니다.
3. 자기 자신을 2로 나눈 t_num값을 감소시키면서 입력받은 값과 나누어 떨어지는지 찾고 나누어쩔어지는 수이면 divisors 리스트에 한 개씩 추가시켜 줍니다.

```python
>>> number = int(input("1이상의 숫자를 입력하세요: "))
1이상의 숫자를 입력하세요: 99
>>>
>>> divisors = []
>>> t_num = int(number/2)
>>>
>>> while t_num > 1:
...     if number % t_num == 0:
...         divisors.append(t_num)
...     t_num -= 1
...
>>> divisors
[33, 11, 9, 3]
>>>
```
