---
layout: post
section-type: post
title: Python Library - chap 13. 병렬처리 - 2. 서브 프로세스 관리하기
category: python
tags: [ 'python' ]
---

`subprocess`는 자식 프로세스의 생성과 관리 기능을 제공합니다. subprocess는 새로 프로세스를 시작하거나, 프로세스의 표준 입출력과 오류 출력에 대하여 파이프로 연결하거나, 종료 상태를 취득합니다.

## 자식 프로세스 실행하기
자식 프로세스 실행에는 `subprocess.call()` 메서드를 사용합니다.

### subprocess를 이용하여 명령어를 실행하는 예

```Python
>>> import subprocess

# 실행하려는 명령어와 인수를 리스트로 넘김
>>> result = subprocess.call(['echo','Hello World!'])
Hello World!
>>> result
0

# shell=True라고 지정하면 셸을 거쳐 명령어가 실행됨
# 여기에서는 'exit 1'을 지정하여 셸을 비정상 종료시키고 있음
>>> result = subprocess.call(['exit 1'], shell=True)
>>> result
1
```
메서드를 실행하면, 실행한 명령어의 종료 상태가 반환값으로 반환됩니다.(정상 종료한 경우에는 0이 반환됨) "shell=True"를 지정하면 셸을 통해 명령어가 실행되므로 셸 특유의 다양한 기능을 사용할 수 있는 반면, 실행 결과가 사용자의 플랫폼에 의존하여 달라집니다. 특별한 경우가 아니라면 "shell=True"는 지정하지 않는 것이 좋습니다.  

정상 종료하지 않았을 때 예외를 발생시키려면 `subprocess.check_call()` 메서드를 이용합니다.

### 자식 프로세스가 비정상 종료할 때 예외 발생

```python
>>> subprocess.check_call(['exit 1'], shell=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/3.5.2/lib/python3.5/subprocess.py", line 581, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command '['exit 1']' returned non-zero exit status 1
```
subprocess.check_call() 메서드는 자식 프로세스가 정상 종료되지 않았을 때 CalledProcessError 예외가 발생합니다.

## 자식 프로세스를 실행하여 표준 출력 결과 얻기
subprocess.call() 보다 복잡한 처리를 하려는 경우, 예를 들어 표준 입출력/오류 출력과 값을 주고받고 싶을 때에는 `subprocess.Popen` 클래스를사용합니다.

### Popen 클래스의 인스턴스를 생성할 때 지정할 수 있는 주요 인수

옵션 이름 | 설명
---|---
args | 실행할 프로그램을 문자열 또는 시퀀스로 지정한다.
stdin, stdout, stderr | 표준 입출력 및 표준 오류 출력의 파일 핸들러를 지정한다. 기본값은 None.
shell | True이면 셸을 거쳐 명령어를 실행한다. 기본값은 False.

자식 프로세스의 표준 입력에 데이터를 보내고 싶을 때, 혹은 자식 프로세스의 표준 출력 및 표준 오류 출력으로부터 데이터를 받고 싶을 때는 각각의 인수에 subprocess.PIPE를 지정해야 합니다. subprocess.PIPE는 표준 스트림에 대해 파이프 여는 것을 지정하기 위한 특별한 값입니다.

### 명령어의 표준 출력 결과를 얻는 예

```python
>>> from subprocess import Popen, PIPE
>>> cmd = 'echo Hello World!'

# 자식 프로세스 생성
>>> p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

# 실행한 결과를 표준 출력으로 얻음
>>> stdout_data, stderr_data = p.communicate()
>>> stdout_data
b'Hello World!\n'
```

> #### 자식 프로세스의 표준 출력을 얻을 때는 communicate()를 사용하자  
subprocess 모듈은 자식 프로세스의 표준 출력을 얻는 방법으로 communicate() 메서드 외에 stdout.read(), stderr.read()와 같은 메서드를 제공합니다.
하지만 communicate() 메서드 외의 방법을 이용하면 표준 출력 데이터의 양이 매우 클 때, OS의 파이프 버퍼가 대기 상태가 되어 데드록(deadlock)이 발생하는 문제가 있습니다.
이와 같은 데드록을 피하기 위해, 자식 프로세스의 표준 출력을 얻을 때는 communicate()를 이용하면 됩니다.

## 여러 자식 프로세스를 연결하여 최종 결과 얻기
명령어를 파이프로 이어서 이용하는 것처럼, 자식 프로세스의 출력을 다른 자식 프로세스의 입력으로 전달하는 처리를 작성할 수 있습니다. 앞선 프로세서의 출력(Popen.stdout)을 다음 프로세스의 입력(stdin)으로 전달하면 됩니다.

### 자식 프로세스의 출력을 다른 출력 프로세스의 입력으로 전달하는 예

```python
>>> from subprocess import Popen, PIPE

# 첫 번째 자식 프로세스 생성(Hello World! 라고 출력함)
>>> cmd1 = 'echo Hello World!'
>>> p1 = Popen(cmd1, shell=True, stdout=PIPE, stderr=PIPE)

# 첫 번째 자식 프로세스를 두 번째 프로세스의 입력으로 넘겨줌(받은 출력을 소문자로 변환함)
>>> cmd2 = 'tr "[:upper]" "[:lower]"'
>>> p2 = Popen(cmd2, shell=True, stdin=p1.stdout, stdout=PIPE, stderr=PIPE)

# 최종 출력 결과를 얻음
>>> stdout_data, stderr_data = p2.communicate()
>>> stdout_data
b'Hello World!\n'
```
