---
layout: post
section-type: post
title: Introducing Python - 데이터 주무르기
category: python
tags: [ 'python' ]
---

# Chap7. 데이터 주무르기

- **문자열** : 텍스트 데이터에 사용되는 **유니코드** 문자의 시퀀스
- **바이트와 바이트 배열** : 이진 데이터에 사용되는 8비트 정수의 시퀀스

## 7.1 텍스트 문자열

### 7.1.1 유니코드
- **유니코드** : 전 세계 언어의 문자를 정의하기 위한 국제 표준 코드
- 수학 및 기타 분야의 기호들도 포함

#### 파이썬 3 유니코드 문자열
파이썬 3 문자열은 바이트 배열이 아닌 유니코드 문자열이다. (파이썬2와 3의 가장 큰 차이점)  
파이썬 3는 일반적인 바이트 문자열과 유니코드 문자를 구별한다. 유니코드 식별자(ID) 혹은 문자에 대한 이름을 안다면, 이 문자를 파이썬 문자열에 사용할 수 있다.

- 4자리 16진수와 그 앞에 \u는 유니코드의 기본 평면 256개 중 하나의 문자를 지정한다. 첫 번째 두 숫자는 평면 번호이다(00~FF). 다음의 두 숫자는 평면에 있는 문자의 인덱스다. 평면 00은 아스키코드드이고, 평면 안의 문자 위치는 아스키코드의 번호와 같다.
- 높은 평면의 문자일수록 비트수가 더 필요하다. 이에 대한 파이썬의 이스케이프 시퀀스는 \U이고, 8리의 16진수를 사용한다. 숫자에 남는 공간이 있다면 왼쪽에 0을 채운다.
- 모든 문자는 표준 이름 \N{name}을 지정할 수 있다. 유니코드 문자 이름 인덱스 페이지에서 표준 이름 리스트를 참조한다.

파이썬의 `unicodedata` 모듈은 유니코드 식별자와 이름으로 검색할 수 있는 함수를 제공한다.

- **lookup()** : 대/소문자를 구분하지 않는 인자를 취하고, 유니코드 문자를 반환한다.
- **name()** : 인자로 유니코드 문자를 취하고, 대문자 이름을 반환한다.

```Python
def unicode_test(value):
    import unicodedata
    name = unicodedata.name(value)
    value2 = unicodedata.lookup(name)
    print('value="%s", name="%s", value2="%s"' % (value, name, value2))

# 아스키 문자를 테스트
>>> unicode_test('A')
value="A", name="LATIN CAPITAL LETTER A", value2="A"

# 아스키 문자 부호를 테스트
>>> unicode_test('$')
value="$", name="DOLLAR SIGN", value2="$"

# 유니코드 통화 문자
>>> unicode_test('\u00a2')
value="¢", name="CENT SIGN", value2="¢"
```

단 글꼴에 한계가 있다. 모든 글꼴은 유니코드에 대한 이미지를 가지고 있지 않으며, 일부 플레이스홀더 문자로 표시할 것이다. 예를 들어 딩벳 글꼴의 SNOWMAN에 대한 유니코드이다.

```Python
>>> unicode_test('\u2603')
value="☃", name="SNOWMAN", value2="☃"
```

é 와 같은 문자는 어떻게 할까? E에 대한 문자 인덱스를 찾으면, LATIN SMALL LETTER E WITH ACUTE 이름은 00e9 값을 가진다.

```Python
# 먼저 유니코드로 문자 이름을 얻는다.
>>> unicodedata.name('\u00e9')
'LATIN SMALL LETTER E WITH ACUTE'

# 이름으로 코드를 얻는다.
>>> unicodedata.lookup('LATIN SMALL LETTER E WITH ACUTE')
'é'
```

코드와 이름으로 문자열 café를 저장할 수 있다.

```Python
>>> place = 'caf\u00e9'
>>> print(place)
café
>>> place = 'caf\N{LATIN SMALL LETTER E WITH ACUTE}'
>>> print(place)
café
```

문자열 len 함수는 유니코드의 바이트가 아닌 **문자수** 를 센다.

```Python
>>> print(len('$'))
1
>>> print(len('\U0001f47b'))
1
```

#### UTF-8 인코딩과 디코딩

파이썬에서 일반 문자열을 처리할때는 각 유니코드 문자를 저장하는 방법엔 문제가 없지만, 외부 데이터를 교환할 때는 다음 과정이 필요하다.

