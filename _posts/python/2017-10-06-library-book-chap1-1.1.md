---
layout: post
section-type: post
title: Python Library - chap 1. 텍스트 처리하기 - 1.1 일반적인 문자열 조작하기
category: python
tags: [ 'python' ]
---

# chap 1. 텍스트 처리하기

프로그램을 작성할 때 가장 기본이 되는 텍스트 처리 기능에 대해 다룹니다. Python에서는 문자열을 편리하게 다루는 기능이나 문자열형(str) 메서드를 여럿 제공합니다. 이들 기능을 잘 활용하여 텍스트 데이터를 분석하고 정형화된 결과를 출력해봅니다.

## 1.1 일반적인 문자열 조작하기

### 문자열 검사 메서드
문자열 객체(str)에는 문자열이 지정된 형식인지 아닌지를 검사하는 메서드가 있습니다. 이들 메서드의 반환값은 모두 bool(True/False)입니다.

#### 문자열 검색 메서드

메서드 이름 | 설명
---|---
isalnum() | 문자열이 숫자와 문자일 때만 True를 반환한다.
isalpha() | 문자열이 문자일 때만 True를 반환한다. 한국어 등 ASCII 문자열이 아니더라도 숫자나 기호가 포함되어 있지 않으면 True를 반환합니다.
isdecimal() | 문자열이 십진수 숫자를 나타내면 True를 반환한다.
isdigit() | 문자열이 숫자르 나타내는 문자로만 이루어졌으면 True를 반환한다.
isidentifier() | 식별자로 사용할 수 있는 문자열이면 True를 반환한다.
islower() | 문자열이 모두 소문자면 True를 반환한다.
isnumeric() | 수를 나타내는 문자열이면 True를 반환한다. 한자 숫자 등도 포함된다.
isprintable() | 프린트 가능한 문자열이면 True를 반환한다.
isspace() | 스페이스, 탭 등의 공백 문자면 True를 반환한다.
istitle() | 맨 처음만 대문자이고 뒤에 소문자인 문자열이면 True를 반환한다.
isupper() | 문자열이 모두 대문자면 True를 반환한다.

#### 문자열 검사 메서드 사용 예

```python
>>> '123abc'.isalnum() # 영어와 숫자로만 구성된 문자열
True
>>> '123abc#'.isalnum() # 기호가 들어간 문자열
False
>>> 'abcd'.isalpha()
True
>>> '가나다라'.isalpha()
True
>>> 'UPPERCASE'.isupper()
True
>>> 'lowercase'.islower()
True
>>> 'Title String'.istitle()
True
>>> num = '123456789' # 아라비아 숫자
>>> num.isdecimal(), num.isdigit(), num.isnumeric()
(True, True, True)
>>> num = '１２３４５' # 전각 아라비아 숫자
>>> num.isdigit(), num.isdecimal(), num.isnumeric()
(True, True, True)
>>> num = '①②③④⑤' # 원숫자
>>> num.isdigit(), num.isdecimal(), num.isnumeric()
(True, False, True)
>>> num = 'Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ' # 로마숫자
>>> num.isdigit(), num.isdecimal(), num.isnumeric()
(False, False, False) # 맥으로 입력하는 부분에서 문제가 있는듯합니다. isnumeric() 함수가 숫자로 인식하지 못하네요.
>>> num = '⼀⼆㆔亖五'
>>> num.isdigit(), num.isdecimal(), num.isnumeric()
(False, False, False)
```

### 문자열 변환 메서드
문자열 객체(str)에는 문자열을 변환하는 메서드가 있습니다. 이들 메서드의 반환값은 모두 문자열입니다. 다음 메서드는 대소문자 구분이 있는 알파벳일 때만 유효하며 한국어와 같은 기타 언어는 변하지 않습니다.

#### 문자열 변환 메서드

메서드 이름 | 설명
---|---
upper() | 문자열을 모두 대문자로 변환한다.
lower() | 문자열을 모두 소문자로 변환한다.
swapcase() | 대문자는 소문자로, 소문자는 대문자로 변환한다.
capitalize() | 맨 처음 한 문자를 대문자로, 그 외는 소문자로 변환한다.
title() | 단어마다 대문자 한 문자+소문자 형식으로 변환한다.
replace(old,new[,count]) | old를 new로 변환한 문자열을 반환한다. count가 지정된 경우에는 맨 처음부처 지정된 수만큼 변환한다.

#### 문자열 변환 메서드 사용 예

```python
>>> text = 'HELLO world!'
>>> text.upper()
'HELLO WORLD!'
>>> text.lower()
'hello world!'
>>> text.swapcase()
'hello WORLD!'
>>> text.capitalize()
'Hello world!'
>>> text.title()
'Hello World!'
>>> text.replace('world', 'python')
'HELLO python!'
>>> text.replace('L','l',1)
'HElLO world!' # 첫 번째 L만 변환
>>> text.replace('L','l')
'HEllO world!'
```

