---
layout: post
section-type: post
title: Python Library - chap 5. 범용 OS/런타임 서비스 - 5.1 운영체제의 기능 이용하기
category: python
tags: [ 'python' ]
---
운영체제가 제공하는 기능을 이용하는 것을 비롯하여 서버의 운용과 관리에 도움이 되는 표준 라이브러리를 소개합니다. 이를 잘 활용하면 작업 자동화나 효율화에 크게 도움이 됩니다. 또한, Python 인터프리터와 관련된 기능을 제공하는 표준 라이브러리에 대해서도 살펴봅니다.

# 운영체제의 기능 이용하기

os 모듈은 다음과 같은 기능을 제공합니다.

- 실행 중인 프로세스 속성 조작
- 파일 기술자 조작
- 파일과 디렉터리 조작
- 프로세스 관리
- 다양한 시스템 정보에 대한 접근
- 스케쥴러 인터페이스
- 무작위 문자열 생성

## 실행 중인 프로세스 속성 조작하기
os 모듈은 실행 중인 프로세스의 속성 취득이나 변경과 같은 기능을 제공합니다.

### 조작 가능한 프로세스 속성과 대응하는 함수의 예

속성의 종류 | 함수
---|---
환경변수 | environ, getenv(), putenv(), ...
사용자 ID | getuid(), setuid(), geteuid(), seteuid(), ...
그룹 ID | getgid(), setgid(), getgroups(), setgroups(), ...
프로세스 ID |  getpid(), getpgid(), getppid(), ...
스케쥴링 우선도 | getpriority(), setpriority(), ...

프로세스 속성에 대한 기능 대부분은 UNIX 계열 운영체제 기능에 의존하고 있기 때문에, Windows 환경에서는 이용할 수 없는 것도 많습니다.  

os.environ은 Python 프로세스를 구동한 때 환경변수를 저장하는 맵 형식의 객체입니다. UNIX와 Windows에서 모두 이용할 수 있습니다.

### 환경변수에 접근하기

```python
>>> import os
>>> os.environ['HOME']  # 사용자의 홈 디렉터리가 저장된 환경변수
'/Users/dokyungkim'

>>> os.environ['HAM'] = 'egg'  # 새로운 환경 변수 설정
```

os.environ에 저장된 것은 맨 처음 os 모듈이 import된 시점의 환경변수입니다. "맨 처음"이라는 것은 보통은 Python 구동 시에 site.py가 처리되는 도중에 이루어지는 것을 말합니다. 그 후에 변경된 환경변수는 반영되지 않으므로, os.environ을 직접 변경해야 합니다. 또한, 설정한 환경변수는 실행 중인 프로세스 상의 os.environ에만 반영되어 있으므로, 다른 프로세스 간에 값을 공유하는 용도로는 사용할 수 없습니다.  

os 모듈로 조작할 수 있는 다른 프로세스 속성에 대해서도 마찬가지로 실행 중인 프로세스에만 반영됩니다.

## 파일과 디렉터리 조작하기
os 모듈은 낮은 레벨의 파일 조작 기능도 제공합니다. 기능 대부분은 UNIX와 Windows 양쪽에서 이용할 수 있으나, 심볼릭 링크를 이용하는 기능 중에는 Windows에서는 쓸 수 없는 기능도 있습니다.

### 파일 조작 관련 함수

함수 이름 | 설명 | 반환값 | 이용 환경
---|---|---|---
chdir(path) | 현재 작업 디렉터리를 path로 지정한다. | None | UNIX, Windows
chmod(path, mode, \*, dir_fd=None, follow_symlinks=True) | path로 지정한 파일 또는 디렉터리의 모드를 변경한다. | None | UNIX
chown(path, uid, gid, \*, dir_fd=None, follow_symlinks=True) | path로 지정한 파일 또는 디렉터리의 소유자와 그룹을 변경한다. | None | UNIX
getcwd() | 현재 작업 디렉처리를 반환한다. | Str | UNIX, Windows
listdir(path='.') | path로 지정한 디렉터리 안의 파일과 디렉터리를 반환한다. | list | UNIX, Windows
mkdir(path, mode=0o777,\*,dir_fd=None) | path로 지정한 디렉터리를 생성한다. | None | UNIX, Windows
makedirs(name, mode=0o777, exist_ok=False) | name으로 지정한 디렉터리를 재귀적으로 생성한다. <br> 말단 디렉터리뿐만 아니라 중간 디렉터리도 생성한다. | None |  UNIX, Windows
remove(path, \*, dir_fd=None) | path로 지정한 파일을 삭제한다. 디렉터리일 때는 OSError가 발생한다. | None | UNIX, Windows
removedirs(name) | name으로 지정한 디렉터리를 경로 말단부터 재귀적으로 삭제한다. | None | UNIX, Windows
rename(src, dst, \*, src_dir_fd=None, dst_dir_fd=None) | 파일 또는 디렉터리의 경로를 src에서 dst로 변경한다. | None | UNIX, Windows
renames(old, new) | 파일 또는 디렉터리의 경로를 old에서 new로 변경한다. new로 지정한 경로에 makedirs()와 같이 중간 디렉터리를 생성하고, old로 지정한 경로는 removedirs()와 같이 말단 디렉터리부터 재귀적으로 삭제한다. | None | UNIX, Windows
rmdir(path) | path로 지정된 디렉터리를 삭제한다. 디렉터리가 비어있지 않은 경우에는 OSError가 발생한다. | None | UNIX, Windows
symlink(source, link_name, target_is_directory=False, \*, dir_fd=None) | source를 가리키는 심볼릭 링크를 link_name으로 지정한 파일 이름으로 생성한다. | None | UNIX, Windows

