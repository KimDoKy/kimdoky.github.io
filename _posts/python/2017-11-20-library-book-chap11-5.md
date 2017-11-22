---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 5. 대화 모드 디버깅하기
category: python
tags: [ 'python' ]
---

`pdb`는 Python 프로그램용 대화 모드 디버거입니다. pdb를 이용하면 프로그램 실행 도중의 변수값과 오류 발생 시 원인 등을 조사할 수 있습니다. PyCharm 같은 Python IDE에 풍부한 디버거가 탑재되어 있지만 pdb로도 디버깅할 수 있습니다.

## 대표적인 디버거 명령어

옵션 | 설명
---|---
h(elp)[command] | 도움말 명령어. command를 지정하지 않으면 이용 가능한 명령어의 리스트를 표시한다.
w(here) | 스택 트레이스(stack trace)를 출력한다.
n(ext) | 다음 행으로 넘어간다(다음 행 실행).
l(ist)[first[,last]] | 지정한 범위의 소스 코드를 표시한다. 지정하지 않으면 현재 위치 주위 11행을 표시한다.
c(ont(inue)) | 중간점(break point)에 도달할 때까지 실행한다.
q(uit) | 디버거를 종료한다.

## 중간점 삽입하기
pdb.set_trace를 삽입하면 중단점 역할을 합니다. pdb.set_trace의 삽입 위치에 도달한 시점에 디버그 모드로 전환됩니다.

### 디버깅 대상 스크립트: sample_pdb.py

```python
import pdb

def add(a, b):
    pdb.set_trace()
    return a + b

def main():
    add(1, 2)

if __name__ == "__main__":
    main()
```

### sample_pdb.py 실행

```
$ python sample_pdb.py
> /path/sample_pdb.py(5)add()
-> return a + b
(Pdb)

# help 명령어
(Pdb) h

Documented commands (type help <topic>):
========================================
EOF    c          d        h         list      q        rv       undisplay
a      cl         debug    help      ll        quit     s        unt
alias  clear      disable  ignore    longlist  r        source   until
args   commands   display  interact  n         restart  step     up
b      condition  down     j         next      return   tbreak   w
break  cont       enable   jump      p         retval   u        whatis
bt     continue   exit     l         pp        run      unalias  where

Miscellaneous help topics:
==========================
exec  pdb

# 현재 위치 주위 11행을 표시한다.
(Pdb) l
  1  	import pdb
  2
  3  	def add(a, b):
  4  	    pdb.set_trace()
  5  ->	    return a + b
  6
  7  	def main():
  8  	    add(1, 2)
  9
 10  	if __name__ == "__main__":
 11  	    main()

# 스택 트레이스를 표시한다.
(Pdb) w
  /path/sample_pdb.py(11)<module>()
-> main()
  /path/sample_pdb.py(8)main()
-> add(1, 2)
> /path/sample_pdb.py(5)add()
-> return a + b

# 다음 행을 처리한다.
(Pdb) n
--Return--
> /path/sample_pdb.py(5)add()->3
-> return a + b

# 다음 중단점까지 계속 처리한다.
(Pdb) c
```
디버거의 프롬포트가 (Pdb)로 바뀌어 있습니다.

## Python의 대화 모드에서 디버깅하기

### 대화 모드에서 디버깅 모드로 전환하기

```python
>>> import pdb
>>> import sample_pdb  # 디버깅 대상 스크립트(모듈)을 import한다.
>>> pdb.run(sample_pdb.main())  # pdb.run()에 디버깅 대상을 넘김다.
> /path/sample_pdb.py(5)add()
-> return a + b
(Pdb)
```

## 비정산적으로 종료하는 스크립트 디버깅하기 - pdb.pm
pdb.py를 스크립트로서 호출하면 프로그램이 비정산적으로 종료할 때 자동으로 디버그 모드로 전환할 수 있습니다.  

다음 스크립트 "sample_pdb2.py"를 디버깅합니다.

### ZeroDivisionError가 발생하는 스크립트: sample_pdb2.py

```python

def div(a, b):
    return a / b

def main():
    # 다음을 실행하면 1 / 0으로 ZeroDivisionError가 발생한다.
    div(1, 0)

if __name__ == "__main__":
    main()
```

### sample_pdb2.py 실행

```
# 실행하면 자동으로 디버그 모드로 전환
$ python -m pdb sample_pdb2.py
> /path/sample_pdb2.py(1)<module>()

# continue하면 오류가 발생하여 예외가 발생한 곳까지 돌아간다.
-> def div(a, b):
(Pdb) c
Traceback (most recent call last):
   ...
ZeroDivisionError: division by zero
Uncaught exception. Entering post mortem debugging
Running 'cont' or 'step' will restart the program
> /path/sample_pdb2.py(2)div()
-> return a / b

# 변수 내용을 확인
(Pdb) p a
1
(Pdb) p b
0

# 하나 위의 프레임으로 이동
(Pdb) u
> /path/sample_pdb2.py(5)main()
-> div(1, 0)
```

대화 모드에서 오류가 발생할 때 디버그 모드로 전환하려면 pdb.pm() 메서드를 사용합니다.

### 대화 모드에서 자동으로 디버그 모드로 전환하는 예

```python
>>> import pdb
>>> import sample_pdb2
>>> pdb.run(sample_pdb2.main())
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
>>> pdb.pm()
> /path/sample_pdb2.py(2)div()
-> return a / b
(Pdb)
```
