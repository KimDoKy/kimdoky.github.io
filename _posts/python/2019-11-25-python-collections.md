---
layout: post
section-type: post
title: Python - collections (효율적인 컨테이너형 데이터)
category: python
tags: [ 'python' ]
---

# collections (효율적인 컨테이너형 데이터)

알고리즘 문제 해설이나 모범 답안을 보면 `itertools`와 같이 많이 보이는 것이 `collections`이다.  

[`collections`](https://docs.python.org/ko/3.7/library/collections.html?highlight=collections)는 다른 객체를 등록하여 효율적으로 컬렉션을 관리할 수 있다.

## [ChainMap objects](https://docs.python.org/ko/3.7/library/collections.html?highlight=collections#chainmap-objects)

여러 개의 dict 객체를 모아서 각가의 dict 요소를 하나의 dict으로 검색할 수 있다.

attr/method | desc
---|---|---
`maps` | 등록된 매핑 객체 리스트 |
`new_child` | 현재 인스턴스의 모든 맵을 포함된 새 객체를 반환
`parents` | 현재 인스턴스의 첫 번째 맵을 제외한 새 맵을 반환

```python
from collections import ChainMap

baseline = {'music':'bach', 'art':'rembrandt'}
adjustments = {'art':'van gogh', 'opera':'carmen'}

c = ChainMap(adjustments, baseline)

d = c.new_child()
e = c.new_child()
e.maps[0]
# {}

e.maps[-1]
# {'music': 'bach', 'art': 'rembrandt'}

e.parents
# ChainMap({'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'})

d['x'] = 1
d['x']
# 1

del d['x']
list(d)
# ['music', 'art', 'opera']

len(d)
# 3

d.items()
# ItemsView(ChainMap({}, {'art': 'van gogh', 'opera': 'carmen'}, {'music': 'bach', 'art': 'rembrandt'}))

dict(d)
# {'music': 'bach', 'art': 'van gogh', 'opera': 'carmen'}
```

## [Counter objects](https://docs.python.org/ko/3.7/library/collections.html?highlight=collections#counter-objects)

입력 데이터에서 각 값의 counter를 셀때 사용.

```python
cnt = Counter()
for word in ['red', 'blue', 'red', 'green', 'blue', 'blue']:
    cnt[word] += 1
cnt
# Counter({'red': 2, 'blue': 3, 'green': 1})

import re
words = re.findall(r'\w+', open('hamlet.txt').read().lower())
Counter(words).most_common(10)
# [('the', 1091), ('and', 969), ('to', 767), ('of', 675), ('i', 633), ('a', 571), ('you', 558), ('my', 520), ('in', 451), ('it', 421)]
 ```

- `elements()`
지정한 개수만큼 반복되는 요소를 임의의 순서로 반환한다. 1보다 작으면 무시한다.

```python
c = Counter(a=4, b=2, c=0, d=-2)
c
# Counter({'a': 4, 'b': 2, 'c': 0, 'd': -2})
sorted(c.elements())
# ['a', 'a', 'a', 'a', 'b', 'b']
```

- `most_common([n])`
값이 큰 순서대로 키와 값으로 이루어진 tuple을 최대 n건의 리스트로 반환한다.

```python
Counter('abracadabra').most_common(3)
# [('a', 5), ('b', 2), ('r', 2)]
```

- `subtract([반복 가능 또는 맵핑])`
iterable 또는 매핑 객체의 값을 뺀다.

```python
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
c.subtract(d)
c
# Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})
```

```python
sum(c.values())                 # total of all counts
c.clear()                       # reset all counts
list(c)                         # list unique elements
set(c)                          # convert to a set
dict(c)                         # convert to a regular dictionary
c.items()                       # convert to a list of (elem, cnt) pairs
Counter(dict(list_of_pairs))    # convert from a list of (elem, cnt) pairs
c.most_common()[:-n-1:-1]       # n least common elements
+c                              # remove zero and negative counts
```

```python
c = Counter(a=3, b=1)
d = Counter(a=1, b=2)
c + d
# Counter({'a': 4, 'b': 3})
c - d
# Counter({'a': 2})
c & d
# Counter({'a': 1, 'b': 1})
c | d
# Counter({'a': 3, 'b': 2})
```

```python
# 단항에서의 연산은 빈 카운터 객체와 연산을 한다.
c = Counter(a=2, b=-4)
+c
# Counter({'a': 2})
-c
# Counter({'b': 4})
```

## [deque objects](https://docs.python.org/ko/3.7/library/collections.html?highlight=collections#deque-objects)

큐의 맨 앞과 끝에 데이터를 추가, 삭제하여 데이터 수와 관계없이 일정한 속도로 수행한다.(Double ended Queue)  

method | desc
---|---
`append(x)` | x를 오른쪽에 추가
`appendleft(x)` | x를 왼쪽에 추가
`clear()` | 모든 elem를 제거하여 길이를 0 상태로 만듬
`copy()` | 얕은 복사
`count(x)` | x와 같은 elem의 수를 반환
`extend(iterable)` | iterable을 오른쪽에 추가
`extendleft(iterable)` | iterable을 왼쪽에 추가
`index(x[, start[, stop]])` | x의 인덱스를 반환 /<br>찾지 못하면 ValueError
`insert(i, x)` | i 인덱스에 x를 삽입 / maxlen 이상으로 커지만 IndexError
`pop()` | 오른쪽에서 elem를 제거하고 반환 / elem이 없으면 IndexError
`popleft()` | 왼쪽에서 elem를 제거하고 반환 / elem이 없으면 IndexError
`remove(value)` | 먼저 발견된 value를 제거 / 없으면 ValueError
`reverse()` | 순서를 뒤집음
`rotate(n=1)` | n이 양수이면 오른쪽, 음수이면 왼쪽으로 돌림
`maxlen` | deque의 최대 크기를 반환 / 제한이 없으면 None

> 3.5 버전부터 `__add__()`,`__mul__()`,`__imul__()`도 지원

```python
from collections import deque
d = deque('ghi')                 # make a new deque with three items
for elem in d:                   # iterate over the deque's elements
    print(elem.upper())
# G
# H
# I

d.append('j')
d.appendleft('f')
d
# deque(['f', 'g', 'h', 'i', 'j'])

d.pop()
# 'j'
d.popleft()
# 'f'
list(d)
# ['g', 'h', 'i']
d[0]
#'g'
d[-1]
# 'i'
list(reversed(d))
# ['i', 'h', 'g']
'h' in d
# True
d.extend('jkl')
d
# deque(['g', 'h', 'i', 'j', 'k', 'l'])
d.rotate(1)
d
# deque(['l', 'g', 'h', 'i', 'j', 'k'])
d.rotate(-1)
d
# deque(['g', 'h', 'i', 'j', 'k', 'l'])

deque(reversed(d))
# deque(['l', 'k', 'j', 'i', 'h', 'g'])
d.clear()
d.pop()
# Traceback (most recent call last):
#    File "<pyshell#6>", line 1, in -toplevel-
#        d.pop()
# IndexError: pop from an empty deque

d.extendleft('abc')
d
# deque(['c', 'b', 'a'])
```

#### deque recipes

```python
def tail(filename, n=10):
    'Return the last n lines of a file'
    with open(filename) as f:
        return deque(f, n)

# 오른쪽으로 데이터를 추가하고, 왼쪽으로 팝하여, 최근 추가된 요소를 유지하여 사용할 수 있다.
def moving_average(iterable, n=3):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / n

# deque를 사용하여 round robin 스케줄러 구현
# https://ko.wikipedia.org/wiki/라운드_로빈_스케줄링
def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    iterators = deque(map(iter, iterables))
    while iterators:
        try:
            while True:
                yield next(iterators[0])
                iterators.rotate(-1)
        except StopIteration:
            # Remove an exhausted iterator.
            iterators.popleft()

def delete_nth(d, n):
    d.rotate(-n)
    d.popleft()
    d.rotate(n)
```

## [defaultdict objects](https://docs.python.org/ko/3.7/library/collections.html?highlight=collections#defaultdict-objects)

등록되어 있지 않은 키를 호출해도 KeyError가 발생하지 않고, 지정된 기본값을 반환한다.

- `__missing__(key)`
요청 된 키를 찾을 수 없을때 클래스의 `__getitem__()`에 의해 `__missing__()`이 호출된다. 기본 dict과 마찬가지로 None을 반환하는 대신 기본값으로 `default_factory`(인스턴스 변수)를 반환한다.

- `default_factory`
`__missing__()`에서 사용된다. `defaultdict`의 첫번째 인수로 지정한다. 생략하면 None으로 초기화되어 일반 dict와 마찬가지로 KeyError가 발생한다.(지정안하면 의미가 없음)

```python
# default_factory를 지정하지 않으면 None으로 지정된다.
c = defaultdict(i=1)
c
# defaultdict(None, {'i': 1})

# default_factory를 지정하지 않고, 없는 키를 호출하면 KeyError가 발생한다.
c['j']
# KeyError: 'j'

# 같은 키의 요소를 연결하기_1
# dict.setdefault()보다 간단하고 빠르다.
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
d
# defaultdict(list, {})
for k, v in s:
    d[k].append(v)
d
# defaultdict(list, {'yellow': [1, 3], 'blue': [2, 4], 'red': [1]})

# 같은 키의 요소를 연결하기_2
# dict.setdefault()으로 구현
d = {}
for k, v in s:
    d.setdefault(k, []).append(v)

sorted(d.items())
# [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]

# 기본값으로 0을 반환 할때는 인수를 int형 객체를 지정한다.
s = 'mississippi'
d = defaultdict(int)
for k in s:
    d[k] += 1

sorted(d.items())
# [('i', 4), ('m', 1), ('p', 2), ('s', 4)]

# 람다 함수를 사용하여 더 빠르고 유연하게 구현할 수 있다.
def constant_factory(value):
    return lambda: value
d = defaultdict(constant_factory('<missing>'))
d.update(name='Jone', action='ran')
'%(name)s %(action)s to %(object)s' % d
'Jone ran to <missing>'

# 인수를 set으로 지정한 예
s = [('red', 1), ('blue', 2), ('red', 3), ('blue', 4), ('red', 1), ('blue', 4)]
d = defaultdict(set)
for k, v in s:
    d[k].add(v)

sorted(d.items())
# [('blue', {2, 4}), ('red', {1, 3})]
```

## [namedtuple()](https://docs.python.org/ko/3.7/library/collections.html?highlight=collections#namedtuple-factory-function-for-tuples-with-named-fields)

tuple은 데이터를 그룹으로 관리할때 자주 사용한다. `namedtuple()`은 정수 인덱스 뿐아니라 ,속성 이름을 지정하여 요소를 취득할 수 있는 튜플의 파생형을 제공한다.

- `collections.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)`
 - typename : 생성할 튜플현의 이름
 - filed_names : 튜플 요소 이름을 지정
 - rename : True일때 잘못된 요소의 이름을 수정

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)
p
# Point(x=11, y=22)
p[0] + p[1]
# 33
x, y = p
x, y
# (11, 22)
p.x + p.y
# 33
```

`namedtuple()`은 csv나 sqlite3에서 반환된 결과 튜즐에 이름을 할당하는데 특히 효과적!

```python
EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

