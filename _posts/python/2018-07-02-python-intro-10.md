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

```

### 10.4.1 datetime 모듈

```Python

```

### 10.4.2 time 모듈

```Python

```

### 10.4.3 날짜와 시간 읽고 쓰기

```Python

```

### 10.4.4 대체 모듈
