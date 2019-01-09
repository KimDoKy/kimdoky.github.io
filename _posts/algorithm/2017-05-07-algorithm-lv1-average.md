---
layout: post
section-type: post
title: level 1. 평균구하기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 평균구하기

## 문제

def average(list):
함수를 완성해서 매개변수 list의 평균값을 return하도록 만들어 보세요.  
어떠한 크기의 list가 와도 평균값을 구할 수 있어야 합니다.

## 내 답안

```python
def average(list):
    # 함수를 완성해서 매개변수 list의 평균값을 return하도록 만들어 보세요.
    sum = 0
    for i in list:
        sum = sum + i
    return sum / len(list)

# 아래는 테스트로 출력해 보기 위한 코드입니다.
list = [5,3,4]
print("평균값 : {}".format(average(list)));
```

#### 다른 사람의 답안

```python
def average(list):
    return (sum(list) / len(list))

# 아래는 테스트로 출력해 보기 위한 코드입니다.
list = [5,3,4]
print("평균값 : {}".format(average(list)));
```

### 배울점, 느낀점

- 파이썬 라이브러리를 많이 공부 해야겠다. 라이브러리를 모르니까 코드가 더러워진다.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/128>