- 문자열 -> 바이트 (**인코딩**)
- 바이트 -> 문자열 (**디코딩**)

유니코드는 문자의 식별자를 2바이트로 된 유니코드를 사용하지만, 그걸로는 모든 문자를 식별할 수 없다. 3 또는 4 바이트로 인코딩하면 메모리와 디스크 저장공간의 효율이 크게 떨어진다. 그래서 나온것이 **UTF-8** .
UTF-8은 유니코드 한 문자당 1~4 바이트를 사용한다.

- 1 바이트 : 아스키코드
- 2 바이트 : 키릴(Cyrillic)문자를 제외한 대부분의 파생된 라틴어
- 3 바이트 : 기본 다국어 평면의 나머지
- 4 바이트 : 아시아 언어 및 기호를 포함한 나머지

UTF-8은 파이썬, 리눅스, HTML의 표준 텍스트 인코딩이다.

##### 인코딩

인코딩 이름 | 설명
---|---
'ascii' | 7비트의 아스키코드
'utf-8' | 8비트 가변 길이 인코딩 형식, 거의 대부분의 문자 지원
'latin-1' | ISO 8859-1으로도 알려짐
'cp-1252' | 윈도우 인코딩 형식
'unicode-escape' | 파이썬 유니코드 리터럴 형식. \uxxxx 또는 \Uxxxxxxxx

```Python
>>> snowman = '\u2603'
# 한 문자의 파이썬 유니코드 문자열
# 내부적으로 몇 바이트가 저장되었는지 신경쓸 필요 없음
>>> len(snowman)
1

# UTF-8은 가변 길이 인코딩
# 유니코드 문자를 인코딩하기 위해 3바이트를 사용
>>> ds = snowman.encode('utf-8')
>>> len(ds)
3
>>> ds
b'\xe2\x98\x83'
```

UTF-8 이외의 다른 인코딩도 사용 가능
유니코드 문자열을 인코딩할 수 없다면 에러 발생.

```python
# 아스키 인코딩시, 유니코드 문자가 유효한 아스키 문자가 아닌경우
ds = snowman.encode('ascii')
UnicodeEncodeError                        Traceback (most recent call last)
<ipython-input-5-982044abb427> in <module>()
      1 # 아스키 인코딩시, 유니코드 문자가 유효한 아스키 문자가 아닌경우
----> 2 ds = snowman.encode('ascii')

UnicodeEncodeError: 'ascii' codec can't encode character '\u2603' in position 0: ordinal not in range(128)
```

`encode()` 함수는 인코딩 예외를 피하기 위해 두 번째 인자를 취한다. (기본값 : `strict`)  

```python
# `ignore`를 사용하여 알 수 없는 문자를 인코딩하지 않게 한다.
>>> snowman.encode('ascii', 'ignore')
b''
# 'replace'는 알 수 없는 문자를 ?으로 대체한다.
snowman.encode('ascii', 'replace')
b'?'
# 'backslashreplace'는 유니코드 이스케이프처럼 파이썬 유니코드 문자의 문자열을 만든다.
snowman.encode('ascii', 'backslashreplace')
b'\\u2603'
# 'xmlcharrefreplace'는 유니코드 이스케이프 시퀀스를 출력할 수 있는 문자열로 만든다.
snowman.encode('ascii', 'xmlcharrefreplace')
b'&#9731;'
```

##### 디코딩

외부 소스(파일, DB, API)에서 텍스트를 얻을 때마다 바이트 문자열로 인코딩되어 있다. 이 소스에서 실게 사용된 인코딩을 알기 위해, 인코딩 과정을 거꾸로 하여 유니코드 문자열을 얻을 수 있다.

바이트 문자열이 어떻게 인코딩 되어 있는지 알려주지 않는다. 예를 들어 웹사이트의 텍스트를 복사/붙여넣기 했을때 위험할 수 있다.

```Python
# 'café' 유니코드 문자열을 생성
>>> place = 'caf\u00e9'
>>> place
café
>>> type(place)
str

# UTF-8 형식의 place_bytes 라는 바이트 변수로 인코딩
>>> place_bytes = place.encode('utf-8')
>>> place_bytes
b'caf\xc3\xa9'
>>> type(place_bytes)
bytes
>>> len(place_bytes)
5
```

place_bytes는 5바이트로 되어있다. 첫 3바이트는 UTF-8과 똑같이 표현되는 아스키문자다.
마지만 2바이트로 é를 인코딩했다.

