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

### 11.1.3 스레드

스레드는 한 프로세스 내에서 실행된다. 프로세스의 모든 자원에 접근할 수 있다. multiprocessing 모듈은 프로세스 대신 스레드를 사용하는 `threading`가 있다.

```Python
import threading

def do_this(what):
    whoami(what)

def whoami(what):
    print("Thread %s says: %s" % (threading.current_thread(), what))

if __name__ == "__main__":
    whoami("I'm the main program")
    for n in range(4):
        p = threading.Thread(target=do_this,
                args=("I'm function %s" % n,))
        p.start()
```

```
# 실행 결과
Thread <_MainThread(MainThread, started 140736451294144)> says: I'm the main program
Thread <Thread(Thread-1, started 123145375436800)> says: I'm function 0
Thread <Thread(Thread-2, started 123145380691968)> says: I'm function 1
Thread <Thread(Thread-3, started 123145375436800)> says: I'm function 2
Thread <Thread(Thread-4, started 123145380691968)> says: I'm function 3
```

```python
# 프로세스 기반의 dishes.py 예를 스레드로 구현
import threading, queue
import time

def washer(dishes, dish_queue):
    for dish in dishes:
        print("Washing", dish)
        time.sleep(5)
        dish_queue.put(dish)

def dryer(dish_queue):
    while True:
        dish = dish_queue.get()
        print("Drying", dish)
        time.sleep(10)
        dish_queue.task_done()

dish_queue = queue.Queue()
for n in range(2):
    dryer_thread = threading.Thread(target=dryer, args=(dish_queue,))
    dryer_thread.start()

dishes = ['salad', 'bread', 'entree', 'desert']
washer(dishes, dish_queue)
dish_queue.join()
```

```
# 실행 결과
Washing salad
Washing bread
Drying salad
Washing entree
Drying bread
Washing desert
Drying entree
Drying desert
```

`multiprocessing` 모듈과 `threading`모듈의 차이는 `threading`모듈에는 `terminate()` 함수가 없다. 실행되고 잇는 스레드를 종료할 수 있는 간단한 방법은 없다. 자신과 코드의 모든 타입에 문제가 발생할 수 있기 때문이다.  

스레드는 위험하다.(메모리 관리가 어렵다. 그리고 버그가 발생해도 매우 찾기 힘들다.) 스레드를 사용하려면 프로그램의 모든 코드와 이 프로그램을 사용하는 외부 라이브러리에서 반드시 **스레드-세이프** 한 코드를 작성해야 한다.  

스레드는 전역 데이터가 관여하지 않을 때 유용하다. 특히 일부 I/O 작업을 완료할 때까지 기다리는 시간을 절약하는데 유용하다. 이 경우 완전히 별개의 변수를 가지고 있기 때문에 데이터와 씨름할 필요가 없다.  

전역 데이터를 변경하기 위해 때론 스레드를 사용하는 것이 좋을 때가 있다. 여러 개의 스레드를 사용하는 일반적이 이유는 일부 데이터 작업을 나누기 위해서다. 이 경우 데이터 변경에 대한 확실한 정도를 예상할 수 있다.  

데이터를 안전하게 공유하는 방법은 스레드에서 변수를 수정하기 전에 소프트웨어 락(잠금)을 적용하는 것이다. 이건 한 스레드에서 변수를 저장하는 동안 다른 스레드의 접근을 막아준다. 언락(잠금 해제)할지 기억해야 한다. 락은 중첩될 수 있다. 그렇기에 주의를 기울여야 한다.

> 파이썬 스레드는 CPU 바운드 작업을 빠르게 처리 못한다. GIL(Global Interpreter Lock) 표준 파이썬 시스템의 세부 구현사항 때문이다. GIL은 파이썬 인터프리터의 스레딩 문제를 피하기 위해 존재한다. 실제로 파이썬의 멀티 스레드 프로그램은 싱글 스레드 혹은 멀티 프로세스 버전의 프로그램보다 느릴 수 있다.

### 11.1.4 그린 스레드와 gevent

**이벤트 기반(event-based)** 프로그래밍 : 중앙 **이벤트 루프** 를 실행하고, 모든 작업을 조금씩 실행하면서 루프를 반복한다. Nginx 웹 서버는 이러한 설계를 따르고 있어, 아파치 웹 서버보다 빠르다.

gevent 라이브러리는 이벤트 기반이다. 명령 코드를 작성하고, 이 조각들을 코루틴으로 변환한다. 코루틴은 다른 함수와 서로 통신하여, 어느 위치에 있는지 파악하는 제네레이터와 같다. gevent는 블로킹 대신 이러한 메커니즘을 사용하기 위해 파이썬의 socket과 같이 많은 표준 객체를 수정한다.

#### 설치

```
pip install gevent
```

#### 사용 예

독립적으로 여러 사이트의 주소를 찾기 위해 gevent 모듈의 함수를 사용할 수 있다.

```Python
# 각 호스트네임은 차례차례 gethostbyname()의 호출에 전달
# gevent의 gethostbyname()이라서 비동기적으로 실행된다.
import gevent
from gevent import socket
hosts = ['www.naver.com', 'www.daum.net', 'www.google.com']
jobs = [gevent.spawn(gevent.socket.gethostbyname, host) for host in hosts]
gevent.joinall(jobs, timeout=5)
for job in jobs:
    print(job.value)
```

