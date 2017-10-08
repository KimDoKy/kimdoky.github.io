---
layout: post
section-type: post
title: Python Library - chap 3. 날짜와 시각 처리하기 - 3.1 날짜와 시간 다루기
category: python
tags: [ 'python' ]
---
datetime 모듈에는 용도별로 여러 가지 객체가 있습니다.

### datetime 모듈의 객체

객체 이름 | 용도
---|---
date | 날짜 다루기
time | 시각 다루기
datetime | 일시 다루기
timedelta | 두 일시의 차 다루기

## 날짜 다루기 - date 객체
date 객체는 날짜(연, 월, 일)을 취급합니다. 시각에는 time이나datetime 객체를 사용합니다.

### date 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
date(year, month, day) | 지정한 날짜의 date 객체를 생성하는 생성자 | datetime <br> date
today() | 오늘 날짜의 date 객체를 생성하는 생성자 | datetime <br> date
weekday() | 월요일을 0, 일요일을 6으로 하여 요일을 반환 | int
isoweekday() | 월요일을 1, 일요일을 7로 하여 요일을 반환 | int
isoformat() | ISO 8601 형식(YYYY-MM-DD)의 날짜 문자열을 반환 | str
strftime(format) | 지정한 포맷에 따라 날짜 문자열을 반환 | str
__str__() | isoformat()과 같은 결과를 반환 | str

### date 객체의 속성

속성 이름 | 설명 | 반환값
---|---|---
year | 년 값을 반환 | int
month | 월 값을 반환 | int
day | 일 값을 반환 | int

### date 샘플 코드

```python
>>> from datetime import date
>>> newyearsday =  date(2017, 1, 1)

>>> newyearsday.year, newyearsday.month, newyearsday.day # 연,월,일을 얻음
(2017, 1, 1)

>>> newyearsday.weekday() # 2017년 1월 1일은 일요일입니다.
6

>>> newyearsday.isoformat()
'2017-01-01'

>>> str(newyearsday)
'2017-01-01'

>>> newyearsday.strftime('%Y/%m/%d') # 날짜를 /로 나눈 문자열로 변환
'2017/01/01'

>>> newyearsday.strftime('%Y %b %d (%a)') # 날짜를 월, 요일이 포함된 문자열로 변환
'2017 Jan 01 (Sun)'

>>> date.today()
datetime.date(2017, 10, 8)
```

## 시각 다루기 - time 객체

time 객체는 시각을 다룹니다. 일반적인 시각뿐만아니라, 마이크로초나 표준시간대(time zone)도 포함됩니다.  

time의 생성자는 date와 달리 특정 날짜와 관련 없이 임의의 값을 지정한다는 점에 주의해야 합니다.

### time 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None) | 지정한 시각의 time 객체를 생성하는 생성자 | datetime.time
isoformat() | ISO 8601 형식(HH:MM:SS.mmmmmm), 또는 마이크로초가 0일 때는 HH:MM:SS의 문자열을 반환 | str
strftime(format) | 지정한 포맷에 따라 시각 문장열을 반환 | str
__str__() | isoformat()과 같은 결과를 반환 | str
tzname() | 표준시간대 이름의 문자열을 반환 | str

### time 객체의 속성

속성 이름 | 설명 | 반환값
---|---|---
hour | 시 값을 반환 | int
minute | 분 값을 반환 | int
second | 초 값을 반환 | int
microsecond | 마이크로초 값을 반환 | int
tzinfo | 표준시간대 정보를 반환 | 객체

### time 샘플 코드

```python
>>> from datetime import time

>>> time(17, 10, 8)
datetime.time(17, 10, 8)

>>> time(minute=10)
datetime.time(0, 10)

>>> time(second=10)
datetime.time(0, 0, 10)

>>> time(microsecond=10)
datetime.time(0, 0, 0, 10)

>>> now = time(17, 10, 8)

>>> now.hour, now.minute, now.second, now.microsecond
(17, 10, 8, 0)

>>> now.isoformat()
'17:10:08'

>>> now.strftime('%H:%M')
'17:10'

>>> str(now)
'17:10:08'
```

## 일시 다루기 - datetime 객체
datetime 객체는 날짜와 시간(일시)를 다룹니다. date와 time 객체를 합친 기능을 갖고 있습니다.  

datetime 객체는 datetime 모듈과 이름이 같기 때문에 혼동하지 않도록 주의해야 합니다.

### datetime 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None) | 지정한 일시의 datetime 객체를 생성하는 생성자. 연월일은 필수 | datetime.datetime
today() | 기본 표준시가대의 현재 일시를 반환하는 클래스 메서드. 이름이 today이지만 시각 값도 설정한다. | datetime.datetime
utcnow() | UTC(협정세계시) 현재 일시를 반환하는 클래스 메서드 | datetime.datetime
date() | 같은 연월일의 date 객체를 반환한다. | datetime.date
time() |같은 시분초의 time 객체를 반환한다. | datetime.time
isoformat() | ISO 8601 형식(YYYY-MM-DDTHH:MM:SS.mmmmmm), 또는 마이크로초가 0일 때는 YYYY-MM-DDTHH:MM:SS의 문자열을 반환한다. | str
strftime(format) | 지정한 포맷에 따라 일시 문자열을 반환한다. | str
__str__() | isoformat()과 같은 결과를 반환한다. | str
tzname() | 표준시간대 이름의 문자열을 반환한다. | str

### datetime 객체의 속성

속성 이름 | 설명 | 반환값
---|---|---
year | 년 값을 반환 | int
month | 월 값을 반환 | int
day | 일 값을 반환 | int
hour | 시 값을 반환 | int
minute | 분 값을 반환 | int
second | 초 값을 반환 | int
microsecond | 마이트로초 값을 반환 | int
tzinfo | 표준시간대 정보를 반환 | 객체

### datetime 샘플 코드

```python
>>> from datetime import datetime
>>> today = datetime.today() # 현재 일시를 얻음
>>> today.date() # date를 얻음
datetime.date(2017, 10, 8)

>>> today.time() # time을 얻음
datetime.time(18, 38, 31, 472029)

>>> today.isoformat() # ISO  8601 형식의 문자열을 얻음
'2017-10-08T18:38:31.472029'

>>> today.strftime('%Y/%m/%d') # 포맷을 지정하여 문자열을 얻음
'2017/10/08'
```

## 일시의 차 - timedelta 객체

### timedelta 객체의 메서드

메서드 이름 | 설명 | 반환값
---|---|---
timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minites=0, hours=0, weeks=0) | 지정한 수치(정수, 부동소수점 수, 음수도 지정 가능)의 일시 차를 생성하는 생성자 | datetime.timedelta

### timedelta

```python
>>> from datetime import date, datetime, time, timedelta
>>> today = date.today() # 현재 날짜를 얻음
>>> today
datetime.date(2017, 10, 8)

>>> newyearsday = date(2018, 1, 1) # 2018년 1월 1일
>>> newyearsday - today        # 오늘부터 내년 1월 1일까지의 날짜 수
datetime.timedelta(85)

>>> week = timedelta(days = 7) # 1주일간의 timedelta를 생성
>>> today + week               # 바로 1주일 뒤의 날짜를 얻음
datetime.date(2017, 10, 15)

>>> today + week * 2           # 2주 뒤의 날짜를 얻음
datetime.date(2017, 10, 22)

>>> today - week              # 1주일 전의 날짜를 얻음
datetime.date(2017, 10, 1)
```
