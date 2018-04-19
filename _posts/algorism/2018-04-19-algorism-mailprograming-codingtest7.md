---
layout: post
section-type: post
title: mailprograming - 코딩 테스트.7
category: algorism
tags: [ 'algorism' ]
---

주어진 string 에 모든 단어를 거꾸로 하시오.



예제)

```
Input: “abc 123 apple”

Output: “cba 321 elppa”
```

### 풀이

이 문제는 긴 string 을 각 단어로 나눈 다음, 각 단어를 거꾸로 하고, 모든 단어들을 합치면 풀 수 있습니다.

```
public String reverseString(String s) {
    String words[] = split(s);
    StringBuilder res = new StringBuilder();
    for (String word: words)
        res.append(reverse(word) + " ");
    return res.toString().trim();
}

public String[] split(String s) {
    ArrayList <String> words = new ArrayList <>();
    StringBuilder word = new StringBuilder();
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == ' ') {
            words.add(word.toString());
            word = new StringBuilder();
        } else
            word.append(s.charAt(i));
    }
    words.add(word.toString());
    return words.toArray(new String[words.size()]);
}

public String reverse(String s) {
    StringBuilder res = new StringBuilder();
    for (int i = 0; i < s.length(); i++)
        res.insert(0,s.charAt(i));
    return res.toString();
}
```

주로 인터뷰 중에는 split, reverse 등 과 같은 언어에 포함되어있는 함수를 쓰지 못하는 경우가 있습니다.


시간 복잡도: O(n), n = string 의 길이.

공간 복잡도: O(n)
