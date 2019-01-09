---
layout: post
section-type: post
title: algorithm - 기초. 사용자에게 값을 입력받아 직각 삼각형 만들기
category: algorithm
tags: [ 'algorithm' ]
---

사용자에게 값을 입력받은 후 그 값을 이용해서 직각 삼각형을 만듭니다.

> 도형 만들기는 반복문을 익히는 좋은 예제입니다.

### 풀이
1. 사용자에게 삼각형의 길이로 이용할 값을 입력받습니다.
2. 사용자에게 입력받은 값만큼 반복문을 실행시켜줍니다.  
첫 번째 for 문이 실행된 만큼 '* '을 출력합니다.

```python
>>> length = int(input("삼각형의 길이를 입력하세요: "))
삼각형의 길이를 입력하세요: 4
>>> for i in range(0, length):
...     p_str = ""
...     for j in range(0, i+1):
...         p_str += "*"
...     print(p_str)
...
*
**
***
****
>>>
```

2중 for문은 굉장히 효율이 안좋다.

```python
>>> for i in range(0, length):
...     p_str = "*"
...     print(p_str * (i+1))
...
*
**
***
****
>>>
```

같은 문제라도 구현하는 방식에 따라 효율이 달라집니다.
