---
layout: post
section-type: post
title: Python Library - chap 7. 데이터 압축과 아카이브 - 4. lzma 압축 파일 다루기
category: python
tags: [ 'python' ]
---

`lzma` 모듈은 lzma 형식 파일(xz 파일)의 압축과 해제를 실행합니다. 이 모듈을 사용하면 lzma 명령어 등을 사용하지 않고도 lzma 파일을 Python 코드로 다룰 수 있습니다.

### lzma 모듈 함수

함수 이름 | 설명 | 반환값
---|---|---
open(filename, mode='rb', \*, format=None, check=-1, preset=None, filters=None, encoding=None, errors=None, newline=None) | lzma로 압축된 파일을 열어 파일 객체를 반환한다. | lzma.LZMAFile
compress(data) | 지정된 데이터를 lzma로 압축한다. 데이터는 bytes형이어야 한다. | bytes
decompress(data) | 지정된 lzma 데이터를 해제한다. | bytes

다음은 lzma 모듈을 사용하여 lzma 파일을 생성하고 문자열을 압축하는 모습입니다. f.write()를 실행하면 쓰인 문자열 길이가 반환되나, 압축과는 상관 없습니다.

```python
>>> import lzma
>>> with lzma.open('sample.xz', 'wt') as f:
...     f.write('한국어 텍스트를 lzma 압축 파일로 쓰기')
...
23

>>> with lzma.open('sample.xz', 'rt') as f:
...      content = f.read()
...
>>> content
'한국어 텍스트를 lzma 압축 파일로 쓰기'

>>> text = '한국어 텍스트'
>>> b = text.encode('utf-8')
>>> lzma_data = lzma.compress(b)
>>> len(b)  # 짧은 문자열은 압축해도 효과가 없다
19

>>> len(lzma_data)
76

>>> long_text = b'A' * 10000  # 긴 데이터를 압축
>>> lzma_data = lzma.compress(long_text)
>>> len(long_text), len(lzma_data)
(10000, 108)

>>> lzma_decompress_data = lzma.decompress(lzma_data)
>>> len(lzma_decompress_data)
10000
>>> long_text == lzma_decompress_data  # 압축 해제하여 원래대로 돌아간 것을 확인
True
```
