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

### 8.1.2 텍스트 파일 읽기: read(), readline(), readlines()

`read()` 함수를 인자 없이 호출하여 한 번에 전체 파일을 읽을 수 있다. 아주 큰 파일은 읽을 때 메모리가 많이 소비될 수 있기 때문에 주의해야 한다.

```Python
>>> fin = open('my_favorite_things', 'rt')
>>> poem = fin.read()
>>> fin.close()
>>> len(poem)
1331

# 한 번에 읽어들일 크기를 제한할 수 있다.
# 예로 100을 제한한다.
>>> poem = ''
>>> fin = open('my_favorite_things', 'rt')
>>> chunk = 100
>>> while True:
...     fragment = fin.read(chunk)
...     if not fragment:
...         break
...     poem += fragment
...
>>> fin.close()
>>> len(poem)
1331

# 파일을 다 읽어서 끝에 도달하면, read() 함수는 빈 문자열('')을 반환한다.

# readline() 함수를 사용하여 파일을 라인 단위로 읽을 수 있다.
# 파일의 각 라인을 poem 문자열에 추가하여 원본 파일의 문자열을 모두 저장하는 예
>>> poem = ''
>>> fin = open('my_favorite_things', 'rt')
>>> while True:
...     line = fin.readline()
...     if not line:
...         break
...     poem += line
...
>>> fin.close()
>>> len(poem)
1331
# 텍스트 파일의 빈 라인의 길이는 1('\n')이고, 이것을 True로 인식한다.
# 파일 읽기의 끝에 도달하면 read()와 마찮가지로 readline()함수도 False로 간주하는 빈 문자열을 반환한다.

# 텍스트 파일을 가장 읽기 쉬운 방법은 이터레이터를 사용하는 것
# 이터레이터는 한 번에 한 라인씩 반환한다.
>>> poem = ''
>>> fin = open('my_favorite_things', 'rt')
>>> for line in fin:
...     poem += line
...
>>> fin.close()
>>> len(poem)
1331

# readlines() 호출은 한 번에 모든 라인을 읽고, 한 라인으로 된 문자열들의 리스트를 반환한다.
>>> fin = open('my_favorite_things', 'rt')
>>> lines = fin.readlines()
>>> fin.close()
>>> print(len(lines), 'lines read')
37 lines read

>>> for line in lines:
...     print(line, end='')
My Favorite Things
Raindrops on roses
And whiskers on kittens
Bright copper kettles and warm woolen mittens
Brown paper packages tied up with strings
These are a few of my favorite things
Cream-colored ponies and crisp apple strudels
Doorbells and sleigh bells
And schnitzel with noodles
Wild geese that fly with the moon on their wings
These are a few of my favorite things
Girls in white dresses with blue satin sashes
Snowflakes that stay on my nose and eyelashes
Silver-white winters that melt into springs
These are a few of my favorite things
When the dog bites
When the bee stings
When I'm feeling sad
I simply remember my favorite things
And then I don't feel so bad
Raindrops on roses and whiskers on kittens
Bright copper kettles and warm woolen mittens
Brown paper packages tied up with strings
These are a few of my favorite things
Cream-colored ponies and crisp apple strudels
Doorbells and sleigh bells and schnitzel with noodles
Wild geese that fly with the moon on their wings
These are a few of my favorite things
Girls in white dresses with blue satin sashes
Snowflakes that stay on my nose and eyelashes
Silver white winters that melt into springs
These are a few of my favorite things
When the dog bites
When the bee stings
When I'm feeling sad
I simply remember my favorite things
And then I don't feel so bad
```

### 8.1.3 이진 파일 쓰기: write()

**모드** 에 `b`를 포함시키면 파일을 이진 모드로 연다. 이 경우 문자열 대신 바이트를 읽고 쓸 수 있다.

```Python
# 0에서 255까지 256바이트 값을 생성
>>> bdata = bytes(range(0, 256))
>>> len(bdata)
256

# 이진 모드로 파일을 열어서 한 번에 데이터 기록
>>> fout = open('bfile', 'wb')
>>> fout.write(bdata)
256
>>> fout.close()

# 텍스트 파일처럼 특정 단위로 이진 데이터 기록
>>> fout = open('bfile', 'wb')
>>> size = len(bdata)
>>> offset = 0
>>> chunk = 100
>>> while True:
...     if offset > size:
...         break
...     fout.write(bdata[offset:offset+chunk])
...     offset += chunk
...
100
100
56
>>> fout.close()
```

