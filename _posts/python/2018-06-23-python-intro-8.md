---
layout: post
section-type: post
title: Introducing Python - 흘러가는 데이터
category: python
tags: [ 'python' ]
published: false
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
>>> os.SEEK_SET  # 파일의 시작
0
>>> os.SEEK_CUR  # 현재 위치
1
>>> os.SEEK_END  # 파일의 끝
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

## 8.2 구조화된 텍스트 파일

간단한 텍스트 파일은 라인으로 구성되어 있다. 어떤 프로그램에서 데이터를 저장하거나 이를 다른 프로그램으로 보낼 때는, 구조화된 데이터가 필요하다.  

구조화된 텍스트 파일 형식은 많지만 그 중 몇 가지이다.

- CSV(Comma-Separated Value) : 탭('\t'), 콤마(','), 수직 바('|')와 같은 구분자(separator)로 사용한다.
- XML(eXtensible markup), HTML(HyperText Markup Language) : 태그를 '>'와 '<'로 둘러싼다.
- JSON(JavaScript Object Notaion) : 구두점을 사용한다.
- YAML(YAML Ain't Markup Language) : 들여쓰기를 사용한다.
- 프로그램 설정 파일과 같은 여러 가지 형식을 사용한다.

### 8.2.1 CSV

구조된 파일은 스프레드시트와 데이터베이스의 데이터 교환 형식으로 자주 사용된다.  
수동으로 CSV 파일을 한 번에 한 라인씩 읽어서, 콤마로 구분된 필드를 분리할 수 있다.  
그 결과를 리스트와 딕셔너리 같은 자료구조에 넣을 수 있다.  
파일 구문 분석이 생각보다 복잡할 수 있기 때문에 **표준 csv 모듈** 사용을 권장한다.

- 어떤 것은 콤마 대신 수직 바('|')나 탭('\t') 문자를 사용한다.
- 어떤 것을 이스케이프 시퀀스를 사용한다. 만일 필드 내에 구분자를 포함하고 있다면, 전체 필드는 인용 부호로 둘러싸여 있거나 일부 이스케이프 문자가 앞에 올 수 있다.
- 파일은 운영체제에 따라 줄바꿈 문자가 다를수 있다. 유닉스는 '\n', 마이크로소프트는 '\r\n', 애플은 '\n'을 사용한다.
- 열(column)이름이 첫 번째 라인에 올 수 있다.

```Python
# 리스트를 읽어서 CSV 형식의 파일을 작성
>>> import csv
>>> villains = [
...     ['Doctor', 'No'],
...     ['Rosa', 'Klebb'],
...     ['Mister', 'Big'],
...     ['Auric', 'Goldfinger'],
...     ['Ernst', 'Blofeld'],
... ]
...
>>> with open('villains', 'wt') as fout:
...     csvout = csv.writer(fout)
...     csvout.writerows(villains)
```

```
Doctor,No
Rosa,Klebb
Mister,Big
Auric,Goldfinger
Ernst,Blofeld
```
위 내용의 villains 파일이 생성한다.

```Python
# 다시 파일을 읽기
>>> import csv
>>> with open('villains', 'rt') as fin:  # 콘텍스트 매니저
...     cin = csv.reader(fin)
...     villains = [row for row in cin]  # 리스트 컴프리헨션
...
>>> print(villains)
[['Doctor', 'No'], ['Rosa', 'Klebb'], ['Mister', 'Big'], ['Auric', 'Goldfinger'], ['Ernst', 'Blofeld']]
```

`reader()`함수를 사용하여 CSV 형식의 파일을 쉽게 읽을 수 있다. 이 함수는 for 문에서 cin 객체의 행을 추출할 수 있게 한다.

기본값으로 `reader()`와 `writer()`함수를 사용하면, 열을 콤마로 나누어지고, 행은 줄바꿈 문자로 나누어진다.  

리스트의 리스트가 아닌 딕셔너리의 리스트로 데이터를 만들 수 있다.

```python
# DictReader()함수를 사용하여 열 이름을 지정
>>> import csv
>>> with open('villains', 'rt') as fin:
...     cin = csv.DictReader(fin, fieldnames=['first', 'last'])
...     villains = [row for row in cin]
...
>>> print(villains)
[OrderedDict([('first', 'Doctor'), ('last', 'No')]), OrderedDict([('first', 'Rosa'), ('last', 'Klebb')]), OrderedDict([('first', 'Mister'), ('last', 'Big')]), OrderedDict([('first', 'Auric'), ('last', 'Goldfinger')]), OrderedDict([('first', 'Ernst'), ('last', 'Blofeld')])]

# DictWriter()함수를 사용하여 CSV 파일을 재작성
# CSV 파일의 첫 라인에 열 이름을 사용하기 위해 writeheader() 함수를 호출
# 헤더 라인과 함께 villains 파일을 생성
>>> import csv
>>> villains = [
...     {'first': 'Docter', 'last':'No'},
...     {'first': 'Rosa', 'last':'Klebb'},
...     {'first': 'Mister', 'last':'Big'},
...     {'first': 'Auric', 'last':'Goldfinger'},
...     {'first': 'Ernst', 'last':'Blofild'},
... ]
...
>>> with open('villains', 'wt') as fout:
...     cout = csv.DictWriter(fout, ['first', 'last'])
...     cout.writeheader()
...     cout.writerows(villains)
first,last
Docter,No
Rosa,Klebb
Mister,Big
Auric,Goldfinger
Ernst,Blofild
```

```python
# DictReader() 호출에서 필드 이름의 인자를 빼면, 첫 번째 라인(first, last)의 값은 딕셔너리의 키로 사용된다.
>>> import csv
>>> with open('villains', 'rt') as fin:
...     cin = csv.DictReader(fin)
...     villains = [row for row in cin]
...
>>> print(villains)
[OrderedDict([('first', 'Docter'), ('last', 'No')]), OrderedDict([('first', 'Rosa'), ('last', 'Klebb')]), OrderedDict([('first', 'Mister'), ('last', 'Big')]), OrderedDict([('first', 'Auric'), ('last', 'Goldfinger')]), OrderedDict([('first', 'Ernst'), ('last', 'Blofild')])]
```

### 8.2.2 XML

구분된 파일은 행과 열의 2차원 구조로 구성되어 있다. 프로그램간에 자료구조를 교환하기 위해 텍스트를 계층구조, 시퀀스, 셋 또는 다른 자료구조로 인코딩해야 한다.

XML은 가장 잘 알려진 **마크업** 형식이다. XML은 데이터를 구분하기 위해 **태그** 를 사용한다.

```XML
<?xml version="1.0"?>
<menu>
 <breakfast hours="7-11">
  <item price="$6.00">breakfast burritos</item>
  <item price="$4.00">pancakes</item>
 </breakfast>
 <lunch hours="11-3">
  <item price="$5.00">hamburger</item>
 </lunch>
 <dinner hours="3-10">
  <item price="8.00">spaghetti</item>
 </dinner>
</menu>
```

##### XML의 중요한 특징

- 태그는 `<` 문자로 시작한다. menu.xml의 태그는 menu, breakfast, lunch, dinner, item이다.
- 공백은 무시된다.
- 일반적으로 `<menu>`와 같은 시작 태그는 다른 내용이 따라온다. 그러고 나서 `</menu>`와 같은 끝 태그가 매칭된다.
- 태그 안에 태그를 중첩할 수 있다. 예제에서 item 태그틑 breakfast, lunch, dinner 태그의 자식이다. 또한 이 태그들은 `menu` 태그의 자식이다.
- 옵션 속성은 시작 태그에 나올 수 있다. 예제의 price는 item의 속성이다.
- 태그는 값을 가질 수 있다. 예제의 각 item은 값을 가진다. 예를 들어 두 번째 breakfast의 item은 pancakes 값을 가진다.
- thing이라는 태그에 값이나 자식이 없다면, `<thing></thing>`과 같은 시작 태그와 끝 태그가 아닌 `</thing>`과 같은 단일 태그로 표현할 수 있다.
- 속성, 값, 자식 태그의 데이터를 어디에 넣을 것인가에 대한 선택은 다소 임의적이다. 예를 들어 마지막 item 태그를 `<item price="$8.00" food="spaghetti"/>`형식으로 쓸 수 있다.

XML은 데이터 피드(data feed)와 메시지 전송에 많이 사용된다. 그리고 RSS(Rich Site Summary)와 아톰(atom)같은 하위 형식이 있다. 일부는 금융 분야에 같은 특화된 XML 형식을 가진다.

XML의 두드러진 유연성은 접근법과 능력이 다른 여러 파이썬 라이브러리에 영향을 미쳤다.  

##### XML을 하싱하는 간단한 방법 : ElementTree 모듈

```Python
# menu.xml을 파싱하여 태그와 속성을 출력하는 작은 프로그램
>>> import xml.etree.ElementTree as et
>>> tree = et.ElementTree(file='menu.xml')
>>> root = tree.getroot()
>>> root.tag
'menu'
>>> for child in root:
...     print('tag:', child.tag, 'attributes:', child.attrib)
...     for grandchild in child:
...         print('\ttag:', grandchild.tag, 'attributes:', grandchild.attrib)
...
tag: breakfast attributes: {'hours': '7-11'}
	tag: item attributes: {'price': '$6.00'}
	tag: item attributes: {'price': '$4.00'}
tag: lunch attributes: {'hours': '11-3'}
	tag: item attributes: {'price': '$5.00'}
tag: dinner attributes: {'hours': '3-10'}
	tag: item attributes: {'price': '8.00'}
>>> len(root)  # menu의 하위 태그 수
3
>>> len(root[0])  # breakfast의 item 수
2
```

중첩된 리스트와 각 요소에 대해 tag는 태그 문자열이고, attrib는 속성의 딕셔너리다. ElementTree 모듈은 XML에서 파생된 데이터를 검색하고 수정할 수 있는 다양한 방법을 제공한다. 심지어 XML 파일을 쓸 수 있다.

##### 기타 표준 파이썬 XML 라이브러리

- xml.dom : 자바스크립트 개방자에게 친숙한 DOM(Document Object Model)은 웹 문서를 계층구조로 나타낸다. 이 모듈은 전체 XML 파일을 메모리에 로딩하여 XML의 모든 항목을 접근할 수 있게 한다.
- xml.sax : SAX(Simple API for XML)는 즉석 XML을 파싱한다. 즉, 한번에 전체 XML 파일에 메모리에 로딩하지 않는다. 그러므로 매우 큰 XML 스트림을 처리해야 한다면 이 모듈을 비추.

### 8.2.3 HTML
웹의 기본 문서 형식으로 엄청난 양의 데이터가 HTML(Hypertext Markup Language)로 저장되어 있다. 문제는 대부분의 HTML 파일이 규칙을 따르지 않아 파싱이 어려울 수 있다. 또한 HTML의 대부분은 데이터를 교환하기보다는 결과를 표현하는 형태로 더 많이 사용한다.

### 8.2.4 JSON
JSON(JavaScript Object Notaion)은 데이터를 교환하는 인기 있는 형식이다. JSON은 자바스크립트의 서브셋이자, 유효한 파이썬 구문이다. 파이썬과 JSON은 궁합이 좋다.  

JSON은 json 모듈을 이용하면 된다. 이 모듈은 JSON 문자열로 인코딩(dumps)하고, JSON 문자열을 다시 데이터로 디코딩(loads)할 수 있다.

```JSON
menu = {
    "breakfast": {
        "hours": "7-11",
        "items": {
            "breakfast burritos": "$6.00",
            "pancakes": "$4.00"
        }
    },
    "lunch": {
        "hours": "11-3",
        "items": {
            "hamburger": "$5.00"
        }
    },
    "dinner": {
        "hours": "3-10",
        "items": {
            "spaghetti": "$8.00"
        }
    }
}
```

```Python
# dumps()를 사용하여 자료구조(menu)를 JSON 문자열(menu_json)로 인코딩한다.
>>> import json
>>> menu_json = json.dumps(menu)
>>> menu_json
'{"breakfast": {"hours": "7-11", "items": {"breakfast burritos": "$6.00", "pancakes": "$4.00"}}, "lunch": {"hours": "11-3", "items": {"hamburger": "$5.00"}}, "dinner": {"hours": "3-10", "items": {"spaghetti": "$8.00"}}}'

# loads()를 사용하여 JSON 문자열(menu_json)을 자료구조(menu2)로 디코딩
# menu와 menu2는 같은 키와 값을 가진 딕셔너리이다.
>>> menu2 = json.loads(menu_json)
>>> menu2
{'breakfast': {'hours': '7-11',
  'items': {'breakfast burritos': '$6.00', 'pancakes': '$4.00'}},
 'lunch': {'hours': '11-3', 'items': {'hamburger': '$5.00'}},
 'dinner': {'hours': '3-10', 'items': {'spaghetti': '$8.00'}}}

# datetime과 같은 모듈을 사용하여 객체를 인/디코딩시 도중에 예외가 발생한다.
# 표준 JSON 모듈에서 날짜 또는 시간 타입을 정의하지 않았기 때문에 예외가 발생.
>>> import datetime
>>> now = datetime.datetime.utcnow()
>>> now
 datetime.datetime(2018, 6, 25, 4, 19, 45, 410339)

>>> json.dumps(now)
 Traceback (most recent call last)
<ipython-input-12-f164a08299e1> in <module>()
----> 1 json.dumps(now)
...
TypeError: Object of type 'datetime' is not JSON serializable

# JSON이 이행할 수 있는 타입으로 변환(datetime 객채를 문자열과 에포치(epoch)값 같이 변환)
>>> now_str = str(now)
>>> json.dumps(now_str)
'"2018-06-25 04:19:45.410339"'
>>> from time import mktime
>>> now_epoch = int(mktime(now.timetuple()))
>>> json.dumps(now_epoch)
'1529867985'

# JSON 문자열로 인코딩하는 방법은 상속을 통해 수정할 수 있다.
# JSONEncoder의 자식 클래스
# datetime 값을 처리하기 위해 default() 메서드만 오버라이드 한다.
>>> class DTEncoder(json.JSONEncoder):
...     def default(self, obj):
...         # isinstance()는 obj의 타입을 확인한다.
...         if isinstance(obj, datetime.datetime):
...             return int(mktime(obj.timetuple()))
...         # obj가 datetime 타입이 아니라면 기본 JSON 문자열로 인코딩한다.
...         return json.JSONEncoder.default(self, obj)
>>> json.dumps(now, cls=DTEncoder)
'1529867985'

# isinstance()함수는 obj 객체가 datetime.datetime 클래스의 인스턴스인지 확인.
# isinstance()함수는 어느 곳에서든 작동한다.
>>> type(now)
datetime.datetime
>>> isinstance(now, datetime.datetime)
True
>>> type(234)
int
>>> isinstance(234, int)
True
>>> type('hey')
str
>>> isinstance('hey', str)
True
```

> 자료구조에 대해 모르는 상태에서 JSON과 다른 구조화된 텍스트 형식의 파일을 자료구조로 불러 올 수 있다. isinstance()와 타입에 적잘한 메서드를 사용하여 구조를 파악한 후 값을 볼 수 있다. 딕셔너리의 경우 `key(), values(), items()` 메서드로 내용을 추출할 수 있다.

### 8.2.5 YAML

JSON과 유사하게 YAML은 키와 값을 가지고 있지만, 날짜와 시간 같은 데이터 타입을 더 많이 처리한다. 'yaml'이라는 써드파티 라이브러리를 사용하여 이용할 수 있다. `load()`는 YAML 문자열을 파이썬 데이터로, `dump()`는 그 반대 기능을 수행한다.


예로 사용될 yaml 파일 내용이다.(캐나다 시인 제임스 매킨타이어의 정보)

```YAML
name:
  first: James
  last: McIntyre
dates:
  birth: 1828-05-25
  death: 1906-03-31
details:
  bearded: true
  themes: [cheese, Canada]
books:
  url: http://www.gutenberg.org/files/36068/36068-h/36068-h.htm
poems:
  - title: 'Motto'
    text: |
      Politeness, perseverance and pluck,
      To their possessor will bring good luck.
  - title: 'Canadian Charms'
    text: |
      Here industry is not in vain,
      For we have bounteous crops of grain,
      And you behold on every field
      Of grass and roots abundant yield,
      But after all the greatest charm
      Is the snug home upon the farm,
      And stone walls now keep cattle warm.
```

`true`, `false`, `on`, `off`와 같은 bool형으로 변환된다. 정수와 문자열도 파이썬의 타입으로 변환된다. 다른 구문들은 리스트와 딕셔너리를 생성한다.

```Python
>>> import yaml
>>> with open('mcintyre.yaml', 'rt') as fin:
...     text = fin.read()
>>> data = yaml.load(text)
>>> data['details']
{'bearded': True, 'themes': ['cheese', 'Canada']}
>>> len(data['poems'])
2
>>> data['poems'][1]['title']
'Canadian Charms'
```

> PyYAML은 문자열에서 파이썬 객체를 불러올 수 있으나 위험하다. 신뢰할 수 없는 YAML을 불러온다면 `load()` 대신 `safe_load()`를 사용하다. 아직은 **항상** `safe_load()`를 사용하는 것이 좋다.

### 8.2.6 보안 노트

객체를 어떤 파일로 저장하고, 파일에서 객체로 읽어오는 과정에서 보안 문제가 발생할 수 있다.

```xml
<?xml version="1.0"?>
<!DOCTYPE lolz [
 <!ENTITY lol "lol">
 <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
 <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
 <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
 <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
 <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
 <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
 <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
 <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
 <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
]>
<lolz>&lol9;</lolz>
```

위 XML 코드는 위키디피아의 billion laughs인데, 10개의 엔티티가 있다. 각 엔티티는 하위 레벨로 10배씩 확장되어 총 10억개로 확장된다.  

위 XML 코드는 모든 XML 라이브러리를 뚫어버린다. [Defused XML](https://bitbucket.org/tiran/defusedxml)은 파이썬 라이브러리의 취약한 부분은 물론이고 billion laughs와 다른 공격을 나열하고 있다. 이러한 문제를 방지하기 위해 라이브러리의 설정을 변경하는 방법도 제공한다. 다른 라이브러리에 대한 프론트엔드 보안으로 `defusedxml` 라이브러리를 사용할 수 있다.

### 8.2.7 설정 파일

대부분의 프로그램은 다양한 옵션이나 설정을 제공한다. 동적인 것은 프로그램의 인자를 통해 제공되지만, 정적인 것은 어딘가에 유지되어야 한다. 대부분의 직접 만든 설정 파일은 지저분하고 그렇게 빠르지도 않다. writer 프로그램과 reader 프로그램(파서) 모두 관리해야 한다.


예로 윈도우 스타일의 .ini 파일을 처리하는 'configparser' 모듈을 사용한다. 이 파일은 **키=값** 형식의 섹션이다.

```
[english]
greeting = Hello

[french]
greeting = Bonjour

[files]
home = /usr/local
# 간편한 보간법 사용
bin = %(home)s/bin
```

```python
# 설정 파일을 읽어서 자료구조로 변환
>>> import configparser
>>> cfg = configparser.ConfigParser()
>>> cfg.read('settings.cfg')
['settings.cfg']
>>> cfg
<configparser.ConfigParser at 0x1047703c8>
>>> cfg['french']
<Section: french>
>>> cfg['french']['greeting']
'Bonjour'
>>> cfg['files']['bin']
'/usr/local/bin'
```

만약 두 단계보다 더 깊은 중첩 설정이 필요한 경우 YAML이나 JSON 파일 형식을 사용한다.

### 8.2.8 기타 데이터 교환 형식

- MsgPack
- Protocol Buffers
- Avro
- Thrift

위 이진 데이터 교환 형식은 일반적으로 더 간결하고 XML이나 JSON보다 빠르다. 이진 형식이기 떄문에 텍스트 편집기로 쉽게 편집할 수 없다.

### 8.2.9 직렬화하기: pickle

자료구조(객체)를 파일로 저장하는 것을 직렬화(serialization)라고 한다. JSON과 같은 형식은 파이썬 프로그램에서 모든 데이터 타입을 직렬화하는 컨버터가 필요하다. 'pickle' 모듈은 바이너리 형식으로 된 객체를 저장/복원할 수 있다. datetime 객체를 인코딩할 때도 문제가 되지 않는다.

```Python
>>> import pickle
>>> import datetime
>>> now1 = datetime.datetime.utcnow()
>>> pickled = pickle.dumps(now1)
>>> now2 = pickle.loads(pickled)
>>> now1
datetime.datetime(2018, 6, 26, 4, 12, 43, 622795)
>>> now2
datetime.datetime(2018, 6, 26, 4, 12, 43, 622795)
```

'pickle'은 직접 만든 클래스와 객체에서도 작동한다.

```Python
# 'tiny' 문자열을 반환하는 Tiny 클래스
>>> import pickle
>>> class Tiny():
...     def __str__(self):
...         return 'tiny'
...
>>> obj1 = Tiny()
>>> obj1
<__main__.Tiny at 0x1047ab6a0>
>>> str(obj1)
'tiny'
# 직렬화된 obj1 객체의 이진 문자열
>>> pickled = pickle.dumps(obj1)
>>> pickled
b'\x80\x03c__main__\nTiny\nq\x00)\x81q\x01.'
>>> obj2 = pickle.loads(pickled)
>>> obj2
<__main__.Tiny at 0x1047a5518>
>>> str(obj2)
'tiny'
```

obj1의 복사본을 만들기 위해 pickled를 다시 역직렬화하여 obj2 객체로 변환했다. `dump()`로 직렬화하고, `load()`로 역직렬화한다.

> pickle은 파이썬 객체를 만들 수 있기 때문에 보안 문제가 발생할 수 있다. 신뢰할 수 없는 것은 역직렬화하지 않는 것을 추천

## 8.3 구조화된 이진 파일

일부 파일 형식은 특정 자료구조를 저장하기 위해 설계되었지만, 관계형 데이터베이스나 NoSQL 데이터베이스는 그렇지 않다.

### 8.3.1 스프레드시트

엑셀과 같은 스프레드시트는 광범위한 이진 데이터 형식이다.  
스프레드시트를 CSV 파일로 저장하면 'csv'모듈을 사용하여 읽는다. xls 파일이라면 써드파트 패키지 'xlrd'를 사용하면 된다.

### 8.3.2 HDF5

HDF5(Hierarchical Data Format)는 다차원 혹은 계층적 수치 데이터를 위한 이진 데이터 형식이다. 주로 아주 큰 데이터 집합(기가~테라 바이트)에 대한 빠른 임의적인 접근이 필요한 과학 분야에 주로 사용된다. 어떤 경우에는 데이터베이스의 좋은 대안이 될 수도 있다. 쓰기 충돌에 대한 데이터베이스의 보호가 필요하지 않은 웜(WORM:Write Once/Read Many.디스크에 데이터를 단 한번만 쓸 수 있고, 그 후에는 데이터가 삭제되지 않도록 보호하는 데이터 저장 기술) 애플리케이션에 적합하다.

- h5py는 완전한 기능을 갖춘 저수준의 인터페이스다.
- PyTables는 약간 고수준의 인터페이스로, 데이터베이스와 같은 기능을 지원한다.

HDF5의 모범 예는 HDF5 형식으로 곡을 내려받을 수 있는 데이터를 가진 [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/)이다.

## 8.4 관계형 데이터베이스

데이터베이스가 제공하는 기능들.

- 다수의 동시 사용자가 데이터에 접근
- 사용자에 의한 데이터 손상으로부터의 보호
- 데이터를 저장하고 검색하는 효율적인 방법
- **스키마(schema)** 에 의해 정의된 데이터와 **제약조건(constraint)** 에 한정되는 데이터
- 다양한 데이터 타입과의 관계(relationship)를 계산하는 **조인(join)**
- (명령형(imperative) 이기보다는) 서술적인(declarative) 질의 언어: **SQL(Structured Query Language)**

다양한 종류의 데이터 간의 관계를 **테이블(table)** 형태로 표시하기 때문에 **관계형** 이라고 부른다.

일반적으로 하나의 열 또는 열의 그룹은 테이블의 **기본키(primary key)** 다. 기본키 값은 테이블에서 반드시 유일해야 한다. 이는 테이블에 동일한 데이터를 추가하는 것을 방지한다. 이 키는 질의를 빠르게 찾을 수 있도록 **인덱싱(indexing)** 되어 있다.  

파일이 디렉터리 안에 있는 것처럼, 각 테이블은 상위 **데이터베이스** 내에 존재한다. 이러한 두 가지 수준의 계층구조는 더 나은 조직을 유지할 수 있도록 해준다.  

키가 아닌 열값으로 행을 찾으려면, 그 열에 부차적인 **인덱스** 를 정의한다. 그렇지 않으면 데이터베이스 서버는 열값과 일치하는 모든 행을 무차별 검색한다.(**테이블스캔**)  

테이블은 **외래키(foreign key)** 와 서로 연관될 수 있으므로 열값은 이러한 외래키에 대한 제약이 있을 수 있다.

### 8.4.1 SQL

SQL은 **원하는** 결과를 질의하는 서술형 **언어** 다. SQL 질의는 클라이언트에서 데이터베이스 서버로 전송하는 텍스트 문자열이다.  

다양한 SQL들이 데이터베이스 회사들에 의해 생겨났지만, 관계형 데이터베이스를 저장할 때 SQL은 호환성을 제공한다. 하지만 다양한 SQL과 운영에 대한 차이는 데이터를 또 다른 타입의 데이터베이스로 옮기기 어렵게 만든다.

SQL은 두 개의 주요 카테고리가 있다.

- DDL(Data Definition Language.데이터 정의어) : 테이블, 데이터베이스, 사용자에 대한 생성, 삭제, 제약조건(constraint), 권한(permission)을 다룬다.
- DML(Data Manipulation Language.데이터 조작어) : 데이터의 조회, 삽입, 갱신, 삭제를 다룬다.

##### 기본 SQL DDL 명령어

명령 | SQL 패턴 | SQL 예제
---|---|---
데이터베이스 생성 | CREATE DATABASE dbname | CREATE DATABASE d
현재 데이터베이스 선택 | USE dbname | USE d
데이터베이스와 해당 테이블 삭제 | DROP DATABASE dbname | DROP DATABASE d
테이블 생성 | CREATE TABKE tbname (coldefs) | CREATE TABLE t (id INT, count INT)
테이블 삭제 | DROP TABLE tbname | DROP TABLE t
테이블의 모든 행 삭제 | TRUNCATE TABLE tbname | TRUNCATE TABLE t

관계형 데이터베이스의 메인 DML 명령어는 CRUD이다.

- 생성(create): INSERT
- 조회(read): SELECT
- 갱신(update): UPDATE
- 삭제(delete): DELETE

##### 기본 SQL DML 명령어

명령 | SQL 패턴 | SQL 예제
---|---|---
행 추가 | INSERT INTO tbname VALUES(...) | INSERT INTO t VALUES(7, 40)
모든 행과 열 조회 | SELECT * FROM tbname | SELECT * FROM t
모든 행과 특정 열 조회 | SELECT cols FROM tbname | SELECT id, count FROM t
특정 행과 열 조회 | SELECT cols FROM tbname WHERE condition | SELECT id, count FROM t WHERE count > 5 AND id =9
특정 열의 행값 변경 | UPDATE tbname SET col = value WHERE condition | UPDATE t SET count=3 WHERE id=5
행 삭제 | DELETE FROM tbname WHERE condition | DELETE FROM t WHERE count <=10 OR id=16

### 8.4.2 DB-API

DB-API는 관계형 데이터베이스에 접근하기 위한 파이썬의 표준 API다. DB-API를 사용하면 여러 종류의 데이터베이스를 동작하기 위한 별도의 프로그램 없이, 하나의 프로그램만 작성하면 된다.

##### 메인 함수

- connect()
 - 데이터베이스의 연결을 만든다. 이 함수는 사용자 이름, 비밀번호, 서버 주소 등의 인자를 포함한다.
- cursor()
 - 질의를 관리하기 위한 **커서** 객체를 만든다.
- execute(), executemany()
 - 데이터베이스에 하나 이상의 SQL 명령을 실행한다.
- fetchone(), fetchmany(), fetchall()
 - 실행 결과를 얻는다.

###  8.4.3 SQLite

SQLite는 가벼운 오픈소스의 관계형 데이터베이스다. 표준 파이썬 라이브러리로 구현되어 있고, 일반 파일처럼 데이터베이스를 저장한다. 그리고 서로 다른 컴퓨터와 운영체제에 대한 호환이 가능하다.  
간단한 관계형 데이터베이스 애플리케이션에 대한 호환성이 아주 뛰어나다. 하지만 MySQL, PostgreSQL처럼 완벽하진 않다. 그러나 SQL을 지원하고, 동시에 여러 사용자를 관리할 수 있다. 웹 브라우저, 스마트폰, 애플리케이션에서 SQLite를 임베디드 데이터베이스처럼 사용한다.

사용하거나 생성하고자 하는 로컬 SQLite 데이터베이스 파일을 `connect()`로 연결하는 것으로 시작한다. 이 파일은 다른 서버에서 데이블을 고나리하는 디렉터리 구조와 유사한 **데이터베이스** 다. 특수한 문자열 `:memory:`는 메모리에서만 데이터베이스를 생성한다. 빠르고, 테스트에 유용하지만, 프로그램이 종료되거나 컴퓨터를 끄면 데이터가 사라진다.

```Python
# critter : 가변 길이 문자열. 동물 이름(기본 키)
# count : 정수, 현재 동물 수
# damaged : 부동소수점, 관람객으로부터 받은 상처 등 동물의 손실 금액
>>> import sqlite3
>>> conn = sqlite3.connect('enterprise.db')
>>> curs = conn.cursor()
>>> curs.execute('''CREATE TABLE zoo
... (critter VARCHAR(20) PRIMARY KEY,
... count INT,
... damages FLOAT)''')
<sqlite3.Cursor at 0x110a525e0>

3중 인용 부호(''')는 SQL 질의와 같은 긴 문자열을 생성하는데 편리하다.

```Python
>>> curs.execute('INSERT INTO zoo VALUES("duck", 5, 0.0)')
<sqlite3.Cursor at 0x110b1aea0>
>>> curs.execute('INSERT INTO zoo VALUES("bear", 2, 1000.0)')
<sqlite3.Cursor at 0x110b1aea0>
```

플레이스홀더를 사용하여 데이터를 안전하게 넣을 수 있다.

```Python
>>> ins = 'INSERT INTO zoo (critter, count, damages) VALUES(?, ?, ?)'
>>> curs.execute(ins, ('weasel', 1, 2000.0))
<sqlite3.Cursor at 0x110b1aea0>
```

`?`는 삽입할 예정이라는 표시이다. 플레이스홀더를 사용함으로써 인용 부호를 억지로 넣을 필요가 없어졌다.  
플레이스홀더는 웹에서 악의적인 SQL 명령을 삽입하는 외부 공격(SQL 인젝션)으로부터 시스템을 보호한다.

```Python
# 모든 동물을 조회
>>> curs.execute('SELECT * FROM zoo')
<sqlite3.Cursor at 0x110b1aea0>
>>> rows = curs.fetchall()
>>> print(rows)
[('duck', 5, 0.0), ('bear', 2, 1000.0), ('weasel', 1, 2000.0)]

# 오름차순으로 정렬하여 조회
>>> curs.execute('SELECT * FROM zoo ORDER BY count')
<sqlite3.Cursor at 0x110b1aea0>
>>> curs.fetchall()
[('weasel', 1, 2000.0), ('bear', 2, 1000.0), ('duck', 5, 0.0)]

# 내림차순으로 정렬하여 조회
>>> curs.execute('SELECT * FROM zoo ORDER BY count DESC')
<sqlite3.Cursor at 0x110b1aea0>
>>> curs.fetchall()
[('duck', 5, 0.0), ('bear', 2, 1000.0), ('weasel', 1, 2000.0)]

# 특정 조건 조회
# 한 마리당 가장 많은 비용이 드는 동물
>>> curs.execute('''SELECT * FROM zoo WHERE
>>> damages = (SELECT MAX(damages) FROM zoo)''')
<sqlite3.Cursor at 0x110b1aea0>
>>> curs.fetchall()
[('weasel', 1, 2000.0)]

# 데이터베이스 연결과 커서를 열었으면 각각 닫아주어야 한다.
>>> curs.close()
>>> conn.close()
```

### 8.4.4 MySQL

MySQL에 접근하기 위한 드라이버

이름 | Pypi 패키지 | 임포트 | 비고
---|---|---|---
MySQL Connecter |  mysql-connetor-python | mysql.connecter
PYMySQL | pymysql | pymysql
oursql | oursql | oursql | MySQL C 클라이언트 라이브러리 필요

### 8.4.5 PostgreSQL

PostgreSQL 드라이버

이름 | Pypi 패키지 | 임포트 | 비고
---|---|---|---
psycopg2 | psycopg2 | psycopg2 | PostgreSQL 클라이언트 도구의 pg_config 필요
py-postgresql | py-postgresql | py-postgresql

### 8.4.6 SQLAlchemy

##### 설치

```
>>> pip install sqlalchemy
```

##### SQLAlchemy 사용 수준

- 가장 낮은 수준에서 데이터베이스 커넥션 풀을 처리. SQL 명령을 실행하고 그 결과를 반환한다. DB-API와 가장 근접
- 다음 수준은 SQL 표현 언어, 즉 파이써닉한 SQL 빌더다.
- 가장 높은 수준은 SQL 표현 언어를 사용하고, 관계형 자료 구조와 애플리케이션 코드를 바인딩하는 ORM이다.

SQLAlchemy는 데이터베이스 드라이버와 함께 작동하는데 따로 임포트할 필요는 없다. SQLAlchemy에서 제공하는 최초의 연결 문자열에서 드라이버를 선택한다.

```
dialect + driver :// user : password @ host : post / dbname
# dialect : 데이터베이스 타입
# dirver : 사용하고자 하는 데이터베이스의 특정 드라이버
# user, password : 데이터베이스 인증 문자열. 사용자와 비밀번호
# dbname : 서버에 연결할 데이터베이스 이름
```

데이터베이스 | 드라이버
---|---
sqlite | pysqlite(또는 생략)
mysql | mysqlconnector, pymysql, oursql
postgresql | psycopg2, pypostgresql

#### 엔진 레이어

가장 낮은 수준. 기본으로 제공하는 DB-API보다 좀 더 많은 기능이 있다.  

(여기서 SQLite의 연결에 대한 문자열 인자 host, port, user, password는 생략.)  
dbname은 데이터베이스를 어떤 파일에 저장할지 SQLite에 알려준다. dbname을 생략하면 SQLite는 메모리에 데이터베이스를 만든다. `/`로 시작하면 절대 경로 파일이름이다.(리눅스와 맥에만 해당. 윈도우는 `C://`로 시작) `/`로 시작하직 않으면 상대 경로다.

```Python
# 모듈 임포트
# as : alias
# sa : SqlAlchemy
>>> import sqlalchemy as sa
# 데이터베이스 연결하고, 메모리에 스토리지 생성
>>> conn = sa.create_engine('sqlite://')
# 새 열에 있는 데이터베이스 테이블 zoo를 생성
>>> conn.execute('''CREATE TABLE zoo
... (critter VARCHAR(20) PRIMARY KEY,
... count INT,
... damages FLOAT)''')
<sqlalchemy.engine.result.ResultProxy at 0x110f35518>
# conn.execute()는 ResultProxy라는 SQLAlchemy 객체를 반환
>>> ins = 'INSERT INTO zoo (critter, count, damages) VALUES (?, ?, ?)'
# 빈 테이블에 3개의 데이터를 삽입
>>> conn.execute(ins, 'duck', 10, 0.0)
<sqlalchemy.engine.result.ResultProxy at 0x110f35860>
>>> conn.execute(ins, 'bear', 2, 1000.0)
<sqlalchemy.engine.result.ResultProxy at 0x110f35a58>
>>> conn.execute(ins, 'weasel', 1, 2000.0)
<sqlalchemy.engine.result.ResultProxy at 0x110f35b70>
# 데이터베이스 테이블에 입력한 값이 있는지 확인
>>> rows = conn.execute('SELECT * FROM zoo')
# SQLAlchemy에서 row는 리스트가 아닌 ResultProxy 객체다
>>> print(rows)
<sqlalchemy.engine.result.ResultProxy object at 0x110f35c18>
# 리스트처럼 순회하여 row를 얻을 수 있다.
>>> for row in rows:
...     print(row)
('duck', 10, 0.0)
('bear', 2, 1000.0)
('weasel', 1, 2000.0)
```

SQLAlchemy가 연결 문자열에서 데이터베이스 타입을 알아내기 떄문에 코드 앞 부분에 데이터베이스 드라이버를 임포트하지 않아도 된다. 또 다른 장점은 [**커넥션 풀링(connection pooling)**](http://docs.sqlalchemy.org/en/latest/core/pooling.html) 이다.

> 커넥션 풀링은 응용 프로그램이 동시에 사용할 수 있는 총 연결 수를 관리 할 뿐만 아니라 효율적인 재사용을 위해 메모리에서 장기 실행 연결을 유지 관리하는 데 사용되는 표준 기술입니다. 특히 서버 측 웹 응용 프로그램의 경우 커넥션 풀링은 요청에서 다시 사용되는 활성 데이터베이스 연결의 "pool"을 메모리에 유지하는 표준 방법입니다. SQLAlchemy는 엔진과 통합되는 여러 커넥션 풀링 구현을 포함합니다. 또한 일반 DB-API 접근 방식에 풀링을 추가하려는 응용 프로그램에 직접 사용할 수 있습니다.

#### SQL 표현 언어

표현 언어는 하위 수준의 엔진 레이어보다 더 다양한 SQL문을 처리한다. 표현 언어는 중간에서 관계형 데이터베이스 애플리케이션을 쉽게 접근할 수 있도록 해준다.

```Python
>>> import sqlalchemy as sa
>>> conn = sa.create_engine('sqlite://')
# zoo 테이블을 정의하기 위해 SQL문 대신 표현 언어를 사용
# Table() 메서드의 구조는 데이터베이스 테이블의 구조와 일치
# 테이블이 3개의 열을 포함하고 있으므로 Table() 메서드 호출의 괄호 안에 3개의 Column() 메서드 호출이 있다.
>>> meta = sa.MetaData()
>>> zoo = sa.Table('zoo', meta,
...           sa.Column('critter', sa.String, primary_key=True),
...           sa.Column('count', sa.Integer),
...           sa.Column('damages', sa.Float)
...        )
>>> meta.create_all(conn)
# 표현 언어 함수로 데이터를 삽입
>>> conn.execute(zoo.insert(('bear', 2, 1000.0)))
<sqlalchemy.engine.result.ResultProxy at 0x110f67828>
>>> conn.execute(zoo.insert(('weasel', 1, 2000.0)))
<sqlalchemy.engine.result.ResultProxy at 0x110f67f28>
>>> conn.execute(zoo.insert(('duck', 10, 0)))
<sqlalchemy.engine.result.ResultProxy at 0x110f5ea58>
# SELECT문. zoo.select() 메서드는 SELECT * FROM zoo와 같이 zoo 객체로 나타내는 테이블에서 모든 항목을 조회
>>> result = conn.execute(zoo.select())
# 입력 결과 확인
>>> rows = result.fetchall()
>>> print(rows)
[('bear', 2, 1000.0), ('weasel', 1, 2000.0), ('duck', 10, 0.0)]
```

#### ORM

SQLAlchemy의 최상위 레이어에서 ORM은 SQL 표현 언어를 사용하지만, 실제 데이터베이스의 메커니즘을 숨긴다. ORM 클래스를 정의하여 데이터베이스의 데이터 입출력을 처리한다. '객체-관계 매핑'이라는 복잡한 단어 구분 속의 기본 아이디어는 여전히 관계형 데이터베이스를 허용하면서, 코드의 객체를 참조하여 파이썬처럼 작동하게 하는 것이다.

```Python
# 필요 모듈 임포트
>>> import sqlalchemy as sa
>>> from sqlalchemy.ext.declarative import declarative_base
# 데이터베이스 연결
>>> conn = sa.create_engine('sqlite:///zoo.db')
# SQLAlchemy의 ORM사용
# Zoo 클래스 정의, 테이블의 열과 속성 연결
>>> Base = declarative_base()
>>> class Zoo(Base):
...     __tablename__ = 'zoo'
...     critter = sa.Column('critter', sa.String, primary_key=True)
...     count = sa.Column('count', sa.Integer)
...     damages = sa.Column('damages', sa.Float)
...     def __init__(self, critter, count, damages):
...         self.critter = critter
...         self.count = count
...         self.damages = damages
...     def __repr__(self):
...         return "<Zoo({}, {}, {})>".format(self.critter, self.count, self.damages)
# 데이터베이스와 테이블을 생성
>>> Base.metadata.create_all(conn)
# 파이썬 객체를 생성하여 데이터를 삽입
>>> first = Zoo('duck', 10, 0.0)
>>> second = Zoo('bear', 2, 1000.0)
>>> third = Zoo('weasel', 1, 2000.0)
>>> first
<Zoo(duck, 10, 0.0)>
# ORM을 SQL로 내보내기
# 데이터베이스와 대화할 수 있는 세션을 생성
>>> from sqlalchemy.orm import sessionmaker
>>> Session = sessionmaker(bind=conn)
>>> session = Session()
# 데이터베이스에 생성한 새 객체를 세션 내에 작성
# add() 함수는 하나의 객체를 추가하고, add_all()은 리스트를 추가한다.
>>> session.add(first)
>>> session.add_all([second, third])
# 모든 작업을 (강제적으로) 완료한다.
>>> session.commit()
```

터미널에서 실행

```terminal
$ sqlite3 zoo.db
SQLite version 3.16.0 2016-11-04 19:09:39
Enter ".help" for usage hints.
sqlite> .tables
zoo
sqlite> select * from zoo;
duck|10|0.0
bear|2|1000.0
weasel|1|2000.0
```

튜토리얼을 진행해본다면 다음과 같은 수준을 결정할 수 있다.

- 이전 SQLite 절과 같은 일반적인 DB-API
- SQLAlchemy 엔진
- SQLAlchemy 표현 언어
- SQLAlchemy ORM

ORM은 SQL을 추상화한 것이고, 추상화된 것은 어느 시점에선가 문제가 발생할 수 있다. ORM은 주로 간단한 애플리케이션에서 드물게 사용해야 한다.

## 8.5 NoSQL 데이터 스토어

NoSQL은 매우 큰 데이터 집합을 처리하고, 데이터 정의에 대해 좀 더 유연하거나 커스텀 데이터 연산을 지원하기 위해 만들어졌다.

### 8.5.1 dbm 형식

**키 - 값** 저장 형식으로, 다양한 설정을 유지하기 위해 웹 브라우저같은 애플리케이션에 포함된다. dbm 데이터베이스는 파이썬의 딕셔너리와 같은 점이 있다.

- 키에 값을 할당한다. 이것은 디스크에 있는 데이터베이스에 자동으로 저장된다.
- 키로부터 값을 얻는다.

```Python
>>> import dbm
# 'r'은 읽기(read), 'w'는 쓰기(write), 'c'는 읽기/쓰기(파일이 존재하지 않으면 생성)
>>> db = dbm.open('definitions', 'c')
# 딕셔너리처럼 키에 값을 할당
>>> db['mustard'] = 'yellow'
>>> db['ketchup'] = 'red'
>>> db['pesto'] = 'green'
# 할당 값 확인
>>> len(db)
3
>>> db['pesto']
b'green'
# 데이터베이스를 닫고 다시 열어서 잘 저장되었는지 확인
>>> db.close()
>>> db = dbm.open('definitions', 'r')
>>> db['mustard']
b'yellow'
```
키와 값은 바이트로 저장된다. 데이터베이스 객체 DB를 순회할 순 없지만, `len()`으로 키의 갯수를 얻을 수 있다. `get()`과 `setdefault()`는 딕셔너리의 함수처럼 동작한다.

### 8.5.2 Memcached

Memcached는 민첩한 인메모리 키-값의 캐시 서버다. 주로 데이터베이스 앞단에 놓이거나 웹 서버의 세션 데이터를 저장하는데 사용한다.  

Memcached를 사용하려면 Memcached 서버와 파이썬 드라이버가 필요하다.

```
$ pip install python-memcached
```

memcached 서버에 연결하면 다음과 같은 일을 할 수 있다.

- 키에 대한 값을 설정하고 얻는다.
- 값을 증가하거나 감소시킨다.
- 키를 삭제한다.

데이터는 **지속되지 않아서,** 이전에 쓴 데이터가 사라질 수 있다. 캐시 서버의 memcached에 대한 특징이다. 이는 오래된 데이터를 제거하여 메모리 부족을 방지한다.

여러 memcached 서버를 동시에 연결할 수 있다.

```Python
# 실습 실패.
>>> import memcache
>>> db = memcache.Client(['127.0.0.1:11211'])
>>> db.set('marco', 'polo')
>>> db.get('marco')
>>> db.set('ducks', 0)
>>> db.get('ducks')
>>> db.incr('ducks', 2)
>>> db.get('ducks')
```

### 8.5.3 Redis

Redis는 **자료구조 서버** 다. Redis 서버에 있는 모든 데이터는 memcached처럼 메모리에 맞아야 한다.(디스크에 데이터를 저장할 수 있는 옵션이 있다) memcached와 달리 Redis는 다음과 같은 일이 가능하다.

- 서버의 재시작과 신뢰성을 위해 데이터를 디스크에 저장한다.
- 기존 데이터를 유지한다.
- 간단한 문자열 이상의 자료구조를 제공한다.

Redis 데이터 타입은 파이썬 데이터 타입에 가깝기 때문에, Redis 서버는 여러 파이썬 애플리케이션에서 데이터를 공유하기 위한 중계 역할로 매우 유용하다.

##### 설치

```
$ pip install redis
```

https://redislabs.com/lp/python-redis/

일단 문서를 먼저 살펴봐야 책의 내용도 넘어갈 수 있다.  

일단 한번 읽어보고 나중에 실습해 보는걸로..

#### 문자열
#### 리스트
#### 해시
#### 셋
#### 정렬된 셋
#### 비트
#### 캐시와 만료

### 8.5.4 기타 NoSQL

데이터베이스 | 파이썬 API
---|---
Cassandra | pycassa
CouchDB | couchdb-python
HBase | happybase
Kyoto Cabinet | Kyotocabinet
MongoDB | Mongodb
Riak | riak-python-client

위 NoSQL 서버는 메모리보다 큰 데이터를 처리하고, 이들 중 대다수는 여러 대의 컴퓨터를 사용한다.

## 8.6 풀텍스트 데이터베이스

**풀텍스트** 검색을 위한 풀텍스트 데이터베이스

데이터베이스 | 파이썬 API
---|---
Lucene | Pylucene
Solr | SolPython
ElasticSearch | Pyes
Sphinx | Sphinxapi
Xapian | Xappy
Whoosh | 파이썬으로 작성된. API 포함
