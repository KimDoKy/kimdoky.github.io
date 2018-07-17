---
layout: post
section-type: post
title: Introducing Python - Chap10. 시스템
category: python
tags: [ 'python' ]
published: false
---

모든 프로드램에 사용되는 os(operating system) 모듈은 다양한 시스템 함수를 제공한다.

## 10.1 파일
파이썬은 다른 언어처럼 유닉스의 파일 연산 패턴을 지니고 있다. `chown()`, `chmod()` 함수 등은 똑같은 이름을 사용한다.

### 10.1.1 생성하기: open()
파일을 열거나 존재하지 않으면 생성한다.  

```python
>>> fout = open('oops.txt', 'wt')
>>> print('Oops, I created a file', file=fout)
>>> fout.close()
```

### 10.1.2 존재여부 확인하기: exists()

```python
>>> os.path.exists('oops.txt')
True
>>> os.path.exists('waffles')
False
>>> os.path.exists('.')
True
>>> os.path.exists('..')
True
```

### 10.1.3 타입 확인하기: isfile()


```python
>>> name = 'oops.txt'
# 파일인지 확인
>>> os.path.isfile(name)
True
# 디렉터리인지 확인
>>> os.path.isdir(name)
False
>>> os.path.isdir('.')
True
# 절대 경로인지 확인
# 실존하는 경로가 아니어도 된다.
>>> os.path.isabs('name')
False
>>> os.path.isabs('/big/fake/name')
True
>>> os.path.isabs('big/fake/name')
False
```

### 10.1.4 복사하기: copy()

```python
>>> import shutil
>>> shutil.copy('oops.txt', 'ohno.txt')
'ohno.txt'
```

`shutil.move()`는 파일을 복사 후 원본 파일을 삭제한다.

### 10.1.5 이름 바꾸기: rename()

```python
>>> import os
>>> os.rename('ohno.txt', 'ohwell.txt')
```

### 10.1.6 연결하기: link(), sysmlink()

유닉스에서 파일은 한 곳에 있지만, **링크** 라 불리는 여러 이름을 가질 수 있다. **심볼릭 링크(symbolic link)** 는 원본 파일을 새 이름으로 연결한다. 원본 파일과 새 이름의 파일을 한 번에 찾을 수 있도록 한다. `link()`함수는 하드 링크를 생성하고, `symlink()`함수는 심벌릭 링크를 생성한다. `islink()`함수는 파일이 심벌릭 링크인지 확인한다.

```python
# oops.txt 파일의 하드 링크인 yikes.txt 파일 만들기
>>> os.link('oops.txt', 'yikes.txt')
>>> os.path.isfile('yikes.txt')
True
# oops.txt 파일의 심벌릭 링크인 jeepers.txt 파일 만들기
>>> os.path.islink('yikes.txt')
False
>>> os.symlink('oops.txt', 'jeepers.txt')
>>> os.path.islink('jeepers.txt')
True
```

### 10.1.7 퍼미션 바꾸기: chmod()
유닉스 시스템에서 chmod()는 파일의 퍼미션을 변경한다. 읽기, 쓰기, 실행 퍼미션이 있다. 사용자가 속한 그룹과 나머지에 대한 퍼미션이 각각 존재한다. 이 명령은 사용자, 그룹, 나머지 퍼미션을 묶어서 압축된 8진수의 값을 취한다.

```python
# 파일을 생성한 사용자만 읽을 수 있도록 설정
>>> os.chmod('oops.txt', 0o400)
# 8진수 값이 아닌 심벌을 사용할 수 있다.
>>> import stat
>>> os.chmod('oops.txt', stat.S_IRUSR)
```

### 10.1.8 오너십 바꾸기: chown()
이 함수는 유닉스/리눅스/맥에서 사용된다. 숫자로 된 **사용자 아이디(uid)** 와 **그룹 아이디(uid)** 를 지정하여 파일의 소유자와 그룹에 대한 오너쉽을 바꿀수 있다.

```python
>>> uid = 5
>>> gid = 22
>>> os.chown('oops.txt', uid, gid)
```

### 10.1.9 절대 경로 얻기: abspath()
상대 경로를 절대 경로로 만든다.

```python
>>> os.path.abspath('oops.txt')
'..(생략)../intoro_python/chap10/oops.txt'
```