### 서식화 메서드
지정한 형식의 문자열을 작성하기 위한 서식화 메서드 format()에 대해 살펴봅니다.  

서식화 메서드란 미리 포맷을 지정하여 그 포맷에 따라 인수를 배치해서 문자열을 작성하는 것입니다. 다음 코드는 간단한 사용 예입니다. {}로 감싼 부분에 format()의 인수로 지정된 값이 대입되어 문자열이 작성됩니다.

#### format()의 간단한 사용 예

```python
>>> '1 + 2 = {0}'.format(1 + 2)
'1 + 2 = 3'
>>> a = 2
>>> b = 3
>>> '{0} * {1} = {2}'.format(a,b,a*b)
'2 * 3 = 6'
```

서식화 메서드는 다음과 같은 두 가지가 있습니다.

#### format() 메서드

형식 | format(\*args, \**kwargs)
---|---
인수|args - 서식화할 값을 위치 인수로 지정한다.<br>kwargs - 서식화할 값을 키워드 인수로 지정한다.

#### format_map() 메서드

형식 | format_map(mapping)
---|---
인수 | mapping - 서식화할 값을 사전 형식으로 지정한다.

### 치환 필드 지정 방법
서식화 메서드에서 치환 필드({})를 지정하는 방법은 여러 가지가 있습니다.

#### 기본적인 치환 필드 지정 방법

형식 | 설명
---|---
{}{} | 왼쪽부터 순서대로 인수로 지정한 값으로 치환된다.
{0}{1}{2} | 지정된 위치의 인수 값으로 치환된다.
{name}{key} | kwargs 또는 format_map()에서 지정한 사전의 키에 해당하는 값으로 치환된다.

#### 기본적인 서식 지정 코드

```python
>>> '{} is better than {}'.format('Beautiful','ugly')
'Beautiful is better than ugly'
>>> '{1} is better than {0}'.format('implicit', 'Explicit')
'Explicit is better than implicit'
>>> 'My name is {name}'.format(name='doky')
'My name is doky'
>>> person = {'name':'doky', 'twitter':'makingfunk',}
>>> 'My twitter id is {twitter}'.format_map(person)
'My twitter id is makingfunk'
```
또한 인수에 list, dict 등을 지정할 때는 치환 필드를 다음과 같이 지정할 수 있습니다.

#### 복잡한 치환 필드 지정 방법

형식 | 설명
---|---
{0[0]}{name[0]} | 지정된 인수의 0번째 요소가 배치된다.
{1[key]}{name[key]} | 지정된 인수의 지정된 키워드(여기에서는 key)의 값이 배치된다.
{o.attr}{name.attr} | 지정된 인수의 지정된 속성(여기서는 attr)값이 배치된다.

#### 복잡한 서식 지정 코드

```python
>>> words = ['spam', 'ham', 'eggs']
>>> 'I like {0[2]}'.format(words)
'I like eggs'
>>> person = {'twitter':'makingfunk', 'name':'doky'}
>>> 'My name is {person[name]}'.format(person=person)
'My name is doky'
>>> from datetime import datetime
>>> now = datetime.now()
>>> 'Today is {0.year}-{0.month}-{0.day}'.format(now)
'Today is 2017-10-6'
```

### 포맷 지정 방법
서식을 지정할 때 문자열 변환을 위한 포맷을 함게 지정할 수 있습니다. 예를 들어, 문자열로 변환할 때 수치 자릿수를 지정하거나, 공백을 메우는 등, 레이아웃을 조정할 수 있습니다. 이러한 포맷은 콜론(:)의 뒤에 지정합니다.

#### 포맷 지정 방법

형식|설명
---|---
:<30:>30:^30 | 지정한 폭(여기에서는 30)으로 왼쪽 맞춤, 오른쪽 맞춤, 가운데 맞춤
:-<30:->30:^-30 | 왼쪽 맞춤, 오른쪽 맞춤, 가운데 맞춤에서 공백(스페이스)을 지정한 문자(여기에서는 -)로 매운다.
:b :o :d :x :X | 2진수, 8진수, 10진수, 16진수(소문자), 16진수(대문자)로 변환한다.
:f | 고정소수점 수의 문자열로 변환한다.
:% | 백분율 표기로 변환한다.
:, | 수치에 세 자리마다 쉼표(,)를 삽입한다.
:6.2f | 표시할 자릿수를 지정한다. 6은 전체 자릿수, 2는 소수점 이하 자릿수를 나타낸다.
:%Y-%m-%d-%H:%M:%S | 날짜 형식 특유의 서식으로, 연월일 등으로 변환한다.

#### 포맷 지정 샘플 코드

