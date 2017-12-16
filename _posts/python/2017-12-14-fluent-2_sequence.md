---
layout: post
section-type: post
title: Fluent Python - part2_chap2. 데이터 구조체 - 시퀀스
category: python
tags: [ 'python' ]
---

# 데이터 구조체

시퀀스, 매핑, 집합 등 컬렉션형의 사용 및 문자열과 바이트의 차이점에 대해 다룹니다. 기존에 제공되는 기능을 돌아보고, 조회하지 않을 때 딕셔너리의 키를 재정렬하거나, 지역화된 유니코드 문자열을 정렬할 때 주의해야 할 점 등 특이한 작동 방식에 대해 설명합니다. 시퀀스와 매칭을 설명하고, dict와 set 형의 기반이 되는 해시 테이블을 살펴봅니다.

# 시퀀스

파이썬을 만들기 전에 귀도는 ABC 언어에 참여하고 있었는데, ABC 언어는 초보자를 위한 프로그래밍 환경을 개발하기 위해 10년간 진행한 연구 프로젝트입니다. ABC는 시퀀스에 대한 범용 연산, 내장된 튜플과 매핑 자료형, 들여쓰기를 이용한 구문 구조 등 '파이썬스러운 것'이라 생각되는 여러 개념을 소개했고 파이썬은 시퀀스를 단일하게 처리하는 ABC의 특징을 물려받았습니다. 문자열, 리스트, 바이스 시퀀스, 배열, XML 요소, 데이터베이스 결과에는 모두 반복, 슬라이싱, 정렬, 연결 등 공통된 연산을 적용할 수 있습니다.

## 2.1 내장 시퀀스 개요
파이썬 표준 라이브러리는 C로 구현된 시퀀스형을 제공합니다.

#### 컨테이너 시퀀스
서로 다른 자료형의 항목들을 담을 수 있는 list, tuple, collections.deque 형

#### 균일 시퀀스
단 하나의 자료형만 담을 수 있는 str, bytes, bytearray, memoryview, array.array형

**컨테이너 시퀀스(container sequence)** 는 객체에 대한 참조를 담고 있으며 객체는 어떠한 자료형도 될 수 있지만, **균일 시퀀스(flat sequence)** 는 객체에 대한 참조 대신 자신의 메모리 공간에 각 항목의 값을 직접 담습니다. 따라서 균일 시퀀스가 메모리를 더 적게 사용하지만, 문자, 바이트, 숫자 등 기본적인 자료형만 담을 수 있습니다.  

시퀀스형은 가변성에 따라 분류할 수도 있습니다.

#### 가변 시퀀스
list, bytearray, array.array, collections.deque, memoryview 형

#### 불변 시퀀스
tuple, str, bytes 형

![]({{site.url}}/img/post/python/fluent/2.1.png)
위 그림을 보면 가변 시퀀스가 불변 시퀀스와 어떻게 다른지, 어느 메서드를 상속하는지 알 수 있습니다. 내장된 구체적인 시퀀스형들이 실제로 Sequence나 MutableSequence 추상 베이스 클래스(abstract base class)(ABC)를 상속하는 것은 아니지만, 추상 베이스 클래스를 이용하면 실제 시퀀스형에서 어느 기능을 제공할지 예측할 수 있습니다.  

가장 기본적인 시퀀스형인 list는 가변적이며 혼합된 자료형을 담을 수 있습니다. 지능형 리스트는 낯선 구문 때문에 많이 사용되지 않습니다. 제네레이터를 사용하면 어떤 자료형의 시퀀스도 쉽게 채울 수 있습니다.

## 2.2 지능형 리스트와 제너레이터 표현식
지능형 리스트(리스트형의 경우)나 제네레이터 표현식(그 외 시퀀스의 경우)을 사용하면 시퀀스를 간단히 생성할 수 있습니다. (지능형 리스트는 컴프리핸션을 말하는 것 같다.)

> tip. 파이썬 프로그래머들은 종종 지능형 리스트를 **listcomp** , 제네레이터 표현식을 **genexp** 으로 표기한다.

### 2.2.1 지능형 리스트와 가독성

```Python
>>> symbols = 'ø∆åˆ¬∫©∂'
>>> codes = []
>>> for symbol in symbols:
...     codes.append(ord(symbol))
...
>>> codes
[248, 8710, 229, 710, 172, 8747, 169, 8706]
```

```Python
>>> symbols = 'ø∆åˆ¬∫©∂'
>>> codes = [ord(symbol) for symbol in symbols]
>>> codes
[248, 8710, 229, 710, 172, 8747, 169, 8706]
```

위의 코드가 읽기 쉽지만 지능형 리스트을 안다면 뒤의 코드가 읽기 좋게 느껴질 수 있습니다.

생성된 리스트를 사용하지 않을 거라면 지능형 리스트 구문을 사용하지 말아야 합니다. 그리고 코드를 짧게 만들어야 합니다. 지능형 리스트 구문이 두 줄 이상 넘어가는 경우에는 코드를 분할하거나 for문을 이용해서 작성하는 것이 낫습니다. 정답은 없기 때문에 상식적으로 판단해야 합니다.
> tip. 파이썬에선 [], {}, () 안에서의 개행이 무시된다. 따라서 줄을 넘기기 위해 역슬래시(\\)를 사용하지 않고도 여러 줄에 걸쳐 리스트, 지능형 리스트, 제네레이터 표현식, 딕셔너리를 작성할 수 있습니다.

