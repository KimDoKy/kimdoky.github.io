---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.6 열거형으로 상수 정의하기
category: python
tags: [ 'python' ]
---
enum은 열거형을 정의합니다.

## 상숫값 정의하기
열거형은 상숫값의 이름을 정의할 때 사용합니다. 열거형의 값은 enum.Enum의 파생 클래스에 "이름=값"의 형식으로 정의합니다.  

그 예로 삼국시대의 국가인 고구려, 백제, 신라, 가야에 각각 1, 2, 3, 4라는 값을 할당한 열거형을 만들어 봅니다.

### enum 샘플 코드

```python
>>> import enum
>>> class Dynasty(enum.Enum):  # 열거형은 enum.Enum을 상속하여 생성
...     GOGURYEO = 1
...     BAEKJE = 2
...     SILLA = 3
...     GAYA = 4
...
>>> dynasty = Dynasty.SILLA  # 신라
```

열거형의 이름과 값은 각각 enum 객체의 name 속성과 value 속성으로 구할 수 있습니다.

### 열거형의 속성

```python
>>> dynasty = Dynasty.SILLA  # 신라
>>> dynasty
<Dynasty.SILLA: 3>
>>> dynasty.name  # 열거형의 이름
'SILLA'
>>> dynasty.value  # 열거형의 값
3
```

### 열거형의 비교
열거형은 Enum에서 파생된 열거형의 인스턴스로, 같은 열거형의 같은 상수일 때 == 연산자로 비교하면 True가 반환됩니다.

```python
>>> class Spam(enum.Enum):
...     HAM = 1
...     EGG = 2
...     BACON = 2
...

>>> isinstance(Spam.HAM, Spam)  # HAM, EGG, BACON은 Spam형 인스턴스
True

>>> Spam.HAM == Spam.HAM  # 같은 값끼리 비교
True

>>> Spam.HAM == Spam.EGG  # 다른 값끼리 비교
False

>>> Spam.EGG == Spam.BACON  # 다른 이름이라도 값이 동일하면 같다
True
```

### 다른 형과 비교
같은 값이라도 다른 형의 값과 비교하면 False가 됩니다.

```python
>>> class Spam2(enum.Enum):
...     HAM = 1
...     EGG = 2
...     BACON = 2
...

>>> Spam.HAM == Spam2.HAM  # 다른 열거형의 같은 값(=1) 사이의 비교
False

>>> Spam.HAM == 1  # 정숫값과 비교
False
```

### unique 장식자
클래스 장식자(decorator)로서 enum.unique()를 지정하면 같은 값의 열거형은 오류가 됩니다.

```python
>>> @enum.unique
... class Spam(enum.Enum):
...     HAM = 1
...     EGG = 1
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/enum.py", line 573, in unique
    (enumeration, alias_details))
ValueError: duplicate values found in <enum 'Spam'>: EGG -> HAM
```

### 열거값의 반복자
열거형은 열거값을 정의한 순서대로 얻는 반복자를 반환합니다. 이 반복자에서는 중복되는 열거값은 하나밖에 구하지 않습니다.

```python
>>> class Spam(enum.Enum):
...     HAM = 1
...     EGG = 2
...     BACON = 1  # 중복 값: 출력되지 않는다.
...

>>> list(Spam)
[<Spam.HAM: 1>, <Spam.EGG: 2>]
```