```Python
# 바이트 문자열을 유니코드 문자열로 디코딩
>>> place2 = place_bytes.decode('utf-8')
>>> place2
'café'
```

'café'를 UFT-8로 인코딩한 후, 한 번 더 UTF-8로 디코딩 했다.

```python
# 다른 인코딩 방식으로 디코딩한다면?
>>> place3 = place_bytes.decode('ascii')
UnicodeDecodeError                        Traceback (most recent call last)
<ipython-input-19-b2f66e476fde> in <module>()
----> 1 place3 = place_bytes.decode('ascii')

UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 3: ordinal not in range(128)
```

아스키 디코드는 예외를 일으킨다. 0xc3 바이트 값은 아스키코드에 유효하지 않기 때문이다.  
아스키코드는 128(16진수 80)에서 255(16진수 FF) 사이에 있는 값의 일부 8비트 문자 셋이 인코딩에 유효하지만, UTF-8과는 다르다.

```Python
>>> place4 = place_bytes.decode('latin-1')
>>> place4
'cafÃ©'
>>> place5 = place_bytes.decode('windows-1252')
>>> place5
'cafÃ©'
```
**가능 하면 UTF-8을 사용하라** . UTF-8은 모든 유니코드 문자를 표현할 수 있고, 어디에서나 지원한다. 디코딩과 인코딩을 빠르게 수행한다.

### 7.1.2 포맷
포맷은 보고서와 그 외의 정리된 출력물을 만들기 위해 사용한다.  

파이썬에는 옛 스타일과 새로운 스타일의 포매팅 문자열이 있다.

#### 옛 스타일 : %

- 형식 : `string % data`
- 문자열 안에 끼워 넣을 데이터를 표시하는 형식

기호 | 설명
---|---
%s | 문자열
%d | 10진 정수
%x | 16진 정수
%o | 8진 정수
%f | 10진 부동소수점수
%e | 지수로 나타낸 부동소수점수
%g | 10진 부동소수점수 혹은 지수로 나타낸 부동소수점수
%% | 리터럴 %

```Python
# 정수 n, 부동소수점수 f, 문자열 s
>>> n = 42
>>> f = 7.03
>>> s = 'string'

# 기본 포맷 출력
>>> '%d %f %s' % (n, f, s)
'42 7.030000 string'

# 각 변수에 102ㅏ의 필드를 설정, 오른쪽 정렬
>>> '%10d %10f %10s' % (n, f, s)
'        42   7.030000     string'

# 왼쪽 정렬
>>> '%-10d %-10f %-10s' % (n, f, s)
'42         7.030000   string    '

# 최대 문자 길이가 4, 오른쪽 정렬
# 이 설정은 문자열을 잘라내고, 소수점 이후의 숫자 길이를 4로 제한한다.
>>> '%10.4d %10.4f %10.4s' % (n, f, s)
'      0042     7.0300       stri'

# 오른쪽 정렬
>>> '%.4d %.4f %.4s' % (n, f, s)
'0042 7.0300 stri'

# 하드코딩하지 않고, 인자로 필드 길이를 지정
>>> '%*.*d %*.*f %*.*s' % (10, 4, n, 10, 4, f, 10, 4, s)
'      0042     7.0300       stri'
```

#### 새로운 스타일의 포매팅  : {}와 format

