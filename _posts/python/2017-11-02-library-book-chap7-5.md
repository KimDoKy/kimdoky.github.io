---
layout: post
section-type: post
title: Python Library - chap 7. 데이터 압축과 아카이브 - 5. zip 압축 파일 다루기
category: python
tags: [ 'python' ]
---

`zipfile` 모듈은 zip 형식으로 압축된 파일(ZIP 파일)을 다룹니다. 이 모듈을 사용하면 zip 명령어 등을 사용하지 않고도 zip 파일을 Python 코드로 다룰 수 있습니다.

### zipfile 모듈의 함수와 메서드

함수 이름 / 메서드 이름 | 설명 | 반환값
---|---|---
ZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True) | ZIP 파일을 읽고 쓰기 위한 객체를 생성하는 생성자이다. | zipfile.ZipFile
is_zipfile(filename) | 지정된 파일이 ZIP 파일인지 여부를 반환하는 클래스 메서드이다. | True/False
infolist() | ZipInfo(ZIP 파일 중 한 파일에 대한 정보를 정리한 객체) 리스트를 반환한다. | list
namelist() | Zip 파일 내에 압축된 파일 이름 리스트를 반환한다. | list
getinfo(name) | 지정된 파일의 ZipInfo 객체를 구한다. | zipfile.ZipInfo
open(name, mode='r', pwd=None) | ZIP 파일 안의 지정된 파일을 연다. | zipfile.ZipExtFile
extract(member, path=None, pwd=None) | 지정된 ZIP 파일 안의 파일을 지정한 경로에 압축 해제한다. member에는 파일 이름 또는 ZipInfo를 지정한다. 해제한 파일의 경로를 반환한다. | str
extractall(path=None, member=None, pwd=None) | ZIP 파일 안의 모든 파일을 지정한 경로에 압축 해제한다. | 없음
write(filename, arcname=None, compress_type=None) | 지정한 파일을 ZIP 파일로 쓴다. arcname을 지정하면 해당 이름으로 압축된다. | 없음
writestr(zinfo_or_arcname, bytes[, compress_type]) | 지정한 bytes 데이터를 ZIP 파일로 쓴다. 파일 이름은 ZipInfo 또는 파일 이름으로 지정한다. | 없음
close() | ZipFile을 닫는다. | 없음

### ZipInfo 객체의 주요 속성

속성 이름 | 설명 | 반환값
---|---|---
filename | 파일 이름 | str
date_time | 파일의 최종 갱신 일시를 튜플로 반환한다. | tuple
compress_size | 압축 후 파일 크기 | int
file_size | 압축 전 파일 크기 | int

코드 예제를 돌리기 전에 실습 디렉터리 트리입니다.

```
├── sample.bz2
├── sample.gz
├── zip.txt
├── zip2.txt
└── zip3.txt
```

### ZIP 파일 생성하기

```python
>>> import zipfile
>>> wzip = zipfile.ZipFile('zip_sample.zip', mode='w')
>>> wzip.write('zip.txt', 'zip1.txt')
>>> wzip.namelist()
['zip1.txt']

>>> wzip.writestr('zip2.txt', b'test text')
>>> wzip.namelist()
['zip1.txt', 'zip2.txt']

>>> wzip.write('zip3.txt')
>>> wzip.namelist()
['zip1.txt', 'zip2.txt', 'zip3.txt']

>>> wzip.close()
>>> zipfile.is_zipfile('zip_sample.zip')
True
```

### 파일 형식을 검사하여 ZIP 파일 안을 읽어오기

```python
>>> zipfile.is_zipfile('zip_sample.zip')  # zip 파일인지 검사
True

>>> zipfile.is_zipfile('sample.bz2')
False

>>> zip = zipfile.ZipFile('zip_sample.zip')  # zip 파일을 연다
>>> len(zip.namelist())  # 파일 수 확인
3

>>> zip.namelist()[:2]  # 맨 처음 두 건의 파일 이름을 구한다
['zip1.txt', 'zip2.txt']

>>> f = zip.open('zip2.txt')  # 파일을 연다
>>> content = f.read()
>>> content
b'test text'
>>> content[:3]
b'tes'
```

### ZIP 파일 안의 파일을 압축 해제하기

```python
>> for name in zip.namelist():  # zipfile 메뉴얼 찾기
...     if 'zip' in name:
...         zip_list = name
...
>>> zip_list
'zip3.txt'
>>> zipinfo = zip.getinfo(zip_list)  # ZipInfo 취득
>>> zipinfo.filename, zipinfo.date_time
('zip3.txt', (2017, 11, 3, 0, 23, 38))

>>> zip.extract(zipinfo)  # zipfile 메뉴얼 압축 해제
'/Users/dokyungkim/Git/DK_study/Blog_ex/python/library/chap7/zip3.txt'

>>> zip.extractall('zip_extract')  # 모든 파일의 압축 풀기. path를 지정하면 지정한 path로 압축해제 되고, 지정하지 않으면 현재 디렉터리에 압축 해제된다
>>> zip.close()
>>>
>>> import os
>>> os.listdir('zip_extract')  # 파일 압축이 풀린 것을 확인
['zip1.txt', 'zip2.txt', 'zip3.txt']
```
