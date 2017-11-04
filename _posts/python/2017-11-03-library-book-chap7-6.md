---
layout: post
section-type: post
title: Python Library - chap 7. 데이터 압축과 아카이브 - 6. tar 파일 다루기
category: python
tags: [ 'python' ]
---

`tarfile` 모듈은 tar 형식으로 압축된 파일을 다룹니다. gzip, bz2, lzma 형식의 압축 파일도 다룰 수 있습니다. 이 모듈을 사용하면 tar 명령어를 사용하지 않고도 .tar.gz, .tar.bz2 등의 파일을 Python에서 직접 조작할 수 있습니다.

### open() 메서드

형식 | open(name=None, mode='r', fileobj=None, bufsize=10240, \**kwargs)
---|---
설명 | 파일 이름(name), 또는 파일 객체(fileobj)로 지정된 tar 파일은 연다. mode에서는 "r:gz"처럼 압축 형식을 지정할 수 있으나, "r"이라고 지정하면 자동으로 판별하므로 기본값이라도 상관없다. 쓸 때에는 압축 형식을 지정해야 한다.
인수 | name - tar 파일의 파일 이름을 지정한다. <br> fileobj - tar 파일의 파일 객체를 지정한다. <br> mode - tar 파일을 열 때의 모드를 지정한다. 기본값은 "읽기 모드"이다. 파일 이름으로 판별하기 때문에 압축 형식을 지정할 필요는 없다. 쓸 때에는 "w:gz"처럼 압축 형식을 지정해야 한다.
반환값 | tarfile.TarFile

### add() 메서드

형식 | add(name, arcname=None, recursive=True, exclude=None, \*, filter=None)
---|---
설명 | 지정된 파일을 tar 파일 압축에 추가한다.
인수 | name - 파일 이름, 디렉터리 이름 등을 지정한다. <br> arcname - 압축 안에서 다른 파일 이름을 사용하려면 지정한다. <br> recursive - True를 지정하면 디렉터리를 지정할 때 재귀적으로 디렉터리 안의 파일을 압축에 추가한다. <br> exclude - 파일 이름을 인수로 취하며 True/False를 반환하는 함수를 지정한다. False를 반환하는 해당 파일은 압축에 추가되지 않는다. 폐지예정의 인수이므로 filter를 사용하는 것이 좋다.<br> filter - TarInfo를 인수로 취하며 TarInfo를 반환하는 함수를 지정한다. None을 반환하는 해당 파일은 압축에 추가되지 않는다.

### TarFile 객체으 메서드

메서드 이름 | 설명 | 반환값
---|---|---
is_tarfile(filename) | 지정된 파일이 tar 파일인지 여부를 반환하는 클래스 메서드이다. | bool
getnames() | tar 파일 내에 압축된 파일 이름 리스트를 반환한다. | list
getmember(name) | 지정한 파일 이름의 TarInfo 객체를 얻는다. | tarfile.TarInfo
extractfile(member) | 지정된 파일의 파일 객체를 반환한다. member에는 파일 이름 또는 TarInfo를 지정한다. | tarfile.ExFileObject
extract(member, path="", set_attrs=True) | 압축 안의 지정된 파일을 지정된 경로에 압축 해제한다. member에는 파일 이름 또는 TarInfo를 지정한다. 해제한 파일 경로를 반환한다. | 없음
extractall(path=".", member=None) | 압축 안의 모든 파일을 지정된 경로에 압축 해제한다. | 없음
close() | TarFile을 닫는다. | 없음

### TarInfo 객체의 속성

속성 이름 | 설명 | 반환값
---|---|---
name | 파일 이름 | str
size | 파일 크기 | str
mtime | 최종 갱신 시각 | int
mode | 허가 비트 | int

작업할 디렉터리의 파일 구조이다.

```
tar_sample
├── about.txt
├── bugs.txt
├── content.txt
└── test.txt
```

### tar 파일 생성하기

```python
>>> import tarfile
>>> wtar = tarfile.open('example.tar.gz', mode='w:gz')
>>> wtar.add('test.txt', 'tarfile.txt')
>>> wtar.getnames()
['tarfile.txt']

>>> wtar.add('about.txt')
>>> wtar.add('bugs.txt')
>>> wtar.add('content.txt')
# wtar.add('tar_sample') 이런식으로 디렉터리를 지정할 수도 있다.
>>> wtar.getnames()
['tarfile.txt', 'about.txt', 'bugs.txt', 'content.txt']
>>> wtar.close()
>>> tarfile.is_tarfile('sample.tar.gz')
True
```

### 파일 형식을 검사하여 tar 파일 안을 읽어오기

```python
>>> tarfile.is_tarfile('zip_sample.zip')  # tar 파일인지 검사
False

>>> tarfile.is_tarfile('sample.bz2')
False

>>> tar = tarfile.open('sample.tar.gz')  # tar 파일을 연다
>>> len(tar.getnames())  # 파일 수 확인
6

>>> tar.getnames()[:5]  # 맨 처음 5건의 파일 이름을 구한다.
['tar_sample', 'tar_sample/.DS_Store', 'tar_sample/about.txt', 'tar_sample/bugs.txt', 'tar_sample/content.txt']

>>> f = tar.extractfile('tar_sample/content.txt')  # 파일을 연다
>>> contents = f.read()
>>> contents[:6]  # 맨 처음부터 6자까지 구한다. (압축할때 한글을 utf-8로 압축하지 않았다.)
b'\xed\x85\x8c\xec\x8a\xa4'
```

### tar 파일 압축 해제하기

```python
>>> for name in tar.getnames():  # content 파일 찾기
...     if 'content' in name:
...         tarfile_text = name
...
>>> tarfile_text
'tar_sample/content.txt'

>>> tarinfo = tar.getmember(tarfile_text)  # tarfile_text 취득
>>> tarinfo.name, tarinfo.size, tarinfo.mtime, tarinfo.mode
('tar_sample/content.txt', 36, 1509710650, 420)

>>> tar.extract(tarfile_text)  # tarfile_text 압축 해제
>>> tar.extractall()  # 전체 파일 압축 해제
>>> tar.close()
>>> import os
>>> os.listdir('tar_sample')
['.DS_Store', 'about.txt', 'bugs.txt', 'content.txt', 'test.txt']
```
