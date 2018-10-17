---
layout: post
section-type: post
title: Python - 기초 다지기 (classmethod, staticmethod)
category: python
tags: [ 'python' ]
---

## 캡슐화(Encapsulation)

클래스를 정의할 때 내부의 속성과 메서드를 묶어서 하나의 단위로 처리할 수 있다. 이렇게 하나의 단위로 묶어서 클래스를 만드는 것을 캡슐화했다고 한다.

파이썬에서는 속성과 메서드가 전부 공개되어있기 때문에 속성을 숨길 방안이 없다.

### `_이름`

 클래스 내부에 `_`가 있는 속성이나 메서드는 관행적으로 private으로 약속하고 처리한다. 이는 외부에서 보호된 이름으로 사용되기에 호출해서 사용하면 안된다.

```python

class Protected:

    def __init__(self, name, age):
        self.__set(name, age)

    def _set(self, name, age):
        self._name = name
        self._age = age

    def getname(self):
         return self._name

    def getage(self):
        return self.age
```

### mangling을 이용한 정보 은닉

이름 앞에 두 개의 언더스코어를 작성해서 처리한다.

이렇게 하면 내부적으로 __클래스__ 이름으로 처리되도록 구성된다.
클래스 외부에서는 직접 `__+이름` 으로는 호출해도 검색이 불가능하지만, 내부 클래스나 인스턴스에서는 `__+이름` 으로 처리한다.


```python
class Mangling:

    def __init__(self, name, age):
        self.__set(name, age)

    def __set(self, name, age):
        self.__name = name
        self.__age = age

    def getname(self):
        return self.__name

    def getage(self):
        return self.__age
```

### property를 이용한 정보 은닉

정보 은닉을 처리해도 기본으로 퍼블릭이므로 모든 것을 조회할 수 있다.

프로퍼티를 지정할 때도 주로 데코레이터를 사용한다. 메서드 바로 위에 `@property`를 지정하면 함수명으로 하나의 인스턴스를 만들고 그 내부의 getter 메서드에 등록된다. 갱신이 필요하다면 `@g함수명.setter`로 처리해야 한다. 하지만 내부의 속성 이름을 알고 있다면 메서드 대신 속성에 직접 접근해서 조회나 갱신이 가능하다.

```python

class PropertyClass:

    def __init__(self, name):
        self._name = name

    @property
    def name(slef):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
```

이 클래스에 name으로 조회나 갱신을 하려면 두 개의 메서드가 필요하다. 메서드의 이름은 동일하지만 하나는 조회, 하나는 속성을 갱신한다.

조회하는 메서드 위에 `@property`를 지정하면 내부적으로 name이라는 인스턴스가 만들어지고 그 내부에 이 메서드가 getter로 등록된다.

두 번째 메서드는 name 인스턴스에 점 연산자를 이용해서 setter로 프로퍼티를 만들면 동일한 메서드가 등록된다.

정의가 끝나고 이를 로딩하면 이 클래스가 객체로 전환된다. 이 클래스 내부의 네임스페이스를 조회하면 name 속성이 property 인스턴스라는 것과, 클래스 내부에 정의된 메서드들이 name이라는 property 인스턴스 내부에 들어가 있는 것을 알 수 있다.

> 출처 [손에 잡히는 파이썬](https://book.naver.com/bookdb/book_detail.nhn?bid=13454524)
