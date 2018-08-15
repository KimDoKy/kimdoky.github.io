---
layout: post
section-type: post
title: 컴퓨터 공학 - 자료구조
category: algorism
tags: [ 'algorism' ]
---

## 자료 구조(data structure)

- 데이터를 효율적으로 검색, 변경, 삭제할 수 있도록 저장, 관리하는 방법
- 가장 기본적인 자료 구조는 배열(array)
 - 메모리에 순서대로 할당하기 때문에 캐시 히트가 일어날 확률이 매우 높음
 - 배열 안에 변수 위치를 인덱스로 나타냄. 인덱스를 통해 변수를 빠르게 접근함
 - 데이터 검색은 빈번하게 일어나지만 새로운 데이터 삽입이 없을 때 유리
- 데이터 검색보다 새로운 데이터 삽입이나 기존 데이터 삭제가 많다면 연결 리스트(linked list)를 사용하는 것이 적합

자료 구조의 핵심
- 삽입(insert)
- 검색(search)
- 삭제(delete)

추상 자료형
ADT(Absttact Data Type)
- 자료 구조에서 삽입, 탐색, 삭제 등을 담당하는 함수들의 사용 설명서
- 추상화 : 인터페이스와 구현을 분리
 - 인터페이스 : 함수의 이름, 인자, 반환형 등을 명시한 것

```python
>>> help(list.append)
Help on method_descriptor:

append(...)
    L.append(object) -> None -- append object to end
# 인터페이스
## append : 함수의 이름
## object : 인자
## None : 반환형
```

## 연결 리스트(linked list)

- 데이터와 참조로 구성된 노드가 한 방향 또는 양방향으로 쭉 이어져 있는 자료 구조
- 참조는 다음 노드나 이전 노드를 가리킴

### 노드
- 자료 구조를 구현할 때 데이터를 담는 틀

```python
class Node:
    def __init__(self, data=None):
       # 노드는 데이터 부분과
       # 다음 노드를 가리키는 참조 부분을 가진다.
       self.__data = data
       self.__next = None

   # 노드 삭제를 확인하기 위한 코드
   def __del__(self):
       print('data of {} is deleted'.format(self.data))

   @property
   def data(self):
       return self.__data

   @data.setter
   def data(self, data):
       self.__data = data

   @property
   def next(self):
       return self.__next

   @next.setter
   def next(self, n):
       self.__next = n
```

### 연결 리스트 구현

- 단일 연결 리스트 : 단일 연결 리스트의 노드에는  참조가 하나만 있음
- 이중 연결 리스트 : 다음 노드를 가리키는 참조와 이전 노드를 가리키는 참조가 있음
- 단일 연결 리스트 클래스의 멤버는 연결 리스트의 첫 번째 데이터를 가리키는 head, 마지막 데이터르 ㄹ가리키는 tail, 리스트에 저장된 데이터의 개수를 나타내는 d_size로 구성됨.

#### 연결 리스트의 추상 자료형(ADT)
- `S.append(data) -> None` : 데이터를 삽입하는 함수.
- `S.search_target(target, start=0) -> (data, pos)` : 데이터를 검색하는 첫 번째 함수. 데이터를 순회하면서 대상 데이터를 찾아 그 위치와 함께 반환.
- `S.search_pos(pos) -> data` : 데이터를 검색하는 두 번째 함수. 인자로 위치픞 전달하면 연결 리스트에서 해당 위치에 있는 데이터를 반환
- `S.remove(target) -> data` : 데이터를 삭제하는 함수. 데이터를 지우면서 해당 데이터를 반환
- `S.empty() -> bool` : 연결 리스트가 비어있으면 True
- `S.size() -> int` : 연결 리스트의 데이터 개수를 반환

#### 생성자, empty(), size()

```python
class Linked_list:
    def __init__(self):
        # 연결 리스트의 첫 번째 노드를 가리킴
        self.head = None
        # 연결 리스트의 마지막 노드를 가리킴
        self.tail = None
        # 데이터 개수
        self.d_size = 0

    def empty(self):
        if self.d_size == 0:
            return True
        else:
            return False

    def size(self):
        return self.d_size
```

#### append() 함수의 구현: 데이터 삽입
새로운 노드를 만들어 다음 데이터를 저장하고 이 노드를 연결 리스트의 마지막에 추가한다.
연결 리스트가 비어 있을 경우와 데이터가 한 개 이상 있을 경우의 수가 있음