import csv
for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
    print(emp.name, emp.title)

import sqlite3
conn = sqlite3.connect('/companydata')
cursor = conn.cursor()
cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
for emp in map(EmployeeRecord._make, cursor.fetchall()):
    print(emp.name, emp.title)
```

#### namedtuple은 튜플에서 상속받은 메소드 외에도 3가지 메소드와 2가지 속성을 추가로 지원한다!

- `somenamedtuple._make(iterable)`
기존 시퀀스에서 새 인스턴스를 반환

```python
t = [11, 22]
Point._make(t)
# Point(x=11, y=22)
```

- `somenamedtuple._asdict()`
요소의 이름과 값을 매핑한 OrderedDict 인스턴스를 반환

```python
p = Point(x=11, y=22)
p._asdict()
# OrderedDict([('x', 11), ('y', 22)])
```

- `somenamedtuple._replace(**kwargs)`
지정된 필드를 새로운 값으로 교체한 튜플의 새 인스턴스를 반환

```python
p = Point(x=11, y=22)
p._replace(x=33)
# Point(x=33, y=22)
```

- `somenamedtuple._fields`
필드 이름을 나열하는 문자열 튜플을 반환.

```python
p._fields
# ('x', 'y')

# 이렇게 활용하면 됨!
Color = namedtuple('Color', 'red green blue')
Pixel = namedtuple('Pixel', Point._fields + Color._fields)
Pixel(11, 22, 128, 255, 0)
# Pixel(x=11, y=22, red=128, green=255, blue=0)
```

- `somenamedtuple._field_defaults`
dict에 필드 이름을 기본값으로 매핑

```python
Account = namedtuple('Account', ['type', 'balance'], defaults=[0])
Account._field_defaults
# {'balance': 0}
Account('premium')
# Account(type='premium', balance=0)
```

```python
# 지정된 필드를 검색
getattr(p, 'x')
# 11

