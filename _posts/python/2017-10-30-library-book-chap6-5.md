---
layout: post
section-type: post
title: Python Library - chap 6. 파일과 디렉터리 접근하기 - 5. 고급 파일 조작
category: python
tags: [ 'python' ]
---

`shutil` 모듈은 디렉터리 파일과 압축 파일에 대한 고도의 조작 기능을 제공합니다.

## 파일 복사하기

`shutil`에는 파일 자체를 복사하는 메서드나 파일의 속성을 복사하는 메서드가 있습니다.

### 파일 복사 계열 함수

함수 이름 | 설명 | 반환값
---|---|---
copymode(src, dst, \*, follow_symlinks=True) | 권한을 src에서 dst로 복사한다. | None
copystat(src, dst, \*, follow_symlinks=True) | 권한, 최종 접근 시간, 최종 변경 시간 및 기타 파일 정보를 src에서 dst로 복사한다. | None
copy(src, dst, \*, follow_symlinks=True) | 파일 src를 파일 또는 디렉터리를 가리키는 dst로 복사한다. | str
copy2(src, dst, \*, follow_symlinks=True) | copy()와 같은 기능에 추가로 모든 메타 데이터를 복사한다.

`copy()`는 파일의 데이터와 권한을 복사하지만, 파일 생성 시간이나 변경 시간은 복사하지 않습니다. 메타 데이터를 복사하려면 `copy2()`를 사용합시다.

## 재귀적으로 디렉터리와 파일 조작하기

`shutil`를 사용하면 지정한 디렉터리의 재귀적인 복사나 삭제, 이동이 가능합니다. 이들 기능에는 `os` 모듈의 파일 조작 기능이나 `shutil` 모듈 자신의 파일 복사 계열 기능을 이용할 수 있습니다.

### 재귀적인 조작 실행 함수

함수 이름 | 설명 | 반환값
---|---|---
ignore_patterns(\*patterns) | patterns에 glob 형식의 문자열을 여러 개 지정할 수 있다. | 호출 기능 객체
rmtree(path, ignore_errors=False, onerror=None) | 지정한 디렉터리를 삭제한다. | None
move(src, dst) | 지정한 디렉터리로 이동한다. | str

## 특정 디렉터리의 내용 복사하기
디렉터리를 통째로 복사할 때는 `copytree()`를 사용합니다.

### copytree() 함수

형식 | copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2, ignore_dangling_symlinks=False)
---|---
설명 | 특정 디렉터리 아래 구조를 그대로 다른 위치로 복사한다.
인수 | src - 복사 대상 디렉터리 경로를 지정한다. <br> dst - 복사 후의 디렉터리 경로를 지정한다. 이는 존재할 때 예외가 발생한다. <br> symlinks - 참이면 심볼릭 링크는 복사 후에도 심볼릭 링크가 되나, 거짓이면 링크 위치의 파일 자체가 복사된다. <br> ignore - 제외할 파일을 결정하는 호출 기능 객체를 지정한다. <br> copy_function - 복사에 사용할 호출 가능 객체를 지정한다. <br> ignore_dangling_symlinks - 참이면 인수 symlinks가 거짓일 때, 링크 참조 위치가 존재하지 않더라도 오류로 취급하지 않는다.
반환값 | 복사한 디렉터리 이름

다음 예에서는 `ignore_patterns()`를 사용하여 특정 파일만 복사 대상에서 제외하고 있습니다.

### 지정한 디렉터리를 복사하는 샘플 코드

