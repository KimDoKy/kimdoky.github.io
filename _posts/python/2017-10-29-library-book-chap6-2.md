---
layout: post
section-type: post
title: Python Library - chap 6. 파일과 디렉터리 접근하기 - 2. 직관적으로 파일 경로 조작하기
category: python
tags: [ 'python' ]
---

pathlib 모듈은 파일 경로 조작이나 파일 자체의 조작을 객체지향 스타일의 직관적인 인터페이스로 제공합니다.  

pathlib 모듈이 제공하는 클래스는 I/O를 수반하지 않는 기능으로 제공하는 "순수 경로(pure path)"와 I/O를 수반하는 기능을 제공하는 "구상 경로(concrete path)"를 나타내는 것, 이렇게 두 가지로 나눌 수 있습니다.

## 클래스 구성

### pathlib이 제공하는 클래스

클래스 이름 | 설명 | 기반 클래스
---|---|---
pathlib.PurePath | 순수 경로 클래스의 기반 클래스 | 없음
pathlib.PurePosixPath | Windows 이외 용도의 순수 경로 클래스 | PurePath
pathlib.PureWindowsPath | Windows용 순수 경로 클래스 | PurePath
pathlib.Path | 구상 경로 클래스의 기반 클래스 | PurePath
pathlib.PosixPath | Windows 이외 용도의 구상 경로 클래스 | PurePosixPath, Path
pathlib.WindowsPath | Windows용 구상 경로 클래스 | PureWindowsPath, Path

PurePath, Path는 인스턴스화하면 플랫폼에 따라 적절한 서브클래스를 반환하므로, 명시적으로 서브클래스를 이용하는 경우는 많지 않습니다.

### UNIX 계열 운영체제일 때

```python
>>> from pathlib import Path
>>> Path('.')  # 기반 클래스를 인스턴스화
PosixPath('.')  # 모듈쪽에서 플랫폼을 인식하여 PosixPath의 인스턴스를 반환하고 있다.
```

어떤 클래스를 선택해야 할지 모를 때는 Path를 사용하면 됩니다. 구상 경로 클래스인 Path는 순수 경로 클래스인 PurePath의 서브클래스이므로, 순수 경로 클래스와 구상 클래스 양쪽의 기능을 모두 사용할 수 있습니다.

## 연산자로 경로 결합하기

PurePath와 Path 및 그 서브클래스에서는 나눗셈 연산자로 경로를 결합할 수 있습니다.

### 연산자를 사용해 경로 결합하기

```python
>>> from pathlib import PurePath
>>> p = PurePath('/hoge/fuga/')
>>> p / 'piyo'
PurePosixPath('/hoge/fuga/piyo')
```

## 순수 경로 다루기 - PurePath

PurePath는 순수 경로의 기반 클래스입니다. 인스턴스화하면 Windows일 떄는 PureWindowsPath 클래스, Windows가 아닐 떄는 PurePosixPath 클래스의 인스턴스 객체가 됩니다. 순수 경로의 기능은 파일 시스템에 접근하지 않기 때문에, 운영체제 상에 존재하지 않는 파일 경로를 다룰 수도 있습니다.

### PurePath 클래스의 속성

속성 이름 | 설명 | 반환값
---|---|---
PurePath.drive | WindowsPath일 때는 드라이브 문자<br>PosixPath일 때 빈 문자를 반환한다. | str
PurePath.root | 루트를 나타내는 문자를 반환한다. | str
PurePath.anchor | 드라이브와 루트를 결합한 문자열을 반환한다. | str
PurePath.parents | 경로의 상위 경로에 접근할 수 있는 시퀀스이다. | 경로 객체를 요소로 하는 시퀀스
PurePath.parent | 경로의 바로 위 경로이다. | 경로 객체
PurePath.name | 경로 요소의 맨 끝을 나타내는 문자열을 반환한다. | str
PurePath.suffix | 경로 요소의 맨 끝에 확장자가 있으면 해당 확장자를 반환한다. | str
PurePath.suffixes | 경로 요소의 맨 끝 확장자를 리스트로 반환한다. | list
PurePath.stem | 경로 요소의 맨 끝에서 확장자를 빼고 반환한다. | str

### PurePath 클래스의 메서드

함수 이름 | 설명 | 반환값
---|---|---
PurePath.is_absolute() | 경로가 절대 경로이면 True를 반환한다. | bool
PurePath.joinpath(\*other) | 경로에 인수 other로 지정한 모든 경로를 연결한다. | 경로 객체
PurePath.match(pattern) | glob 형식의 이누 pattern과 일치하면 True를 반환한다. | bool

### PurePath 클래스를 사용한 샘플 코드

