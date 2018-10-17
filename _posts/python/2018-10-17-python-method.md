---
layout: post
section-type: post
title: Python - 기초 다지기 (classmethod, staticmethod)
category: python
tags: [ 'python' ]
---

## classmethod

파이썬 데코레이터를 이용해서 클래스의 메서드로 등록할 수 있다.

classmethod는 하나의 클래스이고 데코레이터로 등록이 발생하면 클래스에서 처리할 수 있는 클래스 메서드로 전환해준다.

클래스 메서드가 등록되면 이 메서드의 이름이 클래스 네임스페이스에 등록되고, cls 변수가 첫 번째로 정의되어 클래스와 바인딩되면 처리가 된다.

클래스 메서드를 데코레이터로 등록할 때는 반드시 `@classmethod`라고 작성해야 한다.



```python
# classmethod example

class Klass_clas:

    @classmethod
    def set(cls, name, value):
        setsttr(cls, name, value)
```

## staticmethod

파이썬에서 정적 메서드는 클래스나 인스턴스에 대한 바인딩 지정이 필요 없다. 데코레이터 `@staticmethod`로 지정하면 정적 메서드가 생성된다.

```python
# staticmethod example

class Klass_st:
    name = “”
    age = 0
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def set(cls, name, value):
        setattr(cls, name, value)

    @staticmethod
    def get(obj):
        return obj.name, obj.age
```


## self/cls 매개변수 이해하기

파이썬에서 인스턴스 메서드와 클래스 메서드를 정의할 때 첫 번째 인자로 self, cls 변수를 지정하는지 이해해야 한다.

메서드가 함수와의 큰 차이는 내부 속성에 `__self__`가 생기고 이 속성이 메서드의 첫 번째 인자로 자동으로 셋팅되는 것이다.

그래서 첫 번째 인자의 이름과 상관없이 첫 번째 지정된 변수에 무조건 매칭되므로 self/cls 관행을 따르는 것이 프로그램 가독성에 좋다.



인스턴스 메서드에서 매개변수 첫 번째 인자에 self를 관행적으로 붙이는 것은 인스턴스 바인딩 시 self 자리의 값은 항상 __self__ 속성에 들어와 있는 인스턴스 레퍼런스가 자동으로 셋팅되어 실행되기 때문이다.


> 출처 [손에 잡히는 파이썬](https://book.naver.com/bookdb/book_detail.nhn?bid=13454524)
