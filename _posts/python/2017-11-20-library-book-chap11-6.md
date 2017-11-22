---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 6. 코드의 실행 시간을 측정하기
category: python
tags: [ 'python' ]
---

`timeit`은 코드의 실행 시간을 측정합니다.  

timeit은 실행하는 Python 코드 자체를 문자열로 넘겨야 하므로, 너무 크지 않은 코드들을 처리하는데 사용합니다. 코드 실행 시간을 측정하면 구현 성능을 분석할 수 있기 때문에 병목 구간 발견에 도움이 됩니다.  

실행 시간을 측정하는 방법으로는 명령줄 인터페이스를 이용하는 방법과 Python 인터페이스를 이용하는 방법, 두 종류의 방법이 있습니다.

## 명령줄에서 코드의 실행 시간 측정하기

### timeit의 형식

```
$ python -m timeit [-n N] [-r N] [-s S] [-t] [-c] [-h] [statement ...]
```

### 명령줄 옵션

옵션 | 설명
---|---
-n N, --number=N | Python 코드를 실행하는 횟수를 지정한다. 생략하면 10회부터 시작하여 소요 시간이 0.2초가 되도록 반복 횟수가 자동으로 계산된다.
-r N, --repeat=N | 실행 시간 측정을 반복할 횟수를 지정한다(기본값은 3).
-s S, --setup=S | 맨 처음 1회만 실행하는 명령문을 지정한다(기본값은 pass).
-p, --process | 이를 지정하면, 실시간이 아닌 프로세스 시간을 측정한다.
-v, --verbose | 이를 지정하면, 결과를 자세한 수치로 반복하여 표시한다.

명령줄 인터페이스를 이용하면, 특별히 지정하지 않는 한 반복 횟수는 자동으로 결정됩니다.

### 명령줄에서 timeit의 사용 예

```
# 지정된 Python 코드를 100만 회 실행할 때의 실행 시간을 측정하며, 이를 3회 반복한다.
$ python -m timeit '"test" in "This is a test."'
10000000 loops, best of 3: 0.152 usec per loop

# 맨 처음 한 번만 셋업문을 지정할 수 있다.
$ python -m timeit 'text = "This is a test."; char = "test"' 'char in text'
1000000 loops, best of 3: 0.266 usec per loop

# 여러 행을 포함한 식을 측정할 수도 있다.
$ python -m timeit 'try:' ' "This is test".__bool__' 'except AttributeError:' ' pass'
1000000 loops, best of 3: 0.924 usec per loop
```

## Python 인터페이스에서 코드의 실행 시간 측정하기
코드의 실행 시간을 측정하기 위해, timeit 모듈은 다음 두 개의 함수를 제공합니다.

### timeit 모듛의 함수

함수 이름 | 설명
---|---
timeit(stmt='pass', setup='pass', timer=<default timer>, number=1000000) | Timer 인스턴스를 생성하여, 해당 timeit() 함수를 사용해 Python 코드(stmt)를 number회 실행한다.
repeat(stmt='pass', setup='pass', timer=<default timer>, repeat=3, number=1000000) | Timer 인스턴스를 생성하여, 해당 timeit() 함수를 사용해 Python 코드(stmt)를 number회 실행하는 것을 repeat회 반복한다.

### 두 함수에서 이용할 수 있는 Timer 클래스

형식 | class Timer(stmt='pass', setup='pass', timer=<timer function>)
---|---
설명 | 주어진 Python 코드의 실행 시간을 측정하기 위한 클래스
인수 | stmt - 실행 시간을 측정하려는 Python 코드(기본값은 pass). <br> setup - 맨 처음에 한 번만 실행하는 문을 지정한다(기본값은 pass). <br> timer - 타이며 함수를 지정한다(플랫폼에 의존적).

### Timer 클래스의 함수

형식 | 설명
---|---
timeit(number=1000000) | 주어진 Python 코드를 number회 실행한 시간을 측정한다(기본값은 100만회). 그 결과로 실행에 소요된 시간(초)을 부동소수점 수로 반환한다.
repeat(repeat=3, number=1000000) | timeit()을 number회 실행하는 것을 repeat회 반복하고, 그 결과를 리스트로 반환한다(기본값은 3회).

Timer 클래스에서 사용할 수 있는 타이머 함수는 플랫폼 의존이라는 점을 주의해야 합니다.

- Windows - time.clock()은 마이크로초의 정밀도, time.time()은 1/60초의 정밀도
- UNIX - time.clock()은 1/100초의 정밀도, time.time()은 더 정확함

### timeit 함수의 사용 예

```python
>>> import timeit

# main 문을 100만 회 실행하는 시간을 측정하여, 걸린 시간을 부동소수점 수로 반환한다.
>>> timeit.timeit('"test" in "This is a test."')
0.15757492700504372

# timeit()을 3회 반복한 결과를 리스트로 반환한다.
>>> timeit.repeat('"test" in "This is a test."')
[0.15957088599679992, 0.15703950200258987, 0.15391590000217548]

# Timer 클래스를 이용하여 셋업문을 지정할 수 있다.
>>> t = timeit.Timer('char in text', setup='text = "This is a test."; char = "test"')
>>> t.timeit()
0.18281066199415363

# 여러 행을 포함한 식을 측정할 수도 있다.
>>> s = """\
... try:
...    "This is a test".__bool__
... except AttributeError:
...    pass
... """
>>> timeit.timeit(stmt=s)
0.8883515230045305
```
