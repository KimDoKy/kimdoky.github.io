---
layout: post
section-type: post
title: level 1. centuryFromYear
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] centuryFromYear

## 문제
Given a year, return the century it is in. The first century spans from the year 1 up to and including the year 100, the second - from the year 101 up to and including the year 200, etc.

**Example**

For `year = 1905`, the output should be
`centuryFromYear(year) = 20`;
For `year = 1700`, the output should be
`centuryFromYear(year) = 17`.

**Input/Output**

- [time limit] 4000ms (py3)
- [input] integer year

A positive integer, designating the year.

Guaranteed constraints:
`1 ≤ year ≤ 2005`.

- [output] integer

The number of the century the year is in.


## 내 답안

```python
def centuryFromYear(year):
    if year % 100 == 0:
        s = year // 100
    else:
        s = year // 100 + 1
    return s
```

#### 다른 사람의 답안

```python
def centuryFromYear(year):
    return (year+99) // 100
```

### 배울점, 느낀점

- 다른 사람들은 아이디어가 참 좋다.

#### 출처
> <https://codefights.com/>
