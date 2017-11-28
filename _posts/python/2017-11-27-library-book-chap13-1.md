---
layout: post
section-type: post
title: Python Library - chap 13. 병렬처리 - 1. 복잡한 프로세스를 생성하여 병렬처리하기
category: python
tags: [ 'python' ]
---

클라우드 기술의 급속한 발전으로, 누구나 강력한 머신을 손쉽게 이용할 수 있게 되었습니다. 그에 따라 머신 리소스를 한계까지 사용하는 병렬처리 기술이 주목받고 있습니다.  

Python에서는 기본적으로 고기능 병렬처리 라이브러리를 지원하고 있습니다. 이 라이브러리를 이용하면 복잡한 프로세스 관리도 간단히 작성할 수 있습니다.

# 복잡한 프로세스를 생성하여 병렬처리하기

`multiprocessing`은 복잡한 프로세스의 생성과 병렬처리를 지원합니다.

## 프로세스 생성하기
Process 객체를 만들어 start() 메서드를 호출하면 간단하게 자식 프로세스를 생성할 수 있습니다.

### multiprocessing 모듈을 이용해 간단히 자식 프로세스를 생성하는 예: sample_process.py

```Python
from multiprocessing import Process
import os

def f(x):
    print("{0} - 프로세스 ID: {1} (부모 프로세스 ID: {2})".format(x, os.getpid(), os.getppid()))

def main():
    for i in range(3):
        p = Process(target=f, args=(i, ))
        p.start()
    p.join()

if __name__ == "__main__":
    main()
```

Process 객체를 생성할 때 자식 프로세스를 생성하는 대상(target)과 인수(args)를 지정하고 있습니다. 또한 자식 프로세스 종료를 기다리도록 join() 메서드를 이용하고 있습니다.  

join() 메서드를 생략하면 병렬처리가 완료되기 전에 다음 처리가 시작될 가능성이 있습니다.  

이 코드를 실행하면 다음과 같은 결과를 얻게을 수 있고, 같은 부모 프로세스로부터 여러 개의 자식 프로세스가 생성된 것을 확인할 수 있습니다.

### sample_process.py 실행

```
$ python sample_peocess.py
0 - 프로세스 ID: 1789 (부모 프로세스 ID: 1774)
1 - 프로세스 ID: 1790 (부모 프로세스 ID: 1774)
2 - 프로세스 ID: 1791 (부모 프로세스 ID: 1774)
```

생성된 프로세스가 종료되었는지 확인할 때는 `is_alive()` 메서드를 사용합니다.

```Python
>>> p.is_alive()
False  # 프로세스가 종료되었음
```

## 프로세스 간 객체 교환하기
프로세스 간 통신을 위해 "큐(Queue)"와 "파이프(Pipe)" 두 가지 수단이 준비되어 있습니다.  

### 큐(Queue)
큐는 thread-safe, process-safe 통신 방법입니다. thread-safe, process-safe라는 것은 여러 개의 스레드 및 프로세스가 동시에 병렬로 실행되어도 문제가 방생하지 않는다는 것을 의미합니다. 보통 어떤 객체에 접근하는 스레드나 프로세스는 한 번에 하나로 제한됩니다. 따라서 이 thread-safe, process-safe라는 것은 멀티스레드, 멀티프로세스 프로그래밍에서 매우 중요한 개념입니다.

#### Queue를 이용하여 프로세스 간 통신하는 예: sample_queue.py

```Python
from multiprocessing import Process, Queue

def sender(q, n):
    # 큐에 메시지를 송신
    q.put('{0}회째의 Hello World'.format(n))

def main():
    q = Queue()
    for i in range(3):
        p = Process(target=sender, args=(q, i))
        p.start()

    # 큐로 보낸 메시지를 수신
    print(q.get())
    print(q.get())

    p.join()

if __name__ == "__main__":
    main()
```

#### sample_queue.py 실행

```
$ python sample_queue.py
0회째의 Hello World
1회째의 Hello World
```

### 파이프(Pipe)
Pipe는 양방향 통신을 가능하게 하는 기술입니다. 큐보다 몇 배 더 빠르게 동작하지만, thread-safe가 아니므로 엔드 포인트가 2개 밖에 없는 경우에 사용합니다.

#### Pipe를 사용하여 프로세스 간 통신하는 예: sample_pipe.py

