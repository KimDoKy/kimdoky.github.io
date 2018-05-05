---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 시퀀스를 슬라이스하는 방법을 알자
category: python
tags: [ 'python' ]
---

파이썬은 시퀀스를 슬라이스(slice)해서 조각으로 만드는 문법을 제공하다.  
가장 간단한 슬라이싱 대상은 내장 타입인 list, str, bytes이다. `__getitem__`과 `__setitem__`이라는 특별한 메서드를 구현하는 파이썬의 클래스에도 슬라이싱을 적용할 수 있다.  

슬라이싱 문법의 기본 형태는 `somelist[start:end]`이며, 여기서 start 인덱스는 포함되고 end 인덱스는 제외된다.

```python
>>> a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

>>> print('First four:', a[:4])
First four: ['a', 'b', 'c', 'd']

>>> print('Last four: ', a[-4:])
Last four:  ['e', 'f', 'g', 'h']

>>> print('Middle two: ', a[3:-3])
Middle two:  ['d', 'e']
```

리스트의 처음부처 슬라이스할 때는 인덱스 0을 생략한다.  
리스트의 끝까지 슬라이스할 떄도 마지막 인덱스는 생략한다.  
리스트의 끝을 기준으로 오프셋을 계산할 때는 음수로 슬라이스하는 것이 편하다.  

슬라이싱은 start와 end 인덱스가 리스트의 경계를 벗어나도 적절하게 처리한다. 덕분에 입력 시퀀스에 대응해 처리할 최대 길이를 코드로 쉽게 설정할 수 있다.

```python
first_twenty_items = a[:20]
last_twenty_items = a[-20:]

# 이와 대조로 같은 인덱스를 직접 접근하면 예외가 발생한다.
>>> a[20]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```

> 리스트의 인덱스를 음수 변수로 지정하면 슬라이싱으로 뜻밖의 결과를 얻는 상황이 있다. 예를 들어 `somelist[-n:]`이라는 구문은 `somelist[-3:]`처럼 n이 1보다 클 때는 제대로 동작한다. 그러나 n이 0이어서 `somelist[-0:]`이 되면 원본 리스트의 복사본을 만든다.

슬라이싱의 결과는 완전히 새로운 리스트이다. 수정해도 원본에는 영향이 없다.

```python
b = a[4:]
print('Befor:   ', b)
b[1] = 99
print('After:   ', b)
print('No change:', a)

>>>
After:    ['e', 99, 'g', 'h']
Befor:    ['e', 'f', 'g', 'h']
No change:['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
```

`a, b = c[:2]` 같은 튜플 할당과 달리 슬라이스 할당의 길이는 달라도 된다. 할당받은 슬라이스의 앞뒤 값을 유지된다. 리스트는 새로 들어온 값에 맞춰 길이를 조정한다.

```python
print('Before ', a)
a[2:7] = [99, 22, 14]
print('After ', a)

>>>
Before  ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
After  ['a', 'b', 99, 22, 14, 'h']
```

시작과 끝 인덱스를 모두 생략하고 슬라이스하면 원본 리스트의 복사본을 얻는다.

```python
>>> b = a[:]
>>> assert b == a and b is not a
# a와 b는 같지만 a가 b(원본의 복사본)는 아니다.
```

슬라이스에 시작과 끝 인덱스를 지정하지 않고 할당하면(새 리스트를 할당하지 않고) 슬라이스의 전체 내용을 참조 대상의 복사본으로 대체한다.

```python
b = a
print('Before', a)
a[:] = [101, 102, 103]
assert a is b  # 여전히 같은 리스트 객체임
print('After', a)  # 이제 다른 내용을 담음

>>>
Before ['a', 'b', 99, 22, 14, 'h']
After [101, 102, 103]

## 좀 더 간단한 예
>>> a = b
>>> a
[101, 102, 103]
>>> b
[101, 102, 103]
>>> a[:] = [1,2,3,4,5]
>>> a
[1, 2, 3, 4, 5]
>>> b
[1, 2, 3, 4, 5]
```

## 핵심 정리

- 너무 장황하지 않게 하자. 즉, start 인덱스에 0을 설정하거나 end 인덱스에 시퀀스의 길이를 설정하지 말자.
- 슬라이싱은 범위를 벗어난 start나 end 인덱스를 허용하므로 a[:20]이나 a[-20]처럼 시퀀스의 앞쪽이나 뒤쪽 경계에 놓인 슬라이스를 표현하기 쉽다.
- list 슬라이스에 할당하면 원본 시퀀스에 지정한 범위를 참조 대상의 내용으로 대체한다(길이가 달라도 동작한다.)
