---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.8 반복자와 조합하여 처리하기
category: python
tags: [ 'python' ]
---
itertools는 반복자와 조합하여 다양한 처리를 구현할 수 있도록 각종 도구를 제공합니다.  

Python에서는 연속된 일련의 데이터를 반복자를 사용하여 표현합니다. 반복자는 단순한 인터페이스 객체로, 반복자의 __next__() 메서드를 호출하면 반복자의 다음 값을 반환하고 반환할 값이 존재하지 않을 때에는 StopIteration 예외가 발생합니다. Python에서는 반복문이나 데이터 전달 등에서 반복자를 이용합니다.

### 반복자 값을 합치기


### accumulate() 함수
iterable 객체의 모든 값을 더한 결과를 구할 등, 모든 요소를 합쳐 결과를 구할 때는 itertools.accumulate()를 사용합니다.

형식 | itertools.accumulate(iterable func=operator.add)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> func - 두 개의 인수를 취하는 함수를 지정한다. 생략하면 operator.add()가 되어, 요소를 맨 앞부터 순서대로 더한다.
반환값 | accumulate 반복자

다음 예에서는 함수로 두 개 인수의 곲을 반환하는 spam()을 지정하고 있으며, 리스트의 맨 앞 요소인 1이 처음 값이 되고, 다음 값은 spam(1,2), 마지막 값은 spam(2,3)이 반환됩니다.

### itertools.accumulate() 샘플 코드

```python
>>> import itertools
>>> def spam(left, right):
...     return left * right
...

>>> for v in itertools.accumulate([1,2,3], spam):
...     print(v)
...
1
2
6
```

itertools.accumulate()는 지정한 iterable 객체의 처음 값을 초깃값으로 하며, 이어서 초깃값과 iterable 객체 다음 값을 인수로서 함수를 호출하여 그 결과값을 반환합니다. 이 후의 값은 앞에서 함수를 호출한 결과값과 iterable 객체의 다음 값을 인수로서 다시 함수를 호출한 결과값이 됩니다.

### itertools.accumulate()의 동작

