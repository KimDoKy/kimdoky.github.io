---
layout: post
section-type: post
title: Python Library - chap 3. 날짜와 시각 처리하기 - 3.3 datetime의 강력한 확장 모듈
category: python
tags: [ 'python' ]
---
표준 라이브러리의 datetime 모듈에 대한 강력한 확장 기능을 제공하는 dateutil에 대해 다룹니다.

- 다양한 문자열 형식의 날짜 구문 해석
- 상대적인 날짜의 차이 계산
- 유연한 반복 규칙

## dateutil 설치

```
$ pip install python-dateutil
```

## 날짜 구문 해석하기 - parser
parser 모듈은 날짜를 나타내는 다양한 형식의 문자열을 적절하게 해석합니다.

### parse() 메서드

형식 | dateutil.parser.parse(timestr.parserinfo=None, \**kwargs)
---|---
설명 | 날짜 문자열의 구문을 해석함
인수 | timestr - 날짜를 나타내는 문자열 <br> parserinfo - 날짜 해석의 동작을 변경하기 위한 객체 <br> \**kwargs - 주로 다음과 같은 인수를 지정할 수 있음 <br> default - 존재하지 않는 값의 datetime을 지정한다. <br> dayfirst - True를 지정하면 날짜가 해석 대상 문자열의 맨 앞에 있는 것으로 간주하여 해석한다. <br> yearfirst - True를 지정하면 연도가 해석 대상 문자열의 맨 앞에 있는 것으로 간주하여 해석한다.
반환값 | datetime.datetime

### 다양한 날짜 문자열의 해석

```python
>>> from dateutil.parser import parse
>>> parse('2017/10/09 17:57:50')
datetime.datetime(2017, 10, 9, 17, 57, 50)

>>> parse('2017-10-09')
datetime.datetime(2017, 10, 9, 0, 0)

>>> parse('20151009')
datetime.datetime(2015, 10, 9, 0, 0)

>>> parse('20151009175750')
datetime.datetime(2015, 10, 9, 17, 57, 50)

>>> parse('Mon, 10 Sep 2017 17:57:50 KST')
datetime.datetime(2017, 9, 10, 17, 57, 50, tzinfo=tzlocal())

>>> parse('Mon, 09 Sep 2017 17:57:50 GMT')
datetime.datetime(2017, 9, 9, 17, 57, 50, tzinfo=tzutc())
```
문자열이 지정되어 있지 않은 부분은 실행한 날짜의 0시 0분이 기본값으로 사용됩니다. default를 지정하면 해당 값을 사용할 수 있습니다.

### default를 지정한 해석

```python
>>> from datetime import datetime
>>> default = datetime(2017, 10, 09) # 일자릿수 앞에 0을 붙이면 문법 오류가 일어납니다.
  File "<stdin>", line 1
    default = datetime(2017, 10, 09)
                                  ^
SyntaxError: invalid token

>>> default = datetime(2017, 10, 9) # default 날짜 작성

>>> parse('Mon, 9 Sep 2017 17:57:50', default=default)
datetime.datetime(2017, 9, 9, 17, 57, 50)

>>> parse('Mon 17:57:50', default = default) # 시분초와 요일 지정
datetime.datetime(2017, 10, 9, 17, 57, 50)

>>> parse('17:57:50', default=default) # 시분초를 지정
datetime.datetime(2017, 10, 9, 17, 57, 50)

>>> parse('17:57', default=default) # 시, 분을 지정
datetime.datetime(2017, 10, 9, 17, 57)
```

날짜 부분이 "1/2/3"과 같이 되어 있으묜, 보통은 "월이 맨 처음"인 것으로 간주하여 해석합니다. dayfirst, yearfirst를 지정하면 맨 처음 수치를 일 또는 연도로 간주하게 할 수 있습니다. 또한 parse() 메서드는 수치를 보고(12초과되는 수는 월의 값이 아니다 등) 적절한 형식에 맞춰 해석을 시도합니다.

### dayfirst, yearfirst 를 지정한 해석

```python
>>> parse('1/2/3')  # 월/일/년 으로 해석
datetime.datetime(2003, 1, 2, 0, 0)

>>> parse('1/2/3', dayfirst=True)  # 맨 처음을 일로 해석
datetime.datetime(2003, 2, 1, 0, 0)

>>> parse('1/2/3', yearfirst=True)  # 맨 처음을 연도로 해석
datetime.datetime(2001, 2, 3, 0, 0)

>>> parse('15/2/3')  # 일/월/년으로 해석
datetime.datetime(2003, 2, 15, 0, 0)

>>> parse('15/2/3', yearfirst=True)  # 맨 처음을 연도로 해석
datetime.datetime(2015, 2, 3, 0, 0)
```

