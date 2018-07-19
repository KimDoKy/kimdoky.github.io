---
layout: post
section-type: post
title: Introducing Python - Chap11.병행성과 네트워크
category: python
tags: [ 'python' ]
published: false
---

### 네트워크에서 병행성이 좋은 이유

- 성능(performance) : 느린 요소(component)를 기다리지 않고, 빠른 요소를 바쁘게 유지한다.
- 견고함(robustness) : 하드웨어 및 소프트웨어의 장애를 피하기 위해 작업을 복제하여 여러 가지 안정적인 방식으로 운영한다.
- 간소화(simplicity) : 복잡한 작업을 좀 더 이해하기 쉽고, 해결하기 쉬운 여러 작은 작업으로 분해한다.
- 커뮤니케이션(commutication) : 데이터(바이트)를 보내고 싶은 곳에 원격으로 전송하고, 다시 테이터를 수신받는다.

### 이 장에서 다루는 내용

- 병행성
- 콜백(callback), 그린 스레드(green thread), 코루틴(coroutine) 같은 다른 접근 방법
- 병행성과 네트워크에 대한 기술 사용

## 11.1 병행성

컴퓨터가 일을 수행하면서 뭔가를 기다리는 이유

- I/O 바운드 : 대부분 이 경우에 해당. CPU는 메모리나 네트워크보다 몇 천배 빠르다.
- CPU 바운드 : 과학이나 그래픽 작업같은 **엄청난 계산** 이 필요할 때 발생

병행성 관련 용어

- 동기(synchronous) : 한 줄의 행렬처럼, 한 작업은 다른 작업을 따른다.
- 비동기(asynchronous) : 작업들이 독립적이다.

싱글 머신에서 다수의 작업을 가능한 빠르게 처리하려면, 이들을 독립적으로 만들어야 한다. 느린 작업이 다른 작업을 막아서는 안된다.  

서로 같이 일을 처리하기 위해 모든 작업을 가져온다. 모든 공유 제어 또는 상태에서는 병목 현상이 발생할 수 있다. 여러 작업을 관리하기 위해 **큐(queue)** 를 시작한다.

### 11.1.1 큐

큐는 리스트와 같다. 일을 한쪽 끝에서 추가하고, 다른 쪽 끝에서 가져간다. 먼저 들어온 순서대로 가져간다. (일반적으로 큐는 **FIFO(first in first out)** 라고 한다.)  

일반적으로 큐는 **메시지** 를 전달한다. 메시지는 모든 종류의 정보이다. 분산 작업 관리를 위한 큐의 경우 **작업 큐(work queue, job queue, task queue)** 라고 한다.

### 11.1.2 프로세스
싱글 머신에서 표준 라이브러리인 multiprocessing 모듈은 Queue 함수를 포함한다.

```Python
# 식기 세척기와 여러 대의 건조대 프로세스의 예
import multiprocessing as mp

def washer(dishes, output):
    for dish in dishes:
        print('Washing', dish, 'dish')
        output.put(dish)

def dryer(input):
    while True:
        dish = input.get()
        print('Drying', dish, 'dish')
        input.task_done()

dish_queue = mp.JoinableQueue()
dryer_proc = mp.Process(target=dryer, args=(dish_queue,))
dryer_proc.daemon = True
dryer_proc.start()
dishes = ['salad', 'bread', 'entree', 'dessert']
washer(dishes, dish_queue)
dish_queue.join()
```

```
# 실행 결과
Washing salad dish
Washing bread dish
Washing entree dish
Washing dessert dish
Drying salad dish
Drying bread dish
Drying entree dish
Drying dessert dish
```

이 큐는 파이썬 이터레이터와 매우 비슷하다. 실제로 분리된 프로세스를 시작하며, 식기세척기(washer)와 건조기(dryer)가 통신한다. `JoinableQueue` 함수와 모든 접시가 건조되었다는 것을 식기세척기가 알게 하는 `join()` 메서드를 사용했다. `multiprocessing`모듈에는 다른 큐 타입도 있다.
