---
layout: post
section-type: post
title: Python Library - chap 3. 날짜와 시각 처리하기 - 3.4 전 세계 표준시간대 정보 다루기
category: python
tags: [ 'python' ]
---

## pytz 설치

```
pip install pytz
```

## 표준시간대 정보 다루기
pytz에서는 timezone() 함수를 사용하여 표준시간대 정보를 구합니다.

### timezone() 함수

형식 | pytz.timezone(zone)
---|---
설명 | 지정된 표준시간대 이름에 대응하는 표준시간대 정보를 반환한다.
인수 | zone - 표준시간대를 표시한 문자열을 지정한다.
반환값 | pytz.tzinfo

pytz.tzinfo는 표준시간대에 관련된 정보를 기억하는 객체입니다. datetime.tzinfo를 상속한 것입니다.

### tzinfo 객체의 메서드

함수 이름 | 설명 | 반환값
---|---|---
localize(datetime) | 표준시간대가 지정된 datetime을 생성한다. | datetime.datetime
utcoffset(datetime) | UTC로부터 지정된 일시의 차를 반환한다. | datetime.timedelta
dst(datetime) | 서머타임의 차를 반환한다. | datetime.timedelta
tzname(datetime, is_dst=False) | 표준시간대 이름을 반환한다. | str

### pytz로 일시를 변환하는 샘플 코드

```python
>>> import pytz
>>> from datetime import datetime
>>> fmt = '%Y-%m-%d %H:%M:%S %Z%z'
>>> seoul = pytz.timezone('Asia/Seoul')  # 서울의 표준시간대 정보를 구함
>>> eastern = pytz.timezone('US/Eastern')  # 미국 동부 시각 표준시간대 정보를 구함

>>> seoul_dt = seoul.localize(datetime(2017, 3, 1, 17, 22))
>>> seoul_dt.strftime(fmt)
'2017-03-01 17:22:00 KST+0900'
>>> eastern_dt = seoul_dt.astimezone(eastern)  # 동부 시각으로 변경
>>> eastern_dt.strftime(fmt)  # 동부시각(EST)으로 변경된 것을 확인
'2017-03-01 03:22:00 EST-0500'

>>> seoul_dt = seoul.localize(datetime(2017, 10, 9, 19, 8))
>>> eastern_dt = seoul_dt.astimezone(eastern)
>>> eastern_dt.strftime(fmt)  # 동부 시각의 서머타임으로 변경된 것을 확인
'2017-10-09 06:08:00 EDT-0400'
```

### utcoffset() 등의 샘플 코드
1월과 6월의 날짜로 utcoffset() 등을 실행하여 서머타임 여부에 따라 결과가 바뀌는 것을 확인합니다.

```python
>>> jan = datetime(2017, 1, 1)  # 1월 날짜
>>> jun = datetime(2017, 6, 1)  # 6월 날짜
>>> eastern.utcoffset(jan)
datetime.timedelta(-1, 68400)

>>> eastern.utcoffset(jun)
datetime.timedelta(-1, 72000)

>>> eastern.dst(jan)
datetime.timedelta(0)

>>> eastern.dst(jun)
datetime.timedelta(0, 3600)

>>> eastern.tzname(jun)
'EDT'

>>> eastern.tzname(jan)
'EST'
```

## 표준시간대의 리스트
pytz에는 표준시간대 이름을 반환하는 편리한 속성이 몇 가지 준비되어 있습니다.

### pytz의 속성

함수 이름 | 설명 | 반환값
---|---|---
country_timezones | ISO 3166 국가코드에 대해 표준시간대를 반환하는 dict 데이터 | dict
countty_names | ISO 3166 국가코드에 대해 영어 국가명을 반환하는 dict 데이터 | dict
all_timezones | pytz에서 사용 가능한 전체 표준시간대 이름의 리스트 | list
all_timezones_set | 전체 표준시간대 이름의 집합 | set
common_timezones | 일반적인 표준시간대 이름의 리스트. 사용하지 않는 표준시간대 이름은 포함되어 있지 않음 | list
common_timezones_set | 일반적인 표준시간대 이름의 집합 | set

### pytz의 속성을 이용한 샘플 코드

```python
>>> pytz.country_timezones['nz']  # 지정한 국가의 표준시간대를 구함
['Pacific/Auckland', 'Pacific/Chatham']
>>> pytz.country_names['nz']  # 국가명을 구함
'New Zealand'

>>> len(pytz.all_timezones)
593

>>> len(pytz.common_timezones)
439

>>> 'Singapore' in pytz.all_timezones_set
True

>>> 'Singapore' in pytz.common_timezones_set  # Singapore는 일반적인 표준시간대 이름에는 존재하지 않음
False

>>> 'Asia/Singapore' in pytz.common_timezones_set
True
```
