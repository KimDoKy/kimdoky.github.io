---
layout: post
section-type: post
title: level 1. 정수제곱근판별하기
category: algorism
tags: [ 'algorism' ]
---

# [level 1] 정수제곱근판별하기

## 문제
nextSqaure함수는 정수 n을 매개변수로 입력받습니다.  
n이 임의의 정수 x의 제곱이라면 x+1의 제곱을 리턴하고, n이 임의의 정수 x의 제곱이 아니라면 'no'을 리턴하는 함수를 완성하세요.  
예를들어 n이 121이라면 이는 정수 11의 제곱이므로 (11+1)의 제곱인 144를 리턴하고, 3이라면 'no'을 리턴하면 됩니다.


## 내 답안

```python
import math

def nextSqure(n):
    # 함수를 완성하세요
    if int(math.sqrt(n)) == math.sqrt(n):
        return pow(math.sqrt(n)+1,2)
    else:
        return 'no'

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(nextSqure(121)));
```

#### 다른 사람의 답안

```python
def nextSqure(n):
    sqrt = n ** (1/2)

    if sqrt % 1 == 0:
        return (sqrt + 1) ** 2
    return 'no'

---

def nextSqure(n):
    sqrt = pow(n, 0.5)
    return pow(sqrt + 1, 2) if sqrt == int(sqrt) else 'no'

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(nextSqure(121)));
```

### 배울점, 느낀점

- 제곱근 라이브러리 math.sqrt()

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/119>
