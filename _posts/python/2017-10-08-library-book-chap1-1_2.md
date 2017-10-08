---
layout: post
section-type: post
title: Python Library - chap 1. 텍스트 처리하기 - 1.2 정규 표현 다루기
category: python
tags: [ 'python' ]
---
정규 표현을 처리하는 모듈 re에 대해 다룹니다.  

## 기본 함수

### re.search() 함수

형식 | re.search(pattern, strisssng, flags=0)
---|---
설명 | 지정된 문자열이 정규 표현이 일치하는지 확인한다.
인수 | pattern - 정규 표현 문자열을 지정한다.<br> string - 정규 표현에 일치하는지 확인할 문자열을 지정한다. <br> flags - 정규 표현을 컴파일할 때, 동작을 변경하는 플래그를 지정한다.
반환값 | 일치하면 매치 객체를 반환하고, 일치하지 않으면 None을 반환한다.

### re.match() 함수

형식 | re.match(pattern, string, flags=0)
---|---
설명 | 지정된 문자열이 정규 표현에 일치하는지 확인한다. search()와는 다르게 문자열의 맨 앞글자부터 일치하는지 확인한다.

### 기본적인 정규 표현의 매치 처리

```python
>>> import re
>>> re.match('a.c','abc') # 일치하면 매치 객체를 반환한다.
<_sre.SRE_Match object; span=(0, 3), match='abc'>

>>> re.search('a.c', 'abc') # 일치하면 매치 객체를 반환한다.
<_sre.SRE_Match object; span=(0, 3), match='abc'>

>>> re.match('b', 'abc') # match는 맨 앞글자를 확인하므로 일치하지 않는다.
>>> re.search('b', 'abc') # search에는 일치한다.
<_sre.SRE_Match object; span=(1, 2), match='b'>
```

## re 모듈의 상수(플래그)
re 모듈에는 정규 표현을 컴파일할 때 지정하는 플래그가 상수로 준비되어 있습니다. 플래그에는 한 문자로 이루어진 것(A,B 등)과 플래그의 뜻을 나타내는 단어인 것(ASCII 등), 두 종류가 있습니다.  

주요 플래그를 정리하면 다음과 같습니다. OR(|) 연산자를 사용해 여러 개의 플래그를 조합할 수도 있습니다.

### re 모듈의 상수(플래스)

상수 이름 | 설명
---|---
A 또는 ASCII | \w 등의 매치 처리에서 ASCII 문자만을 사용한다.
I 또는 IGNORECASE | 대소문자를 구별하지 않고 매치한다.
M 또는 MULTILINE | ^와 $를 각 행의 맨 처음과 맨 끝에 매치한다.
S 또는 DOTALL | 점(.)을 줄바꿈까지 포함하여 매치한다.

### 플래그 샘플 코드

```python
>>> re.search('\w', '가나다라마ABC')
<_sre.SRE_Match object; span=(0, 1), match='가'>

>>> re.search('\w', '가나다라마ABC', flags=re.A) # ASCII 문자만 매치
<_sre.SRE_Match object; span=(5, 6), match='A'>

>>> re.search('[abc]+', 'ABC', re.I) # 대소문자 무시
<_sre.SRE_Match object; span=(0, 3), match='ABC'>

>>> re.match('a.c', 'A\nC', re.I)
>>> re.match('a.c', 'A\nC', re.I | re.S) # 여러 개의 플래그 지정
<_sre.SRE_Match object; span=(0, 3), match='A\nC'>
```

## 정규 표현 객체

### re.compile() 메서드

형식 | re.compile(pattern, flags=0)
---|---
설명 | 지정된 정규 표현을 컴파일하여 정규 표현 객체를 반환한다.
인수 | pattern - 정규 표현 문자열을 지정한다.<br>flags - 정규 표현을 컴파일할 때, 동작을 변경하는 플래그를 지정한다.
반환값 | 정규 표현 객체

모든 메서드는 re.메서드_이름(pattern, 그_외_인수) 형식으로도 호출할 수 있습니다.

### 정규 표현 객체 메서드

