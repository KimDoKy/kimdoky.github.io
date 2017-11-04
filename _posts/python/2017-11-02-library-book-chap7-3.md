---
layout: post
section-type: post
title: Python Library - chap 7. 데이터 압축과 아카이브 - 3. bzip2 압축 파일 다루기
category: python
tags: [ 'python' ]
---

`bz2` 모듈은 bzip2 형식의 파일 압축과 해제를 실행합니다. 이 모듈을 사용하면 bzip2 명령어 등을 사용하지 않고도 bzip2 파일을 Python 코드로 다룰 수 있습니다.  

### bz2 모듈

함수 이름 | 설명 | 반환값
---|---|---
open(filename, mode='r', compresslevel=9, encoding=None, errors=None, newline=None) | bz2로 압축된 파일을 열어 파일 객체를 반환한다. compresslevel은 0~9까지 지정가능하며 9가 압축률이 가장 높지만 시간이 오래 걸린다. | bz2.BZFile
compress(data, compresslevel=9) | 지정된 데이터를 bz2로 압축한다. 데이터는 bytes형이어야 한다. | bytes
decompress(data) | 지정된 bz2 데이터를 해제한다. | bytes

다음은 bz2 모듈을 사용하여 bzip2 파일을 생성하고 문자열을 압축하는 모습입니다. f.write()를 실행하면 쓰인 문자열 길이가 반환되나, 압축과는 상관 없습니다.

### bz2 모듈 샘플 코드

```python
>>> import bz2
>>> with bz2.open('sample.bz2', 'wt') as f:
...     f.write('한국어 텍스트를 bz2 압축 파일로 쓰기')
...
22

>>> with bz2.open('sample.bz2', 'rt') as f:
...     content = f.read()
...
>>> content
'한국어 텍스트를 bz2 압축 파일로 쓰기'

>>> text = '한국어 텍스트'
>>> b = text.encode('utf-8')
>>> bz2_data = bz2.compress(b)
>>> len(b)  # 짧은 문자열은 압축해도 효과가 없다.
19

>>> len(bz2_data)
62

>>> long_text = b'A' * 10000  # 긴 데이터를 압축
>>> bz2_data = bz2.compress(long_text)
>>> len(long_text), len(bz2_data)
(10000, 47)
>>> bz2_decompress_data = bz2.decompress(bz2_data)
>>> len(bz2_decompress_data)
10000
>>> long_text == bz2_decompress_data  # 압축 해제하여 원래대로 돌아간 것을 확인
True
```
