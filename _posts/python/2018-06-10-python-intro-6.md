---
layout: post
section-type: post
title: Introducing Python - 객체와 클래스
category: python
tags: [ 'python' ]
---

# Chap 6. 객체와 클래스

## 6.4 메서드 오버라이드

새 클래스는 먼저 부모 클래스로부터 모든 것을 상속 받는다.


### 첫 번째 예

```Python
class Car():
    def exclaim(self):
        print("I'm a Car!")

class Yugo(Car):
    def exclaim(self):
        print("I'm Yugo! Much like a Car, but more Yugo-ish.")
```

```
# 두 클래스로부터 각각 객체를 생성
>>> give_me_a_car = Car()
>>> give_me_a_yugo = Yugo()
```

```
# 각 객체의 exclaim() 메서드를 호출
>>> give_me_a_car.exclaim()
I'm a Car!

give_me_a_yugo.exclaim()
I'm Yugo! Much like a Car, but more Yugo-ish.
```

위 예에서는 `exclaim()` 메서드를 오버라이드 했다.

`__init__()` 메서드를 포함한 모든 메서드를 오버라이드 할 수 있다.

### 두 번째 예

```Python
class Person():
    def __init__(self, name):
        self.name = name

class MDPerson(Person):
    def __init__(self, name):
        self.name = "Docter " + name

class JDPersion(Person):
    def __init__(self, name):
        self.name = name + ", Esquire"
```

`__init__()` 초기화 메서드는 부모 클래스의 Person과 같은 인자를 취하지만, 객체의 인스턴스 내부에서는 다른 name 값을 지정한다.

```
>>> person = Person('Fudd')
>>> docter = MDPerson('Fudd')
>>> lawyer = JDPersion('Fudd')
>>> print(person.name)
Fudd
>>> print(docter.name)
Docter Fudd
>>> print(lawyer.name)
Fudd, Esquier
```

## 6.5 메서드 추가하기

자식 클래스는 부모 클래스에 없는 메서드를 **추가** 할 수 있다.

```python
class Car():
    def exclaim(self):
        print("I'm a Car!")

class Yugo(Car):
    def exclaim(self):
        print("I'm a Yogo! Muck like a Car, but more Yugo-ish")
    def need_a_push(self):
        print("A little help here?")
```

객체를 생성한다.

```Python
give_me_a_car = Car()
give_me_a_yugo = Yugo()
```
Yugo 객체는 need_a_push() 메서드 호출에 대답할 수 있다.

```Python
>>> give_me_a_yugo.need_a_push()
A little help here?
```

제네릭 Car 객체는 대답할 수 없다.

```Python
>>> give_me_a_car.need_a_push()
Traceback (most recent call last)
<ipython-input-9-25de065dd6f4> in <module>()
----> 1 give_me_a_car.need_a_push()

AttributeError: 'Car' object has no attribute 'need_a_push'
```

Yugo는 Car가 할 수 없는 Yugo의 개성을 나타낼 수 있다.

## 6.6 부모에게 도움 받기: super

자식 클래스에서 부모 클래스의 메서드를 호출하려면 `super()` 메서드를 사용하면 된다.

```Python
class Person():
    def __init__(self, name):
        self.name = name

# 서브 클래스의 __init__() 메소드에 email 매개변수가 추가됨    
class EmailPerson(Person):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email
```

자식 클래스에서  `__init__()` 메서드를 정의하면 부모 클래스의 `__init__()` 메서드를 대체하기 때문에 더 이상 자동으로 부모 클래스의 `__init__()` 메서드가 호출되지 않는다. 그러므로 이것을 명시적으로 호출해야 한다.  

- `super()` 메서드는 부모 클래스(Person)의 정의를 얻는다.
- `__init__()` 메서드는 Person.__init__() 메서드를 호출한다. 이 메서드는 self 인자를 슈퍼 클래스로 전달하는 역할을 한다. 그러므로 슈퍼 클래스에 어떤 선택적 인자를 제공하기만 하면 된다. 이 경우 Person()에서 받는 인자는 name이다.
- self.email = email은 EmailPerson 클래스를 Person 클래스와 다르게 만들어 주는 새로운 코드다.

```Python
# 객체 생성
bob = EmailPerson('Bob Frapples', 'bob@frapples.com')

# name과 email 속성에 접근
>>> bob.name
'Bob Frapples'
>>> bob.email
'bob@frapples.com'
```

물론 아래와 처럼 정의할 수도 있다.

```Python
class EmailPerson(Person):
    def __init__(self, name, email):
        self.name = name
        self.email = email
```
하지만 이렇게 사용하면 상속을 사용할 수 없다.  
`super()`를 사용하면 부모 클래스의 정의가 변경되면 상속받은 자식 클래스도 변경사항이 반영된다.

## 6.7 자신: self

파이썬은 적절한 객체의 속성과 메서드를 찾기 위해 인스턴스 메서드의 첫 번째 인자로 `self` 인자를 사용한다.

```Python
>>> car = Car()
>>> car.exclaim()
I'm a Car!
```
- car 객체의 Car 클래스를 찾는다.
- car 객체를 Car 클래스의 exclaim() 메서드의 self 매개변수에 전달한다.

## 6.8 get/set 속성값과 프로퍼티

다른 언어들에서는 private 객체 속성을 접근하기 위해 `getter`,`setter` 메서드를 사용한다.  

