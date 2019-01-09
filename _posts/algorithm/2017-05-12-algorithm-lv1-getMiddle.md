---
layout: post
section-type: post
title: level 1.가운데 글자 가져오기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 가운데 글자 가져오기

## 문제

getMiddle메소드는 하나의 단어를 입력 받습니다.  
단어를 입력 받아서 가운데 글자를 반환하도록 getMiddle메소드를 만들어 보세요.  
단어의 길이가 짝수일경우 가운데 두글자를 반환하면 됩니다.  
예를들어 입력받은 단어가 power이라면 w를 반환하면 되고, 입력받은 단어가 test라면 es를 반환하면 됩니다.

## 내 답안

```python
def string_middle(str):
    # 함수를 완성하세요
    len_str = len(str)//2
    if len(str) % 2 == 0:
        return str[len_str-1:len_str+1]
    elif len(str) <= 0:
        return str
    else:
        return str[len_str]

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(string_middle("power"))
```

#### 다른 사람의 답안

```python
def string_middle(str):
    return str[(len(str)-1)//2:len(str)//2+1]

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(string_middle("power"))

----
def string_middle(str):
    a = len(str)
    if a % 2 == 0 :
        a = (a-2) / 2
    else :
        a = (a-1) / 2
    return str[int(a) : -int(a)]
# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(string_middle("power"))
```

### 배울점, 느낀점

- 파이썬 공부가 절실함...

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/83>