실행결과

```
125.209.222.141
203.133.167.16
74.125.204.105
```

`gevent.spawn()`은 각각의 `gevent.socket.gethostbyname(host)`를 실행하기 위해 **greenlet(그린 스레드(green thread) or 마이크로 스레드(microthread))** 를 생성한다.

greenlet과 일반 스레드의 차이는 블록(block)을 하지 않는다는 것이다. 한 그레드에서 어떤 이슈로 블록되었다면, gevent는 제어를 다른 하나의 greenlet으로 바꾼다.  

`gevent.joinall()` 메서드는 생성된 모든 작업이 끝날 때까지 기다린다. 그리고 호스트네이에 대한 IP 주소를 한 번에 얻게 된다.  

gevent 버전의 socket 대신, **몽키-패치(monkey-patch)** 함수를 쓸 수 있다. 이 ㅎ마수는 gevent 버전의 모듈을 호출하지 않고, greenlet을 사용하기 위해 socket과 같은 표준 모듈을 수정한다. gevent에 적용하고 싶은 작업이 있을 때 유용하다. gevent에 접근할 수 없는 코드에도 적용할 수 있다.

```Python
# 이 프로그램뿐만 아니라 표준 라이브러리에서도 소켓이 호출되는 모든 곳에 gevent 소켓을 사용하도록 함
# C로 작성된 라이브러리가 아닌 파이썬 코드에서만 작동
# 가능한 gevent 영향을 많이 받아 속도가 향상
from gevent import monkey; monkey.patch_all()
```

```
125.209.222.141
211.231.99.17
172.217.31.132
```

gevent는 잠재적 위험이 있다. 모든 이벤트 기반의 시스템에서, 실행하는 각 코드 단위는 상대적으로 빠르게 처리되어야 한다. 논블로킹(nonblocking)임에도 많은 일을 처리해야 하는 코드는 여전히 느리다.  

> tornado, gunicorn 이라는 이벤트 기반의 두 프레임워크가 있다. 이들은 저수준의 이벤트 처리와 빠른 웹 서버 모두를 제공한다. 아파치같은 전통적인 웹 서버없이 빠른 웹사이트 구축에 유용하다.


### 11.1.5 twisted

twisted는 비동기식 이벤트 기반 네트워킹 프레임워크다. 데이터를 받거나 커넥션을 닫는 것과 같이 이벤트와 함수를 연결한다. 이 함수는 이러한 이벤트가 발생할 때 호출된다. 이것은 **콜백(callback)** 디자인으로 되어 있으며, 자바스크립트의 코드와 친숙하다. 일부 개발자는 콜백 기반 코드는 애플리케이션이 커지면 관리가 어려워진다고 한다.

twisted는 TCP와 UDP 위에서 많은 인터넷 프로토콜을 지원하는 큰 패키지다.

twisted 예제 중 knock-knock 서버와 클라이언트를 실습한다.

```Python
# knock-server.py

from twisted.internet import protocol, reactor

class Knock(protocol.Protocol):
    def dataReceived(self, data):
        print('Client: ', data)
        if data.startswith('Knock knock'):
            response = "Who's there?"
        else:
            response = data + " who?"
        print('Sever: ', response)
        self.transport.write(response)

class KnockFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Knock()

reactor.listenTCP(8000, KnockFactory())
reactor.run()
```

```Python
# knock-client.py

from twisted.internet import reactor, protocol

class KnockClient(protocol.Protocol):
    def connectionMode(self):
        self.transport.write("Knock knock")

    def dataReceived(self, data):
        if data.startswith("Who's there?"):
            response = "Disappearing client"
            self.transport.write(response)
        else:
            self.transport.loseConnection()
            reactor.stop()

class KnockFactory(protocol.ClientFactory):
    protocol = KnockClient

def main():
    f = KnockFactory()
    reactor.connectTCP("localhost", 8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
```

> 아직 사용법이 서툴러서 작동 확인이 안되었다. 추가 공부 후 업데이트 예정

### 11.1.6 asyncio
귀도 반 로섬은 파이썬 병행성 이슈에 대해, 많은 패키지는 자신의 이벤트 루프를 가지면, 각 이벤트는 자신이 유일하길 원했다. 수많은 토론후 '비동기 입출력 지원 재정리: asyncio 모듈'을 제안했다.
asyncio 모듈은 twisted와 gevent 그리고 다른 비동기 메서드와 호환될 수 잇는 일반적인 이벤트 루프를 제공한다. 파이썬 공식 사이트의 예제 참고.

### 11.1.7 Redis
싱글박스와 멀티박스 병해성 사이를 연결해주는 브리지에 대해 다룬다.  

큐를 만들 수 있는 빠른 방법은 Redis의 리스트다. Redis 서버는 하나의 머신에서 실행한다. 클라이언트는 같은 머신에서 실행하거나 네트워크를 통해서 접근할 수 있다. 두 경우 모두 클라이언트는 TCP를 통해 서버와 통신을 하여 네트워킹을 한다. 하나 이상의 공급자 클라이언트는 리스트의 한쪽 끝에 메시지를 푸시한다. 하나 이상의 클라이언트 워커는 리스트를 감시하며, **블로킹 팝** 연산을 수행한다. 리스트가 비어 있는 경우에는 메시지를 기다린다. 메시지가 도착하자마자 첫 번째 워커가 메시지를 처리한다.
