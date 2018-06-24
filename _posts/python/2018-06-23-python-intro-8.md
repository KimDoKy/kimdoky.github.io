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
