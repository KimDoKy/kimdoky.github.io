---
layout: post
section-type: post
title: level 1.같은 숫자는 싫어
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 같은 숫자는 싫어

## 문제

no_continuous함수는 스트링 s를 매개변수로 입력받습니다.  

s의 글자들의 순서를 유지하면서, 글자들 중 연속적으로 나타나는 아이템은 제거된 배열(파이썬은 list)을 리턴하도록 함수를 완성하세요.  
예를들어 다음과 같이 동작하면 됩니다.  

- s가 '133303'이라면 ['1', '3', '0', '3']를 리턴
- s가 '47330'이라면 [4, 7, 3, 0]을 리턴


## 내 답안

```python
def no_continuous(s):
    # 함수를 완성하세요
    list = []
    before = 0
    for i in s:
        if before == i:
            pass
        else:
            list.append(i)
        before = i
    return list

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( no_continuous( "133303" ))
```

#### 다른 사람의 답안

```python
def no_continuous(s):
    a = []
    for i in s:
        if a[-1:] == [i]: continue
        a.append(i)
    return a

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( no_continuous( "133303" ))
----
def no_continuous(s):
    prev = '-1'
    ret = []
    for c in s:
        if c != prev:
            ret.append(c)
        prev = c
    # 함수를 완성하세요
    return ret

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( no_continuous( "133303" ))
```

### 배울점, 느낀점

- 의식의 흐름대로 코딩을 하니 내 코드가 이해하기 더 쉬운것 같다  
- list 다루는 방법을 더 공부해야한다.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/86>
