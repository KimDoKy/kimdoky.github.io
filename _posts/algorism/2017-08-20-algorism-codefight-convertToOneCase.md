---
layout: post
section-type: post
title: CodeFight - convertToOneCase (단어 안에 대소문자 갯수 비교하여 대소문자 변경하기)
category: algorism
tags: [ 'algorism' ]
---

Alex often finds words that have letters both in upper and lower case, and they make him feel terrible. He's so tired of this that he decides to convert all these words to one letter case.

To choose the case, he calculates the number of lower case letters and the number of upper case letters. If these numbers have the same parity, Alex converts the word to lower case. Otherwise, he converts the word to upper case. Note that Alex doesn't convert words that only have letters that are one case.

Given the word that Alex wants to convert, return the modified word.

### Example

- For `word = "KeY"`, the output should be
`convertToOneCase(word) = "KEY"`.

This word contains `2` upper case letters and `1` lower case letter. `2` and `1` have the opposite parity, so this word should be converted to upper case.

For `word = "FOObar"`, the output should be
`convertToOneCase(word) = "foobar"`.

This word contains `3` letters in both upper and lower case. `3` and `3` have the same parity, so this word should be converted to lower case.

For `word = "chamomile"`, the output should be
`convertToOneCase(word) = "chamomile"`.

The letters in this word are only in one case, so Alex doesn't convert it.

### Input/Output

- **[time limit] 4000ms (py3)**
- **[input] string word**

The word that Alex wants to convert. It contains only English letters.

Guaranteed constraints:
`1 ≤ word.length ≤ 1000.`

- **[output] string**

The modified word.

---
## 나의 답안

```python
def convertToOneCase(word):
    upper_count = len(re.findall(r'[A-Z]', word))
    lower_count = len(re.findall(r'[a-z]', word))
    if upper_count == 0 or lower_count == 0:
        return word
    elif upper_count % 2 == lower_count % 2:
        return word.lower()
    else:
        return word.upper()
```
