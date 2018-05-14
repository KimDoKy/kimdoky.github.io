---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.9
category: algorism
tags: [ 'algorism' ]
---


정수 배열(int array)이 주어지면 0이 아닌 정수 순서를 유지하며 모든 0을 배열 오른쪽 끝으로 옮기시오. 단, 시간복잡도는 O(n), 공간복잡도는 O(1)여야 합니다.



예제)
```
Input: [0, 5, 0, 3, -1]

Output: [5, 3, -1, 0, 0]



Input: [3, 0, 3]

﻿Output: [3, 3, 0]
```

### 풀이

이 문제는 0을 오른쪽으로 옮기는것보다 0이 아닌 정수를 왼쪽으로 옮긴다고 생각하면 쉽게 풀수 있습니다.


```
void solve(int[] input) {
    int position = 0; // 0이 아닌 정수가 들어갈 곳
    for (int i = 0; i < input.length; i++) {
        if (input[i] != 0) {
            swap(input, i, position);
            position++;
        }
    }
}

void swap(int[] arr, int a, int b) {
    if (a == b) return;
    int temp = arr[a];
    arr[a] = arr[b];
    arr[b] = temp;
}
```

시간 복잡도: O(n)

공간 복잡도: O(1)
