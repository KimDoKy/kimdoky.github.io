---
layout: post
section-type: post
title: Python Library - chap 5. 범용 OS/런타임 서비스 - 5.3 인터프리터 관련 정보를 얻고 조작하기
category: python
tags: [ 'python' ]
---
sys모듈은 Python 인터프리터에서 사용하는 변수와 Python 인터프리터의 동작에 관련된 함수를 제공합니다.

## 명령줄의 인수 얻기 -  sys.argv
sys.srgv는 Python 스크립트를 실행할 때 주어지는 인수가 저장되는 리스트입니다. sys.argv[0]은 실행된 스크립트 자신의 파일 이름입니다.

### hoge.py 파일

```python
import sys
print(sys.srgv)
```

이 스크립트를 인수를 붙여 실행하면 다음과 같습니다.

```
$ python hoge.py -a abc
['hoge.py', '-a', 'abc']
```

물론 sys.argv를 그대로 사용하여 명령줄(command line) 인수를 처리하는 데는 문제가 없습니다. 하지만 올바른 인수가 주어지지 않거나 인수를 순서 없이 부여하고 싶을 때, UNIX 명령어와 같은 방법으로 인수를 다루려고 하면 잘 되지 않습니다.  

복잡한 명령줄 인수를 처리해야 할 때에는 argparse 모듈을 사용하면 적은 명령어로 유연하게 인수 처리를 구현할 수 있습니다.

## 라이브러리의 import path  조작하기 - sys.path
sys.path는 import 대상 모듈이나 패키지를 탐색하는 위치가 되는 여러 개의 파일 경로를 저장한 리스트입니다. sys.path에 파일 경로를 추가하면 해당 파일 경로에 있는 Python 패키지나 모듈을 import 문으로 import 할 수 있습니다.  

sys.path는 다음과 같은 요소로 초기화됩니다.

- 실행된 Python 스크립트가 있는 경로 또는 대화 모드인 경우에는 빈 문자열(시작할 때 현재 디렉터리에서 탐색)
- 환경변수 PYTHONPATH로 설정된 경로
- Python의 설치 위치

### PYTHONPATH를 지정하여 대화 모드를 시작하는 예

```
$ ls /home/my/scripts
myscript.py

$ PYTHONPATH=/home/my/scripts python
```

### PYTHONPATH가 지정된 상태에서 sys.path의 값 확인

```
>>> import sys
>>> import pprint
>>> pprint.pprint(sys.path)
['',  # 대화 모드로 시작된 빈 문자열이 리스트 맨 앞에 지정됨
 '/home/my/scripts',  # 환경변수로 지정한 경로
 '/usr/local/var/pyenv/versions/3.5.2/lib/python35.zip',  # 이후는 Python 설치 위치로부터 설정되어 있음
 '/usr/local/var/pyenv/versions/3.5.2/lib/python3.5',
 '/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/plat-darwin',
 '/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/lib-dynload',
 '/usr/local/var/pyenv/versions/jupyter/lib/python3.5/site-packages']
>>> import myscript  # PYTHONPATH로 설정한 디렉터리 안의 모듈을 import 가능
```

모듈은 리스트의 맨 앞 경로부터 순서대로 검색되어, 맨 처음 발견된 것이 import됩니다. 따라서  표준 라이브러리와 같은 이름의 모듈을 생성하는 것은 피하거나 주의해야 합니다.  

실행할 때 임의의 파일 경로를 추가하려면 다음과 같이 합니다.

```python
>>> import sys
>>> sys.path.append('/home/my/scripts')
>>> import myscript
```

## 프로그램 종료하기 - sys.exit
sys.exit()는 호출한 시점에 Python 스크립트 실행을 종료시킵니다. 또한 대화 모드에서 호출한 경우에는 대화모드를 종료시킵니다.

### sys.exit() 함수

형식 | exit([arg])
---|---
설명 | Python을 종료한다.
인수 | arg - 수치 또는 임의의 객체를 지정한다.

sys.exit()는 SystemExit 얘외를 발생시키도록 구현되어 있으므로, 이 예외를 잡으면 (catch)종료 처리를 중단할 수도 있습니다.  

인수 arg에는 종료 상태(status)를 지정할 수 있습니다. 수치 이외의 객체를 주면, 주어진 객체를 문자열로 sys.stderr에 출력하고 호출한 원래 위치에 종료 코드 1을 반환하고 종료합니다. 또한, 인수를 생략하면 종료 코드 0으로 종료합니다.

### sys.exit()에 인수를 지정하여 종료하는 예

```python
import sys
sys.exit('프로그램을 종료합니다.')
```

많은 셸에서는 $?라는 변수에 직전에 실행한 명령어의 종료 코드가 대입됩니다. 앞의 코드가 기술된 exit.py라는 파일을 셸로부터 호출합니다.

```
$ python exit.py
프로그램을 종료합니다.

$ echo $?  # 직전에 실행한 명령어의 종료 코드를 출력
1
```

코드에서 sys.exit()의 인수로 수치 이외의 값을 주었기 때문에, 종료 코드가 1이 되어 있는 것을 알 수 있습니다.  

단순히 Python 스크립트의 실행을 중지하고 싶은 경우라면, 인수 없이 sys.exit()를 호출하기만 하면 됩니다. 만약 Python 스크립트의 실행을 중지하는 이유가 여러 개이고 이를 호출한 원 위치(셸 등)에 전달해야 할 필요가 있다면, sys.exit()를 호출할 때 인수에 각각 다른 수치를 넘기면 됩니다.

## 콘솔 입출력 - sys.stdin, stdout, stderr
sys 모듈에는 인터프린터가 사용하는 콘솔의 입출력용 객체가 있어, 표준 출력이나 표준 오류 출력, 표준 입력을 다룰 수 있습니다.  

다음 3개의 객체는 모두 파일 객체입니다. 보통의 파일과 마찬기지로 write()나 read() 메서드로 읽고 쓰기가 가능하지만, 각각 쓰기 전용이나 읽기 전용의 성질을 갖고 있습니다.

### 입출력 객체의 종류

객체 | 설명 | 타입
---|---|---
sys.stdin | 표준 입력 객체 | 읽기 전용
sys.stout | 표준 출력 객체 | 쓰기 전용
sys.stderr | 표준 오류 출력 객체 | 쓰기 전용

### 입출력 객체의 사용 예

```python
>>> sys.stdout.write('standard output message\n')
standard output message  # 표준 출력된 메시지
24  # write() 메서드의 반환값

>>> sys.stderr.write('standard error message\n')
standard error message  # 표준 오류 출력된 메시지
23  # write() 메서드의 반환값

>>> sys.stdin.write('standard input message?\n')
Traceback (most recent call last):  # 표준 입력 객체는 읽기 전용이므로, 쓰기는 실패함
  File "<stdin>", line 1, in <module>
io.UnsupportedOperation: not writable

>>> sys.stdin.read()
standard input message  # 콘솔에 임의의 문자열을 입력하고 줄바꿈
'standard input message\n'  # Control + D 가 입력되면, read() 메서드로 받은 입력을 반환함
```
