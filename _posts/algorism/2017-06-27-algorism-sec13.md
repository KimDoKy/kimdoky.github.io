---
layout: post
section-type: post
title: algorism - 기초. 리스트를 정렬하기
category: algorism
tags: [ 'algorism' ]
---

사용자에게 여러 숫자를 입력받은 후 오름차순으로 정렬해서 출력합니다.

### 풀이
1. while문을 이용해서 리스트 요소의 개수가 5개가 될 때까지 사용자에게 값을 입력받습니다.
2. for문을 중첩시켜서 리스트 안에 담긴 또다른 요소와 비교를 합니다.
3. 만약에 또 다른 요소와 비교를 했을 때 그 요소가 자기보다 크면 해당요소와 위치를 바꿉니다.

```python
>>> numbers = []
>>>
>>> while not len(numbers) == 5:
...     t_n = int(input("숫자를 입력하세요: "))
...     numbers.append(t_n)
...
숫자를 입력하세요: 25
숫자를 입력하세요: 34
숫자를 입력하세요: 2
숫자를 입력하세요: 53
숫자를 입력하세요: 15
>>>
>>> for n in range(0, len(numbers)):
...     for t_n in range(0, len(numbers)):
...         if numbers[n] < numbers[t_n]:
...             tmp = numbers[t_n]
...             numbers[t_n] = numbers[n]
...             numbers[n] = tmp
...
>>> numbers
[2, 15, 25, 34, 53]
>>>
```
