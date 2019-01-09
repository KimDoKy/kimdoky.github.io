---
layout: post
section-type: post
title: algorithm - 기초. 팩토리얼 만들기
category: algorithm
tags: [ 'algorithm' ]
---

> 팩토리얼 : 1부터 주어진 숫자까지의 곱

### etc
```
입력:
0 ~ 10 사이의 숫자를 입력하세요: 5

출력:
120
```

### 풀이
1. 사용자에게 0에서부터 10까지의 숫자를 입력받도록 합니다.
2. 결과 값을 저장할 변수를 선언합니다.
3. 반복문응 통해서 1부터 입력숫자까지 반복해서 결과 값을 저장할 변수와 곱해줍니다.

```python
>>> num = 0
>>> while not (num < 11 and num > 0):
...     num = int(input("0 ~ 10 사이의 숫자를 입력하세요: "))
...
0 ~ 10 사이의 숫자를 입력하세요: 5
>>> result = 1
>>> for i in range(1, num + 1):
...     result *= i
...
>>> result
120
```
