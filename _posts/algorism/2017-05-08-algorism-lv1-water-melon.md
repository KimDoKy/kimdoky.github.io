---
layout: post
section-type: post
title: level 1. 수박수박수박수박수박수?
category: algorism
tags: [ 'algorism' ]
---

# [level 1] 수박수박수박수박수박수?

## 문제
water_melon함수는 정수 n을 매개변수로 입력받습니다.  
길이가 n이고, 수박수박수...와 같은 패턴을 유지하는 문자열을 리턴하도록 함수를 완성하세요.  

예를들어 n이 4이면 '수박수박'을 리턴하고 3이라면 '수박수'를 리턴하면 됩니다.

## 내 답안

```python
def water_melon(n):
    # 함수를 완성하세요.
    s = "수박" * n
    t = s[:n]
    return t


# 실행을 위한 테스트코드입니다.
print("n이 3인 경우: " + water_melon(3));
print("n이 4인 경우: " + water_melon(4));
```

#### 다른 사람의 답안

```python
def water_melon(n):
    s = "수박" * n
    return s[:n]


# 실행을 위한 테스트코드입니다.
print("n이 3인 경우: " + water_melon(3));
print("n이 4인 경우: " + water_melon(4));

----

def water_melon(n):
    return "수박"*(n//2) + "수"*(n%2)


# 실행을 위한 테스트코드입니다.
print("n이 3인 경우: " + water_melon(3));
print("n이 4인 경우: " + water_melon(4));

---

def water_melon(n):
    # 함수를 완성하세요.
    if n %2 == 0:
        return ("수박" *int(n/2))
    else:
        return ("수박"*int((n-1)/2) + "수")


# 실행을 위한 테스트코드입니다.
print("n이 3인 경우: " + water_melon(3))
print("n이 4인 경우: " + water_melon(4))
```

### 배울점, 느낀점

- 같은 문제라도 사람에 따라 푸는 방법이 모두 다름이 신기하다.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/108>
