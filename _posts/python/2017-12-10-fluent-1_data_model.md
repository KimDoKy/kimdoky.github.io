---
layout: post
section-type: post
title: Fluent Python - part1_chap1. 파이썬 데이터 모델
category: python
tags: [ 'python' ]
---

데이터 모델은 일종의 프레임워크로써, 시퀀스, 반복자, 함수, 클래스, 컨텍스트 관리자 등 언어 자체의 구성단위에 대한 인터페이스를 공식적으로 정의합니다.

파이썬 인터프린터는 특별 메서드를 호출해서 기본적인 객체 연산을 수행하는데, 종종 특별한 구문에 의해 호출됩니다. 특별한 메서드는 `__getitem__()`처럼 앞뒤에 이중 언더바를 갖습니다.  

특별 메서드는 다음과 같은 기본적인 언어 구조체를 구현하고 지원하고 함께 사용할 수 있게 해줍니다.

- 반복
- 컬렉션
- 속성 접근
- 연산자 오버로딩
- 함수 및 메서드 호출
- 객체 생성 및 제거
- 문자열 표현 및 포맷
- 블록 등 컨텍스트 관리

> 특별 메서드는 더블 언더바를 사용하기 때문에 던더(dunder) 메서드라고 불린다.

## 1.1 파이썬 카드 한 벌

특별 메서드 `__getitem__()`과 `__len__()`만으로도 강력한 기능을 구현할 수 있습니다.  

다음 코드는 카드 놀이에 사용할 카드 한 벌을 나타내는 클래스입니다.

```Python
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class  FrenchDeck:
    ranks = [str (n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
            return len(self._cards)

    def __getitem__(self, position):
            return self._cards[position]
```

`collections.namedtuple()`를 이용해서 개별 카드를 카드를 나타내는 클래스를 구현합니다.
`namedtuple`은 데이터베이스의 레코드처럼 메서드를 가지지 않는 일력의 속성으로 구성된 클래스를 만들수 있습니다. 이 클래스를 이용하면 다음과 같이 카드 한 장을 표현할 수 있습니다.

```Python
>>> beer_card = Card('7', 'diamonds')
>>> beer_card
Card(rank='7', suit='diamonds')
```

FrenchDeck 클래스는 간단하지만 많은 기능을 구현합니다. 먼저 일반적인 파이썬 컬렉션과 마찬가지로 `len()` 함수를 통해 자신이 갖고 잇는 카드의 수를 반환합니다.

```Python
>>> deck = FrenchDeck()
>>> len(deck)
52
```
deck에서 인덱스를 이용하여 특정 카드를 읽을 수 있습니다. 이 기능은 `__getitem__()` 메서드가 제공합니다.

```Python
>>> deck[0]
Card(rank='2', suit='spades')
>>> deck[-1]
Card(rank='A', suit='hearts')
```
임의의 카드는 `random.choice()` 메서드를 사용하여 고를 수 있습니다.

```Python
>>> from random import choice
>>> choice(deck)
Card(rank='A', suit='spades')
>>> choice(deck)
Card(rank='2', suit='diamonds')
>>> choice(deck)
Card(rank='5', suit='clubs')
```

특별 메서드를 통해 파이썬 데이터 모델을 사용할 때 두 가지 장점이 있습니다.

- 사용자가 표준 연산을 수행하기 위해 클래스 자체에서 구현한 임의 메서드명을 암기할 필요가 없다.
- 파이썬 표준 라이브러리에서 제공하는 풍부한 기능을 별도로 구현할 필요없이 바로 사용할 수 있다.

장점은 이외에도 많이 있다.  

`__getitem__()` 메서드는 `self._cards`의 [] 연산자에 작업을 위임하므로 deck 객체는 슬라이싱(slicing)도 자동으로 지원한다. 새로 생성한 deck 객체에서 앞의 카드 3장을 가져오고, 12번째 인덱스에서 시작해서 13개씩 건너뛰어 에어스만 가여오는 방법입니다.

```Python
>>> deck[:3]
[Card(rank='2', suit='spedes'), Card(rank='3', suit='spedes'), Card(rank='4', suit='spedes')]
>>> deck[12::13]
[Card(rank='A', suit='spedes'), Card(rank='A', suit='diamonds'), Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]
```

`__getitem__()` 특별 메서드를 구현함으로써 deck을 반복할 수도 있습니다.