```python
>>> it = itertools.accumulate([1,2,3,4], spam)
>>> next(it)  # 처음 값은 iterable 객체의 맨 앞 값
1
>>> next(it)  # left:1 right:2 처음 값(=1) * 2 = 2
2
>>> next(it)  # left:2 right:3 처음 값(=2) * 3 = 6
6
>>> next(it)  # left:6 right:4 처음 값(=6) * 4 = 24
24

>>> next(it)  # iterable 객체 종료
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

## iterable 객체 연결하기

### chain() 함수
itertools.chain()은 여러 개의 iterable 객체를 연결한 반복자를 만듭니다.

형식 | itertools.chain(\*iterable)
---|---
인수 | iterable - iterable 객체를 지정한다.
반환값 | chain 반복자

### itertools.chain() 샘플 코드

```python
>>> it = itertools.chain([1,2,3], {'a','b','c'})  # 리스트와 집합을 열결
>>> for v in it:
...     print(v)
...
1
2
3
b
c
a
```

### from_iterable() 함수
itertools.chain.from_iterable()은 연결할 iterable 객체들을 하나의 iterable 객체로 지정합니다.

형식 | itertools.chain.from_iterable(iterable)
---|---
인수 | iterable - 연결할 대상을 반환하는 iterable 객체를 지정한다.
반환값 | chain 반복자

### itertools.chain.from_iterable() 샘플 코드

```python
>>> iters = ([1,2,3], {'a', 'b', 'c'})
>>> for c in itertools.chain.from_iterable(iters):
...     print(c)
...
1
2
3
b
c
a
```

## 값의 순열, 조합, 지적 구하기

### permutations() 함수
itertools.permutations()는 iterable 객체 값을 얻어 지정한 길이의 순열을 만드는 반복자를 생성합니다.

형식 | itertools.permutations(iterable, r)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> r - 순열의 길이를 지정한다.
반환값 | permutations 반복자

### itertools.permutations() 샘플 코드

```python
>>> for v in itertools.permutations('ABC', 2):
...     print(v)
...
('A', 'B')
('A', 'C')
('B', 'A')
('B', 'C')
('C', 'A')
('C', 'B')
```

### combinations() 함수
iterable 객체 값 조합에는 itertools.combinations()를 사용합니다.

형식 | itertools.combinations(iterable, r)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> r - 조합의 길이를 지정한다.
반환값 | combinations 반복자

### itertools.combinations() 샘플 코드

```python
>>> for v in itertools.combinations('ABC', 2):
...     print(v)
...
('A', 'B')
('A', 'C')
('B', 'C')
```

### itertools.combinations_with_replacement() 함수
itertools.combinations_with_replacement()도 마찬가지로 도합을 생성하지만, 같은 값의 중복까지 포함한 조합을 반환합니다.

형식 | itertools.combinations_with_replacement(iterable, r)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> r - 조합의 길이를 지정한다.
반환값 | combinations_with_replacement 반복자

### itertools.combinations_with_replacement() 샘플 코드

```python
>>> for v in itertools.combinations_with_replacement('ABC', 2):
...     print(v)
...
('A', 'A')
('A', 'B')
('A', 'C')
('B', 'B')
('B', 'C')
('C', 'C')
```

### product() 함수
itertools.product()는 직적(direct product, 두 집합의 원소를 하나씩 뽑아 짝짓는 것)을 구합니다. 즉, 여러 개의 iterable 객체를 지정하여 각 객체로부터 요소를 하나씩 추출한 조합을 반환합니다.

형식 | itertools.product(\*iterable, repeat=1)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> repeat - 값을 조합할 횟수를 지정한다. repeat은 키워드 전용 인수이므로, 반드시 repeat=2와 같이 키워드 형식으로 지정한다.
반환값 | product 반복자

### itertools.product() 샘플 코드

```python
>>> for v in itertools.product('ABC', [1,2,3]):
...     print(v)
...
('A', 1)
('A', 2)
('A', 3)
('B', 1)
('B', 2)
('B', 3)
('C', 1)
('C', 2)
('C', 3)
```

### itertools.product('ABC', p1,2,3])의 처리(repeat=1)
repeat는 값을 조합할 횟수를 지정합니다. repeat가 1일 때 itertools.product('ABC',[1,2,3])은 다음과 같은 결과를 반환합니다.

```python
def prod():
    for p in 'ABC':
        for q in [1,2,3]:
            yield(p,q)
```

### itertools.product('ABC', p1,2,3])의 처리(repeat=2)

```python
def prod():
    for p in 'ABC':
        for q in [1,2,3]:
            for r in 'ABC':
                for s in [1,2,3]:
                    yield(p,q,r,s)
```

## iterable 객체의 필터링

### filter() 함수
iterable 객체에서 특정 조건을 만족하는 값만 추출할 때는 내장 함수 filter()를 사용합니다.

형식 | filter(function, iterable)
---|---
인수 | function - None 또는 값을 검사하는 함수를 지정한다. <br> iterable - iterable 객체를 지정한다.
반환값 | filter 반복자

### filter() 샘플 코드

```python
>>> def is_even(n):  # n이 짝수이면 True
...     return n % 2 == 0
...

>>> for v in filter(is_even, [1,2,3,4,5,6]):
...     print(v)
...
2
4
6
```

### filter(None, iterable) 샘플 코드
function에 None을 지정하면 iterable 객체에서 참인 값만을 반환합니다.

```python
>>> items = [1,0,'Spam','',[],[1]]
>>> for v in filter(None, items):
...     print(v)
...
1
Spam
[1]
```

### filterfalse() 함수
itertools.filterfalse()는 filter()와는 반대로, 지정한 함수가 거짓인 값만을 반환하는 반복자를 생성합니다. 함수로서 None을 지정하면 iterable 객체에서 거짓인 값만을 반환하는 반복자를 생성합니다.

형식 | itertools.filterfalse(function, iterable)
---|---
인수 | function - None 또는 값을 검사하는 함수를 지정한다. <br> iterable - iterable 객체를 지정한다.
반환값 | filterfalse 반복자

### itertools.filterfalse() 샘플 코드

```python
>>> def is_even(n):  # n이 짝수이면 True를 반환
...     return n % 2 == 0
...
>>> for v in itertools.filterfalse(is_even, [1,2,3,4,5,6]):
...     print(v)
...
1
3
5
>>> items = [1,0, 'Spam', '', [], [1]]
>>> for v in itertools.filterfalse(None, items):
...     print(v)
...
0

