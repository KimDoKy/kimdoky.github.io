---
layout: post
section-type: post
title: level 1. 문자열 다루기 기본
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 문자열 다루기 기본

## 문제

alpha_string46함수는 문자열 s를 매개변수로 입력받습니다.  
s의 길이가 4혹은 6이고, 숫자로만 구성되있는지 확인해주는 함수를 완성하세요.  
예를들어 s가 "a234"이면 False를 리턴하고 "1234"라면 True를 리턴하면 됩니다.

## 내 답안

```python
def alpha_string46(s):
    #함수를 완성하세요
    if len(s) == 4 or len(s) == 6:
        return s.isdigit()
    else:
        return False

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( alpha_string46("a234") )
print( alpha_string46("1234") )
```

#### 다른 사람의 답안

```python
def alpha_string46(s):
    return s.isdigit() and len(s) in [4, 6]

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( alpha_string46("a234") )
print( alpha_string46("1234") )
----

def alpha_string46(s):
    import re
    return bool(re.match("^(\d{4}|\d{6})$", s))

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( alpha_string46("a234") )
print( alpha_string46("1234") )

```

### 배울점, 느낀점

- 컴프리헨션.. isdigit() 숫자 판별

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/100>
