---
layout: post
section-type: post
title: Python Library - chap 1. 텍스트 처리하기 - 1.3 Unicode 데이터베이스에 접근하기
category: python
tags: [ 'python' ]
---
Unicode 데이터베이스에 접근하는 기능을 제공하는 unicodedata를 살펴봅니다. 이모티콘의 이름(SNOWMAN 등)을 지정하여 이모티콘(☃️)을 얻거나, 반대로 지정한 문자의 이름을 얻을 수 있습니다.

### unicodedata 모듈 함수

함수 이름 | 설명 | 반환값
---|---|---
lookup(name) | 지정된 이름에 대응하는 문자를 반환한다. 존재하지 않는 경우는 KeyError를 반환한다. | str
name(chr[,default]) | 문자 chr에 대응하는 이름을 반환한다. 이름이 정의되어 있지 않으면 ValueError를 반환한다. default가 지정되어 있으면 해당 값을 반환한다.

### unicodedata 샘플 코드

```python
>>> import unicodedata
>>> unicodedata.lookup('LATIN SMALL LETTER A')
'a'

>>> unicodedata.lookup('UNKNOWN CHARACTER')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: "undefined character name 'UNKNOWN CHARACTER'"

>>> for chr in ('A', 'A', '1', '1', 'ㄱ', '가'): # 여러 문자의 이름을 얻음
...     unicodedata.name(chr)
...
'LATIN CAPITAL LETTER A'
'LATIN CAPITAL LETTER A'
'DIGIT ONE'
'DIGIT ONE'
'HANGUL LETTER KIYEOK'
'HANGUL SYLLABLE GA'
```

## Unicode 문자열의 정규화
unicodedata 모듈의 normalize() 메서드를 사용하면 Unicode 문자열을 정규화할 수 있습니다. 문자열의 정규화는 모양이 같아 보이거나 반각과 전각이 섞인 문자열을 통일하는 등의 용도로 사용합니다.

### normalize() 메서드

형식 | normalize(form, unistr)
---|---
인수 | form - 정규화 형식을 지정한다. NFC, NFKC, NFD, NFKD를 지정할 수 있다.<br> unistr - 정규화할 대상 문자열을 지정한다.
반환값 | 정규화된 문자열을 반환한다.

다음 샘픔 코드에서 문자열을 지정한 형식으로 정규화하고 있습니다. 유니코드에서 한글은 한글 음절 11,172자 완성형과 한글 자모 240자 조합형으로 표현할 수 있으며, 정규화흫 사용하면 상호 간에 변환할 수 있습니다. 한국어는 NFC를 지정하면 전부 완성형으로, NFD를 지정하면 전부 조합형으로 정규화됩니다. 또한, 영어와 숫자는 NFKC를 지정하면 모두 반각으로 정규화됩니다.

### Unicode 문자열의 정규화 샘플 코드

```python

>>> unicodedata.normalize('NFC', '한글AÅ!！@＠﹫') # NFC로 정규화
'한글AÅ!！@＠﹫'

>>> unicodedata.normalize('NFKC', '한글AÅ!！@＠﹫') # NFKC로 정규화
'한글AÅ!!@@@'
```