[]
```

### compress() 함수
itertools.compress()에는 data와 selectors 두 개의 iterable 객체를 지정하며, selectors에서 얻은 값이 참이면 data에서 얻은 같은 순번의 값을 반환하는 반복자를 생성합니다.

형식 | itertools.compress(data, selectors)
---|---
인수 | data - iterable 객체를 지정한다.<br> selectors - iterable 객체를 지정하고, 얻은 값이 참이면 data에서 얻은 값을 반복자 값으로서 반환한다.
반환값 | compress 반복자

### itertools.compress() 샘플 코드

```python
>>> for v in itertools.compress(['spam', 'ham', 'egg'], [1,0,1]):
...     print(v)
...
spam
egg
```

## 등차수열 만들기

### count() 함수
itertools.count()는 연속한 두 값의 차가 지정한 공차(증가분) 값이 되는 등차수열의 반복자를 생성합니다.

형식 | itertools.count(start=0, step=1)
---|---
인수 | start - 수열의 초기값을 지정한다. <br> step - 값의 공차를 지정한다.
반환값 | count 반복자

### itertools.count() 샘플 코드

```python
>>> for v in itertools.count(1, 2):
...     if v > 5: break
...     print(v)
...
1
3
5
```

## 반복자에서 범위를 지정하여 값 구하기

### islice() 함수
itertools.islice()는 itertools 객체로부터 지정한 범위의 값을 얻는 반복자를 생성합니다. 리스트 등의 시퀀스 객체로부터 sequence[2:5]로 요소를 얻는 것처럼, 반복자로부터 순번을 지정하여 요소를 얻습니다.

형식 | itertools.islice(iterable, stop) <br> itertools.islice(iterable, start, stop[, step])
---|---
인수 | iterable - 반복자를 지정한다. <br> stop - iterable로부터 값 읽어오기를 종료할 위치를 양의 정수로 지정한다. None을 지정하면 맨 마지막 요소까지 처리를 계속한다. <br> start - iterable로부터 얻을 처음 값 위치를 양의 정수로 지정한다. <br> step - iterable로부터 얻을 값 위치의 증가분을 양의 정수로 지정한다. 생략하면 1이 되며, 모든 값을 반환한다.
반환값 | islice 반복자

### itertools.islice() 샘플 코드

```python
>>> list(itertools.islice([0,1,2,3,4,5,6,7,8,9],5))
[0, 1, 2, 3, 4]

>>> list(itertools.islice(itertools.count(1,1), 3,8,2))
[4, 6, 8]
```


### dropwhile() 함수
itertools.dropwhile()은 반복자로부터 얻은 값이 지정한 함수의 조건을 충족하는 동안은 값을 drop하고, 그 후에는 모든 값을 반환하는 반복자를 생성합니다.

형식 | itertools.dropwhile(predicate, iterable)
---|---
인수 | predicate - 값을 검사하는 함수를 지정한다. <br> iterable - iterable 객체를 지정한다.
반환값 | dropwhile 반복자

### itertools.dropwhile() 샘플 코드

```python
>>> def is_odd(v): return v % 2  # 홀수일 때 True를 반환한다.
...

