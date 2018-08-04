---
layout: post
section-type: post
title: tip. UnicodeDecodeError. 'utf-8' codec ..
category: tip
tags: [ 'tip' ]
---

# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xba in position 0: invalid start byte

같은 파이썬 코드라도 운영체제에 따라서 파일을 저장하는 인코딩은 차이가 있다.

윈도우는 기본적으로  `cp949`로 인코딩되고, 맥은 `utf-8`으로 인코딩된다.  
그러다보니 윈도우 환경에서 한글 파일을 저장하여 구동 확인까지 확인된 파이썬 파일이 맥 환경에서는 한글 파일을 읽어오는 과정에서 `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xba in position 0: invalid start byte` 에러가 발생하였다.

해결법은 간단하다. 한글 파일을 읽어올때 바이트로 읽어오고, 코드에서 활용할때 해당 방식으로 디코딩해주면 된다.

```python
with open('key_list.txt', 'rb') as file:
    for keyword in file:
        key_list.append(keyword.decode('cp949'))
```