```python
>>> from pathlib import PurePath
>>> p = PurePath('/hoge/fuga/piyo.txt')
>>> p.drive
''
>>> p.root
'/'
>>> p.anchor
'/'
>>> list(p.parents)
[PurePosixPath('/hoge/fuga'), PurePosixPath('/hoge'), PurePosixPath('/')]
>>> p.parent
PurePosixPath('/hoge/fuga')
>>> p.name
'piyo.txt'
>>> p.suffix
'.txt'
>>> p.stem
'piyo'
>>> p.is_absolute()
True
>>> p.joinpath('foo','bar','baz')
PurePosixPath('/hoge/fuga/piyo.txt/foo/bar/baz')
>>> p.match('piyo.*')
True
```

## 구상 경로 다루기 - Path

Path는 구상 경로의 기반 클래스입니다. 인스턴스화하면 Windows일 때는 WindowsPath 클래스, Windows가 아닐 때는 PosixPath 클래스의 인스턴스 객체가 됩니다. 구상 경로의 기능은 파일 시스템에 접근하기 때문에, 기본적으로 운영체제 상에 조작 대상 파일 경로가 존재해야 합니다.

### Path 클래스의 메서드

함수 이름 | 설명 | 반환값
---|---|---
Path.cwd() | 현재 디렉터리를 나타내는 경로 객체를 반환한다. 클래스 메서드이다. | 경로 객체
Path.chmod(mode) | 경로의 권한(permission)을 변경한다. | None
Path.exists() | 경로가 존재하면 True를 반환한다. | bool
Path.glob(pattern) | 경로가 가리키는 디렉터리 아래의 pattern에 일치하는 파일을 경로 객체로서 반환하는 발생자(generator)를 반환한다. | 발생자
Path.is_dir() | 경로가 디렉터리면 True를 반환한다. | bool
Path.is.file() | 경로가 파일이면 True를 반환한다. | bool
Path.iterdir() | 경로 아래에 존재하는 파일이나 디렉터리를 경로 객체로서 반환하는 발생자를 반환한다. | 발생자
Path.mkdir(mode=0o777, parents=False) | 경로를 새로운 디렉터리로 생성한다. | None
Path.rename(target) | 경로의 이름을 변경한다. 인수 target에는 문자열이나 경로 객체를 지정한다. | None
Path.resolve() | 경로를 절대 경로로 하고, 심볼릭 링크를 해제한다. | 경로 객체
Path.rmdir() | 경로가 가리키는 디렉터리를 삭제한다. | None

### Path 클래스를 사용한 샘플 코드

```python
>>> from pathlib import Path
>>> p = Path.cwd() / 'newfile.txt'

>>> p.exists()
False

>>> f = p.open('w+')
>>> p.exists()
True

>>> p.resolve()
PosixPath('...(현재 디렉터리)/newfile.txt')
```
경로가 가리키는 디렉터리 안의 파일이나 디렉터리를 탐색할 때는 Path.glob()이나 Path.iterdir()이 편리합니다.

### 디렉터리 구조 예

```
├── a.py
├── b.py
├── datas
│   ├── c.txt
│   └── d.txt
└── readme.txt
```

다음은 앞의 디렉터리 구조 안에서 탐색하는 예입니다.

### 디렉터리 내부 탐색

```python
>>> from pathlib import Path
>>> p = Path('.')  # 디렉터리 안의 파일과 디렉터리를 스캔
>>> p.iterdir()
<generator object Path.iterdir at 0x102200c50>

>>> sorted(p.iterdir())
[PosixPath('a.py'), PosixPath('b.py'), PosixPath('datas'), PosixPath('readme.txt')]

>>> p.glob('**/*.txt')  # 디렉터리 아래의 확장자가 txt인 파일을 재귀적으로 스캔
<generator object Path.glob at 0x102200c50>

>>> sorted(p.glob('**/*.txt'))
[PosixPath('datas/c.txt'), PosixPath('datas/d.txt'), PosixPath('readme.txt')]
```

반환값은 스캔한 결과로 발견된 파일이나 디렉터리를 반환하는 발생자이기 때문에, `for ... in p.iterdir():` 처럼 반복문으로 처리할 수 있습니다.  

Path.glob()에 \*\*/로 시작하는 패턴을 지정하면, 이 디렉터리와 모든 서브 디렉터리를 재귀적으로 스캔합니다. 탐색할 디렉터리 아래에 방대한 수의 파일이나 디렉터리가 있을 때는 상당한 시간이 걸리게 되므로 주의하도록 합시다.

> #### 잠정 패키지(Provisional Package) 다루기  
잠정 패키지는 공식 문서에 기재되어 있으며, 해당 모듈이나 API는 별도의 비 권장 기간 없이 변경 또는 삭제될 수 있습니다.  
현재 모듈 내 API 단위에서 잠정으로 취급되는 것이 몇 가지 있습니다. 잠정 패키지를 이용하는 환경에서 Python 버젼을 업그레이드 할 때는 미리 API 변경이나 삭제 여부를 확인해야 합니다.
