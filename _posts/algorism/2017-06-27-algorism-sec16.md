---
layout: post
section-type: post
title: algorism - 기초. 단어 바꾸기(split함수 사용)
category: algorism
tags: [ 'algorism' ]
---

### 풀이
1. 사용자에게 '어려워요'라는 단어가 들어간 문장을 입력받습니다.
2. 문장을 공백을 기준으로 분리해서 리스트에 저장합니다.
3. 수정된 문자열을 저장할 변수를 선언합니다.
4. 반복문을 이용해서 단어가 저장된 리스트의 첫 번재 요소부터 '어려워요'라는 단어가 나오면 '쉬워요'라는 단어로 바꿔줍니다.
5. 리스트의 제일 마지막 요소를 검색하기 전에는 문자열에 리스트의 단어를 한 개씩 조합시킬 때 뒤에 공백을 추가시켜주고, 마지막 요소일 때는 공백을 추가시키지 않고 조합합니다.
6. 반복문이 실행이 완료되면 조합된 문자열을 확인합니다.

```python
>>> python = "파이썬은 아주 어려워요"
>>> list1 = python.split(" ")
>>> list1
['파이썬은', '아주', '어려워요']
>>> result_string = ""
>>> for s in range(0, len(list1)):
...     if list1[s] == '어려워요':
...         list1[s] = '쉬워요'
...     if s != len(list1) -1:
...         result_string += list1[s] + ' '
...     else:
...         result_string += list1[s]
...
>>> result_string
'파이썬은 아주 쉬워요'
```


코드 확인 예정
