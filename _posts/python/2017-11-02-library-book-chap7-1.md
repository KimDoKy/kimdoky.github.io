---
layout: post
section-type: post
title: Python Library - chap 7. 데이터 압축과 아카이브 - 1. zlib 라이브러리로 데이터 압축하기
category: python
tags: [ 'python' ]
---

`zlib` 모듈은 `zlib` 라이브러리를 사용하여 데이터 압축과 해제를 실행합니다. `zlib` 라이브러리에는 `gzip` 파일 등에서 이용하는 압축 알고리즘이 제공됩니다. `gzip` 파일의 압축, 해제에는 gzip 모듈이 사용됩니다.

### zlib 모듈의 메서드

함수 이름 | 설명 | 반환값
---|---|---
compress(data[, level]) | 지정한 데이터(bytes 형식)의 압축 결과를 반환한다.<br>level에는 0~9까지 지정 가능하며, 0가 가장 압축률이 높지만 시간이 오래 걸린다. | bytes
decompress(data[, wbit[, bufsize]]) | 지정된 압축 데이터(bytes 형식)의 압축 해제 결과를 반환한다. | bytes

다음은 zlib 모듈을 사용한 데이터의 압축과 해제의 예입니다. 압축 대상 데이터가 작을 때에는 압축 후의 데이터가 더 커지는 일도 있습니다.

### zlib 모듈 샘플 코드

```python
>>> import zlib
>>> text = "한국어 텍스트"
>>> b = text.encode('utf-8')
>>> compressed_data = zlib.compress(b)
>>> len(b)
19
>>> len(compressed_data)
28

>>> long_text = b'A' * 10000  # 긴 데이터를 압축
>>> compressed_data = zlib.compress(long_text)
>>> len(long_text), len(compressed_data)
(10000, 34)

>>> decompressed_data = zlib.decompress(compressed_data)
>>> len(decompressed_data)
10000

>>> long_text == decompressed_data  # 압축 해제하여 원래대로 돌아간 것을 확인
True
```