>>> list(itertools.dropwhile(is_odd, [1,1,1,2,3,4]))
[2, 3, 4]
```

### takewhile() 함수
반대로 itertools.takewhile()은 반복자로부터 얻은 값이 지정한 함수의 조건을 충족하는 동안에만 값을 반환하는 반복자를 생성합니다.

형식 | itertools.takewhile(predicate, iterable)
---|---
인수 | predicate - 값을 검사하는 함수를 지정한다. <br> iterable - iterable 객체를 지정한다.
반환값 | takewhile 반복자

### itertools.takewhile() 샘플 코드

```python
>>> def is_odd(v): return v % 2  # 홀수일 때 True를 반환한다.
...
>>> list(itertools.takewhile(is_odd, [1,1,1,2,3,4]))
[1, 1, 1]
```

## 같은 값을 반복하기

### repeat() 함수
itertools.repeat()는 지정한 값을 반복하는 반복자를 생성합니다.

형식 | itertools.repeat(object, times=None)
---|---
인수 | object - 반복할 값을 지정한다. <br> times - 값을 반복할 횟수를 지정한다. 생략하면 값을 무한 반복한다.
반환값 | repeat 반복자

### itertools.repeat() 샘플 코드

```python
>>> list(itertools.repeat('a', 5))
['a', 'a', 'a', 'a', 'a']
```

### cycle() 함수
itertools.cycle()은 지정한 iterable 객체의 모든 값을 반복하는 반복자를 생성합니다.

형식 | itertools.cycle(itertools)
---|---
인수 | iterable - 반복할 값의 iterable 객체를 지정한다.
반환값 | cycle 반복자

### itertools.cycle() 샘플

```python
>>> for c in itertools.islice(itertools.cycle('abc'), 1, 5):
...     print(c)
...
b
c
a
b
```

## 연속 값 구하기

### groupby() 함수
itertools.groupby()는 지정한 iterable 객체로부터 값을 얻어 연속하는 같은 값을 그룹으로 취합하여 반환하는 반복자를 생성합니다.

형식 | itertools.groupby(iterable, key=None)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> key - 요소를 비교할 값으로 변환하는 함수를 지정한다. 생략하거나 None을 지정하면 요소를 그대로 비교한다.
반환값 | groupby 반복자

itertools.groupby()는 길이 2인 튜플을 반환하며, 맨 앞 요소는 iterable로부터 얻은 값, 두 번째 요소는 연속한 같은 값의 객체를 반환하는 반복자입니다.

### itertools.groupby() 샘플 코드

```python
>>> for value, group in itertools.groupby(['a','b','b','c','c','c']):
...     print(value, group, tuple(group))
...
a <itertools._grouper object at 0x1094ba208> ('a',)
b <itertools._grouper object at 0x1094ba1d0> ('b', 'b')
c <itertools._grouper object at 0x1094ba128> ('c', 'c', 'c')
```

### key를 지정한 itertools.groupby() 샘플 코드
key를 함수로 지정하면 변환한 값으로 그룹을 생성할 수 있습니다.

```python
>>> def is_odd(v): return v % 2

>>> for value, group in itertools.groupby([10,20,31,11,3,4], is_odd):
...     print(value, tuple(group))
...
0 (10, 20)
1 (31, 11, 3)
0 (4,)
```

## 여러 iterable 객체의 요소로 튜플 만들기

### zip() 함수
zip()은 지정한 여러 개의 iterable 객체로부터 값을 하나씩 얻어서 이를 튜플 요소로 반환하는 반복자를 생성합니다.

형식 | zip(\*iterables)
---|---
인수 | iterable - iterable 객체를 지정한다. zip()의 길이는 iterables 중 가장 짧은 iterable 객체와 같은 길이가 된다.
반환값 | zip 반복자

### zip() 샘플 코드

```python
>>> for v in zip((1,2,3),('a','b','c'),('가','나','다')):
...     print(v)
...
(1, 'a', '가')
(2, 'b', '나')
(3, 'c', '다')
```

### 행과 열 교환하기
zip()은 행렬의 행과 열을 교환하는 함수로도 쓸 수 있습니다.

```python
>>> matrix = [(1,2,3),(4,5,6),(7,8,9)]  # 3x3 행혛
>>> transformed = list(zip(*matrix))  # 행과 열을 교환
>>> transformed
[(1, 4, 7), (2, 5, 8), (3, 6, 9)]

