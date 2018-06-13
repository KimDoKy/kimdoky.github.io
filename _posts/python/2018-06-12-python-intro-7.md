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