```Python
>>> for card in deck:
...     print(card)
...
Card(rank='2', suit='spedes')
Card(rank='3', suit='spedes')
Card(rank='4', suit='spedes')
Card(rank='5', suit='spedes')
Card(rank='6', suit='spedes')
Card(rank='7', suit='spedes')
Card(rank='8', suit='spedes')
Card(rank='9', suit='spedes')
Card(rank='10', suit='spedes')
Card(rank='J', suit='spedes')
Card(rank='Q', suit='spedes')
Card(rank='K', suit='spedes')
Card(rank='A', suit='spedes')
Card(rank='2', suit='diamonds')
Card(rank='3', suit='diamonds')
Card(rank='4', suit='diamonds')
Card(rank='5', suit='diamonds')
Card(rank='6', suit='diamonds')
Card(rank='7', suit='diamonds')
Card(rank='8', suit='diamonds')
Card(rank='9', suit='diamonds')
Card(rank='10', suit='diamonds')
Card(rank='J', suit='diamonds')
Card(rank='Q', suit='diamonds')
Card(rank='K', suit='diamonds')
Card(rank='A', suit='diamonds')
Card(rank='2', suit='clubs')
Card(rank='3', suit='clubs')
Card(rank='4', suit='clubs')
Card(rank='5', suit='clubs')
Card(rank='6', suit='clubs')
Card(rank='7', suit='clubs')
Card(rank='8', suit='clubs')
Card(rank='9', suit='clubs')
Card(rank='10', suit='clubs')
Card(rank='J', suit='clubs')
Card(rank='Q', suit='clubs')
Card(rank='K', suit='clubs')
Card(rank='A', suit='clubs')
Card(rank='2', suit='hearts')
Card(rank='3', suit='hearts')
Card(rank='4', suit='hearts')
Card(rank='5', suit='hearts')
Card(rank='6', suit='hearts')
Card(rank='7', suit='hearts')
Card(rank='8', suit='hearts')
Card(rank='9', suit='hearts')
Card(rank='10', suit='hearts')
Card(rank='J', suit='hearts')
Card(rank='Q', suit='hearts')
Card(rank='K', suit='hearts')
Card(rank='A', suit='hearts')
```

반복은 암묵적으로 수행되는 경우도 많이 있습니다. 컬렉션에 `__contains__()` 메서드가 없다면 `in` 연산자는 차례대로 검색합니다. 예를 들어 FrenchDeck 클래스의 경우 반복할 수 있으므로 `in`이 작동합니다.

```Python
>>> Card('Q', 'hearts') in deck
True
>>> Card('7', 'beasts') in deck
False
```

정렬도 가능합니다.  

일반적으로 카드는 숫자(rank)로 순위를 정하고, 숫자가 같은 경우에는 스페이드, 하트, 다이아몬드, 클로버 순으로 정합니다. 이 규칙대로 카드 순위를 정하는 함수입니다.

```Python
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
```
카드 한 벌을 오름차순으로 나열할 수 있습니다.

```Python
>>> for card in sorted(deck, key=spades_high):
...     print(card)
...
Card(rank='2', suit='clubs')
Card(rank='2', suit='diamonds')
Card(rank='2', suit='hearts')
Card(rank='2', suit='spades')
Card(rank='3', suit='clubs')
Card(rank='3', suit='diamonds')
Card(rank='3', suit='hearts')
Card(rank='3', suit='spades')
Card(rank='4', suit='clubs')
Card(rank='4', suit='diamonds')
Card(rank='4', suit='hearts')
Card(rank='4', suit='spades')
Card(rank='5', suit='clubs')
Card(rank='5', suit='diamonds')
Card(rank='5', suit='hearts')
Card(rank='5', suit='spades')
Card(rank='6', suit='clubs')
Card(rank='6', suit='diamonds')
Card(rank='6', suit='hearts')
Card(rank='6', suit='spades')
Card(rank='7', suit='clubs')
Card(rank='7', suit='diamonds')
Card(rank='7', suit='hearts')
Card(rank='7', suit='spades')
Card(rank='8', suit='clubs')
Card(rank='8', suit='diamonds')
Card(rank='8', suit='hearts')
Card(rank='8', suit='spades')
Card(rank='9', suit='clubs')
Card(rank='9', suit='diamonds')
Card(rank='9', suit='hearts')
Card(rank='9', suit='spades')
Card(rank='10', suit='clubs')
Card(rank='10', suit='diamonds')
Card(rank='10', suit='hearts')
Card(rank='10', suit='spades')
Card(rank='J', suit='clubs')
Card(rank='J', suit='diamonds')
Card(rank='J', suit='hearts')
Card(rank='J', suit='spades')
Card(rank='Q', suit='clubs')
Card(rank='Q', suit='diamonds')
Card(rank='Q', suit='hearts')
Card(rank='Q', suit='spades')
Card(rank='K', suit='clubs')
Card(rank='K', suit='diamonds')
Card(rank='K', suit='hearts')
Card(rank='K', suit='spades')
Card(rank='A', suit='clubs')
Card(rank='A', suit='diamonds')
Card(rank='A', suit='hearts')
Card(rank='A', suit='spades')
```

