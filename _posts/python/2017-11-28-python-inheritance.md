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