```python
>>> import shutil
>>> ignore = shutil.ignore_patterns('*.pyc', '*swp')  # pyc, swp 확장자 파일은 제외한다.
>>> ignore  # ignore(path, names)라는 호출이 가능한 객체
<function ignore_patterns.<locals>._ignore_patterns at 0x10180ad90>

>>> shutil.copytree('./from', './to', ignore=ignore)
'./to'  # 복사한 디렉터리 이름을 반환한다.
# 복사 중에 발생한 모든 오류는 리스트로 반환된다.

>>> exit()
------------------------------------------------------------

$ l from  # from 디렉터리 파일 확인
total 0
drwxr-xr-x  5 dokyungkim  staff   170B 11  1 22:14 .
drwxr-xr-x  9 dokyungkim  staff   306B 11  1 22:15 ..
-rw-r--r--  1 dokyungkim  staff     0B 11  1 22:14 a.pyc
-rw-r--r--  1 dokyungkim  staff     0B 11  1 22:13 a.txt
-rw-r--r--  1 dokyungkim  staff     0B 11  1 22:14 b.swp

$ l  # to 디렉터리 생성된 것 확인
total 0
drwxr-xr-x  9 dokyungkim  staff   306B 11  1 22:15 .
drwxr-xr-x  5 dokyungkim  staff   170B 10 29 20:53 ..
drwxr-xr-x  5 dokyungkim  staff   170B 11  1 22:14 from
drwxr-xr-x  3 dokyungkim  staff   102B 11  1 22:14 to
------------------------------------------------------------
$ l to  # ignore에서 설정한 파일만 제외하고 복사된 것 확인
total 0
drwxr-xr-x  3 dokyungkim  staff   102B 11  1 22:14 .
drwxr-xr-x  9 dokyungkim  staff   306B 11  1 22:15 ..
-rw-r--r--  1 dokyungkim  staff     0B 11  1 22:13 a.txt
```

glob 형식의 지정으로는 부족하거나 복사 대상 파일 이름을 이용하여 임의의 처리를 실행하고자 할 때는 직접 함수를 정의하여 인수 ignore에 지정합니다.

## 압축 파일의 생성과 압축 해제

`shutil` 모듈은 압축 파일의 생성과 압축 해제 기능도 제공합니다. 압축 파일 관련 기능은 `zipfile` 모듈과 `tarfile` 모듈에 따라 다릅니다.  

또한, 표준으로 지원되지 않는 형식의 아카이브를 등록할 수도 있습니다.

### make_archive() 함수

형식 | make_archive(base_name, format[,root_dir[,base_dir[,verbose,[, dry_run[, owner[, group[, logger]]]]]]])
---|---
설명 | 압축 파일을 생성한다.
인수 | base_name - 지정한 문자열에 확장자가 추가된 압축 파일이 생성된다. <br> format - 압축 포맷을 지정한다. <br> root_dir - 압축 파일의 루트 디렉터리를 지정한다. 기본값은 현재 디렉터리이다. <br> base_dir - 압축을 시작할 디렉터리를 지정한다. 기본값은 현재 디렉터리이다. <br> verbose - 현재는 사용하지 않는다. <br> dry_run - 압축 파일을 생성하지 않고 로그 출력만 실행한다. <br> owner - 생성된 압축 파일의 소유자를 지정한다. <br> group - 생성된 압축 파일의 그룹을 지정한다. <br> logger - 로그 출력에 사용할 로거를 지정한다.
반환값 | 생성한 압축 파일 이름

### unpack_archive() 함수

형식 | unpack_archive(filename[, extract_dir[, format]])
---|---
설명 | 압축 파일을 해제한다.
인수 | filename - 해제할 대상 압축 파일의 경로를 지정한다. <br> extract_dir - 압축을 풀 위치가 될 디렉터리를 지정한다. <br> format - 해제에 이용할 압축 포맷을 지정한다.

사용 예로 다음 디렉터리 구조로부터 example 디렉터리 이하를 압축해봅니다.

### archive 대상 디렉터리 구조

```
/tmp/
└── example
    ├── fuga.txt
    ├── hoge.txt
    └── piyo.txt
```

### archive 파일 생성과 해제 샘플 코드

```
>>> shutil.make_archive(base_name='example_test', format='gztar', root_dir='/tmp', base_dir='example')
'/tmp/example_test.tar.gz'
>>> shutil.unpack_archive(filename='example_test.tar.gz', extract_dir='/tmp/ex')
# path에 전체 경로를 기술해야 디렉터리를 찾습니다.
# 보안상의 이유로 상대경로만 적어두었습니다.
```

`make_archive()`의 결과 /tmp/example_test.tar.gz가 생성되었으며, `unpack_archive()`의 결과로 /tmp/ex/example 디렉터리와 그 아래 세 개의 텍스트 파일이 해제 되었습니다.

```
/tmp/
├── ex
│   └── example
│       ├── fuga.txt
│       ├── hoge.txt
│       └── piyo.txt
├── example
│   ├── fuga.txt
│   ├── hoge.txt
│   └── piyo.txt
└── example_test.tar.gz
```

---