### 10.1.10 심벌릭 링크 경로 얻기: realpath()
심벌릭 링크 파일의 원본 파일의 이름을 얻는다.

```python
# oops.txt의 심벌릭 링크인 jeepers.txt 파일의 원본 파일 이름 얻기
>>> os.path.realpath('jeepers.txt')
'..(생략)../intoro_python/chap10/oops.txt'
```

### 10.1.11 삭제하기: remove()

```python
>>> os.remove('oops.txt')
>>> os.path.exists('oops.txt')
False
```

## 10.2 디렉터리

### 10.2.1 생성하기: mkdir()

```python
>>> os.mkdir('poems')
>>> os.path.exists('poems')
True
```

### 10.2.2 삭제하기: rmdir()

```python
>>> os.rmdir('poems')
>>> os.path.exists('poems')
False
```

### 10.2.3 콘텐츠 나열하기: listdir()

```python
# 테스트를 위해 디렉터리 생성
>>> os.mkdir('poems')
>>> os.listdir('poems')
[]  # 하위 디렉터리가 없다.
>>> os.mkdir('poems/mcintyre') # 하위 디렉터리 생성
>>> os.listdir('poems')
['mcintyre']
>>> fout = open('poems/mcintyre/the_good_man', 'wt')
>>> fout.write('''Cheerful and happy was his mood,
... He to the poor was kind and good''')
65
>>> fout.close()
>>> os.listdir('poems')
['mcintyre']
>>> os.listdir('poems/mcintyre')
['the_good_man']
```

### 10.2.4 현재 디렉터리 바꾸기: chdir()

```python
>>> os.chdir('poems')
>>> os.listdir('.')
['mcintyre']
>>> os.chdir('mcintyre')
>>> os.listdir('.')
['the_good_man']
>>> os.chdir('..')
>>> os.getcwd()
'..(생략)../intoro_python/chap10/poems'
```

### 10.2.5 일치하는 파일 나열하기: glob()

`glob()`함수는 복잡한 정규표현식이 아닌, 유닉스 쉘 규칙을 사용하여 일치하는 파일이나 디렉터리의 이름을 검색한다.

- 모든 것에 일치: `*`(re 모듈에서의 `.*`와 같다.)
- 한 문자에 일치: `?`
- a,b 혹은 c 문자에 일치: `[abc]`
- a,b 혹은 c를 제외한 문자에 일치: `[!abc]`

```python
>>> import glob
# m으로 시작하는 모든 파일이나 디렉터리 찾기
>>> glob.glob('m*')
['mcintyre']
# 두 글자로 된 파일이나 디렉터리 찾기
>>> glob.glob('??')
[]
# m으로 시작하고 e로 끝나는 여덟 글자의 단어 찾기
>>> glob.glob('m??????e')
['mcintyre']
# k,l이나 m으로 시작하고, e로 끝나는 단어 찾기
>>> glob.glob('[klm]*e')
['mcintyre']
```

## 10.3 프로그램과 프로세스

하나의 프로그램을 실행할 때, 운영체제는 한 **프로세스** 를 생성한다. 프로세스는 운영체제의 **커널(kernel.파일과 네트워트 연결, 사용량 통계 등 핵심 역할 수행)** 에서 시스템 리소스(CPU, 메모리, 디스크 공간) 및 자료구조를 사용한다. 한 프로세스는 다른 프로세스로부터 독립된 존재다. 프로세스는 서로 참조하거나 방해할 수 없다.

운영체제는 실행 중인 모든 프로세스를 추적하다. 각 프로세스에 시간을 조금씩 할애하여 한 프로세스에서 다른 프로세스로 전환한다. 운영체제는 두 가지 목표가 있는데, 프로세스를 공정하게 실행하여 되도록 많은 프로세스가 실행되게 하고, 사용자의 명령을 반응적으로 처리하는 것이다.

표준 라이브러리의 os 모듈에서 시스템 정보를 접근하는 함수를 제공한다.

```Python
# pid(프로세스 ID), uid, gid 출력
>>> os.getpid()
86026
>>> os.getuid()
501
>>> os.getgid()
20
```

### 10.3.1 프로세스 생성하기(1): subprocess