### 8.1.4 이진 파일 읽기: read()

파일을 `rb` 모드로 열기만 하면 된다.

```python
>>> fin = open('bfile', 'rb')
>>> bdata = fin.read()
>>> len(bdata)
256
>>> fin.close()
```

### 8.1.5 자동으로 파일 닫기: with

파일을 연 후 닫지 않았을 때, 파이썬은 이 파일이 더 이상 참조되지 않는다는 것을 확인한 뒤 파일을 닫는다. 즉, 명시적으로 닫지 않아도 함수가 끝날 때 자동으로 파일을 닫는다는 것을 의미한다. 하지만 오랫동안 작동하는 함수나 메인 프로그램에 파일을 열어 두었다면, 명시적으로 닫아야 한다.  

파이썬에는 파일을 영는 것과 같은 일을 수행하느느 **콘텍스트 메니저** 가 있다. 파일을 열때 `with 표현식 as 변수 형식`을 사용한다.

```Python
>>> with open('my_favorite_things', 'wt') as fout:
...     fout.write(poem)
...
```

콘텍스트 매니저 코드 블록의 코드 한 줄이 실행되고 나서 자동으로 파일을 닫아준다.

### 8.1.6 파일 위치 찾기: seek()

파일을 읽고 쓸 때, 파이썬은 파일에서 위치를 추적한다.  
`tell()`함수는 파일의 시작으로부터의 현재 오프셋을 바이트 단위로 반환한다.
`seek()`함수는 다른 바이트 오프셋으로 위치를 이동할 수 있다. 이 함수를 사용하면 마지막 바이트를 읽기 위해 처음부터 마지막까지 파일 전체를 읽지 않아도 된다. `seek()` 함수로 파일의 마지막 바이트를 추적하여 마지막 바이트만 읽을 수 있다.

```Python
>>> fin = open('bfile', 'rb')
>>> fin.tell()
0

# seek() 함수로 파일의 마지막에서 1바이트 전 위치로 이동
>>> fin.seek(255)
255

# 마지막 바이트 확인
>>> bdata = fin.read()
>>> len(bdata)
1
>>> bdata[0]
255
```

`seek()`함수는 현재 오프셋을 반환한다.  

`seek()` 함수의 형식은 `seek(offset, origin)`이다.

- origin이 0일 때(기본값), 시작 위치에서 offset 바이트 이동한다.
- origin이 1일 때, 현재 위치에서 offset 바이트 이동한다.
- origin이 2일 때, 마지막 위치에서 offset 바이트 전 위치로 이동한다.

이 값은 표준 os 모듈에 정의되어 있다.

```python
>>> import os
>>> os.SEEK_SET
0
>>> os.SEEK_CUR
1
>>> os.SEEK_END
2
```

다른 방법으로 마지막 바이트를 읽기.

```Python
>>> fin = open('bfile', 'rb')
# 파일의 마지막에서 1바이트 전 위치로 이동
>>> fin.seek(-1, 2)
255
>>> fin.tell()
255
# 마디막 바이트 확인
>>> bdata = fin.read()
>>> len(bdata)
1
>>> bdata[0]
255
# 파일에서 현재 위치로 이동
>>> fin = open('bfile', 'rb')
# 파일의 마지막에서 2바이트 전 위치로 이동
>>> fin.seek(254, 0)
254
>>> fin.tell()
254
# 1바이트 앞으로 이동
>>> fin.seek(1, 1)
255
>>> fin.tell()
255
# 파일의 마지막 바이트 확인
>>> bdata = fin.read()
>>> len(bdata)
1
>>> bdata[0]
255
```

이 함수들은 이진 파일에서 위치를 이동할 때 유용하게 쓰인다. 텍스트 파일에서도 사용가능하나, 아스키코드가 아니라면 오프셋을 계산하기 힘드므로 텍스트 파일은 비추.