# dict를 tuple으로 변환(unpacking)
d = {'x': 11, 'y': 22}
Point(**d)
# Point(x=11, y=22)

# sub class를 사용하여 기능을 추가나 변경할 수 있다.
# 계산 된 필드와 고정 너비, print 형식을 추가하는 예
class Point(namedtuple('Point', ['x', 'y'])):
    __slots__ = () # 인스턴스 dict 작성으로 방지하여 메모리 요구사항을 낮게 유지
    @property
    def hypot(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5
    def __str__(self):
        return 'Point: x=%6.3f y=%6.3f hypot=%6.3f' % (self.x, self.y, self.hypot())

    for p in Point(3, 4), Point(14, 5/7):
        print(p)
# Point: x= 3.000 y= 4.000 hypot= 5.000
# Point: x=14.000 y= 0.714 hypot=14.018

# 기존에 선언한 namedtuple의 필드에 새로운 필드를 추가한 튜플 유형을 구현
Point3D = namedtuple('Point3D', Point._fields + ('z',))
Point3D('a', 'v', 'z')
# Point3D(x='a', y='v', z='z')

# __doc__ 필드에 직접 할당하여 문서 문자열을 사용자 정의 할 수 있습니다 .
Book.__doc__ += ': Hardcover book in active collection'
Book.id.__doc__ = '13-digit ISBN'
Book.title.__doc__ = 'Title of first printing'
Book.authors.__doc__ = 'List of authors sorted by last name'

# _replace()를 사용하여 기본값을 구현할 수 있다.
Account = namedtuple('Account', 'owner balance transaction_count')
default_account = Account('<owner name>', 0.0, 0)
johns_account = default_account._replace(owner='Jone')
johns_account
# Account(owner='Jone', balance=0.0, transaction_count=0)

```