### 2.2.2 지능형 리스트와 map()/filter() 비교
`map()`과 `filter()` 함수를 이용해서 수행할 수 있는 작업은 기능적으로 문제가 있는 파이썬 람다(lambda)를 억지로 쓰지 않고도 지능형 리스트를 이용해서 모두 구현할 수 있습니다.

```Python
>>> symbols = 'ø∆åˆ¬∫©∂'
>>> beyond_ascii = [ord(s) for s in symbols if ord(s) > 200]
>>> beyond_ascii
[248, 8710, 229, 710, 8747, 8706]

>>> beyond_ascii = list(filter(lambda c: c > 200, map(ord, symbols)))
>>> beyond_ascii
[248, 8710, 229, 710, 8747, 8706]
````
아래 코드로 지능형 리스트와 map()/filter() 조합의 속도를 간단히 비교할 수 있습니다.

```python
import timeit

TIMES = 10000

SETUP = """
symbols = '$¢£¥€¤'
def non_asc  ii(c):
    return c > 127
"""

def clock(label, cmd):
    res = timeit.repeat(cmd, setup=SETUP, number=TIMES)
    print(label, *('{:.3f}'.format(x) for x in res))

clock('listcomp        :', '[ord(s) for s in symbols if ord(s) > 127]')
clock('listcomp + func :', '[ord(s) for s in symbols if non_ascii(ord(s))]')
clock('filter + lambda :', 'list(filter(lambda c: c > 127, map(ord, symbols)))')
clock('filter + func   :', 'list(filter(non_ascii, map(ord, symbols)))')
```
위 코드의 결과입니다.
```
listcomp        : 0.017 0.015 0.019
listcomp + func : 0.023 0.025 0.028
filter + lambda : 0.023 0.025 0.026
filter + func   : 0.025 0.022 0.023
```

### 2.2.3 데카르트 곱
지능형 리스트는 두 개 이상의 반복 가능한 자료형의 데카르트 곱을 나타내는 일련의 리스트를 만들 수 있습니다. 데카르트 곱 안에 들어 있는 각 항목은 입력으로 받은 반복 가능한 데이터의 각 요소에서 만들어진 튜플로 구성됩니다. 생성된 리스트의 길이는 입력으로 받은 반복 가능한 데이터의 길이와 같습니다.

![]({{site.url}}/img/post/python/fluent/2.2.png)

예를 들어 2가지 색과 3가지 티셔츠 리스트를 지능형 리스트를 이용해 생성해봅니다.

```Python
>>> colors = ['black', 'white']
>>> sizes = ['s', 'm', 'l']
>>> tshirts = [(color, size) for color in colors for size in sizes]
>>> tshirts
[('black', 's'), ('black', 'm'), ('black', 'l'), ('white', 's'), ('white', 'm'), ('white', 'l')]

>>> for color in colors:
...     for size in sizes:
...         print((color, size))
...
('black', 's')
('black', 'm')
('black', 'l')
('white', 's')
('white', 'm')
('white', 'l')
```

지능형 리스트는 단지 리스트를 만들 뿐입니다. 다른 종류의 시퀀스를 채우려면 제네레이터 표현식을 사용해야 합니다.

### 2.2.4 제네레이터 표현식
튜플, 배열 등이 시퀀스를 초기화할 땐 제네레이터 표현식을 사용하는 것이 메모리를 더 적게 사용합니다.(반복자 프로토콜(iterator protocol)을 이용해 항목을 하나씩 생성하기 때문)  

사용법은 지능형 리스트와 같지만 '[ ]' 대신 '( )'를 사용합니다.

```Python
>>> symbols = '¢£¥€¤'
>>> tuple(ord(symbol) for symbol in symbols)
(162, 163, 165, 8364, 164)

>>> import array
>>> array.array('I', (ord(symbol) for symbol in symbols))
array('I', [162, 163, 165, 8364, 164])
# 배열 생성자는 인수를 두 개 받으므로, 제네레이터 표현식 앞위에 반드시 괄호를 넣어야 합니다. 배열의 첫 번째 인수는 배열에 들어 갈 숫자들을 저장할 자료형을 지정합니다.
```

데카르트 곱에서 지능형 리스트로 생성했을 때와는 달리 제네레이터로 생성하면 리셔츠 리스트 6개 항목을 메모리안에 생성하지 않습니다. 제네레이터 표현식은 한 번에 한 항목을 생성할 수 있도록 for 루프에 데이터를 전달하기 때문입니다. 만약 사용할 리스트가 천 개가 있다면 제네레이터 표현식을 사용하면 천개의 항목이 들어 있는 리슽트를 생성하는 일을 피할 수 있습니다.

```python
>>> colors = ['black', 'white']
>>> sizes = ['s', 'm', 'l']
>>> for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
...     print(tshirt)
...
black s
black m
black l
white s
white m
white l
# 제네레이터 표현식은 한 번에 하나의 항목을 생성합니다. 6개의 티셔츠 종류를 담고 있는 리스트를 만들지 않습니다.
```
