---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.1 다양한 컨테이너형 다루기
category: python
tags: [ 'python' ]
---
Python에는 내장형의 리스트나 사전, 집합 등의 범용적인 자료구조가 있습니다. 또한, 그외에도 다양한 용도로 활용할 수 있는 자료구조를 표준 라이브러리로 제공하고 있습니다.  

목적에 맞는 자료구조와 알고리즘을 적절하게 선택할 수 있도록, 각각의 기능과 특징을 잘 이해해야 합니다.

## 다양한 컨테이너형 다루기
다른 객체를 등록하여 효율적으로 관리할 수 있는 컬렉션을 제공하는 collections에 대해 다룹니다.

### 데이터의 횟수 세기
입력 데이터로부터 각 값의 출현 횟수를 셀 때는 collections.Counter를 사용하면 됩니다.

### collections.Counter 샘플 코드

```python
>>> import collections
>>> c = collections.Counter()
>>> c['spam'] += 1  # 'spam'을 카운트 업
>>> c[100] += 1    # 100을 카운트 업
>>> c[200] += 1    # 200을 카운트 업
>>> c[200] += 3    # 200을 카운트 업
>>> c
Counter({200: 4, 100: 1, 'spam': 1})
```
collections.Counter는 dict형에서 파생된 클래스로, dict에 데이터의 건수를 카운트하는 기능을 추가한 것입니다.

### Counter 클래스

형식 | class Counter([iterable-or-mapping],[key=value, key=value, ...])
---|---
인수 | iterable-or-mapping - Counter 객치의 초깃값을 지정하는 매핑 객체 또는 iterable 객체를 지정한다. <br> key - Counter 객체에 등록할 키 값을 지정한다. <br> value - key에 대응하는 값을 지정한다.
반환값 | Counter 객체


collections.Counter에 dict 등의 매핑 객체를 지정하면 같은 키와 값을 갖는 Counter 객체를 생성합니다. 키 값을 열거하는 iterable 객체를 지정하면 각각의 키 값의 개수를 값으로 하여 Counter 객체를 생성합니다.

### collections.Counter 객체 구축

```python
>>> counter = collections.Counter(
...     [1,2,3,1,2,1,2,1])
>>> counter
Counter({1: 4, 2: 3, 3: 1})
```

등록되어 있지 않은 키 값은 0이 됩니다. 등록되어 있지 않은 키를 참조하더라도 KeyError 예외는 발생하지 않습니다.

### 미등록 키를 참조할 때

```python
>>> counter = collections.Counter() # 빈 Counter
>>> counter
Counter()
>>> counter['spam'] # 존재하지 않는 요소를 참조해도 오류는 발생하지 않는다.
0
>>> counter['spam'] += 1  # 'spam'을 추가
>>> counter
Counter({'spam': 1})
```

Counter 객체는 일반 dict 객체의 메서드 외에도, 추가로 다음 표에 정리한 메서드를 제공합니다.

### Counter 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
elements() | 요소의 키를 값 수 만큼 반복하는 반복자(iterable)를 반환한다. | 키 값의 반복자
most_common([n]) | 값이 큰 순서대로 키와 값 한 쌍을 반환한다. n에 정숫값을 지정하면 최대 n건의 요소를 반환한다. | 리스트 객체
subtract([iterable-or-mapping]) | 요소로부터 iterable 또는 매핑 객체의 값을 뺀다. | None

Counter 객체는 다음 3개의 표에 나타낸 연산자를 지원합니다.

### Counter 객체가 지원하는 이항 연산자

연산자 | 설명
---|---
+ | 두 개의 Counter 객체의 모든 요소로부터 Counter 객체를 생성한다. 같은 키의 요소는 값을 더한다.
- | 좌변의 Counter 객체 요소에서 우변의 Counter 객체와 같은 키의 요소 값을 뺀 값으로 새롭게 Counter 객체를 생성한다. 뺄센 결괏값이 음수가 되는 요소는 포함되지 않는다.
& | 두 개의 Counter 객체 요소 중, 양쪽에 동시에 존재하는 키의 값으로부터 새롭게 Counter 객체를 생성한다. 요소의 값은 두 값 중 작은 쪽이 된다.
\| | 두 개의 Counter 객체의 모든 요소로 새롭게 Counter 객체를 생성한다. 키가 같으면 두 값 중 큰 쪽의 값이 된다.

