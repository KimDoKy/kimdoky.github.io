---
layout: post
section-type: post
title: level 1. 짝수와 홀수
category: algorism
tags: [ 'algorism' ]
---

# [level 1] 짝수와 홀수

## 문제

evenOrOdd 메소드는 int형 num을 매개변수로 받습니다.  
num이 짝수일 경우 "Even"을 반환하고 홀수인 경우 "Odd"를 반환하도록 evenOrOdd에 코드를 작성해 보세요.  
num은 0이상의 정수이며, num이 음수인 경우는 없습니다.

## 내 답안

```python
def evenOrOdd(num):
    s = ""
    if num % 2 == 0:
        s = "Even"
    else:
        s = "Odd"
    return s

#아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : " + evenOrOdd(3))
print("결과 : " + evenOrOdd(2))
```

#### 다른 사람의 답안

```python
def evenOrOdd(num):
    return num % 2 and "Odd" or "Even"

#아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : " + evenOrOdd(3))
print("결과 : " + evenOrOdd(2))
```

### 배울점, 느낀점

- 논리 연산을 이렇게 사용 할 수도 있구나..

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/124>