>>> list(zip(*transformed))  # 한 번 더 행과 열을 교환하면 원래대로 돌아감
[(1, 2, 3), (4, 5, 6), (7, 8, 9)]
```

### zip_longest() 함수
zip()은 지정한 iterable 객체 중 어떤 하나가 모든 값을 다 반환하면, 다른 iterable 객체에 값이 남아있더라도 종료됩니다. 모든 iterable 객체의 모든 값으로부터 튜플을 생성하려면 itertools.zip_longest()를 사용합니다.

형식 | itertools.zip_longest(\*iterables, fillvalue=None)
---|---
인수 | iterables - iterable 객체를 지정한다. <br> fillvalue - iterable 객체가 고갈될 때 사용할 값을 지정한다.
반환값 | zip_longest 반복자

### itertools.zip_longest() 샘플 코드

```python
>>> for v in itertools.zip_longest('abcdefg', '123', '가나다라마', fillvalue='-'):
...     print(v)
...
('a', '1', '가')
('b', '2', '나')
('c', '3', '다')
('d', '-', '라')
('e', '-', '마')
('f', '-', '-')
('g', '-', '-')
```

## 반복자의 값 변환하기

### map() 함수
반복자의 값에 함수를 적용하여 다른 값으로 변환할 때는 map()을 사용합니다.

형식 | map(func, \*iterables)
---|---
인수 | func - 값을 변환할 함수를 지정한다. <br> iterables - iterable 객체를 지정한다. map()의 길이는 iterables 중 가장 짧은 iterable 객체과 같은 길이가 된다.
반환값 | map 반복자

### map() 샘플 코드

```python
>>> for v in map(chr, [0x40, 0x41, 0x42, 0x43]):
...     print(v)
...
@
A
B
C
```

### map()에 여러 개의 iterable 객체 지정하기

```python
>>> for v in map(min, 'spam', 'ham' , 'egg'):  # min(c1,c2,c3)을 호출하고 최솟값을 반환함
...     print(v)
...
e
a
a
```
Python3에서는 func에 None을 지정할 수 없습니다. 따라서 여러 개의 iterable 객체 요소로부터 튜플을 만들 때에는 zip()을 사용해야 합니다.

### startmap() 함수
iterable 객체가 다른 iterable 객체에 그룹화되어 있을 때에는 itertools.startmap()도 쓸 수 있습니다.

형식 | itertools.startmap(func, iterables)
---|---
인수 | func - 값을 변환할 함수를 지정한다. <br> iterables - iterable 객체를 반환할 iterable 객체를 지정한다.
반환값 | startmap 반복자

itertools.startmap()은 인수를 iterable 객체에 저장하여 지정하는 점을 빼면 map()과 같습니다.

### itertools.startmap() 샘플 코드

```python
>>> iterables = ['spam', 'ham', 'egg']
>>> for v in itertools.starmap(min, iterables):  # min(c1, c2, c3)을 호출하고 최솟값을 반환함
...     print(v)
...
a
a
e

>>> for v in map(min, *iterables):  # starmap(min, iterables)와 map(min, *iterables)는 같다.
...     print(v)
...
e
a
a
```

## 반복자 복제하기

### tee() 함수
itertools.tee()는 iterable 객체의 반복자가 반환하는 값을 저장하여, 같은 값을 반환하는 반복자를 여러 개 생성합니다.

형식 | itertools.tee(iterable, n=2)
---|---
인수 | iterable - iterable 객체를 지정한다. <br> n - 생성할 반복자 수를 지정한다.
반환값 | 복제한 반복자의 튜플

### itertools.tee() 샘플 코드

```python
>>> import random
>>> def values():
...     for i in range(10):
...         yield random.random()
...
>>> iter = values()
>>> a,b,c = itertools.tee(iter, 3)
>>> sum(a), sum(b), sum(c)
(4.15453965708554, 4.15453965708554, 4.15453965708554)
```