### Counter 객체가 지원하는 누계 연산자

연산자 | 설명
---|---
+= | 좌변의 Counter 객체에 우변의 Counter 객체의 요소를 추가한다. 같은 키의 요소는 값을 더한다.
-= | 좌변의 Counter 객체 요소에서 우변의 Counter 객체의 같은 키 값을 갖는 요소 값을 뺀다. 계산 결괏값이 음수가 되는 요소는 삭제됩니다.
&= | 좌변의 Counter 객체 요소 중, 우변의 Counter 객체의 요소에 포함되어 있지 않은 키의 요소를 삭제한다. 요소의 값은 두 가지 값 중 작은 쪽의 값이 된다.
\|= | 두 개의 Counter 객체 전체의 요소로부터 새롭게 Counter 객체를 생성한다. 키가 같으면 두 값 중 큰 쪽의 값이 된다.

### Counter 객체가 지원하는 단항 연산자

연산자 | 설명
---|---
+ | 빈 Counter 객체에 더한다.
- | 빈 Counter 객체에서 뺀다.

### collections.Counter의 연산자

```python
>>> counter1 = collections.Counter(spam=1, ham=2)
>>> counter2 = collections.Counter(ham=3, egg=4)
>>> counter1 + counter2
Counter({'ham': 5, 'egg': 4, 'spam': 1})

>>> counter1 - counter2
Counter({'spam': 1})

>>> counter1 & counter2
Counter({'ham': 2})

>>> counter1 | counter2
Counter({'egg': 4, 'ham': 3, 'spam': 1})

>>> counter1 += counter2
>>> counter1
Counter({'ham': 5, 'egg': 4, 'spam': 1})
```

연산 결과에는 값이 0 이하인 요소는 포함되지 않습니다.

### 음수인 카운터 값

```python
>>> counter1 = collections.Counter(spam=-1, ham=2)
>>> counter2 = collections.Counter(ham=2, egg=-3)
>>> counter1 + counter2
Counter({'ham': 4})

>>> counter1 - counter2
Counter({'egg': 3})
```

단항 연산자 +와 -는 비어 있는 Counter 객체와 덧셈, 뺄셈을 수행합니다.

### collections.Counter의 단항 연산자

```python
>>> counter1 = collections.Counter(spam=-1, ham=2)
>>> +counter1
Counter({'ham': 2})

>>> -counter1
Counter({'spam': 1})
```

## 여러 개의 dict 요소를 모아서 하나의 dict으로 만들기
collections.ChainMap은 여러 개의 dict 객체를 모아서 각각의 dict 요소를 하나의 dict으로 검색할 수 있게 만듭니다.

### collections.ChainMap 샘플 코드

```python
>>> d1 = {'spam' : 1}
>>> d2 = {'ham' : 2}
>>> c = collections.ChainMap(d1, d2)  # d1, d2를 묶음
>>> c['spam']  # d1['spam']을 구함
1
>>> c['ham']  # d2['hsm']를 구함
2
```

collections.ChainMap에는 dict 등의 맵핑 객체를 등록합니다. collections.ChainMap 객체의 요소를 구하면, 등록한 매핑 객체를 등록 차례에 따라 검색하여 발견된 요소의 값은 반환합니다.

### ChainMap 클래스

형식 | class ChainMap([map1, map2, ...])
---|---
인수 | map1, map2, ... - 합칭 매핑 객체를 지정한다.
반환값 | ChainMap 객체

collections.ChainMap 객체의 요소를 추가 또는 삭제하게 되면, 맨 앞에 등록한 매핑 객체에 반영됩니다.

### collections.ChainMap의 갱신

```python
>>> d1 = {'spam':1}
>>> d2 = {'ham':2}
>>> c1 = collections.ChainMap(d1,d2)
>>> c1['bacom'] = 3  # 사전 d1에 'bacon'을 추가
>>> d1
{'bacom': 3, 'spam': 1}

>>> c1.clear()  # 사전 d1을 클리어
>>> d1
{}
```
collections.ChainMap 객체에는 다음과 같은 속성과 메서드가 있습니다.

### ChainMap 객체의 속성과 메서드