```python
def append(self, data):
    # 삽입할 노드를 만든다
    new_node = Node(data)
    # 첫 번째 경우
    # 리스트가 비어 있을 때
    if self.empty():
        self.head = new_node
        self.tail = new_node
        self.d_size += 1
    # 데이터가 한 개 이상 있을 때
    else:
        self.tail.next = new_node
        self.tail = new_node
        self.d_size += 1
```

#### search_target(), search_pos() 함수 구현: 데이터 검색(순회)
- 연결 리스트를 처음부터 끝까지 순회하며 대상 데이터를 찾거나 위치를 통해 데이터를 가져옴
- 인덱싱을 통해 한번에 접근할 수 없고, 매번 처음부터 순서대로 순회해야 하는 단점이 있음

```python
    def search_target(self, target, start=0):
        '''
        search_target(target, start=0) -> (data, pos)
        start로부터 target과 일치하는 첫 번째 데이터와 그 위티를 반환
        target이 존재하지 않을 때: -> (None, None)
        '''
        if self.empty():
            return None
        # 첫 번째 노드를 기리킨다
        pos = 0
        # 노드의 순회 코드
        cur = self.head
        # pos가 탐색 시작 위치 start보다 클 때만
        # 대상 데이터와 현재 노드의 데이터를 비교
        if pos >= start and target == cur.data:
            return cur.data, pos

        while cur.next:
            pos += 1
            # 노드의 순회 코드
            # cur이 노드의 next를 통해 다음 노드로 이동
            cur = cur.next
            # pos가 탐색 위치 start보다 클 때만
            # 대상 데이터와 현재 노드의 데이터를 비교
            if pos >= start and target == cur.data:
                return cur.data, pos

            return None, None
```

- search_pos() 함수도 연결 리스트를 순회하면서 검색하는 것은 search_target() 함수와 같지만, 데이터로 위치를 전달해 해당 위치에 있는 데이터를 반환한다는 점이 다르다.

```python
def search_pos(self, pos):
    '''
    search_pos(pos) -> data
    pos가 범위를 벗어날 때 -> None
    '''
    # pos가 범위를 벗어나면 None을 반환
    if pos > self.size() - 1:
        return None

    cnt = 0
    cur = self.head
    if cnt == pos:
        return cur.data
    # cnt가 pos와 같아질 때 순회를 멈춘다
    while cnt < pos:
        cur = cur.next
        cnt += 1

    return cur.data
```

#### remove() 함수의 구현: 데이터의 삭제

- 대상 데이터가 있으면 해당 데이터를 삭제하고, 삭제된 데이터를 반환
- 대상 데이터가 없으면 None을 반환
- 4가지 고려사항
 - 1. 데이터 개수가 1개 일 경우
 - 2. 지우려는 노드가 head가 가리키는 노드일 경우
 - 3. 지우려는 노드가 tail이 가리키는 노드일 경우
 - 4. 앞의 3가지 예외 이외의 일반적인 경우

```python
def remove(self, target):
    if self.empty():
        return None

    # before는 current 노드의 이전 노드를 가리킨다
    # 삭제할 때 요긴하게 쓰인다
    bef = self.head
    cur = self.head

    # 삭제 노드가 첫 번째 노드일 때
    if target == cur.data:
        # 데이터가 하나일 때
        if self.size() == 1:
            self.head = None
            self.tail = None
        # 데이터가 두 개 이상일 때
        else:
            self.head = self.head.next
        self.d_size -= 1
        return cur.data

    while cur.next:
        bef = cur
        cur = cur.next
        # 삭제 노드가 첫 번때 노드가 아닐 때
        if target == cur.data:
            # 삭제 노드가 마지막 노드일 때
            if cur == self.tail:
                self.tail = bef
            # 일반적인 경우
            bef.next = cur.next
            self.d_size -= 1
            return cur.data

    return None
```

- 노드 삭제는 레퍼런스 카운팅을 0으로 만들면 됨
- 파이썬의 가비지 컬렉션은 레퍼런스 카운팅으로 구현되어 있음

#### 연결 리스트 테스트 코드

```python
def show_list(slist):
    if slist.empty():
        print('The list is empty')
        return

    for i in range(slist.size()):
        print(slist.search_pos(i), end = '  ')
```


##### 리스트 객체를 하나 만들어 데이터를 하나만 삽입후 삭제

```python
if __name__ == '__main__':
    slist = Linked_list()
    print("데이터 개수: {}".format(slist.size()))
    show_list(slist)
    print()

    # 데이터가 하나일 경우
    slist.append(2)
    print("데이터 개수: {}".format(slist.size()))
    show_list(slist)
    print()

    # 데이터가 하나일 경우 잘 삭제되는지 테스트
    if slist.remove(2):
        print("데이터 개수: {}".format(slist.size()))
        show_list(slist)
    print()
```

