---
layout: post
section-type: post
title: Python - Inheritance(상속), MRO
category: python
tags: [ 'python' ]
---

# 상속(Inheritance)

- 코드 중복을 최소화하기 위해서 사용
- 파이썬 클래스의 최상위 클래스인  **object** 를 상속
- 클래스 간에 상속관계에 놓이면, 부모/자식 관계 성립
- 자식 클래스는 부모 클래스의 모든 내역을 상속
- 다중상속 지원

![]({{site.url}}/img/post/python/inheritance.png)
위 코드를 상속을 통해 중복을 제거합니다.

```python
class Person(object):
  def __init__(self, name):
    self.name = name

  def run(self):
    print('뜁니다.')

  def eat(self, food):
    print('{}를 먹습니다.'.format(food))

  def sleep(self):
    print('잠을 잡니다.')

class Hulk(Person):
  def angry(self):
    print('분노를 합니다.')

class Spiderman(Person):
  def spider_web(self):
    print('거미줄을 쏩니다.')

class Ironman(Person):
  def laser(self):
    print('레이져를 쏩니다.')
```

# MRO(Method Resolution Order)

- 파이썬의 클래스 탐색순서는 MRO를 따릅니다.
 - Class.**mro** 를 통해 확인 가능
- MRO가 꼬이도록 클래스를 정의 ㅋ할 수는 없습니다.
 - TypeError: Cannot create a consistent method resolution order(MRO)

```Python
>>> class A: pass
...
>>> A.mro()
[<class '__main__.A'>, <class 'object'>]

>>> class B(A): pass
...
>>> B.mro()
[<class '__main__.B'>, <class '__main__.A'>, <class 'object'>]

>>> class C(A): pass
...
>>> C.mro()
[<class '__main__.C'>, <class '__main__.A'>, <class 'object'>]

>>> class D(B,C): pass
...
>>> D.mro()
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]

>>> class E(C,B): pass
...
>>> E.mro()
[<class '__main__.E'>, <class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>]

>>> class F(D,E): pass  # 정의 불가!!
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Cannot create a consistent method resolution
order (MRO) for bases C, B
```

MRO를 정확히 이해하고 있어야 다중상속을 이용하는 어떻게 이루어지는지 명확히 알 수 있습니다.
(django의 CBV를 이해하기 위해 필수)

## 부모의 함수 호출

- 내장함수 `super`를 통해 부모의 함수 호출
 - D의 mro()순서는 D > B > C > A
 - D().fn()의 실행결과로서 A, C, B, D가 출력
- super 호출 시에 MRO에 기반하여 호출

```Python
>>> class A:
...     def fn(self):
...         print('A')
...
>>> class B(A):
...     def fn(self):
...         super().fn()
...         print('B')
...
>>> class C(A):
...     def fn(self):
...         super().fn()
...         print('C')
...
>>> class D(B, C):
...     def fn(self):
...         super().fn()
...         print('D')
>>> A().fn()
A
>>> B().fn()
A
B
>>> C().fn()
A
C
>>> D().fn()
A  # A는 B와 C 모두의 부모이므로 B,C보다 앞서면 안된다.
C  
B  # B 다음에 B의 직계부모 A가 나오면 C보다 앞서므로 조건이 충족되지 않는다.
D
```