## 날짜의 차 계산하기 - relativedelta

relativedelta 모듈은 유연하게 여러 날짜의 차이를 계산합니다.

### relativedelta() 메서드

형식 | dateutil.relativedelta.relativedelta(dt1=None, dt2=None, years=0, months=0, days=0, leapdays=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0, year=None, month=None, day=None, weekday=None, yearday=None, nlyearday=None, hour=None, minute=None, second=None, microsecond=None)
---|---
설명 | 날짜 차이를 계산한다.
인수 | dt1, dt2 - 두 개의 일시를 부여하면 그 차에 해당하는 relativedelta 객체를 반환 <br> year, month, day, hour, minute, microsecond - 연월일 등을 절대값으로 지정 <br> years, months, weeks, days, hours, minutes, seconds, microseconds - 연월일 등을 상대적인 값으로 지정. 수치의 앞에 +,-를 붙임 <br> weekday -  요일을 지정 <br> leapdays - 윤년일 때 날짜에 지정된 일수를 추가함 <br> yearday, nlyearday - 그 해의 몇 번째 날인지 지정. nlyearday는 윤일을 점프한다.

### relativedelta로 다양한 날짜 계산

```python
>>> from dateutil.relativedelta import relativedelta
>>> from datetime import datetime, date
>>> now = datetime.now()  # 현재 일시를 얻음
>>> now
datetime.datetime(2017, 10, 9, 18, 23, 2, 299972)

>>> today = date.today()  # 현재 날짜를 얻음
>>> today
datetime.date(2017, 10, 9)

>>> now + relativedelta(months=+1)  # 한 달 후
datetime.datetime(2017, 11, 9, 18, 23, 2, 299972)

>>> now + relativedelta(months=-1, weeks=+1)  # 한 달 전의 일주일 뒤
datetime.datetime(2017, 9, 16, 18, 23, 2, 299972)

>>> today + relativedelta(months=+1, hour=10)  # 한 달 후 10시
datetime.datetime(2017, 11, 9, 10, 0)
```

### 요일 지정
요일 지정은 요일에 (-1), (+1)과 같이 지정할 수 있습니다.

```python
>>> from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
>>> today + relativedelta(weekday=FR)  # 다음 금요일
datetime.date(2017, 10, 13)

>>> today + relativedelta(day=31, weekday=FR(-1))  # 이 달의 마지막 금요일
datetime.date(2017, 10, 27)

>>> today + relativedelta(weekday=TU(+1))  # 다음 화요일
datetime.date(2017, 10, 10)

>>> today + relativedelta(days=+1, weekday=TU(+1))  # 오늘을 제외한 다음 화요일
datetime.date(2017, 10, 10)
```

![]({{site.url}}/img/post/python/library/3_3.png)

### yearday, nlyearday 지정

```python
>>> date(2017,1,1) + relativedelta(yearday=100)  # 2017년의 100일째
datetime.date(2017, 4, 10)

>>> date(2017,12,31) + relativedelta(yearday=100)  # 날짜와 상관없이 그 해 맨 처음부터 셈
datetime.date(2017, 4, 10)

>>> date(2012,1,1) + relativedelta(yearday=100)  # 2012년의 100일째
datetime.date(2012, 4, 9)

>>> date(2012,1,1) + relativedelta(nlyearday=100)  # 2012년의 율일을 제외한 100일째
datetime.date(2012, 4, 10)
```

### relativedelta에서 두 개의 일시가 주어진 경우의 패턴

```python
>>> relativedelta(date(2017,1,1), today)  # 올해부터의 차를 구함(2017년 10월 9일을 기준)
relativedelta(months=-9, days=-8)

>>> relativedelta(date(2018,1,1), today)  # 내년까지의 차를 구함
relativedelta(months=+2, days=+23)
```

## 반복 규칙 - rrule
rrule은 달력 애플리케이션 등에서 반복을 지정하기 위해 자주 사용합니다. 반복 규칙은 iCalendar RFC의 내용을 바탕으로 하고 있습니다.

### rrule() 메서드