파이썬 표준 라이브러리 `subprocess` 모듈은 존재하는 다른 프로그램을 시작하거나 멈출 수 있다.

```Python
# 유닉스 date 프로그램의 결과를 얻어온다.
>>> import subprocess
>>> ret = subprocess.getoutput('date')
>>> ret
'2018년 7월  5일 목요일 12시 37분 00초 KST'
```

시간이 오래 걸리는 뭔가를 호출할 땐 **'병행성'** 으로 해야 한다.

```Python
# `getoutput()` 함수의 인자는 완전한 쉘 명령의 문자열이라서 인자, 파이프, I/O 리다이렉션(<,>) 등을 포함할 수 있다.
>>> ret = subprocess.getoutput('date -u')
>>> ret
'2018년 7월  5일 목요일 03시 39분 55초 UTC'

# date -u 명령에서 파이프로 wc 명령은 연결
# 1줄, 9단어, 51글자를 센다.
>>> ret = subprocess.getoutput('date -u | wc')
>>> ret
'       1       9      51'

# check_output() 변형 메서드는 명령과 인자의 리스트를 취한다.
# 표준 출력으로 문자열이 아닌 바이트 타입을 반환하고, 쉘을 사용하지 않는다.
>>> ret = subprocess.check_output(['date', '-u'])
>>> ret
b'2018\xeb\x85\x84 7\xec\x9b\x94  5\xec\x9d\xbc \xeb\xaa\xa9\xec\x9a\x94\xec\x9d\xbc 03\xec\x8b\x9c 42\xeb\xb6\x84 47\xec\xb4\x88 UTC\n'

# getstatusoutput()는 프로그램의 종료 상태를 표시하고, 프로그램 상태 코드와 결과를 튜플로 반환한다.
>>> ret = subprocess.getstatusoutput('date')
>>> ret
(0, '2018년 7월  5일 목요일 12시 43분 20초 KST')

# call()은 결과가 아닌 상태 코드만 저장한다.
# 0은 유닉스 계열에서 성공적으로 종료를 의미
# 실행시 날짜와 시간을 출력하지만 ret 변수에는 상태 코드만 저장한다.
>>> ret = subprocess.call('date')
2018년 7월  5일 목요일 12시 43분 46초 KST
>>> ret
0
```

인자를 사용하여 두 가지 방법으로 프로그램을 실행할 수 있다.

1. 인자를 한 문자열에 저장

```python
# date -u는 현재 날짜와 시간을 UTC로 출력한다.
# date -u 명형을 인식할 shell=True 가 필요하다.
# 명령을 별도의 문자열로 분할하고, '*' 같은 와일드카드 문자를 사용할 수 있다.
>>> ret = subprocess.call('date -u', shell=True)
2018년 7월  5일 목요일 03시 44분 12초 UTC
```

2. 인자의 리스트를 사용한다. (쉘을 호출 할 필요가 없다.)

```python
>>> ret = subprocess.call(['date', '-u'])
2018년 7월  5일 목요일 03시 44분 53초 UTC
```

### 10.3.2 프로세스 생성하기(2): multiprocessing

'multiprocessing' 모듈은 파이썬 함수를 별도의 프로세스로 실행하거나 한 프로그램에서 독립적인 여러 프로세스를 실행 한다.

```Python
# mp.py로 저장후 실행한다.
import multiprocessing
import os

def do_this(what):
    whoami(what)

def whoami(what):
    print("Process %s says: %s" % (os.getpid(), what))

if __name__ == '__main__':
    whoami("I'm the main program")
    for n in range(4):
        p = multiprocessing.Process(target=do_this,
                args=("I'm function %s" % n,))
        p.start()
```

```
# 실행 결과
Process 24948 says: I'm the main program
Process 24964 says: I'm function 0
Process 24965 says: I'm function 1
Process 24966 says: I'm function 2
Process 24967 says: I'm function 3
```

`Process()` 함수는 새 프로세스를 생성하여 그곳에 `do_this()` 함수를 실행한다. for 문에서 루프를 4번 돌기 때문에 `do_this()` 함수를 실행한 후 종료하는 4개의 새로운 프로세스가 생성되었다.