파이썬은 모든 속성과 메서드가 `public`이기 때문에 파이써닉하게 **프로퍼티** 를 사용하면 된다.

```Python
# hidden_name이라는 속성으로 클래스를 정의
# 외부에서 직접 접근하지 못하도록 getter(get_name())와 setter(set_name()) 메스드를 정의
# print를 통해 언제 호출되는지 확인
# name 속성의 프로퍼티로 정의
class Duck():
    def __init__(self, input_name):
        self.hidden_name = input_name
    def get_name(self):
        print('inside the getter')
        return self.hidden_name
    def set_name(self, input_name):
        print('inside the setter')
        self.hidden_name = input_name
    name = property(get_name, set_name)
```

마지막 라인 전까지 메서드들은 getter와 setter 메서드처럼 동작한다.  
마지막 라인에서 두 메서드를 name이라는 속성의 프로퍼티로 정의한다.  
`property()`의 인자는 getter 메서드와 setter 메서드이다.  

```python
# Duck 객체의 name을 참조할 때 get_name() 메서드를 통해 호출하여 hidden_name 값을 반환
>>> fowl = Duck('Howard')
>>>fowl.name
inside the getter
'Howard'

# 보통의 getter 메서드처럼 get_name() 메서드를 직접 호출
>>> fowl.get_name()
inside the getter
'Howard'

# name 속성에 값을 할당하면 set_name() 메서드를 호출된다.
>>> fowl.name = 'Daffy'
inside the setter
>>> fowl.name
inside the getter
'Daffy'

# set_name() 메서드는 여전히 직접 호출이 가능
>>> fowl.set_name('Daffy')
inside the setter
>>> fowl.name
inside the getter
'Daffy'
```

### 프로퍼티의 또 다른 사용법 : **Decorator**

- getter 메서드 앞에 `@property` 데코레이터를 쓴다.
- setter 메서드 앞에 `@name.setter` 데코레이터를 쓴가.

```Python
class Duck():
    def __init__(self, input_name):
        self.hidden_name = input_name
    @property
    def name(self):
        print('inside the getter')
        return self.hidden_name
    @name.setter
    def name(self, input_name):
        print('inside the setter')
        self.hidden_name = input_name
```

여전히 name을 속성처럼 접근할 수 있다. 하지만 get_name(), set_name() 메서드가 없다.
객체에 저장된 속성(hidden_name)을 참조하기 위해 name 프로퍼티를 사용했다.

```Python
>>> fowl = Duck('Howard')
>>> fowl.name
inside the getter
'Howard'
>>> fowl.name = 'Donald'
inside the setter
>>> fowl.name
inside the getter
'Donald'
```

### 프로퍼티는 **계산된 값** 을 참조할 수 있다.

radius 속성과 계산된 diameter 프로퍼티를 가진 circle 클래스를 정의

```Python
class Circle():
    def __init__(self, radius):
        self.radius = radius
    @property
    def diameter(self):
        return 2 * self.radius
```

```Python
# radius 속성의 초기값으로 Circle 객체를 생성
>>> c = Circle(5)
>>> c.radius
5

# radius와 같은 속성처럼 diameter를 참조할 수 있다.
>>> c.diameter
10

# radius 속성을 언제든지 바꿀수 있다. diameter 프로퍼티는 현재 radius 값으로부터 계산된다.
>>> c.radius = 7
>>> c.diameter
14

# 속성에 대한 setter 프로퍼티를 명시하지 않으면 외부로부터 이 속성을 설정할 수 없다.(읽기전용 속성)
>>> c.diameter = 20
Traceback (most recent call last)
<ipython-input-31-808ea3f73d1a> in <module>()
----> 1 c.diameter = 20

AttributeError: can't set attribute
```

직접 속성을 접근하는 것보다 프로퍼티를 통해서 접근하면, 속성의 정의가 바뀌면 모든 호출자도 자동으로 적용된다.

## 6.9 private 네임 맹글링

파이썬은 클래스 정의 외부에서 볼 수 없도록 속성에 대한 네이밍 컨벤션(naming convention)이 있다. (속성 이름 앞에 더블 언더스코어(`__`)를 붙인다.)

```Python
# hidden_name을 __name__으로 변경
class Duck():
    def __init__(self, input_name):
        self.__name = input_name
    @property
    def name(self):
        print('inside the getter')
        return self.__name
    @name.setter
    def name(self, input_name):
        print('inside the setter')
        self.__name = input_name
```

```python
# 정상 동작 확인
>>> fowl = Duck('Howard')
>>> fowl.name
inside the getter
'Howard'
>>> fowl.name = 'Donald'
inside the setter
>>> fowl.name
inside the getter
'Donald'

# __name 속성으로 바로 접근할 수 없다.
>>> fowl.__name
Traceback (most recent call last)
<ipython-input-36-39d081ea2ef8> in <module>()
----> 1 fowl.__name

AttributeError: 'Duck' object has no attribute '__name'
```

네이밍 컨벤션은 속성을 private로 만들지 않지만, 파이썬은 이 속성이 외부 코드에서 발견할 수 없도록 이름을 맹글링(mangling)했다.

```Python
>>> fowl._Duck__name
'Donald'
```
inside the getter를 출력하지 않았다. 이것은 속성을 완벽하게 보호하지는 않지만, 네임 맹글링은 속성의 의도적인 직접 접근을 어렵게 만든다.
