---
layout: post
section-type: post
title: level 1. checkPalindrome
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] checkPalindrome

## 문제
Given the string, check if it is a palindrome.
> A palindrome is a string that reads the same left-to-right and right-to-left.

**Example**

- For `inputString = "aabaa"`, the output should be
`checkPalindrome(inputString) = true`;
- For `inputString = "abac"`, the output should be
`checkPalindrome(inputString) = false`;
- For `inputString = "a"`, the output should be
`checkPalindrome(inputString) = true`.

**Input/Output**

- [time limit] 4000ms (py3)
- [input] string inputString

A non-empty string consisting of lowercase characters.

Guaranteed constraints:
`1 ≤ inputString.length ≤ 10`.

- [output] boolean

`true` if `inputString` is a palindrome, `false` otherwise.


## 내 답안

```python
def checkPalindrome(inputString):
    harf = len(inputString) // 2
    if len(inputString) == 1:
        return 1
    elif len(inputString) % 2 == 1:
        a = inputString[0:harf]
        b1 = inputString[harf+1:]
        b2 = b1[::-1]
        if a == b2:
            return 1
        else:
            return 0
    else:
        return 0
```

#### 다른 사람의 답안

```python
def checkPalindrome(inputString):
    return inputString == inputString[::-1]
```

### 배울점, 느낀점

- 토요일 스터디 할때 당시 머릿속으로 이론만 그려두고 구현하지 못하였는데 어느정도 구현해서 문제를 넘어갔다.
- 하지만 다른 사람이 풀어둔걸 보니 자괴감이..
- 세상엔 괴물이 많다.

#### 출처
> <https://codefights.com/>
