---
layout: post
section-type: post
title: level 1. 스트링을 숫자로 바꾸기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 스트링을 숫자로 바꾸기

## 문제

strToInt 메소드는 String형 str을 매개변수로 받습니다.  
str을 숫자로 변환한 결과를 반환하도록 strToInt를 완성하세요.  
예를들어 str이 "1234"이면 1234를 반환하고, "-1234"이면 -1234를 반환하면 됩니다.  
str은 부호(+,-)와 숫자로만 구성되어 있고, 잘못된 값이 입력되는 경우는 없습니다.

## 내 답안

```python
def strToInt(str):
    #함수를 완성하세요
    return int(str)

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(strToInt("-1234"));
```

#### 다른 사람의 답안

```python
def strToInt(str):
    result = 0

    for idx, number in enumerate(str[::-1]):
        if number == '-':
            result *= -1
        else:
            result += int(number) * (10 ** idx)

    return result


# 아래는 테스트로 출력해 보기 위한 코드입니다.
print(strToInt("-1234"));
```

### 배울점, 느낀점

- 응?? 뭐지... 대부분 나랑 같이 풀었지만 위의 다른사람 답변은.. 그냥 삽질인가..

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/111>
