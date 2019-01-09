---
layout: post
section-type: post
title: level 1. 서울에서 김서방찾기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 서울에서 김서방찾기

## 문제
findKim 함수(메소드)는 String형 배열 seoul을 매개변수로 받습니다.  

seoul의 element중 "Kim"의 위치 x를 찾아, "김서방은 x에 있다"는 String을 반환하세요.  
seoul에 "Kim"은 오직 한 번만 나타나며 잘못된 값이 입력되는 경우는 없습니다.  

## 내 답안

```python
def findKim(seoul):
    # 함수를 완성하세요
    kimIdx = seoul.index("Kim")
    return "김서방은 {}에 있다".format(kimIdx)


# 실행을 위한 테스트코드입니다.
print(findKim(["Queen", "Tod", "Kim"]))
```

#### 다른 사람의 답안

```python
def findKim(seoul):
    return "김서방은 {}에 있다".format(seoul.index('Kim'))


# 실행을 위한 테스트코드입니다.
print(findKim(["Queen", "Tod", "Kim"]))

---

def findKim(seoul):
    kimIdx = 0
    # 함수를 완성하세요
    for kimIdx in range(len(seoul)):
        if(seoul[kimIdx] == "Kim"):
            break

    return "김서방은 {}에 있다".format(kimIdx)


# 실행을 위한 테스트코드입니다.
print(findKim(["Queen", "Tod", "Kim"]))
```

### 배울점, 느낀점

- index와  find의 차이점.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/105>