형식 | dateutil.rrule.rrule(freq, dtstart=None, interval=1, wkst=None, count=None, until=None, bysetpos=None, bymonth=None, bymonthday=None, byyearday=None, byeaster=None, byweekno=None, byweekday=None, byhour=None, byminute=None, bysecond=None, cache=False)
---|---
설명 | 반복 규칙을 지정한다.
인수 | freq - 반복 빈도를 YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY 중 하나로 지정한다. <br>  cache - 캐시할지 여부를 지정한다. 같은 rrule을 계속 사용할 때에는 True를 지정한다. <br> dtstart - 시작 일시를 datetime으로 지정한다. 지정하지 않으면 datetime.now()의 값이 사용된다. <br> interval - 간격을 지정한다. 예를 들어 H OURLY에서 간격(interval)을 2로 지정하면 두 시간 간격이 된다. <br> wkst - 주의 맨 처음 요일을 MO, TU 등으로 지정한다. <br> count - 반복 횟수를 지정한다. <br> until - 종료 일시를 datetime으로 지정한다. <br> bysetpos - byXXXX로 지정한 규칙에 대하여, 몇 회째의 것을 유효한 것으로 할지를 +,-의 수치로 지정한다. 예를 들어 byweekday(=MO,TU,WE,TH,FR),bysetpos=-2 라고 지정하면 맨 뒤에서 두 번째의 평일을 지정한다는 의미가 된다. <br> bymonth, bymonthday, byyearday, byweekno, byweekday, byhour, byminute, bysecond, byeaster - 지정한 기간만을 대상으로 한다. 단일 수치 또는 튜플로 지정할 수 있다.

### rrule 샘플 코드

```python
>>> from dateutil.rrule import rrule
>>> from dateutil.rrule import DAILY, WEEKLY, MONTHLY
>>> from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU
>>> import pprint
>>> import sys
>>> sys.displayhook = pprint.pprint  # 표시를 보기 쉽게 만들고자 설정한다.
>>> start = datetime(2017, 10, 9)
>>> list(rrule(DAILY, count=5, dtstart=start))  # 지정한일로부터 5일간
[datetime.datetime(2017, 10, 9, 0, 0),
 datetime.datetime(2017, 10, 10, 0, 0),
 datetime.datetime(2017, 10, 11, 0, 0),
 datetime.datetime(2017, 10, 12, 0, 0),
 datetime.datetime(2017, 10, 13, 0, 0)]

>>> list(rrule(DAILY, dtstart=start, until=datetime(2017, 11, 1)))  # 지정 기간 매일
[datetime.datetime(2017, 10, 9, 0, 0),
 datetime.datetime(2017, 10, 10, 0, 0),
 datetime.datetime(2017, 10, 11, 0, 0),
 datetime.datetime(2017, 10, 12, 0, 0),
 datetime.datetime(2017, 10, 13, 0, 0),
 datetime.datetime(2017, 10, 14, 0, 0),
 datetime.datetime(2017, 10, 15, 0, 0),
 datetime.datetime(2017, 10, 16, 0, 0),
 datetime.datetime(2017, 10, 17, 0, 0),
 datetime.datetime(2017, 10, 18, 0, 0),
 datetime.datetime(2017, 10, 19, 0, 0),
 datetime.datetime(2017, 10, 20, 0, 0),
 datetime.datetime(2017, 10, 21, 0, 0),
 datetime.datetime(2017, 10, 22, 0, 0),
 datetime.datetime(2017, 10, 23, 0, 0),
 datetime.datetime(2017, 10, 24, 0, 0),
 datetime.datetime(2017, 10, 25, 0, 0),
 datetime.datetime(2017, 10, 26, 0, 0),
 datetime.datetime(2017, 10, 27, 0, 0),
 datetime.datetime(2017, 10, 28, 0, 0),
 datetime.datetime(2017, 10, 29, 0, 0),
 datetime.datetime(2017, 10, 30, 0, 0),
 datetime.datetime(2017, 10, 31, 0, 0),
 datetime.datetime(2017, 11, 1, 0, 0)]

>>> list(rrule(WEEKLY, count=8, wkst=SU, byweekday=(TU, TH), dtstart=start))  # 매주 화, 목
[datetime.datetime(2017, 10, 10, 0, 0),
 datetime.datetime(2017, 10, 12, 0, 0),
 datetime.datetime(2017, 10, 17, 0, 0),
 datetime.datetime(2017, 10, 19, 0, 0),
 datetime.datetime(2017, 10, 24, 0, 0),
 datetime.datetime(2017, 10, 26, 0, 0),
 datetime.datetime(2017, 10, 31, 0, 0),
 datetime.datetime(2017, 11, 2, 0, 0)]

>>> list(rrule(MONTHLY, count=3, byweekday=FR(-1), dtstart=start))  # 매월 마지막 금요일
[datetime.datetime(2017, 10, 27, 0, 0),
 datetime.datetime(2017, 11, 24, 0, 0),
 datetime.datetime(2017, 12, 29, 0, 0)]

>>> list(rrule(WEEKLY, interval=2, count=3, dtstart=start))  # 격주
[datetime.datetime(2017, 10, 9, 0, 0),
 datetime.datetime(2017, 10, 23, 0, 0),
 datetime.datetime(2017, 11, 6, 0, 0)]
```