속성/메서드 이름 | 설명 | 반환값
---|---|---
map | 등록된 매핑 객체의 리스트 |
parents | 맨 앞에 등록된 매핑 객체 이외의 매핑 객체를 요소로 하여 새로운 ChainMap 객체를 생성하는 속성 | ChainMap 객체
new_child(m=None) | 매핑 객체 m과 등록된 모든 매핑 객체를 요소로 하여 새 ChainMap 객체를 생성한다. | ChainMap 객체

## 기본값이 있는 dict
보통 dict 객체는 등록되어 있지 않은 키를 참조하면 KeyError 예외가 발생합니다. 그러나 collections.defaultdict는 dict에서 파생된 클래스지만, 등록되어 있지 않은 키를 참조해도 예외가 발생하지 않고 기본값으로 지정된 값을 반환합니다.

### collections.defaultdict 샘플 코드

```pyhton
>>> d = {'spam':100}  # 일반 dict
>>> d['ham']  # 미등록 키를 참조하면 오류 발생
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'ham'
>>> d['spam']  # 등록된 요소
100
>>> def value():
...     return 'default-value'
...

>>> d = collections.defaultdict(value, spam=100)
>>> d
defaultdict(<function value at 0x1074b2ae8>, {'spam': 100})
>>> d['ham']
'default-value'
```

collections.defaultdict는 미등록 키가 참조될 때, 값을 반환하는 호출 가능 객체를 지정해서 작성합니다.

### defaultdict 클래스

형식 | class defaultdict([default_factory, ...])
---|---
인수 | default_factory - 미등록 키 값이 참조될 때 값을 반환할 호출 가능 객체를 지정한다. 생략하면 None이 되며 미등록 키를 참조하면 일반 dict와 마찬가지로 예외가 발생합니다. <br> ... - dict()와 마찬가지로 dict의 초깃값을 지정한다.
반환값 | defaultdict 객체

기본값으로 수치 0을 반환할 때는 인수에 int형 객체를 지정합니다. 또한, 기본값으로 빈 dict나 리스트를 반환할 때도 각각 dict나 list형 객체를 지정합니다.

### 초깃값으로 형 객체 지정

```python
>>> c = collections.defaultdict(int)  # 숫자 0을 기본값으로
>>> c['spam']
0

>>> c = collections.defaultdict(list)  # 새 리스트르 기본값으로
>>> c['spam'].append(100)
>>> c['spam'].append(200)
>>> c
defaultdict(<class 'list'>, {'spam': [100, 200]})
```

미등록 요소에 대하여 += 이나 -= 등의 누계 연산자도 사용할 수 있습니다.

### defaultdict에 누계 연산자 사용

```python
>>> c = collections.defaultdict(int)  # 숫자 0을 기본값으로
>>> c['spam'] += 100  # c['spam']=c['spam']+100 과 같음
>>> c
defaultdict(<class 'int'>, {'spam': 100})
```

## 등록 순서를 저장하는 dict
일반 dict 객체로부터 for 문 등으로 요소 리스트를 얻을 때, 요소를 가져오는 순서는 일정하지 않습니다. 같은 처리를 두 번 반복하면 첫 번째와 두 번째에 다른 순서로 요소를 가져올 가능성이 있습니다.  

collections.OrderedDict는 요소를 등록한 순서를 기록해두는 dict 객체로 요소 리스트를 항상 등록된 순서에 따라 구합니다.

### collections.OrderedDict 샘플 코드

```python
>>> d = collections.OrderedDict()  # OrderedDict 생성
>>> d['spam'] = 100
>>> d['ham'] = 200
>>> for key in d: print(key)  # 항상 등록 순서대로 요소를 구함
...
spam
ham
```

collections.OrderedDict는 dict형과 마찬가지로 다른 dict나 시퀀스, 키워드 인수 등으로 초깃값을 지정해 생성할 수 있습니다. 이때 시퀀스를 지정한 경우에는 시퀀스의 요소순으로 등록되며, 요소의 순서도 기록됩니다.  

하지만 다른 dict를 초깃값으로 지정할 때, 그 dict이 collections.OrderedDict가 아니라면 dict로부터 요소를 가져오는 순서는 정해져 있지 않습니다. 따라서 collections.OrderedDict의 요소도 어떤 순서로 등록되는지 알 수 없습니다.  