```Python
# 기본 사용법
>>> '{} {} {}'.format(n, f, s)
'42 7.03 string'

# 새로운 스타일에서 순서 지정
# 0은 첫 번째 인자인 부동소수점수 f, 1은 문자열 s, 2는 마지막 인자인 정수 n을 참조
>>> '{2} {0} {1}'.format(f, s, n)
'42 7.03 string'

# 인자는 딕셔너리 혹은 이름을 지정한 인자가 될 수 있다.
>>> '{n} {f} {s}'.format(n=42, f=7.03, s='string')
'42 7.03 string'

# 0은 딕셔너리 전체, 1은 딕셔너리 다음에 오는 문자열
>>> d = {'n':42, 'f':7.03, 's':'string'}
'{0[n]} {0[f]} {0[s]} {1}'.format(d, 'other')
'42 7.03 string other'

# 타입 지정자는 ':' 다음에 입력한다.
>>> '{0:d} {1:f} {2:s}'.format(n, f, s)
'42 7.030000 string'

>>> '{n:d} {f:f} {s:s}'.format(n=42, f=7.03, s='stirng')
'42 7.030000 stirng'

# 다른 옵션(최소 필드 길이, 최대 문자 길이, 정렬 등)
# 최소 필드 길이 10, 오른쪽 정렬(기본값)
# 문자열은 왼쪽 정렬이 기본값인듯 하다.
>>> '{0:10d} {1:10f} {2:10s}'.format(n, f, s)
'        42   7.030000 string    '
# '>'는 오른쪽 정렬을 더 명확히 한다.
>>> '{0:>10d} {1:>10f} {2:>10s}'.format(n, f, s)
'        42   7.030000     string'
# 왼쪽 정렬
>>> '{0:<10d} {1:<10f} {2:<10s}'.format(n, f, s)
'42         7.030000   string    '

# 중앙 정렬
>>> '{0:^10d} {1:^10f} {2:^10s}'.format(n, f, s)
'    42      7.030000    string  '

# 정밀(percision)값은 예 스타일과 같이 소수부 숫자의 자릿수와 문자열의 최대 문자수를 의미
# 새로운 스타일에서는 이것을 정수에 사용할 수 없다.
>>> '{0:>10.4d} {1:>10.4f} {2:10.4s}'.format(n, f, s)
ValueError                                Traceback (most recent call last)
<ipython-input-55-f52a97892439> in <module>()
----> 1 '{0:>10.4d} {1:>10.4f} {2:10.4s}'.format(n, f, s)

ValueError: Precision not allowed in integer format specifier

>>> '{0:>10d} {1:>10.4f} {2:>10.4s}'.format(n, f, s)
'        42     7.0300       stri'

# ':' 이후에, 정렬(>,<,^) 혹은 길이 지정자 이전에 채워 넣고 싶은 문자를 입력
>> '{0:!^20s}'.format('BIGGG')
'!!!!!!!BIGGG!!!!!!!!'
 ```

### 7.1.3 정규표현식

정규표현식은 표준 모듈 `re`를 사용한다. 원하는 문자열 **패턴** 을 정의하여 소스 문자열과 일치하는지 비교한다.

```Python
>>> import re
# match의 첫 번째 인자는 패턴이고, 두 번째 인자는 문자열 소스이다.
>>> result = re.match('You', 'Young Frankenstein')
>>> print(result)
<_sre.SRE_Match object; span=(0, 3), match='You'>
# 추후에 패턴 확인을 빠르게 하기 위해 패턴을 먼저 컴파일할 수 있다.
>>> youpattern = re.compile('You')
>>> result = youpattern.match('Young Frankenstein')
>>> print(result)
<_sre.SRE_Match object; span=(0, 3), match='You'>
```

#### 다른 메서드들

- search() : 첫 번째 일치하는 객체를 반환한다.
- findall() : 중첩에 상관없이 모두 일치하는 문자열 리스트를 반환한다.
- split() : 패턴에 맞게 소스를 쪼갠 후 문자열 조각의 리스트를 반환한다.
- sub() : 대체 인자를 하나 더 받아서 패턴과 일치하는 모든 소스 부분을 대체 인자로 변경한다.

##### 시작부터 일치하는 패턴 찾기: match()

```Python
>>> import re
>>> source = 'Young Frankenstein'
# match는 소스의 시작부터 패턴이 일치하는지 확인한다.
>>> m = re.match('You', source)
>>> if m:  # match는 객체를 반환한다. 무엇이 일치하는지 보기 위한 작업이다.
>>>     print(m.group())
You
# 문자열이 You로 시작하는지 확인한다.
>>> m = re.match('^You', source)
>>> if m:
>>>     print(m.group())
You
# match()는 패턴이 소스의 처음에 있는 경우에만 작동하기 때문에, Frank는 작동하지 않는다.
>>> m = re.match('Frank', source)
>>> if m:
>>>     print(m.group())
# search()는 패턴이 아무데나 있어도 작동한다.
>>> m = re.search('Frank', source)
>>> if m:
>>>     print(m.group())
Frank
# 패턴을 바꿔서 작동 시키기
>>> m = re.match('.*Frank', source)
>>> if m:
>>>     print(m.group())
Young Frank
# .는 **한 문자** 를 의미한다.
# *는 이전 패턴이 여러 개 올 수 있다는 것을 의미한다.
# *는 0회 이상의 문자가 올 수 있다는 것을 의미한다.
```