메서드 이름 | 설명 | 반환값
---|---|---
search(string[,pos[,endpos]]) | 지정한 문자열이 정규 표현에 일치하는지를 반환한다. pos, endpos는 처리할 위치를 나타낸다. | 매치 객체 또는 None
match(string[,pos[,endpos]]) | 지정한 문자열이 정규 표현에 일치하는지를 반환한다. search()와는 달리, 맨 처음부터 일치하는지 확인한다. | 매치 객체 또는 None
fulmatch(string[,pos[,endpos]]) | 지정한 문자열 전체가 정규 표현에 일치하는지를 반환한다. | 매치 객체 또는 None
split(string[,maxsplit=0]) | 지정한 문자열을 정규 표현 패턴에 일치하는지 문자열로 분할한다. maxsplit은 분할할 최대 개수이다. | 문자열의 list
sub(repl, string, count=0) | 문자열 안의 정규 표현 패턴에 일치한 문자열을 repl로 치환한다. count는 변환하는 상한을 지정한다. | str
findall(string[,pos[,endpos]) | 지정한 문자열 안의 정규 표현에 일치한 문자열을 리스트로 반환한다. | 문자열의 list
finditer(string[,pos[,endpos]]) | 지정한 문자열 안의 정규 표현에 일치한 매치 객체를 반복자(iterator)로 반환한다. | 매치 객체 또는 None

### 정규 표현 객체 메서드의 샘플 코드

```python
>>> regex = re.compile('[a-n]+') # a-n 범위의 영어 소문자에 매치
>>> type(regex)
<class '_sre.SRE_Pattern'>

>>> regex.search('python') # h 문자에 일치
<_sre.SRE_Match object; span=(3, 4), match='python'>

>>> regex.match('python') # 맨 앞글자가 일치하지 않으므로 None을 반환
>>> regex.fullmatch('eggs') # 문자열 전체과 일치하는지 검사
>>> regex.fullmatch('egg')
<_sre.SRE_Match object; span=(0, 3), match='egg'>

>>> regex2 = re.compile('[-+()]') # 전화번호에 사용되는 기호 패턴 정리
>>> regex2.split('080-1234-5678')
['080', '1234', '5678']

>>> regex2.split('(080)1234-5678')
['', '080', '1234', '5678']

>>> regex2.split('+81-80-1234-5678')
['', '81', '80', '1234', '5678']

>>> regex2.sub('', '+81-80-1234-5678') # 기호를 삭제한다.
'818012345678'

>>> regex3 = re.compile('\d+') # 문자 한개 이상으로 된 숫자의 정규 표현
>>> regex3.findall('080-1234-5678')
['080', '1234', '5678']

>>> for m in regex3.finditer('+81-80-1234-5678'):
...     m
...
<_sre.SRE_Match object; span=(1, 3), match='81'>
<_sre.SRE_Match object; span=(4, 6), match='80'>
<_sre.SRE_Match object; span=(7, 11), match='1234'>
<_sre.SRE_Match object; span=(12, 16), match='5678'>
```

## 매치 객체
re.match(), re.search() 등에서 정규 표현에 일치한 문자열에 관한 정보는 저장하는 객체입니다.

### group() 메서드

형식 | group([group1,...])
---|---
설명 | 지정한 서브 그룹에 일치한 문자열을 반환한다. 여러 개의 서브 그룹을 지정할 떄는 문자열을 튜플로 반환한다. 서브 그룹을 나타내는 숫자 또는 그룹 이름을 인수로 지정한다. 인수로 지정하지 않으면 0과 마찬가지로 일치한 문자열 전체를 반환한다.
인수 | group1 - 서브 그룹을 숫자 또는 서브 그룹 이름으로 지정한다.
반환값 | 문자열 또는 문자열의 튜플

### group() 샘플 코드

```python
>>> regex = re.compile('(\d+)-(\d+)-(\d+)') # 전화번호의 정규 표현
>>> m = regex.match('080-1234-5678')
>>> m.group() # 일치한 문자열 전체를 얻음
'080-1234-5678'

>>> m.group(1), m.group(2), m.group(3) # 각 서브 그룹의 문자열을 얻음
('080', '1234', '5678')

>>> regex2 = re.compile(r'(?P<first>\w+) (?P<last>\w+)') # 이름을 구하는 정규 표현

>>> m2 = regex2.match('Making funk: PyCon KR Chair')
>>> m2.group(0) # 일치한 문자열 전체를 얻음
'Making funk'

>>> m2.group('first'), m2.group('last') # 서브 그륩을 그룹 이름으로 지정
('Making', 'funk')
```

### 매치 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
groups(default=None) | 패턴에 일치한 서브 그룹의 문자열을 튜플로 반환한다. default에는 일치하는 문자열이 존재하지 않을 때의 반환값을 지정한다. | tuple
groupdict(default=None) | 패턴에 일치한 서브 그룹을 dict 형식으로 반환한다. default에는 일치하는 문자열이 존재하지 않을 때의 반환값을 지정한다. | dict
expand(template) | template 문자열에 대하여 \1 또는 \g<name> 의 형식으로 서브 그룹을 지정하면, 일치한 문자열로 치환된다. | str

### 매치 객체의 샘플 코드

```python
>>> import re
>>> regex = re.compile(r'(?P<first>\w+) (?P<last>\w+)')
>>> m = regex.match('Kim Doky: #making funk')
>>> m.groups() # 일치한 문자열을 모두 얻음
('Kim', 'Doky')

>>> m.groupdict() # 일치한 문자열을 dict형식으로 얻음
{'last': 'Doky', 'first': 'Kim'}

>>> m.expand(r'last: \2, first: \1') # expand를 사용하여 문자열을 반환
'last: Doky, first: Kim'

>>> m.expand(r'last: \g<last>, first: \g<first>')
'last: Doky, first: Kim'
```