FrenchDeck이 암묵적으로 object를 상속받지만, 상속 대신 데이터 모델과 구성을 이용해서 기능을 가져옵니다. `__len__()`과 `__getitem__()` 특별 메서드를 구현함으로써 FrenchDeck은 표준 파이썬 시퀀스처럼 작동하므로 반복 및 슬라이싱 등의 핵심 언어 기능 및 'random'의 'choice()', 'reversed()', 'sorted()'함수 등 표준 라이브러리를 사용할 수 있습니다. 구성 덕분에 `__len__()`과 `__getitem__()` 메서드는 모든 작업을 list 객체인 `self._cards`에 떠넘길 수 있습니다.

> #### 셔플링은 가능할까?  
지금 구현한 FrenchDeck으로는 셔플링을 할 수 없습니다. **불변** 객체이기 때문입니다. 캡슐화를 어기고 `_cards` 속성을 직접 조작하지 않는 한 카드의 값과 위치를 바꿀 수 없습니다.  `__setitem__()` 한 줄짜리 메서그를 추가해서 이 문제를 해결할 수 있습니다.

## 1.2 특별 메서드는 어떻게 사용되나?
특별 메서드는 파이썬 인터프린터가 호출하기 위한 것입니다. list, str, bytearray 등과 같은 내장 자료형의 경우 파이썬 인터프린터는 손쉬운 방법을 선택합니다. 실제로 CPython의 경우 `len()` 메서드는 메모리에 있는 가변 크기 내장 객체를 나차내는 PyVarObject C 구조체의 ob_size 필드의 값을 반환합니다. 이 방법은 메서드를 호출하는 것보다 빠릅니다.  

종종 특별 메서드는 암묵적으로 호출되기도 합니다. 예를 들어 `for i in x:`의 경우 실제로는 `iter(x)`를 호출하며, 이 함수는 다시 `x.__iter__()`를 호출합니다.  

일반적으로 사용자가 특별 메서드를 직접 호출하는 경우는 거의 없습니다. 있다면 `__init__()` 메서드 정도입니다. 사용자가 구현한 `__init__()` 메서드 안에서 슈퍼클래스의 `__init__()` 메서드를 호출하기 때문입니다.  

특별 메서드를 호출해야 하는 경우엔 일반적으로 `len()`, `iter()`, `str()` 등 관련된 내장 함수를 호출하는 것이 좋습니다. 내장 함수가 해당 특별 함수를 호출하기 때문입니다. 하지만 내장 데이터형의 경우 특별 메서드를 호출하지 않는 경우도 있으며 메서드 호출보다 빠릅니다. 후에 `iter()`에서 다시 다룹니다.  

사용자 정의 속성을 만들 때 `__foo__`와 같은 더블 언더바를 가진 속성명을 피해야 합니다. 지금은 사용하지 않더라도 추후에 새로 추가 정의 될 수 있습니다.

### 1.2.1 수치형 흉내 내기
`+`와 같은 연산자에 사용자 정의 객체가 응답할 수 있게 해두는 몇몇 특별한 메서드가 있습니다. 간단한 예를 들어 사용법만 알아봅니다.  

ex) 수학이나 물리학에서 사용되는 2차원 유클리드 벡터를 나타내는 클래스를 구현합니다.

![]({{site.url}}/img/post/python/fluent/1.2.1.png)
> 2차원 벡터 덧셈 예제. Vector(2, 4) + Vector(2, 1)은 Vector(4, 5)가 된다.
> tip. 내장된 complex 형을 이용해서 2차원 벡터를 표현할 수도 있다. 하지만 직접 구현한 클래스는 n차원으로 쉽게 확장할 수 있습니다. 추후에 다룹니다.