#### 첫 번째 일치하는 패턴 찾기: search()
`.*` 와일드카드 없이 'Young Frankenstein' 소스 문자열에서 'Frank' 패턴을 찾기 위해 `search()`를 사용할 수 있다.

```Python
>>> m = re.search('Frank', source)
>>> if m:
>>>     print(m.group())
Frank
```

#### 일치하는 모든 패턴 찾기: findall()

```Python
# 문자열에서 n의 갯수 찾기
>>> m = re.findall('n', source)
>>> m
['n', 'n', 'n', 'n']
>>> print('Found', len(m), 'matches')
Found 4 matches
# n 다음 문자가 오는지 찾기
# .은 한 문자를 의미
# ?는 0 또는 1회를 의미
# .? 는 하나의 문자가 0 또는 1회 올 수 있다는 의미
>>> m = re.findall('n.', source)
>>> m
['ng', 'nk', 'ns'] # 마지막 n이 포함되지 않는다.
>>> m = re.findall('n.?', source)
>>> m
['ng', 'nk', 'ns', 'n']
```

#### 패턴으로 나누기: split()
지정한 패턴으로 문자열을 리스트로 나눈다.

```Python
>>> m = re.split('n', source)
>>> m
['You', 'g Fra', 'ke', 'stei', '']
```

#### 일치하는 패턴 대체하기: sub()

문자열 `replace()` 메서드와 비슷하지만, 리터럴 문자열이 아닌 패턴을 사용한다.

```Python
>>> m = re.sub('n', '?', source)
>>> m
'You?g Fra?ke?stei?'
```

#### 패턴: 특수 문자

- 리터럴은 모두 비특수 문자와 일치한다.

패턴 | 일치 / 설명
---|---
. | \n을 제외한 하나의 문자
* | 0회 이상
? | 0 또는 1회
\d | 숫자
\D | 비숫자
\w | 알파벳 문자
\W | 비알파벳 문자
\s | 공백 문자
\S | 비공백 문자
\b | 단어 경계(\w와 \W 또는 \W와 \w 사이의 경계)
\B | 비단어 경계

string 모듈의 printable에는 알파벳 대/소문자, 숫자, 공백, 구두점을 포함한 100가지 아스키 문자가 포함되어 있다.

```Python
>>> import string
>>> printable = string.printable
>>> len(printable)
100
>>> printable[0:50]
'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN'
>>> printable[50:]
'OPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
# 숫자
>>> re.findall('\d', printable)
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# 숫자, 문자, 언더스코어
>>> re.findall('\w', printable)
['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd','e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_']
# 공백 문자
 >>> re.findall('\s', printable)
 [' ', '\t', '\n', '\r', '\x0b', '\x0c']
```

\d는 아스키 문자 '0'에서 '9'뿐만 아니라 유니코드가 정의하는 숫자도 될 수 있다.

```Python
>>> x = 'abc' + '-/*' + '\u00ea' + '\u0115'
>>> re.findall('\w', x)
['a', 'b', 'c', 'ê', 'ĕ']
```

#### 패턴: 지정자

패턴 | 일치
---|---
abc | 리터럴 abc
( expr ) | expr
expr1 \| expr2 | expr1 또는 expr2
. | \n을 제외한 모든 문자
^ | 소스 문자열의 시작
$ | 소스 문자열의 끝
prev ? | 0 또는 1회의 prev
prev* | 0회 이상의 최대 prev
prev*? | 0회 이상의 최소 prev
prev+ | 1회 이상의 최대 prev
prev+? | 1회 이상의 최소 prev
prev {m} | m회의 prev
prev {m, n} | m에서 n회의 최대 prev
prev {m, n}? | m에서 n회의 최소 prev
[abc] | a 또는 b 또는 c
[^abc] | (a 또는 b 또는 c)가 아님
prev (?=next) | 뒤에 next가 오면 prev
prev (?!next) | 뒤에 next가 오지 않으면 prev
(?<=prev) next | 전에 prev가 오면 next
(?<!prev) next | 전에 prev가 오지 않으면 next

> expr은 표현식, prev는 이전 토큰, next는 다음 토큰을 의미한다.

