---
layout: post
section-type: post
title: algorithm - 기초. 최대 공약수 구하기
category: algorithm
tags: [ 'algorithm' ]
---

> 최대공약수 : 두 개 이상의 수에서 약수를 각각 구한 후 그 약수 중에서 공통된 것을 찾고 그 중에서 가장 큰 공통된 약수

### 풀이
1. 사용자로부터 최대 공약수를 구할 두 수를 입력받아 변수에 저장합니다.
2. 두 변수를 비교해서 더 작은 값을 찾고 그 값을 `t_num` 변수에 저장합니다.
3. `t_num`의 값을 하나씩 감소시키면서 입력받은 두 수와 딱 나누어 떨어지는 수를 찾습니다.
4. 딱 떨어지는 수를 찾으면 딱 떨어지는 수(최대공약수)를 출력하고, break를 이용해 반복문을 멈춥니다.

```python
>>> number1 = int(input("첫번째 숫자를 입력하세요: "))
첫번째 숫자를 입력하세요: 99
>>> number2 = int(input("두번째 숫자를 입력하세요: "))
두번째 숫자를 입력하세요: 66
>>> t_num = 0
>>> if number1 > number2:
...     t_num = number2
... else:
...     t_num = number1
...
>>> while t_num > 1:
...     if number1 % t_num == 0 and number2 % t_num == 0:
...         print("두 수의 최대공약수는 %d입니다." % t_num)
...         break
...     t_num -= 1
...
두 수의 최대공약수는 33입니다.
>>>
```
