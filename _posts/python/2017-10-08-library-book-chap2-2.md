---
layout: post
section-type: post
title: Python Library - chap 2. 수치 처리하기 - 2.2 고정소수점형 계산하기
category: python
tags: [ 'python' ]
---
고정소수점형(10진 부동소수점)을 다루는 decimal에 대해 설명합니다. decimal 모듈은 유효 자릿수를 지정한 계산이나 반올림, 버림, 올림 등에 이용합니다. 정밀도 지정, 반올림, 버림 등 엄격한 규칙이 요구되는 금액 계산 등에 주로 이용합니다.

## 정밀도를 지정하여 계산하기

### Decimal 클래스

형식 | decimal.Decimal(value="0", context=None)
---|---
설명 | 인수로 지정한 값을 바탕으로 Decimal 객체를 생성합니다.
인수 | value =  인수 <br> context = 산술 context
반환값 | Decimal 객체

### Decimal 객체 생성

```python
>>> from decimal import Decimal
>>> Decimal('1')
Decimal('1')

>>> Decimal(3.14)
Decimal('3.140000000000000124344978758017532527446746826171875')

>>> Decimal((0, (3,1,4), -2)) # 부호(0이 +, 1이 -), 숫자 튜플, 지수
Decimal('3.14')

>>> Decimal((1,(1,4,1,4),-3))
Decimal('-1.414')
```

Decimal 객체는 수치형과 마찬가지로 계산할 수 있습니다.

### Decimal 계산

```python
>>> Decimal('1.1') - Decimal('0.1')
Decimal('1.0')

>>> x = Decimal('1.2')
>>> y = Decimal('0.25')
>>> x + y
Decimal('1.45')

>>> x + 1.0 # float형과의 연산에서는 Exception이 발생함
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'
```

decimal에서는 산술 context 설정을 통해 계산 정밀도를 조정할 수 있습니다.

### 유효 자릿수 설정

```python
>>> from decimal import getcontext
>>> x = Decimal('10')
>>> y = Decimal('3')
>>> x / y # 기본은 28자리
Decimal('3.333333333333333333333333333')

>>> getcontext().prec = 8 # prec을 8로 지정

>>> x / y
Decimal('3.3333333')
```

## 숫자 반올림 방법 지정하기(rounding)
반올림 방법은 quantize()를 사용해서 지정합니다. 반올림, 반내림, 사사오입 등 다양한 방법을 지정할 수 있습니다.

형식 | quantize(exp[, rounding[, context[, watchexp]]])
---|---
설명 | 숫자 반올림 방법 지정
인수 | exp - 자릿수 <br> rounding - 반올림 방법
반환값 | Decimal 객체

### quantize()의 사용 예

```python
>>> from decimal import ROUND_UP
>>> exp = Decimal((0, (1,0), -1))
>>> Decimal('1.04').quantize(exp, rounding=ROUND_UP)
Decimal('1.1')
```

rounding에 지정할 수 잇는 반올림 방법은 다음과 같습니다.

rounding | 설명 | x = 1.04 | x = 1.05 | x = -1.05
---|---|---|---|---
ROUND_UP | 올림 | 1.1 | 1.1 | -1.1
ROUND_DOWN | 버림 | 1.0 | 1.0 | -1.0
ROUND_CEILING | 양의 무한대 방향으로 올림 | 1.1 | 1.1 | -1.0
ROUND_FLOOR | 음의 무한대 방향으로 내림 | 1.0 | 1.0 | -1.0
ROUND_HARF_UP | 사사오입(반올림) | 1.0 | 1.1 | -1.1
ROUND_HARF_DOWN | 오사육입 | 1.0 | 1.0 | -1.-
ROUND_HARF_EVEN | 바로 앞 자릿수가 홀수면 사사오입, 짝수이면 오사육인 | 1.0 | 1.0 | -1.0
ROUND_05UP | 바로 앞 자릿수가 0 또는 5이면 올림, 그렇지 않으면 버림 | 1.1 | 1.1 | -1.1

### ROUND_HARF_DOWN, ROUND_HARF_EVEN, ROUND_05UP

```python
>>> from decimal import *
>>> exp = Decimal((0, (1,0), -1)) # 소수 첫째 자리
>>> Decimal('1.06').quantize(exp, ROUND_HALF_DOWN) # 오사육입
Decimal('1.1')

>>> Decimal('1.15').quantize(exp, ROUND_HALF_EVEN) # 앞자리가 홀수면 사사오입
Decimal('1.2')

>>> Decimal('1.25').quantize(exp, ROUND_HALF_EVEN) # 앞자리가 짝수면 오사육입
Decimal('1.2')

>>> Decimal('1.26').quantize(exp, ROUND_HALF_EVEN)
Decimal('1.3')

>>> Decimal('1.55').quantize(exp, ROUND_05UP) # 앞자리가 0 또는 5이면 ROUND_UP
Decimal('1.6')

>>> Decimal('1.75').quantize(exp, ROUND_05UP) # 앞자리가 0도 5도 아니면 ROUND_DOWN
Decimal('1.7')
```
