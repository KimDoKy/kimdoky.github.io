---
layout: post
section-type: post
title: Python Library - chap 4. 자료형과 알고리즘 - 4.2 힙 큐 이용하기
category: python
tags: [ 'python' ]
---
리스트 객체를 힙 큐로 이용하는 기능을 제공하는 heapq에 대한 설명입니다. 힙 큐는 우선순위 큐라고도 불리며, 리스트 중에 최솟값이 항상 리스트의 맨 앞 요소가 되는 성질을 가지고 있습니다.

## 리스트의 요소를 작은 값부터 순서대로 가져오기
heapq를 이용하면 일련의 값으로부터 최솟값을 빠르게 구할 수 있습니다.

### heapq 샘플 코드

```python
>>> import heapq
>>> queue = []  # heapq로 이용하는 리스트 객체
>>> heapq.heappush(queue, 2)
>>> heapq.heappush(queue, 1)
>>> heapq.heappush(queue, 0)
>>> heapq.heappop(queue)  # heapq로 최소 요소를 구함
0
>>> heapq.heappop(queue)
1
>>> heapq.heappop(queue)
2
>>> heapq.heappop(queue)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: index out of range
```

### heapq() 함수

형식 | heappush(heap, item)
---|---
설명 | 리스트 객체 heap에 item을 추가한다.
안수 | heap - heap으로 이용할 리스트 객체를 지정한다. <br> item - 등록할 객체를 지정한다.

### heappop() 함수

형식 | heappop(heap)
---|---
설명 | 리스트 객체 heap에서 최솟값을 삭제하고 그 값을 반환한다. 리스트가 비었으면 IndexError가 발생한다. <br> 최솟값을 삭제하는 것이 아니라 참조할 때는 heap[0]으로 한다.
인수 | heap - heap으로 이용할 리스트 객체를 지정한다.
반환값 | heap에서 삭제한 값

## 시퀀스에서 상위 n건의 리스트 작성하기
heapq는 일련의 데이터에서 정해진 건수의 값을 큰 순서대로 추출하는 처리를 효율적으로 실행합니다.

### heapq로 일정 건수의 데이터 구하기

```python
>>> queue = [1,2,3,4,5]  # heapq로 이용할 리스트 객체
>>> heapq.heapify(queue)  # 요소를 heapq로 정렬
>>> heapq.heappushpop(queue, 6)  # 값을 추가하고 최솟값을 제거함
1

>>> heapq.heappushpop(queue, 7)  # 값을 추가하고 최솟값을 제거함
2

>>> queue
[3, 4, 7, 6, 5]
```

### heapify() 함수

형식 | heapify(heap)
---|---
설명 | 리스트 객체 heap의 요소를 정렬하여 heapq로 삼는다.
인수 | heap - heap으로 이용할 리스트 객체를 지정한다.

### heappushpop() 함수

형식 | heappushpop(heap, item)
---|---
설명 | 리스트 객체 heap에 item을 추가한 다음, 최솟값을 삭제하고 그 값을 반환한다. 리스트가 비었으면 IndexError가 발생한다.
인수 | heap - heap으로 이용할 리스트 객체를 지정한다. <br> item - 등록할 객체를 지정한다.
반환값 | heap에서 삭제한 값

### heapreplace() 함수

형식 | heapreplace(heap, item)
---|---
설명 | 리스트 객체 heap에서 최솟값을 삭제한 다음, heap에 item을 추가하고 삭제한 값을 반환한다. 리스트가 비었으면 IndexError가 발생한다.
인수 | heap - heap으로 이용할 리스트 객체를 지정한다. <br> item - 등록할 객체를 지정한다.
반환값 | heap에서 삭제한 값

heappushpop()은 item 요소를 추가하고 나서 최솟값을 빼내지만, heapreplace()는 최솟값을 빼내고 나서 item을 추가합니다. 따라서 item이 heapq의 최소값일 때 heappushpop()은 item을 반환하지만, heapreplace()는 item을 추가하기 전에 등록되어 있던 최솟값을 반환합니다.