```Python
# 테스트 할 문자열을 지정
>>> source = '''I wish I may, I wish I might
            Have a dish of fish tonight.'''
# wish 찾기
>>> re.findall('wish', source)
['wish', 'wish']
# wish 또는 fish 찾기
>>> re.findall('wish|fish', source)
['wish', 'wish', 'fish']
# wish로 사작하는지 찾기
>>> re.findall('^wish', source)
[]
# I wish로 시작하는지 찾기
>>> re.findall('^I wish', source)
['I wish']
# fish로 끝나는지 찾기
>>> re.findall('fish$', source)
[]
# fish tonight. 으로 끝나는지 찾기
>>> re.findall('fish tonight.$', source)
['fish tonight.']

# `^`와 `$`는 **앵커(anchor)** 라고 한다.
# `^`는 검색 문자열의 시작 위치에, `$`는 검색 문자열의 마지막 위치에 고정한다.
# `.$`는 가장 마지막에 있는 한 문자와 `.`을 매칭한다 더 정확하게 하려면 문자 그대로 매칭하기 위해 `.`에 이스케이프 문자를 붙여야 한다.
>>> re.findall('fish tonight\.$', source)
['fish tonight.']
# w 또는 f 다음에 ish가 오는 단어 찾기
>>> re.findall('[wf]ish', source)
['wish', 'wish', 'fish']
# w,s,h가 하나 이상인 단어 찾기
>>> re.findall('[wsh]+', source)
['w', 'sh', 'w', 'sh', 'h', 'sh', 'sh', 'h']
# ght 다음에 비알파벳 문자가 나오는 단어 찾기
>>> re.findall('ght\W', source)
['ght\n', 'ght.']
# wish 이전에 나오는 I 찾기
>>> re.findall('I (?=wish)', source)
['I ', 'I ']
# I 다음에 나오는 wish 찾기
>>> re.findall('(?<=I) wish', source)
[' wish', ' wish']
```

정규표현식 패턴이 파이썬 문자열 규칙과 충돌하는 경우들이 있다.

```Python
>>> re.findall('\bfish', source)
[]
```
파이썬은 문자열에 대해 몇 가지 특별한 이스케이프 문자를 사용한다. 예를 들어 `\b`는 백스페이스를 의미하지만, 정규표현식에서는 단어의 시작 부분을 의미한다. 정규표현식의 패턴을 입력하기 전에 항상 문자 `r`(raw string)을 입력해야 한다. 그러면 파이썬의 이스케이프 문자를 사용할 수 없게되어 충돌을 피할 수 있다.

```python
>>> re.findall(r'\bfish', source)
['fish']
```

#### 패턴: 매칭 결과 지정하기

`match()` 또는 `search()`를 사용할 때 모든 매칭을 m.group()과 같이 객체 m으로부터 결과를 반환한다. 만약 패턴을 괄호로 둘러싸는 경우, 매칭은 그 괄호만의 그룹으로 저장된다. `m.groups()`를 사용하여 그룹의 튜플을 출력한다.

```Python
>>> m = re.search(r'(. dish\b).*(\bfish)', source)
>>> m.group()
'a dish of fish'
>>> m.groups()
('a dish', 'fish')
# (?P< name > expr ) 패턴을 사용한다면, 표현식(expr)이 매칭되고, 그룹 이름(name)의 매칭 내용이 저장된다.
>>> m = re.search(r'(?P<DISH>. dish\b).*(?P<FISH>\bfish)', source)
>>> m.group()
'a dish of fish'
>>> m.groups()
('a dish', 'fish')
>>> m.group('DISH')
'a dish'
>>> m.group('FISH')
'fish'
```

## 7.2 이진 데이터

이진 데이터를 다루기 위해 **엔디안(endian. 컴퓨터 프로세서가 데이터를 바이트로 나누는 방법)**와 정수에 대한 **사인 비트(sign bit)** 개념을 알아야 한다. 그리고 데이터를 추출하거나 변경하는 바이너리 파일 형식과 네트워크 패킷을 배워야 한다. (여기서는 이진 데이터에 대한 기초만 살펴본다.)

### 7.2.1 바이트와 바이트 배열

- **바이트(byte)**는 바이트의 튜플처럼 불변한다.
- **바이트 배열(byte array)**은 바이트의 리스트처럼 변경 가능하다.

