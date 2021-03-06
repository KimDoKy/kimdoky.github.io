---
layout: post
section-type: post
title: algorithm - 기초. 비만도 측정하기
category: algorithm
tags: [ 'algorithm' ]
---

> 비만도 : 표준 체중대비 사용자가 입력한 체중의 비율

### 풀이
1. 사용자에게 남자인지 여자인지를 판별하기 위한 값을 입력받고 변수에 저장합니다.
2. 사용자에게 키를 입력받고 변수에 저장합니다.
3. 사용자에게 몸무게를 입력받고 변수에 저장합니다.
4. 표준체중을 구하기 위한 변수를 선언하고, 남자면(몸무게 = 100) * 0.9로 계산하고 여자면(몸무게 - 100) * 0.85로 계산해서 선언한 변수에 저장합니다.
5. 비만도를 저장하기 위한 변수를 선언하고(몸무게 - 표준체중)/표준체중 * 100으로 계산합니다.
6. 구해진 비만도와 표준체중을 출력합니다.

```python
>>> sex = 0
>>> while not sex:
...     sex = int(input("남자는 1, 여자는 2를 입력하세요: "))
...
남자는 1, 여자는 2를 입력하세요: 1
>>> height = int(input("키를 입력하세요 "))
키를 입력하세요 173
>>> weight = int(input("몸무게를 입력하세요 "))
몸무게를 입력하세요 68
>>> s_weight = 0
>>> if sex == 1:
...     s_weight = (height - 100) * 0.9
... else:
...     s_weight = (height - 100) * 0.85
...
>>> o_weight = (weight - s_weight) / s_weight * 100
>>> print('표준체중 : %f' % s_weight)
표준체중 : 65.700000
>>> print('비만도 : %f' % o_weight)
 비만도 : 3.500761
>>>
```
