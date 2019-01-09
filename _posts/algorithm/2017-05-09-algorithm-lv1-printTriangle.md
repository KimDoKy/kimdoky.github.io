---
layout: post
section-type: post
title: level 1. 삼각형출력하기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 삼각형출력하기

## 문제

printTriangle 메소드는 양의 정수 num을 매개변수로 입력받습니다.  
다음을 참고해 *(별)로 높이가 num인 삼각형을 문자열로 리턴하는 printTriangle 메소드를 완성하세요.  
printTriangle이 return하는 String은 개행문자('\n')로 끝나야 합니다.

높이가 3일때

```
*
**
***
```
높이가 5일때

```
*
**
***
****
*****
```

## 내 답안

```python
def printTriangle(num):
    s = ""
    #함수를 완성하세요
    for i in range(1,num+1):
        s = s + ("*" * i) + "\n"
    return s

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( printTriangle(3) )
```

#### 다른 사람의 답안

```python
def printTriangle(num):
    return ''.join(['*'*i + '\n' for i in range(1,num+1)])


# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( printTriangle(3) )
----

def printTriangle(num):
    s = ""
    #함수를 완성하세요
    for temp1 in range(num):
        for temp2 in range(temp1+1):
            s += "*"
        s += "\n"
    return s
# 아래는 테스트로 출력해 보기 위한 코드입니다.
print( printTriangle(3) )

```

### 배울점, 느낀점

- 컴프리헨션.. 연습해야하는데... 다른 사람의 2중 for문 보다는...하하

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/102>