### 기본적인 파일 조작

```python
>>> import os
>>> os.getcwd()  # 현재 작업 디렉터리를 구함
'/Users/ex/'

>>> os.chdir('/tmp')  # /tmp 디렉터리로 이동
>>> os.mkdir('test')  # test 디레겉리 생성
>>> os.listdir('.')  # 현재 디렉터리 안의 파일과 디렉터리의 리스트를 생성
['test']

>>> os.rmdir('test')  # test 디렉터리 삭제
```

## 다양한 시스템 정보에 대해 접근하기
os 모듈은 운영체제의 시스템 정보에 접근하는 기능을 제공합니다.

### 시스템 정보 관련 함수와 상수

함수 이름 | 설명 | 반환값 | 이용 환경
---|---|---|---
confstr(name) | 시스템 설정 값을 문자열로 반환한다. | str | UNIX
confstr_names | confstr()에 전달할 수 있는 값을 정의한 dict | dict | UNIX
sysconf(name) | 시스템 설정 값을 정수로 반환한다. | int | UNIX
sysconf_names | sysconf()에 전달할 수 잇는 값을 정의한 dict | dict | UNIX
cpu_count() | CPU 수를 가져온다. 가져올 수 없으면 None을 반환한다. | int | UNIX
getloadavg() | 지난 1분, 5분, 15분간 평균 부하를 튜플로 반환한다. | (float, float, float) | UNIX

> ### os.cpu_count()와 multiprocessing.cpu_count  
os.cpu_count()는 문자 그대로 실행한 기계의 CPU 수를 반환합니다. 다른 모듈에 구현된 같은 함수로 multiprocessing.cpu_count()라는 것이 있으나, 이 둘의 차이 점은 Python이 CPU 수를 구하지 못했을 떄의 동작입니다.  
os.cpu_count()는 None을 반환하고, multiprocessing.cpu_count()는 NotImplementedError 예외가 발생합니다. CPU 수를 구하지 못했을 때 정상적으로 동작하지 않는 프로그램이라면 휴자를 사용하여 오류 처리를 하면 좋습니다.

### 파일 경로 관련 상수

함수 이름 | 설명 | 반환값 | 이용 환경
---|---|---|---
curdir | 현재 디렉터리를 나타내는 문자열 상수 | str | UNIX, Windows
pardir | 부모 디렉터리를 나타내는 문자열 상수 | str | UNIX, Windows
sep | 경로 이름의 구분을 나타내는 문자열 | str | UNIX, Windows
extsep | 파일 이름과 확장자를 나누는 문자 | str | UNIX, Windows
linesep | 행의 마지막을 나타내는 문자 | str | UNIX, Windows

## 무작위 문자열 생성하기
### os.urandom()을 사용한 무작위 문자열 생성
os.urandom()은 운영체제가 제공하는 난수 생성기를 사용하여 무작위 문자열을 반환합니다. UNIX, Windows에서 이용할 수 있습니다.

```python
>>> os.urandom(10)  # 10 바이트의 무작위 문자열을 생성
b'\xd5T\xe20\xabE\xc3\x82\xb3Q'
```

random 모듈이 생서하는 난수는 의사 난수입니다. 따라서 보안상의 용도로는 적합하지 않습니다. 보안이 필요할 때는 os.urandom()을 사용하거나 내부에서 os.urandom()을 사용하여 난수를 생성하는 random.SystemRandom 클래스를 이용할 것을 추천합니다.