위 그림을 표현한 벡터 덧셈을 테스트하는 Vector 클래스입니다. `__repr__(), __abs__(), __add__(), __mul__()` 특별 메서드를 이용해서 구현합니다.

```python
from math import hypot

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)
    def __abs__(self):
        return hypot(self.x, self.y)
    def __bool__(self):
        return bool(abs(self))
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
```

```python
>>> v1 = Vector(2,4)
>>> v2 = Vector(2,1)
>>> v1 + v2
Vector(4, 5)
```
'+' 연산자의 결과로 Vector 형이 나오는 점을 주의해야 합니다. Vector 형은 콘솔에서 Vector로 표현됩니다.

```python
>>> v = Vector(3,4)
>>> abs(v)
5.0
```
내장된 `abs()` 함수는 정수나 실수의 절대값을 반환하며, complex 형의 경우에도 값을 한 개만 반환하므로, 벡터의 크기를 계산하는데 `abs()` 함수를 사용합니다.

```python
>>> v * 3
Vector(9, 12)
>>> abs(v * 3)
15.0
```
'\*' 연산자를 사용해 스칼라곱을 수행할 수 있습니다.(즉, 벡터에 어떤 숫자를 곱하면 동일한 방향으로 크기만 커진 벡터를 만든다.)  

`__init__()`을 제외하고 5개의 특별 메서드를 구현했지만, 이 메서드들은 클래스 내부나 콘솔의 테스트 코드에서 직접 호출하지 않습니다. 특별 메서드는 주로 파이썬 인터프린터가 호출하기 때문입니다.

### 1.2.2 문자열 표현
`__repr__()` 특별 메서드는 객체를 문자열로 표현하기 위해 `repr()` 내장 메서드에 의해 호출됩니다. `__repr__()` 메서드를 구현하지 않는다면 해당 객체는 콘솔을 <Vector object at 0x10220a6a0>와 같은 형태로 출력합니다.  

위 코드에서 `__repr__()` 메서드에서 출력할 속성의 표준 표현을 가져오기 위해 %r을 사용하는 것은 좋은 습관이 될 것입니다. Vector(1,2)처럼 인수로 숫자만 받으므로 Vector('1','2')처럼 문자열이 들어오면 동작하지 않습니다.  

`__str__()` 메서드는 `str()` 생성자에 의해 호출되며 `print()`함수에 의해 암묵적으로 사용됩니다. `__str__()`은 사용자에게 보여주기 적당한 형태의 문자열을 반환합니다.  

`__repr__()`와 `__str__()`중 하나만 구현해야 한다면 `__repr__()`메서드를 구현해야 합니다. 파이썬 인터프린터는 `__str__()` 메서드가 구현되지 않았을 때의 대책으로 `__repr__()` 메서드를 호출하기 때문입니다.

### 1.2.3 산술 연산자
위 코드에서 `__add__(), __mul__()`의 기본 사용법을 위해 '+'와 '\*' 연산자를 구현하였습니다. 두 경우 모두 메서드는 Vector 객체를 새로 만들어서 반환하며 두 개의 피연산자는 변경하지 않습니다. 중위 연산자는 의례적으로 피연산자를 변경하지 않고 객체를 새로 만듭니다. 추후에 다룹니다.
> Vector에 숫자를 곱할 수는 있지만, 숫자에 Vector를 곱할 수는 없다. 수학에서의 교환법칙을 어겼기 때문이다.

### 1.2.4 사용자 정의형의 불리언 값

if문, while문, and, or, not에 대한 피연산자로서 불리언형이 필요한 어떤한 객체라도 사용할 수 있습니다. x가 참된 값인지 거짓된 값인지 판단하기 위해 파이썬은 `bool(x)`를 적용하며, 이 함수는 항상 True나 False를 반환합니다.  

`__bool__()`이나 `__len__()`을 구현하지 않으면, 기본적으로 사용자 정의 클래스의 객체는 참된 값이라고 간주합니다. `bool(x)`는 `x.__bool__()`을 호출한 결과를 이용합니다. `__bool__()`이 구현되어 있지 않으면 파이썬은 `x.__len__()`을 호출하며, 이 특별 메서드가 0을 반환하면 False, 그렇지 않으면 True를 반환합니다.