`multiprocessing` 모듈은 많은 기능을 가지고 있다. 프로그램의 전반적인 시간을 줄이기 위해 하나의 작업을 여러 프로세스에 할당할 수 있다. 예를 들어 웹페이지를 스크래핑하고, 이미지 크기를 조정하는 등 작업을 여러 프로세스로 수행할 수 있다. `multiprocessing` 모듈은 프로세스 간의 상호 통신과 모든 프로세스가 끝날 때까지 기다리는 큐 작업을 포함한다.

### 10.3.3 프로세스 죽이기: terminate()

`terminate()`는 프로세스를 종료한다. 프로세스가 무한 루프에 빠지는 등 과부하를 심하게 일으킬 때 사용한다.

```Python
import multiprocessing
import time
import os

def whoami(name):
    print("I'm %s, in process %s" % (name, os.getpid()))

def loopy(name):
    whoami(name)
    start = 1
    stop = 1000000
    for num in range(start, stop):
        print("\tNumber %s of %s. Honk!" % (num, stop))
        time.sleep(1)

if __name__ == '__main__':
    whoami("main")
    p = multiprocessing.Process(target=loopy, args=("loopy",))
    p.start()
    time.sleep(5)
    p.terminate()
```

```
# 실행 결과
I'm main, in process 25415
I'm loopy, in process 25431
	Number 1 of 1000000. Honk!
	Number 2 of 1000000. Honk!
	Number 3 of 1000000. Honk!
	Number 4 of 1000000. Honk!
	Number 5 of 1000000. Honk!
	Number 6 of 1000000. Honk!
```

## 10.4 달력과 시간

```Python
# 윤년 테스트
>>> import calendar
>>> calendar.isleap(1900)
False
>>> calendar.isleap(1996)
True
>>> calendar.isleap(2004)
True
>>> calendar.isleap(2018)
False
```

시간은 타임존과 섬머타임 때문에 다루기가 힘들다.  
파이썬 표준 라이브러리는 datetime, time, calendar, dateutil 등 여러 시간과 날자 관련 모듈이 있다. 일부 기능들은 중복된다.

### 10.4.1 datetime 모듈

##### 주요 메서드

- date : 년, 월, 일
- time : 시, 분, 초, 마이크로초
- dateitme : 날짜와 시간
- timedelta : 날짜 또는 시간 간격

```Python
# 년, 월, 일을 지정하여 date 객체 생성하여, 속성으로 접근
>>> from datetime import date
>>> halloween = date(2015, 10, 31)
>>> halloween
>>> datetime.date(2015, 10, 31)
>>> halloween.day
31
>>> halloween.month
10
>>> halloween.year
2015
# 날짜를 출력
>>> halloween.isoformat()
'2015-10-31'
```

iso는 국제표준화기구(ISO)에서 재정한 날짜와 시간 표현에 대한 국제표준규격 ISO 8601을 참고한다. 년, 월, 일 순으로 표현한다.

```Python
# 오늘 날짜를 출력
>>> from datetime import date
>>> now = date.today()
>>> now
datetime.date(2018, 7, 12)
```

```python
# 날짜에 시간 간격을 더하기
>>> from datetime import timedelta
>>> one_day = timedelta(days=1)
>>> tomorrow = now + one_day
>>> tomorrow
datetime.date(2018, 7, 13)
>>> now + 17*one_day
datetime.date(2018, 7, 29)
>>> yesterday = now - one_day
>>> yesterday
datetime.date(2018, 7, 11)

# datetime 모듈의 time 객체는 하루의 시간을 나타내는데 사용
>>> from datetime import time
>>> noon = time(12, 0, 0)
>>> noon
datetime.time(12, 0)
>>> noon.hour
12
>>> noon.minute
0
>>> noon.second
0
>>> noon.microsecond
0
```

인자는 시부터 마이크로초 순으로 입력한다. 인자를 입력하지 않으면 0으로 간주한다. 마이크로초는 하드웨어와 OS에 따라 달라진다.

