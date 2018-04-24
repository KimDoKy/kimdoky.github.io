---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.8
category: algorism
tags: [ 'algorism' ]
---

정수 배열(int array)이 주어지면 두번째로 큰 값을 프린트하시오.



예제)
```
Input: [10, 5, 4, 3, -1]

Output: 5



Input: [3, 3, 3]

Output: Does not exist.
```

### 풀이

이 문제는 가장 큰 값을 구하는 로직과 거의 똑같습니다. 가장 큰 값과 두번째 큰 값을 저장할 변수를 만들고 배열 원소들과 비교하면 됩니다. 중요한 엣지 케이스는 배열이 0 이나 1개의 원소를 가지고 있으면 두번째 큰 값이 존재 하지 않는것과 [3, 3, 3] 같은 경우 처럼 두번째로 큰 값은 존재 하지 않는겁니다. 이를 계산하기위해 두번째 큰 값을 저장할 변수를 Integer.MIN_VALUE로 두고 for루프가 끝난뒤 값이 변했는지 체크하면 됩니다.


```
void secondLargest(int[] arr) {
    int first, second;
    if (arr.length < 2) {
        print("두번째로 큰 값은 없습니다.");
        return;
    }
    first = second = Integer.MIN_VALUE;
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] > first) {
            second = first;
            first = arr[i];
        }
        else if (arr[i] > second && arr[i] != first) {
            second = arr[i];
        }
    }
    if (second == Integer.MIN_VALUE) {
        print("두번째로 큰 값은 없습니다.");
    }
    else {
        print(second);
    }
}
```

시간 복잡도: O(n)

공간 복잡도: O(1)
