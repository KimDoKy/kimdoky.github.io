---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.4
category: algorithm
tags: [ 'algorithm' ]
---

정수(int)가 주어지면, 팰린드롬(palindrome)인지 알아내시오. 팰린드롬이란, 앞에서부터 읽으나 뒤에서부터 읽으나 같은 단어를 말합니다. 단, 정수를 문자열로 바꾸면 안됩니다.

예제)
```
Input: 12345

Output: False
```

```
Input: -101

Output: False
```

```
Input: 11111

Output: True
```

```
Input: 12421

﻿Output: True
```

---

### 풀이.

일단 엣지 케이스를 살펴봅니다. 정수가 마이너스면 팰린드롬이 될수 없습니다. -로 끝나는 숫자는 없으니까요. 그리고 0이 아닌 정수가 0으로 끝난다면 팰린드롬이 역시 될수 없습니다. 0으로 시작하는 숫자는 없으니까요.



이제 주어진 숫자를 전반과 후반으로 나누어 줍니다. 예를 들면 123321이 주어지면, 123이 전반이고 321이 후반입니다. 전반(123)이 거꾸로된 후반(123)과 값이 같다면 팰린드롬이겠죠. 정수를 전반과 거꾸로 된 후반으로 나누려면 while loop을 써서 정수의 일의 자리수를 뽑아낸후 정수를 10으로 나누면 정수의 각 숫자를 얻어낼수 있습니다.

```
123321 -> 12332, 1 -> 1233, 2 -> 123, 3.
```

이제 거꾸로 된 후반은 10으로 곱한뒤 뽑아낸 일의 자리 숫자를 더하면 됩니다.

```
0 + 1 -> 10 + 2 -> 120 + 3 = 123.
```

﻿이 방법을 거꾸로된 후반이 전반보다 크거나 같을때까지 반복하면 됩니다.



만약 주어진 숫자의 길이가 홀수라면, 거꾸로된 후반에서 1의 자리수를 없애주면 됩니다.
```
12321 -> 전반(12), 거꾸로된 후반(123)
```


전반 = input

거꾸로된 후반 = revertedHalf

```python
bool IsPalindrome(int input) {
    if(input < 0 || (input % 10 == 0 && input != 0)) {
        return false;
    }
    int revertedHalf = 0;
    while(input > revertedHalf) {
        revertedHalf = revertedHalf * 10 + input % 10;
        input /= 10;
    }
    return input == revertedHalf || input == revertedHalf/10;
}
```

시간 복잡도: O(log n) // 숫자의 길이만큼 반복됩니다.

공간 복잡도: O(1)


[매일프로그래밍](https://mailprogramming.com/)
