---
layout: post
section-type: post
title: level 1. 자릿수더하기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 자릿수더하기

## 문제

sum_digit함수는 자연수를 전달 받아서 숫자의 각 자릿수의 합을 구해서 return합니다.  
예를들어 number = 123이면 1 + 2 + 3 = 6을 return하면 됩니다.  
sum_digit함수를 완성해보세요.

## 내 답안

```python
def sum_digit(number):
    '''number의 각 자릿수를 더해서 return하세요'''
    string = str(number)
    sum = 0
    for num in string:
        sum = sum + int(num)
    return sum
# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(sum_digit(123)));

```

#### 다른 사람의 답안

```python
def sum_digit(number):
    if number < 10:
        return number;
    return (number % 10) + sum_digit(number // 10)

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : {}".format(sum_digit(123)));
```

### 배울점, 느낀점

- 재귀함수. 들어는 봤지만 lv1에서 등장..

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/116>
