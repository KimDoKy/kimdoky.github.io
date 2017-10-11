---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.4 수치 배열을 효율적으로 다루기
category: python
tags: [ 'python' ]
---
수치 배열을 효울적으로 다루는 기능을 제공하는 array에 대해 다룹니다. array 모듈의 array.array 형은 갱신이 가능한 시퀀스로, 인스턴스를 생성할 때 지정한 종류의 수치 데이터만 지정합니다.  

array.array는 요소를 Python 객체가 아닌 플랫폼 고유의 이진(binary) 데이터로서 저장하기 때문에, 리스트나 튜플 등과 비교할 때 메모리 효율이 뛰어납니다.

## array.array에 수치 저장하기

array.array는 저장할 값의 종류를 문자로 지정하여 생성합니다.

### array.array 객체 생성하기

```python
>>> import array
>>> arr = array.array('f', [1,2,3,4])  # 단정밀도 부동소수점 array
>>> arr
array('f', [1.0, 2.0, 3.0, 4.0])
```

### array 클래스

형식 | class array(typecode[, initializer])
---|---
인수 | typecode -  array 요소의 자료형 지정 문자 목록에 따른 문자로 지정한다. <br> initializer - array의 초깃값 시퀀스 또는 반복자를 지정한다.
반환값 | array 객체

### 자료형 지정 문자 목록

자료형 지정 문자 | C 언어의 자료형 이름 | Python 자료형 이름 | 최소 바이트 수
---|---|---|---
'b' | signed char | int | 1
'b' | unsigned char | int | 1
'u' | Py)UNICODE | int | 2
'h' | signed short | int | 2
'H' | unsigned short | int | 2
'i' | signed int | int | 2
'I' | unsigned int | int | 2
'l' | signed long | int | 4
'L' | unsigned long | int | 4
'q' | signed long long | int | 8
'Q' | unsigned long long | int | 8
'f' | float | float | 4
'd' | double | float | 8

> 'u'는 권장하지 않음  
> 'Q', 'f'는 python을 빌드한 C 컴파일러가 long long 형을 지원하는 경우에만 사용 가능함.

array,array 객체는 시퀀스 객체로, 리스트 객체 등과 마찬가지로 요소를 추가하거나 삭제할 수 있습니다.

### array.array 객체 조작

```python
>>> arr.append(100.0)  # 요소 추가
>>> arr[2] = 200.    # 요소 갱신
>>> arr
array('f', [1.0, 2.0, 200.0, 4.0, 100.0])

>>> del arr[-1]  # 맨 마지막 요소를 삭제
>>> arr
array('f', [1.0, 2.0, 200.0, 4.0])

>>> sum(arr)  # 요소의 합을 구함
207.0
```

## 이진 데이터의 입출력
array.array 객체는 파일에 이진 데이터를 출력하는 tofile() 메소드를 제공합니다.

### array.array 객체를 파일에 출력하기

```python
>>> arr = array.array('i', (1,2,3,4,5))  # int형 수치 array
>>> with open('bin-int', 'wb') as f:   # 모드를 'b'로 하여 파일 읽기
...     arr.tofile(f)
...
```

파일로부터 이진 데이터를 읽어올 때는 fromfile() 메서드를 사용합니다.

### 파일에서 array.array 객체를 불러오기

```python
>>> arr = array.array('i')
>>> with open('bin-int', 'rb') as f:  # 모드를 'b'로 하여 파일 열기
...     arr.fromfile(f, 5)
...
>>> arr
array('i', [1, 2, 3, 4, 5])
```

### fromfile() 메서드

형식 | array.fromfile(f, n)
---|---
인수 | f - 요소를 읽어올 파일 객체를 지정한다. <br> n - 읽어오는 요소 수를 지정한다.

### tofile() 메서드

형식 | array.tofile(f)
---|---
인수 | f - 요소를 출력할 파일 객체를 지정한다.
