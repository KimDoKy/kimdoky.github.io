---
layout: post
section-type: post
title: Python Library - chap 6. 파일과 디렉터리 접근하기 - 3. 임시 파일과 디렉터리 만들기
category: python
tags: [ 'python' ]
---

`tempfile` 모듈은 임시 파일과 디렉터리를 생성하는 기능을 제공합니다. `tempfile`은 사용자만 읽고 쓸 수 있도록 권한이 설정되고, 생성할 때 경합하지 않는 등, 가능한 한 안전한 방법으로 구현되어 있습니다.  

### tempfile 모듈이 제공하는 함수
이들 함수는 각각 적절한 클래스의 인스턴스를 생성하여 반환하므로, 인스턴스형은 각 함수의 이름과는 다릅니다.

함수 이름 | 설명
---|---
`TemporaryFile()` | 파일 이름이 없는 임시 파일을 생성한다.
`NamedTemporaryFile()` | 파일 이름이 있는 임시 파일을 생성한다.
`SpooledTemporaryFile()` | 일정 크기의 데이터까지는 메모리에 쓰고, 이를 넘어서면 디스크에 쓰는 임시 파일을 생성한다.
`TemporaryDirectory()` | 임시 디렉터리를 생성한다.

다음은 임시 파일을 다루는 세 가지 함수의 동작을 임시 파일에 데이터를 쓸 때, 데이터를 쓰는 위치와 임시 파일이 파일 시스템상에 이름을 가진 파일로 생성되는지 여부에 따라 정리한 표입니다.

### 임시 파일을 다루는 세 가지 함수의 특징

함수 이름 | 데이터를 쓰는 위치 | 파일 이름
---|---|---
`TemporaryFile()` | 디스크 | 없음
`NamedTemporaryFile()` | 디스트 | 있음
`SpooledTemporaryFile()` | 메모리 -> 디스크 | 없음

`TemporaryFile()`로 생성한 임시 파일은 파일 시스템상에 이름을 가진 파일로 생성된다는 보장이 없습니다. 또한, 데이터는 디스크에 쓰이기 때문에 많은 데이터를 다룰 때에도 메모리에 부담을 주지 않습니다.  

`NamedTemporaryFile()`로 생성된 파일은 시스템사엥 이름을 가진 파일로 생성되므로, 다른 프로그램에서도 파일의 존재를 인식하거나 파일 안을 참조할 수 있습니다. 그 외 동작은 `TemporaryFile()`과 같습니다.  

`SpooledTemporaryFile()`은 데이터를 기본적으로 메모리에 쓰지만, 인수로 지정한 크기를 넘어서면 메모리에서 디스크로 쓰는 위치가 바뀌기 때문에, 메모리 소모량이 지나치게 커지는 것을 막을 수 있습니다. 디스크에 쓴 뒤의 동작은 `TemporaryFile()`과 같습니다.

## 임시 파일 생성하기

### TemporaryFile() 함수

형식 | `TemporaryFile(mode='w+b', buffering=None, encoding=None, newline=None, suffix=", prefix='tmp', dir=None)`
---|---
설명 | 임시 파일을 생성한다.
인수 | `mode` - 임시 파일을 열 때 모드를 지정한다. <br> `buffering` - 내장 함수 `open()`의 같은 이름을 지닌 인수와 마찬가지로 취급된다. <br> `encoding` - 내장 함수 `open()`의 같은 이름을 지닌 인수와 마찬가지로 취급된다. <br> `newline` - 내장 함수 `open()`의 같은 이름을 지닌 인수와 마찬가지로 취급된다. <br> `suffix` - 지정된 문자열이 임시 파일 이름의 맨 끝에 부여된다. <br> `prefix` - 지정된 문자열이 임시 파일 이름의 맨 앞에 부여된다. <br> `dir` - 임시 파일을 생성한 디렉터리를 지정한다.

`TemporaryFile()`은 컨텍스트 매니저로서 기능하며, with 블록을 빠져나오면 암묵적으로 `.close()`가 호출됩니다. `.close()`는 임시 파일을 닫음과 동시에 삭제합니다.

### 임시 파일 사용 예

```python
>>> import tempfile
>>> with tempfile.TemporaryFile() as tmp:
...     tmp.write(b'test test test\n')
...     tmp.seek(0)
...     tmp.read()
...
15
0
b'test test test\n'
>>> tmp.write(b'write again\n')  # 파일이 닫힌 뒤이기 때문에 쓰기에 실패
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: write to closed file
```
컨텍스트 매니저로서 사용하지 않고 명시적으로 파일을 삭제하려면, 임시 파일 객체로부터 `.close()`를 호출합니다.

### 명시적으로 임시 파일 삭제

```
tmp = tempfile.TemporaryFile()
temp.close()
```

또한 `TemporaryFile()`로 생성된 임시 파일은 파일 시스템상에 이름을 가진 파일로서 생성된다는 보장이 없습니다. UNIX 환경에서 실행하면, 생성된 파일을 파일 시스템 상에서 발견할 수 없습니다. 파일 시스템상에 임시 파일이 생성된 것을 확인하려면 `NamedTemporaryFile()`을 사용해야 합니다.

### 이름을 가진 임시 파일 생성

```python
>>> import tempfile, os
>>> tmp = tempfile.NamedTemporaryFile()
>>> tmp.name
'/var/folders/63/cd4_xzc12lg7vjqb1hqltffr0000gn/T/tmp84fvgekk'

>>> os.path.exists(tmp.name)
True
```

`NamedTemporaryFile()`로 생성한 임시 파일의 속성 `name`의 값은 생성된 임시 파일의 경로이며, `os.path.exists()`로 파일이 존재하는 것을 확인하였습니다.  

`TemporaryFile()`과 `SpooledTemporaryFile()`로 생성한 임시 파일은 파일 경로를 값으로 하는 속성을 가지지 않기 때문에, 파일 시스템상에서 파일이 존재하는 것을 확인할 수 없습니다.

## 임시 디렉터리 생성하기

`TemporaryDirectory()` 함수는 임시 디렉터리를 생성합니다.

### TemporaryDirectory() 함수

형식 | `TemporaryDirectory(suffix='', prefix='tmp', dir=None)`
---|---
설명 | 임시 디렉터리를 생성한다.
인수 | `suffix` - 지정된 문자열이 임시 파일 이름의 맨 끝에 부여된다. <br> `prefix` - 지정된 문자열이 임시 파일 이름의 맨 앞에 부여된다. <br> `dir` - 임시 파일을 생성할 부모 디렉터리를 지정한다.

`TemporaryDirectory`도 `TemporaryFile`과 마찬가지로 컨텍스트 매니저로서 기능하며, 블록을 빠져나옴과 동시에 디렉터리가 삭제됩니다. `as` 구문으로 선언한 변수에 대입되는 것은 생성된 디렉터리를 나타내는 파일 경로입니다.

### 임시 디렉터리 사용 예

```python
>>> with tempfile.TemporaryDirectory() as dir_path:
...     with tempfile.TemporaryFile(dir=dir_path) as tmp:
...         .... # 임시 파일을 사용한 어떤 처리를 수행
```

컨텍스트 매니저로서 사용하지 않고 명시적으로 디렉터리를 삭제하려면, 임시 디렉터리 객체로부터 `.cleanup()` 메서드를 호출합니다.

### 명시적으로 임시 디렉터리 삭제

```python
>>> tmpdir = tempfile.TemporaryDirectory()
>>> tmpdir.cleanup()
```