또한, 키워드 인수로 초깃값을 지정한 경우에도 collections.OrderedDict의 요소 등록은 키워드 인수의 지정 순서와 일치하지 않습니다. Python에서는 collections.OrderedDict를 호출할 때, 모든 키워드 인수를 바탕으로 dict 객체를 생성하여 이를 collections.OrderedDict에 인수로 건네게 됩니다. collections.OrderedDict는 이렇게 전달받은 키워드 인수의 dict로부터 요소를 가져와서 초깃값을 등록하는데, 이때 dict로부터 요소를 가져오는 순서가 정해져 있지 않기 때문입니다.

### collections.OrderedDict의 초깃값

```python
>>> d = collections.OrderedDict([('spam',100),('ham',200)]) # 시퀀스로 초깃값 설정
>>> d  # 요소는 지정 순서대로 기록됨
OrderedDict([('spam', 100), ('ham', 200)])

>>> d = collections.OrderedDict({'spam':100, 'ham':200}) # 사전으로 초깃값 설정
>>> d  # 요소 등록 순서는 정해져 있지 않음
OrderedDict([('ham', 200), ('spam', 100)])

>>> d = collections.OrderedDict(spam=100, ham=200) # 키워드 인수로 초깃값 설정
>>> d  # 요소등록 순서는 정해져 있지 않음
OrderedDict([('ham', 200), ('spam', 100)])
```

collections.OrderedDict 객체는 다음과 같은 메서드를 제공합니다.

### OrderedDict 객체의 메서드

매서드 이름 | 설명 | 반환값
---|---|---
popitem(last=True) | last가 True인 경우, 맨 마지막에 등록한 요소를 dict에서 삭제하고 반환한다. last가 True가 아니면 맨 처음에 등록된 요소를 dict에서 삭제하고 반환한다. | 삭제한 객체
move_to_end(key, last=True) | last가 True인 경우, 지정한 키를 맨 끝으로 이동한다. last가 True가 아니면 지정한 키를 맨 처음으로 이동한다.

## 튜플을 구조체로 활용하기
Python에서 데이터를 그룹으로 관리할 때 튜플을 자주 사용합니다. 예를 들어 3차원 좌표는 (100, -10, 50)과 같은 튜플로 보관하는 것이 일반적입니다. collections.namedtuple은 정수 인덱스 값뿐만 아니라, 속성 이름을 지정하여 요소를 취득할 수 있는 튜플의 파생형을 제공합니다.

### collections.namedtuple의 사용 예

```python
>>> Coordinate = collections.namedtuple('Coordinate', 'X, Y, Z')
>>> c1 = Coordinate(100, -50, 200)
>>> c1
Coordinate(X=100, Y=-50, Z=200)

>>> c1.X
100
```

collections.namedtuple은 지정한 요소를 갖는 튜플의 파생형을 생성합니다.

### namedtuple() 함수

형식 | namedtuple(typename, field_names, verbose=False, rename=False)
---|---
인수 | typename - 생성할 튜플형의 형 이름을 지정한다. <br> field_names - 튜플 요소 이름을 지정한다. 요소 이름 시퀀스 또는 요소 이름을 공백이나 쉼표로 구분하여 문자열로 지정한다. <br> verbose - 클래스를 정의하는 스크립트를 출력한다. <br> rename - True일 때 잘못된 요소 이름을 자동으로 올바른 이름으로 변환한다.
반환값 | namedtuple 객체

collections.namedtuple의 메모리 사용량은 일반 튜플과 같으며, 일반 클래스 인스턴스나 dict보다 효율적으로 데이터를 관리할 수 있습니다.

## deque(양끝 리스트) 이용하기
collections.deque는 "double ended queue(양끝 큐)"라고 불리는 자료구조로, 큐의 맨 앞과 맨 끝에서 데이터 추가와 삭제를 등록된 데이터 수와 관계없이 일정한 속도로 수행합니다.

### deque 클래스

형식 | class deque([iterable, [maxlen]])
---|---
인수 | iterable - deque의 초깃값을 지정한다. <br> maxlen - deque의 최대 요소 수를 지정한다. 요소 수가 지정한 값 이상이 되면 요소를 맨 앞에 추가할 때는 끝에서부터 요소를 삭제하고, 끝에 추가할 때는 맨 앞부터 요소를 삭제한다.
반환값 | deque 객체