실행 결과

```
데이터 개수: 0
The list is empty

데이터 개수: 1
2
data of 2 is deleted
데이터 개수: 0
The list is empty
```

##### 리스트 중간에 위치한 데이터와 마지막 데이터 지우기

```python
if __name__ == '__main__':
    slist = Linked_list()
    print('데이터 개수: {}'.format(slist.size()))
    show_list(slist)
    print()

    slist.append(3)
    slist.append(1)
    slist.append(5)
    slist.append(2)
    slist.append(10)
    slist.append(7)
    slist.append(2)

    print('데이터 개수: {}'.format(slist.size()))
    show_list(slist)
    print()

    if slist.remove(2):
        print('데이터 개수: {}'.format(slist.size()))
        show_list(slist)
        print()
    else:
        print('target Not found')

    if slist.remove(2):
        print('데이터 개수: {}'.format(slist.size()))
        show_list(slist)
        print()
    else:
        print('target Not found')
```

##### search_target() 함수 테스트
## 테스트 필요
```python
if __name__ == '__main__':
    slist = Linked_list()
    print("데이터 개수: {}".format(slist.size()))
    show_list(slist)
    print()

    slist.append(3)
    slist.append(1)
    slist.append(5)
    slist.append(2)
    slist.append(10)
    slist.append(7)
    slist.append(2)

    print("데이터 개수: {}".format(slist.size()))
    show_list(slist)
    print('\n')

    data1, pos1 = slist.search_target(2)
    if data1:
        print('searched data : {} at pos<{}>'.format(data1, pos1))
    else:
        print('there is no such data')

    data2, pos2 = slist.search_target(2, pos1 + 1)
    if data2:
        print('searched data : {} at pos<{}>'.format(data2, pos2))
    else:
        print('there is no such data')
```

## 스택

- LIFO(Last In, First Out, 후입선출) : 맨 마지막에 입력한 데이터를 맨 먼저 출력하는 것

- push : 데이터를 삽입하는 동작
- pop : 스택의 맨 위에 있는 데이터를 삭제하며 반환하는 동작


#### 스택 구현

- `S.push(data) -> None` : 데이터를 스택의 맨 위에 추가 / 파이썬 리스트의 `append`
- `S.pop() -> data` : 스택의 맨 위에 있는 데이터를 삭제하며 반환 / 파이썬 리스트의 `pop`
- `S.empty() -> bool` : 스택이 비어있으면 True, 비어 있지 않으면 False
- `S.peek() -> data` : 스택의 맨 위에 있는 데이터를 반환하되 삭제하지 않음

```python
class Stack:
    def __init__(self):
        self.container = list()

    def push(self, data):
        self.container.append(data)

    def pop(self):
        return self.container.pop()

    def empty(self):
        if not self.container:
            return True
        else:
            return False

    def peek(self):
        return self.container[-1]

if __name__ == '__main__':
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    s.push(4)
    s.push(5)

    while not s.empty():
        data = s.pop()
        print(data, end = '  ')
```

## 큐
- FIFO(First In, First Out, 선입선출) : 먼저 들어온 데이터가 먼저 나가는 것
- 인큐(enqueue) : 큐에 데이터를 삽입하는 것
- 디큐(dequeue) : 큐에서 데이터를 꺼내는 것

### 큐 구현
- `Q.enqueue(data) -> None` : 큐의 마지막에 데이터를 추가
- `Q.dequeue() -> data` : 큐에서 가장 먼저 들어온 데이터를 삭제하면서 반환
- `Q.empty() -> bool` : 큐가 비어있으면 True, 아니면 False
- `Q.peek() -> data` : 큐에서 가장 먼저 들어온 데이터를 삭제하지 않고 반환

```python
class Queue:
    def __init__(self):
        self.container = list()

    def enqueue(self, data):
        self.container.append(data)

    def dequeue(self):
        return self.container.pop(0)

    def empty(self):
        if not self.container:
            return True
        else:
            return False

    def peek(self):
        return self.container[0]

if __name__ == '__main__':
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)
    q.enqueue(5)

    while not q.empty():
        print(q.dequeue(), end = '  ')
```

## 자료 구조 결정은?
배열은 데이터의 추가나 삭제보다 탐색이 잦을 때, 연결 리스트는 탐색보다는 데이터의 추가나 삭제가 빈번할 때 사용함.
하지만 실제 프로그램을 개발할 때는 여러 가지 상황을 고려해 자료 구조를 결정해야 함.

> 컴퓨터 사이언스 부트캠프 with 파이썬 중..
