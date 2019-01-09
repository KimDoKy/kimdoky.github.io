---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.1
category: algorithm
tags: [ 'algorithm' ]
---

정수 배열(int array)가 주어지면 가장 큰 이어지는 원소들의 합을 구하시오. 단, 시간복잡도는 O(n).

예제}
```
Input: [-1, 3, -1, 5]

Output: 7 // 3 + (-1) + 5
```

```
Input: [-5, -3, -1]

Output: -1 // -1
```

```
Input: [2, 4, -2, -3, 8]

Output: 9 // 2 + 4 + (-2) + (-3) + 8
```
---
### 풀이.

이 문제는 두개의 정수 변수로 현재의 합(currentSum) 과 전체의 제일 큰 합(max Sum)을 저장해야 합니다. 각 원소마다 (currentSum + 원소) 값을 원소 값이랑 비교하고, 더 큰 값이 currentSum이 됩니다. maxSum은 currentSum 이 바뀔때마다 체크하여 제일 큰 값을 저장하면 됩니다.


```python
int solution(int[] arr) {
  int maxSum = arr[0];
  int currentSum = arr[0];
  for(int i = 1; i < arr.length; i++) {
    currentSum = Math.max(currentSum + arr[i], arr[i]);
    maxSum = Math.max(currentSum, maxSum);
  }
  return maxSum;
}
```

시간 복잡도: O(n)

공간 복잡도: O(1)

[매일프로그래밍](https://mailprogramming.com/)