## follow_symlinks 무효화에 따른 동작 변화
파일을 조작하는 함수 대부분은 follow_symlinks가 인수로 지정되어 있습니다. 이 인수의 기본값은 True이며, 대상이 심볼릭 링크일 때 링크된 원본에 처리가 적용됩니다. 이 인수에 False를 넘기면 함수에 의해 각각 다른 동작을 실행하게 되므로 주의해야 합니다.  
다음의 `copyfile()`의 예입니다. 우선 기본 동작인 경우입니다.

>> [mac에서 symlink 구성하기](https://kimdoky.github.io/tip/2017/11/01/tip-mac-symlink.html){:target=`_`blank}

### 실행 전의 초기 파일 구성

```
$ ls -l
total 8
-rw-r--r--  1 dokyungkim  staff  0 11  1 23:28 _a.txt
lrwxr-xr-x  1 dokyungkim  staff  6 11  1 23:26 a.txt -> _a.txt
```

이처럼 \_a.txt를 링크하는 심볼릭 링크 a.txt가 있습니다. a.txt를 `copyfile()`로 복사합니다.

### 인수 follow_symlinks를 지정하지 않을 때

```python
>>> shutil.copyfile('a.txt', 'b.txt')
'b.txt'
```
copyfile은 a.txt의 링크 원본을 따라가 \_a.txt의 내용으로 b.txt를 생성합니다. 다음은 실행 결과입니다. 복사 후 b.txt는 \_a.txt와 같은 크기로 생성된 것을 알 수 있습니다.

### 실행 결과

```
$ ls -l
total 8
-rw-r--r--  1 dokyungkim  staff  0 11  1 23:28 _a.txt
lrwxr-xr-x  1 dokyungkim  staff  6 11  1 23:26 a.txt -> _a.txt
-rw-r--r--  1 dokyungkim  staff  0 11  1 23:32 b.txt
```

다음으로, 초기 파일 구성에서 인수 `follow_symlinks`가 False로 지정된 경우입니다. 인수 follow_symlinks는 잘못된 값이 주어지는 것을 막고자 반드시 이름이 있는(named) 인수를 지정하도록 정의하고 있습니다.

### 인수 follow_symlinks에 False를 지정할 때

```python
>>> shutil.copyfile('a.txt', 'b.txt', follow_symlinks=False)
'b.txt'
```

b.txt는 a.txt와 같은 링크 원본을 가리키는 심볼릭 링크로 생성되었습니다. 앞의 예와는 달리, 복사 후의 b.txt는 a.txt와 마찬가지로 \_a.txt의 심볼릭 링크로 생성된 것을 알 수 있습니다.

### 실행 결과

```
$ ls -l
total 16
-rw-r--r--  1 dokyungkim  staff  0 11  1 23:28 _a.txt
lrwxr-xr-x  1 dokyungkim  staff  6 11  1 23:26 a.txt -> _a.txt
lrwxr-xr-x  1 dokyungkim  staff  6 11  1 23:36 b.txt -> _a.txt
```

### 정리

```
$ cat _a.txt
sample

$ l
total 16
drwxr-xr-x   4 dokyungkim  staff   136B 11  1 23:40 .
drwxr-xr-x  14 dokyungkim  staff   476B 11  1 23:18 ..
-rw-r--r--   1 dokyungkim  staff     7B 11  1 23:39 _a.txt
lrwxr-xr-x   1 dokyungkim  staff     6B 11  1 23:40 a.txt -> _a.txt

# python shell

>>> import shutil
>>> shutil.copyfile('a.txt', 'b.txt')
'b.txt'
>>> shutil.copyfile('a.txt', 'c.txt', follow_symlinks=False)
'c.txt'
>>> shutil.copyfile('a.txt', 'd.txt', follow_symlinks=True)
'd.txt'
>>> exit()

$ ls -l
total 40
-rw-r--r--  1 dokyungkim  staff  7 11  1 23:39 _a.txt
lrwxr-xr-x  1 dokyungkim  staff  6 11  1 23:40 a.txt -> _a.txt
-rw-r--r--  1 dokyungkim  staff  7 11  1 23:43 b.txt
lrwxr-xr-x  1 dokyungkim  staff  6 11  1 23:44 c.txt -> _a.txt
-rw-r--r--  1 dokyungkim  staff  7 11  1 23:44 d.txt

$ cat _a.txt
sample

$ cat a.txt
sample

$ cat b.txt
sample

$ cat d.txt
sample
```