```Python
# blist : 리스트 변수
# the_bytes : 바이트 변수
# the_byte_array : 바이트 배열 변수
>>> blist = [1,2,3,255]
>>> the_bytes = bytes(blist)
>>> the_bytes
b'\x01\x02\x03\xff'
>>> the_byte_array = bytearray(blist)
>>> the_byte_array
bytearray(b'\x01\x02\x03\xff')

# 바이트 변수는 불변
>>> the_bytes[1] = 127
Traceback (most recent call last)
<ipython-input-3-ae169b50bd40> in <module>()
      1 # 바이트 변수는 불변
----> 2 the_bytes[1] = 127

TypeError: 'bytes' object does not support item assignment

# 바이트 배열 변수는 변경 가능
>>> the_byte_array = bytearray(blist)
>>> the_byte_array
bytearray(b'\x01\x02\x03\xff')
>>> the_byte_array[1] = 127
>>> the_byte_array
bytearray(b'\x01\x7f\x03\xff')
```

```Python
# 0에서 255까지의 결과를 생성
>>> the_bytes = bytes(range(0, 256))
>>> the_byte_array = bytearray(range(0, 256))

# 바이트 혹은 바이트 배열 데이터를 출력할 때, 파이썬은 출력할 수 없는 바이트에 대해서는 \xxx를 사용하고, 출력할 수 있는 바이트에 대해서는 아스키코드 값을 사용한다.
>>> the_bytes
b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
```

### 7.2.2 이진 데이터 변환하기: struct

파이썬 표준 라이브러리는 C와 C++의 구조체와 유사한, 데이터를 처리하는 `struct` 모듈이 있다. `struct`를 사용하면 이진 데이터를 파이썬 데이터 구조로 바꾸거나 파이썬 데이터 구조를 이진 데이터로 바꿀 수 있다.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/O_Reilly_Media_logo.svg/1920px-O_Reilly_Media_logo.svg.png)

PNG 데이터에서 이미지의 가로와 세로의 길이를 추출하는 프로그램으로 데이터를 어떻게 처리하는지 다룬다.

```Python
>>> import struct
>>> png = open('chap7_oreilly.png', 'rb')
>>> png.read()
b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x07\x80\x00\x00\x01\xa1\x08\x06\x00\x00\x00\x80\x82\xa9o\x00\x00\x00\x06bKGD\x00\xff\x00\xff ...
>>> png.close()
>>> valid_png_header = b'\x89PNG\r\n\x1a\n'
>>> data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + \
 b'\x00\x00\x07\x80\x00\x00\x01\xa1\x08'
>>> if data[:8] == valid_png_header:
...     width, height = struct.unpack('>LL', data[16:24])
...     print('Valid PNG, width', width, 'height', height)
... else:
...     print('Not a valid PNG')
Valid PNG, width 1920 height 417
```

- data는 PNG 파일의 첫 30바이트를 포함한다.
- valid_png_header는 유효한 PNG 파일의 시작을 표시하는 8바이트의 시퀀스를 포함한다.
- width는 16~20바이트에서 추출하고, height는 21~24바이트에서 추출되었다.

`unpack()`에서 `>LL`은 입력한 바이트 시퀀스를 해석하고, 파이썬의 데이터 형식으로 만들어주는 형식 문자열이다.

- `>`는 정수가 **빅엔디안** 형식으로 저장되었다는 것을 의미한다.
- 각각의 `L`은 4바이트의 부호 없는 긴 정수를 지정한다.

각 4바이트 값을 직접 볼 수 있다.

```Python
>>> data[16:20]
b'\x00\x00\x07\x80'
>>> data[20:24]
b'\x00\x00\x01\xa1'
```

빅엔디안 정수는 왼쪽에서부터 최상위 바이트가 저장된다. 255 이상이므로 뒤에서 두 번째 바이트와 일치한다.

```Python
# 16진수 값이 예상한 10진수 값과 맞는지 확인
>>> 0x0780
1920
>>> 0x01a1
417
# struct 모듈의 pack() 함수로 파이썬 데이터를 바이트로 변환할 수 있다.
>>> import struct
>>> struct.pack('>L', 1920)
b'\x00\x00\x07\x80'
>>> struct.pack('>L', 417)
b'\x00\x00\x01\xa1'
```

##### 엔디안 지정자

지정자 | 바이트 순서
---|---
< | 리틀엔디안
> | 빅엔디안

##### 형식 지정자

