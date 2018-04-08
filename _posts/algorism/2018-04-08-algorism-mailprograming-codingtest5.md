---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.5
category: algorism
tags: [ 'algorism' ]
---

정수 배열과 타겟 숫자가 주어지면, 합이 타겟값이 되는 두 원소의 인덱스를 찾으시오.

단, 시간복잡도 O(n) 여야 합니다.



예제)
```
Input: [2, 5, 6, 1, 10], 타겟 8

Output: [0, 2] // 배열[0] + 배열[2] = 8
```

---

### 풀이.

이 문제는 해쉬맵을 사용하여 원소 값과 원소 인덱스를 저장하면 쉽게 풀수 있습니다. 각 배열의 원소마다 (타겟 - 원소 값)이 해쉬맵에 있는지 확인하면 됩니다.

```python
int[] solution(int[] input, int target) {
	Map<int, int> map = new HashMap<>();
	for (int i = 0; i < input.length; i++) {
		int complement = target - input[i];
		if (map.containsKey(complement)) {
			return [map.get(complement), i];
		}
		map.put(input[i], i);
	}
	return [-1, -1]; // No solution
}
```

시간 복잡도: O(n). 해쉬맵의 containsKey 는 보편적으로 O(1). O(n)*O(1) = O(n).

공간 복잡도: O(n)


[매일프로그래밍](https://mailprogramming.com/)
