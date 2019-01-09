---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.3
category: algorithm
tags: [ 'algorithm' ]
---

정수 n이 주어지면, n개의 여는 괄호 "("와 n개의 닫는 괄호 ")"로 만들 수 있는 괄호 조합을 모두 구하시오. (시간 복잡도 제한 없습니다).



예제)
```
Input: 1

Output: ["()"]
```

```
Input: 2

Output: ["(())", "()()"]
```

```
Input: 3

Output: ["((()))", "(()())", "()(())", "(())()", "()()()"]
```

---

### 풀이.



주로 조합을 구하거나 답의 양이 많을 경우는 재귀함수를 사용하면 됩니다. empty string 부터 시작하여 “(“를 더하고 재귀함수를 부르고, “)”를 더하고 재귀함수를 부르면 됩니다. 여기서 중요한건, 현재 몇개의 여는 괄호를 사용하였는지와 몇개의 닫는 괄호를 사용하였는지 알아야합니다. 괄호조합을 왼쪽에서 오른쪽으로 읽을때, 닫는 괄호가 여는 괄호 개수보다 많으면 정당한 조합이 될 수 없습니다. 그러므로, 재귀함수에서 여는 괄호가 n보다 작을때 여는 괄호를 더한 재귀함수를 만들고, 닫는 괄호 개수가 여는 괄호 개수보다 작을때 닫는 괄호를 더한 재귀함수를 만들면 됩니다.



재귀함수에 주어진 문자열이 (n*2) 길이를 가진다면 알맞는 괄호 조합이니, 리스트에 더해주면 됩니다.


```python
List<String> parenthesisPairs(int n) {
  List<String> ans = new ArrayList();
  recurse(ans, "", 0, 0, n);
  return ans;
}

void recurse(List<String> ans, String cur, int open, int close, int n){
  if (str.length() == n * 2) {
    ans.add(cur);
    return;
  }
  if (open < n) {
    recurse(ans, cur + "(", open + 1, close, n);
  }
  if (close < open) {
    recurse(ans, cur + ")", open, close + 1, n);
  }
}
```


[매일프로그래밍](https://mailprogramming.com/)
