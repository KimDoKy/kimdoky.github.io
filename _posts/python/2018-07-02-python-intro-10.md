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
