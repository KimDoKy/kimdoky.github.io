---
layout: post
section-type: post
title: Introducing Python - 흘러가는 데이터
category: python
tags: [ 'python' ]
---

# Chap8. 흘러가는 데이터

일반 파일, 구조화된 파일, 데이터베이스와 같이 특수 목적에 맞게 최적화된 데이터 스토리지의 각 특징을 다룸.

## 8.1 파일 입출력

데이터를 가장 간단하게 지속하려면 보통 파일(plain file)을 사용한다. 이것을 **플랫 파일(flat file)** 이라 부르기도 한다. 파일은 단지 **파일 이름(filename)** 으로 저장된 바이트 시퀀스다. 파일로부터 데이터를 **읽어서** 메모리에 적재하고, 메모리에서 파일로 데이터를 **쓴다.** 이러한 파일 연산은 유닉스 같은 운영체제를 모델로 만들어졌다.

#### 파일 열기

```Python
fileobj = open(filename, mode)
```

- fileobj은 `open()`에 의해 반환되는 파일 객체다.
- filename은 파일의 문자열 이름이다.
- mode는 파일 타입과 파일로 무엇을 할지 명시하는 문자열이다.
 - r : 파일 읽기
 - w : 파일 쓰기(파일이 없으면 생성하고, 있으면 덮어쓴다.)
 - x : 파일 쓰기(파일이 없을 경우만 해당)
 - a : 파일 추가(파일이 존재하면 파일의 끝에 추가)
  - t : 텍스트 타입(기본값)
  - b : 이진(binaty) 타입

파일을 열고 다 사용했다면, 파일을 **닫아야** 한다.

### 8.1.1 텍스트 파일 쓰기: write()

```Python
# 예제로 사용할 My Favorite Things 가사
>>> poem = '''My Favorite Things
... Raindrops on roses
... And whiskers on kittens
... Bright copper kettles and warm woolen mittens
... Brown paper packages tied up with strings
... These are a few of my favorite things
... Cream-colored ponies and crisp apple strudels
... Doorbells and sleigh bells
... And schnitzel with noodles
... Wild geese that fly with the moon on their wings
... These are a few of my favorite things
... Girls in white dresses with blue satin sashes
... Snowflakes that stay on my nose and eyelashes
... Silver-white winters that melt into springs
... These are a few of my favorite things
... When the dog bites
... When the bee stings
... When I'm feeling sad
... I simply remember my favorite things
... And then I don't feel so bad
... Raindrops on roses and whiskers on kittens
... Bright copper kettles and warm woolen mittens
... Brown paper packages tied up with strings
... These are a few of my favorite things
... Cream-colored ponies and crisp apple strudels
... Doorbells and sleigh bells and schnitzel with noodles
... Wild geese that fly with the moon on their wings
... These are a few of my favorite things
... Girls in white dresses with blue satin sashes
... Snowflakes that stay on my nose and eyelashes
... Silver white winters that melt into springs
... These are a few of my favorite things
... When the dog bites
... When the bee stings
... When I'm feeling sad
... I simply remember my favorite things
... And then I don't feel so bad
'''
>>> len(poem)
1331

# poem을 my_favorite_things 파일에 쓴다.
# write() 함수는 파일에 쓴 파이트 수를 반환한다.(쥬피터에서는 출력되지 않는다.)
>>> fout = open('my_favorite_things', 'wt')
>>> fout.write(poem)
1331
>>> fout.close()

# print() 함수로 텍스트 파일을 만들수 있다.
>>> fout = open('my_favorite_things', 'wt')
>>> print(poem, file=fout)
>>> fout.close()

# print()를 write()처럼 작동하려면 두 인자를 전달한다.
# sep(구분자, 기본값은 스페이스(''))
# end(문자열 끌, 기본값은 줄바꿈('\n'))
>>> fout = open('my_favorite_things', 'wt')
>>> print(poem, file=fout, sep='', end='')
>>> fout.close()

# 파일에 쓸 문자열이 크면 특정 단위로 나누어 파일에 쓴다.
>>> fout = open('my_favorite_things', 'wt')
>>> size = len(poem)
>>> offset = 0
>>> chunk = 100
>>> while True:
...     if offset > size:
...         break
...     fout.write(poem[offset:offset+chunk])
...     offset += chunk
...
100
100
100
100
100
100
100
100
100
100
100
100
100
31
>>> fout.close()

# 중요한 파일이라면, 모드 x를 사용하려 파일을 덮어쓰지 않도록 하다.
>>> fout = open('my_favorite_things', 'xt')
Traceback (most recent call last)
<ipython-input-14-97df53e484ee> in <module>()
----> 1 fout = open('my_favorite_things', 'xt')

FileExistsError: [Errno 17] File exists: 'my_favorite_things'

# 예외 처리 할 수 있다.
>>> try:
...     fout = open('my_favorite_things', 'xt')
...     fout.write('stomp stomp stomp')
... except FileExistsError:
...     print('relativity already exists!')
relativity already exists!
```
