---
layout: post
section-type: post
title: Python - Overriding
category: python
tags: [ 'python' ]
---

# 오버라이딩

- 클래스 상속에서 사용되는 개념
- 상위 클래스가 가지고 있는 메소드를 하위 클래스가 재정의

## 클래스 주요 오버라이딩 멤버함수

- \__init__(self[, ...]) : 생성자 함수 [#doc](https://docs.python.org/3/reference/datamodel.html#object.__init__)
- \__repr__(self) : 시스템이 해당 객체를 인식할 수 있는 Official 문자열 [#doc](https://docs.python.org/3/reference/datamodel.html#object.__repr__)
 - 보통 디버깅을 위해 사용
 - 출력 문자열을 통해, 바로 인스턴스를 생성할 수 있도록, 인스턴스 생성
- \__str__(self) : Informal 문자열. str(obj) 시에 호출
- \__getitem__(self, key) : self[key]를 구현 [#doc](https://docs.python.org/3/reference/datamodel.html#object.__getitem__)
- \__setitem(self, key, value) : self[key]=value [#doc](https://docs.python.org/3/reference/datamodel.html#object.__setitem__)

## 클래스 주요 오버라이딩 멤버함수 - 연산자 재정의 [#ref](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types)

- Binary Arthmetic Operations
 - +,-,*,@,/,//,%,divmod,pow,**,<<,>>,&,^,|
 - ex) x + y 는 x.__add__(y) 함수를 호출
- Augmented Arithmetic Assignments
 - +=, -=, *=, @=, /=, //=, %=, **=, <<=, >>=, &=, ^=, |=
 - ex) x += y 는 x.__iadd__(y) 함수를 호출
- Unary Arthmetic Operations : - , + , abs, ~
 - ex) -obj는 obj.__neg__() 함수를 호출
- built-in functions : complex, int, float, round
 - ex) complex(obj)는 obj.__complex__() 함수를 호출
- Rich Comparison : <, <=, ==, !=, >, >=
 - ex) x < y는 x.__lt__(y) 함수를 호출

### 예시: \__add__, \__iadd__ 구현하기

```Python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __add__(self, value):
        return Person(self.name, self.age + value)

    def __iadd__(self, value):
        self.age += value
        return self

    def __repr__(self):
        return "Person('{}', {})".format(self.name, self.age)

>>> tom = Person('Tom', 10)

>>> tom + 10
Person('Tom', 20)

>>> tom += 20

>>> tom
Person('Tom', 30)
```

## 클래스 주요 오버라이딩 멤버함수 - with절 지원

- \__enter(self) [#ref](https://docs.python.org/3/reference/datamodel.html#object.__enter__)
- \__exit__(self, exctype, excvalue, traceback) [#ref](https://docs.python.org/3/reference/datamodel.html#object.__exit__)
 - exc_type : 예외(Exception) 클래스 타입
 - exc_value : 예외 인스턴스
 - traceback : Traceback 인스턴스
 - 예외가 발생하지 않았다면, 인자 3개 값은 모두 None으로서 호출

### 예시: 클래스를 통한 with절 지원

```Python
class File:
    def __init__(self, path, mode):
        self.path = path
        self.mode = mode

    def __enter__(self):
        self.f = open(self.path, self.mode, encoding='utf-8')

    def __exit__(self, exc_type, exc_value, traceback):
        # 예외 발생여부에 상관없이 파일을 닫습니다.
        self.f.close()

with File('filepath.txt', 'wt') as f:
    f.write('hello world')
```

> AskDjango의 내용입니다. 언제나 잘보고 있어요 ㅎ
