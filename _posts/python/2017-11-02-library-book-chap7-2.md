---
layout: post
section-type: post
title: Python Library - chap 7. 데이터 압축과 아카이브 - 2. gzip 압축 파일 다루기
category: python
tags: [ 'python' ]
---
`gzip` 모듈은 `gzip` 형식 파일의 압축과 해제를 실행합니다. 이 모듈을 사용하면 gzip, gunzip 명령어 등을 사용하지 않고 Python 코드에서 gzip 파일을 다룰 수 있습니다.

### gzip 모듈 메서드

함수 이름 | 설명 | 반환값
---|---|---
open(filename, mode='rb', compresslevel=9, encoding=None, errors=None, newline=None) | gzip으로 압축된 파일을 열어 파일 객체를 반환한다. compresslevel에는 0부터 9까지 지정 가능하며, 9가 압축률이 가장 높지만 시간이 오래 걸린다. | gzip, GzipFile
compress(data, compresslevel=9) | 지정된 데이터를 gzip으로 압축한다. 데이터는 bytes형이어야 한다. | bytes
becompress(data) | 지정된 gzip 데이터를 해제한다. | bytes

다음은 gzip 모듈을 이용하여 gzip 파일을 생성하고 문자열 압축을 실행하는 모습입니다. `f.write()`를 실행하면 쓰인 문자열 길이가 반환되나, 특별히 압축과 상관은 없습니다.

### gzip 모듈 샘플 코드

```python
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import gzip
>>> with gzip.open('sample.gz', 'wt') as f:
...     f.write('한국어 텍스트를 gzip 압축 파일로 쓰기')
...
23
>>> with gzip.open('sample.gz', 'rt') as f:
...     content = f.read()
...
>>> content
'한국어 텍스트를 gzip 압축 파일로 쓰기'
>>> text = '한국어 텍스트'
>>> b = text.encode('utf-8')
>>> gzipped_data = gzip.compress(b)
>>> len(b)  # 짧은 문자열은 압축해도 효과가 없다
19
>>> len(gzipped_data)
40
>>> long_text = b'A' * 10000  # 긴 데이터를 압축
>>> gzipped_data = gzip.compress(long_text)
>>> len(long_text), len(gzipped_data)
(10000, 46)
>>> gunzipped_data = gzip.decompress(gzipped_data)
>>> len(gunzipped_data)
10000
>>> long_text == gunzipped_data  # 압축 해제하여 원래대로 돌아간 것을 확인
True
```
