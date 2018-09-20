---
layout: post
section-type: post
title: 컴퓨터 공학 - 제귀함수
category: algorism
tags: [ 'algorism' ]
---

- 재귀 함수(recursive function) : 자기 자신을 계속 호출

## 팩토리얼(factorial)
- 어떤 수의 계승으로 1부터 어떤 수까지의 곱
- ex. 3의 계승은 3 * 2 * 1. 이를 3! 라고 표현하고 '3팩토리얼'이라고 읽음
 - n! = (n-1)! * n   ex. 3! = 2! * n
 - n = 0 or 1 이면 n! = 1

```python
def factorial(n):
    return factorial(n-1) * n

if __name__ == '__main__':
    n = 3
    res = factorial(n)
    print("The factorial of {} is {}".format(n, res))
```

실행 결과
```
RecursionError: maximum recursion depth exceeded
```
재귀함수가 계속 자기 자신을 호출하여 스택 프레임이 계속 생성되고 스택 오버플로(stack overflow)가 발생.
팩토리얼에는 탈출 조건이 필요. 탈출 조건은 n이 0이나 1일 때 값이 1이라는 것

```python
def factorial(n):
    # 탈출 조건
    if n <= 1:
        return 1
    return factorial(n-1) * n

if __name__ == '__main__':
    n = 3
    res = factorial(n)
    print("The factorial of {} is {}".format(n, res))
```

실행 결과

```
The factorial of 3 is 6
```

## 피보나치 수(fibonacci)
- 0과 1부터 시작하여 다음 수가 앞의 두 수를 더한 값이 되는 수열

```
0,1,1,2,3,5,8,13,21,34,...
```

```python
def fibonacci(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    return fibonacci(n-2) + fibonacci(n-1)

if __name__ == '__main__':
    n = 10
    for i in range(1, n+1):
        print(fibonacci(i), end = '  ')
```

실행결과
```
0  1  1  2  3  5  8  13  21  34  %
```

> 컴퓨터 사이언스 부트캠프 with 파이썬 중..
