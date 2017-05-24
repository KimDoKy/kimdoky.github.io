---
layout: post
section-type: post
title: level 1. 문자열 내 p와 y의 개수
category: algorism
tags: [ 'algorism' ]
---

# [level 1] 문자열 내 p와 y의 개수

## 문제

numPY함수는 대문자와 소문자가 섞여있는 문자열 s를 매개변수로 입력받습니다.  
s에 'p'의 개수와 'y'의 개수를 비교해 같으면 True, 다르면 False를 리턴하도록 함수를 완성하세요. 'p', 'y' 모두 하나도 없는 경우는 항상 True를 리턴합니다.  
예를들어 s가 "pPoooyY"면 True를 리턴하고 "Pyy"라면 False를 리턴합니다.

## 내 답안

```python
def numPY(s):
    # 함수를 완성하세요
    num_p = 0
    num_y = 0
    for i in s:
        if i == 'p' or i == 'P':
            num_p = num_p + 1
        elif i == 'y' or i == 'Y':
            num_y = num_y + 1
    if num_p == num_y:
        return True
    else:
        return False

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( numPY("pPoooyY") )
print( numPY("Pyy") )
```

#### 다른 사람의 답안

```python
def numPY(s):
    # 함수를 완성하세요
    return s.lower().count('p') == s.lower().count('y')

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( numPY("pPoooyY") )
print( numPY("Pyy") )
----

def numPY(s):
    s = s.lower()
    if s.count("p") == s.count("y"):
        return True
    else:
        return False

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( numPY("pPoooyY") )
print( numPY("Pyy") )
```

### 배울점, 느낀점

- count()... python을 좀 더 공부해야겠다. 할것이 너무나도 많다. 문제를 풀때마다 모르고 있었던게 무엇인지 하나하나 나온다.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/97>