deque는 시퀀스 객체로, 리스트 등과 마찬가지로 인덱스를 사용해 요소에 접근할 수 있습니다. 단 deq[1:2]처름 슬라이스를 지정하여 참조할 수는 없습니다.

### collections.deque에 인덱스로 접근

```python
>>> deq = collections.deque('spam')
>>> deq
deque(['s', 'p', 'a', 'm'])

>>> deq[1]
'p'

>>> deq[1] = 'P'
>>> deq
deque(['s', 'P', 'a', 'm'])

>>> deq[1:-1]  # 슬라이스 연산은 지원하지 않음
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: sequence index must be integer, not 'slice'
```

하지만 인덱스를 사용하여 deque 객체 중간에 있는 요소에 접근하면, 요소 수에 따라 처리에 시간이 걸리게 됩니다. 이런 처리가 필요할 때는 deque 객체가 아니라 리스트 객체를 사용하는 편이 빠르게 처리할 수 있습니다.  

요소의 추가나 삭제가 큐의 맨 처음과 끝에서만 이루어지는 처리일 때는 deque의 특징을 활용할 수 있습니다. deque객테는 deque 양끝에 데이터를 추가, 삭제하는 메서드를 다음 표와 같이 제공합니다.

### deque 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
append(x) | x를 deque 끝에 추가한다. |
appendleft(x) | x를 deque 맨 앞에 추가한다. |
extend(iterable) | 리스트 등 iterable 객체의 요소를 deque 끝에 추가한다. |
extendleft(iterable) | 리스트 등 iterable 객체의 요소를 deque 맨 앞에 추가한다. iterable 객체 요소는 맨 처음 요소부터 하나씩 deque 맨 앞에 추가되므로, iterable 객체와는 반대 순서로 deque에 저장된다. |
pop() | deque에서 맨 끝 요소를 가져와 그 값을 반환한다. deque 요소가 존재하지 않으면 IndexError 예외가 발생한다. | 빼낸 객체
popleft() | deque에서 맨 앞 요소를 가져와 그 값을 반환한다. deque 요소가 존재하지 않으면 IndexError 예외가 발생한다. |  빼낸 객체

다음은 deque 객체를 이용하여 최신 데이터 5건의 이동 평균을 계산하는 처리 예입니다.

### 이동 평균 계산

```python
>>> deq = collections.deque(maxlen=5)
>>> for v in range(10):
...     deq.append(v)
...     if len(deq) >= 5:
...         print(list(deq), sum(deq)/5)
...
[0, 1, 2, 3, 4] 2.0
[1, 2, 3, 4, 5] 3.0
[2, 3, 4, 5, 6] 4.0
[3, 4, 5, 6, 7] 5.0
[4, 5, 6, 7, 8] 6.0
[5, 6, 7, 8, 9] 7.0
```

deque 객체 조작 중에 특이한 것으로 rotate(n) 메서드라는 것이 있습니다. n에 양의 정수를 지정하면 deque 객체 요소가 오른쪽으로 회전하고, 음의 정수를 지정하면 왼쪽으로 회전합니다.

### deque.rotate 샘플 코드

```python
>>> deq = collections.deque('12345')
>>> deq
deque(['1', '2', '3', '4', '5'])

>>> deq.rotate(3)  # 오른쪽으로 회전
>>> deq
deque(['3', '4', '5', '1', '2'])

>>> deq.rotate(-3)  # 왼쪽으로 회전
>>> deq
deque(['1', '2', '3', '4', '5'])
```

deque 객체의 맨 앞 요소와 두 번째 요소를 교환하는 처리는 rotate() 메서드르 랏용하여 다음과 같이 작성할 수 있습니다.

```python
>>> deq = collections.deque('12345')
>>> first = deq.popleft()  # 맨 앞 요소를 빼냄
>>> first
'1'

>>> deq.rotate(-1)  # 왼쪽으로 회전시켜 현재 맨 앞 요소를 뒤로 보냄
>>> deq.appendleft(first)  # 맨 앞에 원래 맨 앞에 있었던 요소를 추가함
>>> deq.rotate(1)  # 오른쪽으로 회전하여 다시 제자리로 되돌림
>>> deq
deque(['2', '1', '3', '4', '5'])
```