```Python
from multiprocessing import Process, Pipe
import os

def sender(conn):
    # 다른 자식 프로세스로 Hello World라는 메시지를 송신
    conn.send('Hello World')
    conn.close()

def receiver(conn):
    # 다른 자식 프로세스로부터 메시지를 수신하여 표시
    msg = conn.recv()
    print('메시지 수신: {0}'.format(msg))
    conn.close()

def main():
    # 메시지를 송수신하는 파이프 생성
    parent_conn, child_conn = Pipe()

    # 메시지 송신
    p = Process(target=sender, args=(child_conn,))
    p.start()

    # 메시지 수신
    p = Process(target=receiver, args=(parent_conn, ))
    p.start()

    p.join()

if __name__ == "__main__":
    main()
```

#### sample_pipe.py 실행

```
$ python sample_pipe.py
메시지 수신: Hello World
```

## 프로세스 동기화하기
multiprocessing 모듈에는 threading 모듈과 같은 프로세스 동기화 기능이 있습니다. 프로세스 간에 lock을 사용하여 동기화하지 않으면, 표준 출력 내용에는 각 프로세스의 출력이 섞이게 됩니다.

### 각 프로세스의 출력이 섞여 있는 예: sample_mix.py

```Python
from multiprocessing import Process

def f(i):
    print('{0}번째 프로세스 실행 중'.format(i))

def main():
    for i in range(3):
        p = Process(target=f, args=(i, ))
        p.start()
    p.join()

if __name__ == "__main__":
    main()
```

### sample_mix.py 실행

```
$ python sample_mix.py
0번째 프로세스 실행 중
1번째 프로세스 실행 중
2번째 프로세스 실행 중
```

lock을 사용하면 한 번에 하나의 프로세스만 표준 출력에 기록하도록 할 수 있습니다.

### lock를 사용하여 프로세스 실행을 제어하는 예: sample_lock.py

```Python
from multiprocessing import Process, Lock

def f(lock, i):
    # lock이 unlock 상태가 될 때까지 block
    lock.acquire()

    # 처리 순번 출력
    print('{0}번째 프로세스 실행 중'.format(i))

    # lock 해제
    lock.release()

def main():
    # lock 객체
    lock = Lock()

    for i in range(3):
        p = Process(target=f, args=(lock, i))
        p.start()
    p.join()

if __name__ == "__main__":
    main()
```

### sample_lock.py 실행

```
$ python sample_lock.py
0번째 프로세스 실행 중
1번째 프로세스 실행 중
2번째 프로세스 실행 중
```

## 동시에 실행하는 프로세스 수 제어하기
`Pool` 클래스를 이용하면 동시에 실행하는 프로세스 수를 제어할 수 있습니다. Pool 클래스가 지정된 수의 프로세스를 풀링하여(pooling), 태스크가 들어왔을 때 비어 있는 적당한 프로세스에 태스크를 할당해 줍니다. 사용할 프로세스 상한은 Pool 클래스의 인스턴스를 생성할 때 지정합니다. 객체의 요소 수가 설정된 프로세스 상한값보다 많을 때에는 설정된 상한값 이외의 프로세스는 생성되지 않습니다. 이때에는 다른 요소의 처리가 끝나는 대로, 프로세스를 재이용하여 처리가 이루어집니다.

### 실행하는 프로세스 상한을 설정하고, 비동기 처리하는 예
```Python
>>> from multiprocessing import Pool
>>> def f(x):
...     return x * x
...
>>> p = Pool(processes=4)  # 프로세스 수 상한을 4개로 설정한다.
>>> result = p.apply_async(f, [10])  # 비동기로 f(10) 처리 실행
>>> print(result.get())  # 결과 취득
100
```

### 사용하는 프로세스 수를 제한하고 map을 병렬화

```python
# 사용할 프로세스 상한을 5개로 설정
>>> with Pool(5) as p:
...     p.map(f, [1,2,3])
...
[1, 4, 9]
```

> #### multiprocessing과 threading의 차이  
스레드 생성을 지원하는 threading 모듈도 multiprocessing 모듈과 같이 병렬처리 기능을 제공합니다.  
하지만 threading 모듈에는 Global Interpreter Lock(이하, GIL) 제약 때문에, 한 번에 하나의 스레드 밖에 실행할 수 없다는 단점이 있습니다. GIL이란, 여러 개의 스레드가 동시에 메모리에 접근하지 않도록 1 인터프리터 당 1 스레드를 보장하는 것입니다.(Python뿐만 아니라 많은 LL언어에서는 thread-safe가 아닌 C 언어 모듈을 많이 사용하므로, GIL을 채택하고 있습니다.)  
이에 반해 multiprocessing 모듈은 스레드 대신 서브 프로세스를 이용함으로써, GIL 문제를 회피하여 여러 CPU나 멀티코더 CPU의 리소스를 최대한으로 활용할 수 있습니다.
