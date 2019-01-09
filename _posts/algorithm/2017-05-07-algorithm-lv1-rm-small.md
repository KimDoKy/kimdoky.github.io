---
layout: post
section-type: post
title: level 1. 제일 작은 수 제거하기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 제일 작은 수 제거하기

## 문제

rm_small함수는 list타입 변수 mylist을 매개변수로 입력받습니다.  
mylist 에서 가장 작은 수를 제거한 리스트를 리턴하고, mylist의 원소가 1개 이하인 경우는 []를 리턴하는 함수를 완성하세요.  
예를들어 mylist가 [4,3,2,1]인 경우는 [4,3,2]를 리턴 하고, [10, 8, 22]면 [10, 22]를 리턴 합니다.

## 내 답안

```python
def rm_small(mylist):
    # 함수를 완성하세요
    l = []
    for i in mylist:
        l.append(i)
    l.sort()
    m = l[0]
    mylist.remove(m)

    return mylist


# 아래는 테스트로 출력해 보기 위한 코드입니다.
my_list = [4, 3, 2, 1]
print("결과 {} ".format(rm_small(my_list)))

```

#### 다른 사람의 답안

```python
def rm_small(mylist):
    return [i for i in mylist if i > min(mylist)]

# 아래는 테스트로 출력해 보기 위한 코드입니다.
my_list = [4,3,2,1]
print("결과 {} ".format(rm_small(my_list)))
```

### 배울점, 느낀점

- min 과 컴프리헨션의 조합.
- 세상엔 고수가 많지만 아직 난 초보니까 다른 사람들 지식을 배우면 된다.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/121>
