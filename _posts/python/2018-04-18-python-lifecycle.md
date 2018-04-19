---
layout: post
section-type: post
title: 파이썬 객체의 생명주기
category: python
tags: [ 'python' ]
---

## 생성자(Constructor)와 소멸자(Destructor)

파이썬의 생성자는 `__init__`, 소멸자는 `__del__`로 정의합니다.

객체를 생성할 때 생성자가 실행이 되고, 객체가 사라질 때 소멸자가 실행됩니다.

```python
class PartyAnimal:
    x = 0

    def __init__(self):
        print('I am constructed')

    def party(self) :
        self.x = self.x + 1
        print('So far',self.x)

    def __del__(self):
        print('I am destructed', self.x)

an = PartyAnimal()
# I am constructed
an.party()
# So far 1
an.party()
# So far 2
an = 42
# I am destructed 2
print('an contains',an)
# an contains 42
```
