---
layout: post
section-type: post
title: algorism - 기초. 단어 바꾸기(split함수 미사용)
category: algorism
tags: [ 'algorism' ]
---

사용자가 입력한 문장이나 단어를 미리 지정된 것으로 바꿔서 출력합니다.

### 풀이
1. 사용자에게 "어려워요"라는 단어가 들어간 문장을 입력받습니다.
2. 단어를 저장할 변수와, 문장을 단어별로 따로 분리해서 저장할 리스트를 선언합니다.
3. 반복문을 이용해서 입력받은 문자열의 0번 요소부터 공백인지 아닌지를 판별합니다. 만약 공백이 아닌 경우에는 단어를 저장할 변수에 요소를 하나씩 더해줍니다. 공백일 경우에는 리스트에 조합된 단어 변수를 추가시키고 변수를 초기화 시킵니다.
4. 3번 과정이 끝나면 최종적으로 문자열을 저장할 변수를 선언합니다.
5. 반복문을 이용해서 단어가 저장된 리스트의 첫 번째 요소부터 '어려워요'라는 단어가 나오면 '쉬워요'라는 단어로 바꿔줍니다.
6. 리스트의 제일 마지막 요소를 검색하기 전에는 문자열에 리스트의 단어를 한 개씩 조합시킬 때 뒤에 공백을 추가시켜주고, 마지막 요소일때는 공백을 추가시키지 않고 조합합니다.
7. 6번 반복문이 실행이 완료되면 조합된 문자열을 확인합니다.

```python
>>> python = "파이썬은 아주 어려워요"
>>> word = ""
>>> list1 = []
>>> result_string = ""
>>> for s in range(0, len(python)):
...     if python[s] != " ":
...         word += python[s]
...         if s == len(python) -1:
...             list1.append(word)
...     elif python[s] == " ":
...         list1.append(word)
...         word = ""
...         result_string = ""
...
>>> for s in range(0, len(list1)):
...     if list1[s] == "어려워요":
...         list1[s] = "쉬워요"
...     if s != len(list1) -1:
...         result_string += list1[s] + " "
...     else:
...         result_string += list1[s]
...
>>> result_string
'파이썬은 아주 쉬워요'
```