## 1.3 특별 메서드 개요
파이썬 문서의 '데이터 모델'에서는 83개 특별 메서드가 나오는데, 그중 47개는 산술, 비트, 비교 연산자를 구현하기 위해 사용됩니다.

### 특별 메서드명(연산자 제외)

범주 | 메서드명
---|---
문자열/바이트 표현 | __repr__, __str__, __format__, __bytes__
숫자로 변환 | __abs__, __bool__, __complex__, __int__, __float__, __hash__, __index__
컬렉션 에뮬레이션 | __len__, __getitem__, __setitem__, __delitem__, __contains__
반복 | __iter__, __reversed__, __next__
콜러블 에뮬레이션 | __call__
컨텍스트 관리 | __enter__, __exit__
객체 생성 및 소멸 | __new__, __init__, __delitem__
속성 관리 | __getattr__, __getattribute__, __setsttr__, __delattr__, __dir__
속성 디스크립터 | __get__, __set__, __delete__
클래스 서비스 | __prepare__, __instancecheck__, __subclasscheck__

### 연산자에 대한 특별 메서드명

범주 | 메서드명 및 관련 연산자
---|---
단한 수치 연산자 | __neg__ -, __pos__ +, __abs__ abs()
향상된 비교 연산자 | __lt__ <, __le__ <=, __eq__ ==, __ne__ !=, __gt__ >, __ge__ >=
산술 연산자 | __add__ +, __sub__ -, __mul__ * , __truediv__ /, __floordiv__ //, __mod__ %, __divmod__ divmod(), __pow__ ** 이나 pow(), __round__ round()
역순 산술 연산자 | __radd__, __rsub__, __rmul__, __rtruediv__, __rfloordiv__, __rmod__, __rdivmod__, __rpow__
복합 할당 산술 연산자 | __iadd__, __isub__, __imul__, __itruediv__, ifloordiv__, __imod__, __ipow__
비트 연산자 | __invert__ ~, __lshift__ <<, __rshift__ >>, __and__ &, __or__ \|, __xor__ ^
역순 비트 연산자 | __rlshift__, __rrshift__, __rxor__, __ror__
복합 할당 비트 연산자 | __ilshift__, __irshift__, __iand__, __ixor__, __ior__

> tip. 피연산자의 순서가 바뀌었을 때는(a * b 대힌 b * a 사용) 역순 연산자(reversed operator)가 사용되는 반면, 복합 할당(augmented assignment)은 중위 연산자와 변수 할당을 간략히 표현한다.(a = a * b를 a \*= b로 표현)

## 1.4 왜 len()은 메서드가 아닐까?
파이썬 문서에 의하면 len(x)는 x가 내장형의 객체일 때 아주 빨리 실행된다고 설명합니다. CPython의 내장 객체에 대해서는 메서드를 호출하지 않고, 단지 C 언어 구조체의 필드를 읽어올 뿐입니다.

다시 말해, len()은 abs()와 마찬가지로 파이썬 데이터 모델에서 특별한 대우를 받기 때문에 메서드라고 부르지 않습니다. 그러나 __len__() 특별 메서드 덕분에 사용자 정의한 객체의 len() 메서드를 직접 정의할 수 있습니다.  
> Note. abs()나 len()을 단한 연산자로 생각한다면, 객체지향 언어에서 볼 수 있는 메서드 호출 구문 대신 함수처럼 구현한 이유를 이해할 수 있을겁니다. 사실 이런 기능의 상당 부분은 개척한 파이썬의 선조 언어인 ABC에서는 len()에 대응되는 #연산자가 있습니다.(&s 형태로 사용한다.) x#s 처럼 중위 연산자로사용하면 s안에 x가 나타낸 횟수를 계산하는데, 파이썬에서는 s.count(x)로 호출합니다.

## 1.5 요약
특별 메서드를 구현하면 사용자 정의 객체도 내장형 객체처럼 동작하게 되어, 파이썬그러운 표현력 있는 코딩 스타일을 구사할 수 있습니다.  
파이썬 객체는 디버깅 및 로그에 사용하는 형태(__repr__())와 사용자에게 보여주기 위한 형태(__str__())가 있습니다.

- 출처: [한빛미디어 전문가를 위한 파이썬](http://www.hanbit.co.kr/store/books/look.php?p_code=B3316273713)
