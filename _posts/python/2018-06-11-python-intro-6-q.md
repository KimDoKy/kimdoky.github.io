---
layout: post
section-type: post
title: Introducing Python - chap6 - 연습문제
category: python
tags: [ 'python' ]
---

## 6.1 아무 내용도 없는 Thing 클래스를 만들어 출력하라. 그리고 이 클래스의 example 객체를 생성해서 출력하라. 두 출력값은 같은가?

```Python
class Thing:
    pass

>>> print(Thing)
<class '__main__.Thing'>
>>> example = Thing()
>>> print(example)
<__main__.Thing object at 0x1098e1128>
```

## 6.2 Thing2 클래스를 만들고, 이 클래스의 letters 속성에 값 'abc'를 할당한 후 letters를 출력하라.

```Python
class Thing2:
    letters = 'abc'

>>> Thing2.letters
abc
```

## 6.3 Thing3 클래스를 만들어라. 이번에는 인스턴스(객체)의 letters 속성에 값 'xyz'를 할당한 후 letters를 출력하라. letters를 출력하기 위해 객체를 생성해야 하는가?

```Python
class Thing3:
    def __init__(self):
      self.letters = 'xyz'

>>> something = Thing3()
>>> print(something.letters)
xyz
```

## 6.4 name, symbol, number 인스턴스 속성을 가진 Element 클래스를 만들어라. 이 클래스로부터 'Hydrogen', 'H', 1 값을 가진 객체를 생성하라.

```Python
class Element:
    def __init__(self, name, symbol, number):
      self.name = name
      self.symbol = symbol
      self.number = number

>>> element = Element('Hydrogen', 'H', 1)
>>> element.number
1
```
## 6.5 'name': 'Hydrogen', 'symbol': 'H', 'number': 1 과 같이 키와 값으로 이루어진 el_dict 딕셔너리를 만들어라. 그리고 el_dict 딕셔너리로부터 Element 클래스의 hydrogen 객체를 생성하라.

```Python
>>> el_dict = {'name':'Hydrogen', 'symbol':'H', 'number':1}
>>> hydrogen = Element(el_dict['name'], el_dict['symbol'], el_dict['number'])
>>> hydrogen.name
'Hydrogen'

# 딕셔너리의 키 이름과 클래스의 __init__ 인자가 일치하기 때문에 딕셔너리로부터 직접 객체 초기화가 가능
>>> hydrogen = Element(**el_dict)
>>> hydrogen.name
'Hydrogen'
```

## 6.6 Element 클래스에서 객체의 속성(name, symbol, number)값을 출력하는 dump() 메서드를 정의하라. 이 클래스의 hydrogen 객체를 생성하고, dump() 메서드로 이 속성을 출력하라

```Python
class Element:
    def __init__(self, name, symbol, number):
        self.name = name
        self.symbol = symbol
        self.number = number

    def dump(self):
        print(self.name, self.symbol, self.number)

>>> hydrogen = Element(**el_dict)
>>> hydrogen.dump()
Hydrogen H 1
```

## 6.7 print(Hydrogen)을 호출하라. Element 클래스의 정의에서 dump 메서드를 __str__ 메서드로 바꿔서 새로운 hydrogen 객체를 생성하라. 그리고 print(hydrogen)을 다시 호출해보라.

```Python
>>> print(hydrogen)
<__main__.Element object at 0x1098caa90>

class Element:
    def __init__(self, name, symbol, number):
        self.name = name
        self.symbol = symbol
        self.number = number
    def __str__(self):
        return self.name

>>> hydrogen = Element(**el_dict)
>>> print(hydrogen)
Hydrogen
```

## 6.8 Element 클래스를 수정해서 name, symbol, number의 속성을 private로 만들어라. 각 속성값을 반환하기 위해 getter 프로퍼티로 정의한다.

```Python
class Element():
    def __init__(self, name, symbol, number):
        self.__name = name
        self.__symbol = symbol
        self.__number = number
    @property
    def name(self):
        return self.__name
    @property
    def symbol(self):
        return self.__symbol
    @property
    def number(self):
        return self.__number

>>> hydrogen = Element('hydrogen', 'H', 1)
>>> hydrogen.name
'hydrogen'
>>> hydrogen.symbol
'H'
>>> hydrogen.number
1
```

## 6.9 세 클래스 Bear, Rabbit, Octothorpe를 정의하라. 각 클래스에 eats() 메서드를 정의하라. 각 메서드는 'berries'(Bear), 'clover'(Rabbit), 또는 'campers'(Octothorpe)를 반환한다. 각 클래스의 객체를 생성하고, eats() 메서드의 반환값을 출력하라.

```Python
class Bear():
    def eats(self):
        return 'berries'

class Rabiit():
    def eats(self):
        return 'clover'

class Octothorpe():
    def eats(self):
        return 'campers'

>>> a = Bear()
>>> b = Rabiit()
>>> c = Octothorpe()
>> c.eats()
'campers'
>>> a.eats()
'berries'
```

## 6.10 Laser, Claw, SmartPhone 클래스를 정의하라. 각 클래스는 does() 메서드를 갖고 있다. 각 메서드는 'disintegrate'(Laser), 'crush'(Claw), 또는 'ring'(SmartPhone)을 반환한다. 그리고 각 인스턴스(객체)를 갖는 Robot 클래스를 정의하라. Robot 클래스의 객체가 갖고 있는 내용을 출력하는 does() 메서드를 정의하라.

```Python
class Laser():
    def __init__(self):
        self.name = 'disintegrate'
    def does(self):
        return self.name

class Claw():
    def __init__(self):
        self.name = 'crush'
    def does(self):
        return self.name

class SmartPhone():
    def __init__(self):
        self.name = 'ring'
    def does(self):
        return self.name

        class Robot():
            def __init__(self):
                self.laser = Laser()
                self.claw = Claw()
                self.smartphone = SmartPhone()
            def does(self):
                print(self.laser.does(), self.claw.does(), self.smartphone.does())

>>> robot = Robot()
>>> print(robot.does())
disintegrate crush ring
```