```python
>>> import math
>>> '|{:<30}|'.format('left align')
'|left align                    |'
>>> '|{:>30}|'.format('right align')
'|                   right align|'
>>> '|{:^30}|'.format('center')
'|            center            |'
>>> '{:-^30}'.format('center')
'------------center------------'
>>> '{0:b} {0:o} {0:d} {0:x} {0:X}'.format(1000)
'1111101000 1750 1000 3e8 3E8'
>>> '{0} {0:f}'.format(math.pi)
'3.141592653589793 3.141593'
>>> '{:%}'.format(0.045)
'4.500000%'
>>> '{:,}'.format(10000000000000)
'10,000,000,000,000'
>>> '{:4.2f} {:2.2%}'.format(math.pi, 0.045)
'3.14 4.50%'
>>> from datetime import datetime
>>> now = datetime.now()
>>> 'Today is {:%Y-%m-%d}'.format(now)
'Today is 2017-10-06'
>>> 'Current time is {:%H:%M:%S}'.format(now)
'Current time is 03:19:31'
```

서식 지정에 대한 자세한 내용은 공식 문서의 "Format String Syntax"를 참고하세요.

### 기타 문자열 메서드
앞에서 설명하지는 않았지만 자주 쓰이는 문자열 메서드에 대해 다룹니다.

#### 기타 문자열 메서드

메서드 이름 | 설명 | 반환값
---|---|---
find(sub[,start[,end]]) | 문자열 중에 sub이 존재하는 위치를 반환한다. 없으면 -1을 반환한다. | int
split(sep=None,maxsplit=-1) | 문자열을 분할한다. 기본으로는 공백 문자로 분할한다. | list
join(iterable) | 인수로 지정된 여러 문자열을 결합한다. | str
startswith(prefix[,start[,end]]) | 지정된 접두사를 가진 문자열을 검색한다. prefix에는 튜플로 여러 개의 후보를 지정할 수 있다. start, end는 조사할 위치 지정에 사용한다. | bool
endswith(suffix[,start[,end]]) | 지정된 접미사를 가진 문자열을 검색한다. suffix에는 튜플로 여러 개의 후보를 지정할 수 있다. start, end는 조사할 위치 지정에 사용한다. | bool
encode(encoding="utf-8", errors="strict") | 문자열을 지정한 인코딩 형식으로 변환한다. errors에는 변환 불가능한 문자열이 있을 때 대응 방법을 기술한다. strict이면 오류가 발생하며, ignore이면 해당 문자를 무시하고, replace이면 ?로 변환한다. | bytes

#### 기타 문자열 메서드 사용 예

```python
>>> 'python'.find('th')
2
>>> 'python'.find('TH')
-1
>>> words = '''Beautiful is better than ugly.
... Explicit is better than implicit.'''.split()
>>> words
['Beautiful', 'is', 'better', 'than', 'ugly.', 'Explicit', 'is', 'better', 'than', 'implicit.']
>>> '-'.join(wordsd[:5]) # 리스트를 -로 연결
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'wordsd' is not defined
>>> '-'.join(words[:5])
'Beautiful-is-better-than-ugly.'
>>> 'python'.startswith('py')
True
>>> image_suffix = ('jpg', 'png', 'gif') # 이미지 파일의 확장자로 튜플을 정의
>>> 'image.png'.endswith(image_suffix)
True
>>> 'text.txt'.endswith(image_suffix)
False
>>> text = '가abcd나'
>>> text.encode('ascii') # 한국어가 섞인 문자열을 ascii로 인코딩
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeEncodeError: 'ascii' codec can't encode character '\uac00' in position 0: ordinal not in range(128)
>>> text.encode('ascii','ignore') # 한국어를 무시
b'abcd'
>>> text.encode('ascii', 'replace') # 한국어를 ?로 변환
b'?abcd?'
```

### 문자열 상수 이용하기
string 모듈에는 몇 가지 문자열 상수가 정의되어 있습니다.

#### string 모듈 상수

상수 이름 | 설명
---|---
string.ascii_lowercase | 영문 소문자(abcdefghijklmnopqrstuvwxyz)
string.ascii_uppercase | 영문 대문자(ABCDEFGHIJKLMNOPQRSTUVWXYZ)
string.ascii_letters | 소문자와 대문자를 합친 영문자 전체
string.digits | 10진수 숫자(0123456789)
string.hexdigits | 16진수 숫자(0123456789abcdefABCDEF)
string.octdigits | 8진수 숫자(01234567)
string.punctuation | 기호 문자열(!"#$%&'()\*+,-./:;<=>?@[\]^\_'{\|}~)
string.whitespace | 공백으로 취급되는 문자열(\t\n\r\x0b\x0c)
string.printable | ascii_letter, digits, punctuation, whitespace를 포함한 문자열

#### 문자열 상수 이용 예
```python
>>> import string
>>> 'a' in string.ascii_lowercase # 소문자인지 검사
True
>>> 'a' in string.ascii_uppercase # 대문자인지 검사
False
```
