---
layout: post
section-type: post
title: algorithm - 기초. 사용자에게 값을 입력받아 좌우가 바뀐 직각 삼각형을 만들기
category: algorithm
tags: [ 'algorithm' ]
---

### 풀이
1. 사용자에게 삼각형의 길이를 이용할 값을 입력받습니다.
2. 입력받은 길이만큼 for문에 생성한 리스트를 넣습니다.
3. 임의의 변수와 하나씩 비교해서 임의의 변수보다 작을 경우 임의의 변수를 해강 리스트의 요소로 바꾸는 작업을 반복합니다.

```python
>>> length = int(input("삼각형의 길이를 입력하세요: "))
삼각형의 길이를 입력하세요: 4
>>> for i in range(0, length):
...     p_str = ""
...     for j in range(0, length):
...         if j >= length - (i + 1):
...             p_str += "*"
...         else:
...             p_str += " "
...     print(p_str)
...
   *
  **
 ***
****
>>>
```

```python
>>> for i in range(0, length):
...     print((" " * (length - (i+1))) + ("*" * (i+1)))
...
   *
  **
 ***
****
>>>
```