```Python
# datetime 객체는 날짜와 시간 모두를 포함
>>> from datetime import datetime
>>> some_day = datetime(2015, 1, 2, 3, 4, 5, 6)
>>> some_day
datetime.datetime(2015, 1, 2, 3, 4, 5, 6)

# datetime 객체에도 isoformat() 메서드가 있다.
# 중간에 T는 날짜와 시간을 구분
>>> some_day.isoformat()
'2015-01-02T03:04:05.000006'

# datetime 객체에서 now() 메서드로 현재 날짜와 시간을 얻을 수 있다.
>>> from datetime import datetime
>>> now = datetime.now()
>>> now
datetime.datetime(2018, 7, 12, 0, 38, 8, 314310)
>>> now.year
2018
>>> now.month
7
>>> now.day
12
>>> now.hour
0
>>> now.minute
38
>>> now.second
8
>>> now.microsecond
314310

# combine() 으로 date 객체와 time 객체를 datetime 객체로 병합할 수 있다.
>>> from datetime import datetime, time, date
>>> noon = time(12)
>>> this_day = date.today()
>>> noon_today = datetime.combine(this_day, noon)
>>> noon_today
datetime.datetime(2018, 7, 12, 12, 0)
# date()와 time() 메서드를 사용하여 날짜와 시간을 얻을 수 있다.
>>> noon_today.date()
datetime.date(2018, 7, 12)
>>> noon_today.time()
datetime.time(12, 0)
```

### 10.4.2 time 모듈

절대 시간을 나타내는 방법은 어떤 시작점 이후 시간의 초를 세는 것이다. **유닉스 시간** 은 1970년 1월 1일 자정 이후 시간의 초를 사용한다. 이 값을 **에포치(epoch)** 라 부르며, 시스템 간에 날짜와 시간을 교환하는 간단한 방식이다.

```Python
>>> import time
>>> now = time.time()
>>> now
1531323715.87176
```
숫자를 보면 1970년부터 지금까지 10억초가 넘는다.

```python
# ctime() 함수를 사용하여 에포치 값을 문자열로 변환
>>> time.ctime(now)
'Thu Jul 12 00:41:55 2018'
```

에포치값은 자바스크립트와 같은 다른 시스템에서 날짜와 시간을 교환하기 위한 유용한 공통분모다. 각각의 날짜와 시간 요소를 얻기 위해 time 모듈의 struct_time 객체를 사용할 수 있다. localtime() 메서드는 시간을 시스템의 표준시간대로, gmtime() 메서드는 시간을 UTC로 제공한다.

```python
>>> time.localtime(now)
time.struct_time(tm_year=2018, tm_mon=7, tm_mday=12, tm_hour=0, tm_min=41, tm_sec=55, tm_wday=3, tm_yday=193, tm_isdst=0)
>>> time.gmtime(now)
time.struct_time(tm_year=2018, tm_mon=7, tm_mday=11, tm_hour=15, tm_min=41, tm_sec=55, tm_wday=2, tm_yday=192, tm_isdst=0)

# mktime() 메서드는 struct_time 객체를 에포치 초로 변환한다.
>>> tm = time.localtime(now)
>>> time.mktime(tm)
1531323715.0
```
struct_time 객체는 시간을 초까지만 유지하기 때문에, 이 값은 ()의 에포치 값과 정확히 일치하지는 않는다.

가능하면 **UTC** 를 사용하는 것이 좋다. UTC는 표준시간대와 독립적인 절대 시간이다. 서버를 운영하고 있다면 현지 시간이 아닌 UTC로 설정해야 한다.

그리고 **일광절약시간** 은 사용하지 마라. 연중 한 시간이 한 번 사라지기 때문에 매년 데이터 중복과 손실이 생긴다.

### 10.4.3 날짜와 시간 읽고 쓰기

isoformat() 뿐 아니라 time 모듈의 ctime() 함수로도 날짜와 시간을 쓸 수 있다. 이 ㅎ마수는 에포치 시간을 문자열로 변환한다.

```Python
>>> import time
>>> now = time.time()
>>> time.ctime(now)
'Thu Jul 12 00:46:07 2018'
```

strftime()을 사용하여 날짜와 시간을 문자열로 변환할 수 있다. datetime.date.time 객체에서 메서드로 제공되고, time 모듈에서 함수로 제공된다.

##### strftime() 출력 지정자