지정자 | 설명 | 바이트
---|---|---
x | 1바이트 건너뜀 | 1
b | 부호 있는 바이트 | 1
B | 부호 없는 바이트 | 1
h | 부호 있는 짧은 정수 | 2
H | 부호 없는 짧은 정수 | 2
i | 부호 있는 정수 | 4
I | 부호 없는 정수 | 4
l | 부호 있는 긴 정수 | 4
L | 부호 없는 긴 정수 | 4
Q | 부호 없는 아주 긴 정수 | 8
f | 단정도 부동소수점수 | 4
d | 배정도 부동소수점수 | 8
p | 문자수(count)와 문자 | 1 + count
s | 문자 | count

타입 지정자는 엔지안 문자를 따른다. 어떤 지정자는 문자수를 가리키는 숫자가 선행될 수 있다.(ex. 5B -> BBBBB)

`>LL`을 count로 선행하여 `>2L`으로 지정할 수 있다.

```Python
>>> struct.unpack('>2L', data[16:24])
(1920, 417)
```

`x` 지정자를 사용하여 필요없는 부분을 건너뛸 수 있다.

```Python
>>> struct.unpack('>16x2L6x', data)
(1920, 417)
```

- 빅엔디안 정수 형식 사용함(>)
- 16바이트를 건너뜀(16x)
- 두 개의 부호 없는 긴 정수의 8바이트를 읽음(2L)
- 마지막 6바이트를 건너뜀(6x)

### 7.2.3 기타 이진 데이터 도구

이진 데이터를 정의하고 추출하는 써드파티 오픈소스 패키지

- bitstring
- construct
- hachoir
- binio

construct의 예제이다.
> 책의 예제에 있는 construct의 버전과 현재의 버전 차이가 많이 나서 예제에 나온 메서드들은 대부분 사라졌다.

```Python
>>> from construct import Const, Int8ub, Array, this, Byte, Struct

>>> fmt = Struct(
...     "signature" / Const(b"BMP"),
...     "width" / Int8ub,
...     "height" / Int8ub,
...     "pixels" / Array(this.width * this.height, Byte),
... )
>>> data = format.build(dict(width=3,height=2,pixels=[7,8,9,11,12,13]))
>>> print(data)
b'BMP\x03\x02\x07\x08\t\x0b\x0c\r'
>>> fmt.parse(data)
>>> Container(signature=b'BMP', width=3, height=2, pixels=ListContainer([7, 8, 9, 11, 12, 13]))
>>> result = fmt.parse(data)
>>> print(result)
Container:
    signature = b'BMP' (total 3)
    width = 3
    height = 2
    pixels = ListContainer:
        7
        8
        9
        11
        12
        13
```

### 7.2.4 바이트/문자열 변환하기: binascii()

표준 binascii 모듈은 이진 데이터와 다양한 문자열 표현(16진수, 64진수, uuencodede 등)을 서로 변환할 수 있는 함수를 제공한다.

```Python
# 아스키코드의 호낳ㅂ과 바이트 변수를 보여주기 위해 사용했던 \x xx 이스케이프 대신 16진수의 시퀀스인 8바이트의 PNG 헤더를 출력
>>> import binascii
>>> valid_png_header = b'\x89PNG\r\n\x1a\n'
>>> print(binascii.hexlify(valid_png_header))
b'89504e470d0a1a0a'
# 반대도 가능
>>> print(binascii.unhexlify(b'89504e470d0a1a0a'))
b'\x89PNG\r\n\x1a\n'
```

### 7.2.5 비트 연산자

파이썬은 C 언어와 유사한 비트단위 정수 연산을 제공한다.

연산자 | 설명 | 예제 | 10진수 결과 | 2진수 결과
---|---|---|--6-|---
& | AND | a & b | 1 | 0b0001
\\| | OR | a \| b | 5 | 0b0101
^ | 배타적 OR | a ^ b | 4 | 0b0010
~ | NOT | ~a | -6 | 정수의 크기에 따라 이진 표현이 다름
<< | 비트 왼쪽 이동 | a << 1 | 10 | 0b1010
>> | 비트 오른쪽 이동 | a >> 1 | 2 0b0010

`^` 연산자는 두 인자의 비트가 서로 다를때 1을 반환한다.  
`~` 연산자는 1은 0으로, 0은 1로 비트를 반전시킨다.(부호도 반전시킨다.)
모든 현대 컴퓨터에 사용되는 2의 보수 연산에서 최상위 비트는 부호(1 = 음수)를 나타내기 때문이다.
`<<`, `>>` 연산자는 비트를 이동시킨다. 한 비트 왼쪽 이동을 2를 곱한 것과 같고, 오른쪽 이동은 2로 나눈 것과 같다.
