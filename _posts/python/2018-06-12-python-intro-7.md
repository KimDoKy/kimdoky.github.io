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