문자열 포맷 | 날짜/시간 단위 | 범위
---|---|---
%Y | 년 |1900 ~ ...
%m | 월 | 01 ~ 12
%B | 월 이름 | January
%b | 월 축약 이름 | Jan, ..
%d | 일 | 01 ~ 31
%A | 요일 | Sunday, ...
%a | 요일 축약 이름 | Sun, ...
%H | 24시간 | 00 ~ 23
%I | 12시간 | 01 ~ 12
%p | 오전/오후 | AM, PM
%M | 분 | 00 ~ 59
%s | 초 | 00 ~ 59


```python
# strftime() 함수는 struct_time 객체를 문자열로 변환한다.
# 포맷 문자열 fmt를 정의하여 사용한다.
>>> import time
>>> fmt = "It's %A, %B %d, %Y, local time %I:%M:%S%p"
>>> t = time.localtime()
>>> t
time.struct_time(tm_year=2018, tm_mon=7, tm_mday=12, tm_hour=0, tm_min=47, tm_sec=9, tm_wday=3, tm_yday=193, tm_isdst=0)
>>> time.strftime(fmt, t)
"It's Thursday, July 12, 2018, local time 12:47:09AM"

# date 객체에 사용하면 날짜 부분만 작동한다. 시간을 기본값으로 지정된다.
>>> from datetime import date
>>> some_day = date(2015, 12, 12)
>>> fmt = "It's %B %d, %Y, local time %I:%M:%S%p"
>>> some_day.strftime(fmt)
"It's December 12, 2015, local time 12:00:00AM"

# time 객체는 시간 부분만 변환된다.
>>> from datetime import time
>>> some_time = time(10, 35)
>>> some_time.strftime(fmt)
"It's January 01, 1900, local time 10:35:00AM"

# time 객체는 날짜에는 의미가 없다.
```


```Python
# 년-월-일  포맷을 지켜야 한다.
>>> import time
>>> fmt = "%Y-%m-%d"
>>> time.strptime("2015 06 02", fmt)
Traceback (most recent call last)
<ipython-input-86-e161258e1fdb> in <module>()
----> 1 time.strptime("2015 06 02", fmt)
...
ValueError: time data '2015 06 02' does not match format '%Y-%m-%d'

>>> time.strptime("2015-06-02", fmt)
time.struct_time(tm_year=2015, tm_mon=6, tm_mday=2, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=153, tm_isdst=-1)

# 값이 범위를 벗어나면 예외가 발생
>>> time.strptime("2015-13-29", fmt)
Traceback (most recent call last)
<ipython-input-88-e947ddabad6b> in <module>()
----> 1 time.strptime("2015-13-29", fmt)
...
ValueError: time data '2015-13-29' does not match format '%Y-%m-%d'
```

```python
# 이름은 운영체제의 국제화 설정(로케일.locale)에 따름
# setlocale()을 사용하여 다른 월,일의 이름을 출력
# setlocale()의 첫 번째 인자는 날짜와 시간을 위한 locale.LC_TIME
# setlocale()의 두 번째 인자는 언어와 국가 약어가 결합된 문자
>>> import locale
>>> from datetime import date
>>> halloween = date(2015, 10,31)
>>> for lang_country in ['ko_kr', 'en_us', 'fr_fr', 'de_de', 'es_es', 'is_is',]:
...     locale.setlocale(locale.LC_TIME, lang_country)
...     halloween.strftime('%A, %B %d')
# .... 출력이 안된다...

# lang_country에 대한 값 찾기
>>> import locale
>>> names = locale.locale_alias.keys()

# names로 부터 로케일 이름 얻기
>>> good_names = [name for name in names if len(name) == 5 and name[2] == '_']
>>> good_names[:5]
['a3_az', 'aa_dj', 'aa_er', 'aa_et', 'af_za']
# 특정 언어 로케일 이름 얻기
>>> de = [name for name in good_names if name.startswith('de')]
>>> de
['de_at', 'de_be', 'de_ch', 'de_de', 'de_lu']
```

### 10.4.4 대체 모듈

표준 라이브러리 모듈이 특정 포맷 변환이 부족한 경우 외부 모듈을 사용할 수 있다.

- allow : 많은 날짜와 시간 함수를 결합하여 간단한 API 제공
- dateutil : 대부분의 날짜 포맷을 파싱하고, 상대적인 날짜와 시간도 처리한다.
- iso8601 : ISO8601 포맷에 대한 라이브러리의 부족한 부분을 보충
- fleming : 표준시간대 함수를 제공
