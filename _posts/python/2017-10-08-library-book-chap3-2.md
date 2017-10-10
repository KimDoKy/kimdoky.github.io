---
layout: post
section-type: post
title: Python Library - chap 3. 날짜와 시각 처리하기 - 3.2 시각 다루기
category: python
tags: [ 'python' ]
---
time 모듈은 시각 데이터를 다루는 기능을 제공합니다. time 모듈은 에포크(epoch)라는 기준이 되는 시간으로부터 경과 시간을 다룹니다. 에포크는 보통 1970년 1월 1일 0시 0분 0초입니다.  

Python에는 일시를 다루는 datetime 모듈이 표준으로 있습니다. datetime 모듈은 날짜나 시각을 데이터로서 취급하여 계산 등을 처리하는데 사용합니다.

## 시각 구하기

함수 이름 | 설명 | 반환값
---|---|---
gmtime([secs]) | UTC(협정세계시) 현재 시각을 반환한다. secs를 지정하면 지정된 에포크로부터 경과 시간으로 표현된 시각을 반환한다. | time.struct_time
localtime([secs]) | 지역(local)의 현재 시각을 반환한다. secs를 지정하면 지정된 에포크로부터 경과 시간으로 표현된 시각을 반환한다. | time.struct_time
strftime(format[, t]) | 지정된 시각(time.struct_time)을 지정된 포맷의 문자열 형식으로 변환하여 반환한다. | str
time() | 에포크로부터 경과 시간을 초 단위의 부동소수점 수로 반환한다. | float

### 시각 구하기

```python
>>> import time
>>> time.gmtime()
time.struct_time(tm_year=2017, tm_mon=10, tm_mday=8, tm_hour=16, tm_min=51, tm_sec=2, tm_wday=6, tm_yday=281, tm_isdst=0)

>>> time.localtime()
time.struct_time(tm_year=2017, tm_mon=10, tm_mday=9, tm_hour=1, tm_min=51, tm_sec=17, tm_wday=0, tm_yday=282, tm_isdst=0)

>>> time.strftime('%Y-%m-%d', time.localtime())
'2017-10-09'

>>> time.time()
1507481506.719926
```

## 시각 객체 - struct_time
gmtime(), localtime() 등이 반환하는 struct_time에는 time 패키지에서 다루는 일시의 값이 들어갑니다. struct_time은 이름 있는 튜플 인터페이스를 가직 객체입니다.

### struct_time의 속성

함수 이름 | 설명 | 반환값
---|---|---
tm_year | 년 값을 반환 | int
tm_mon | 월 값을 반환 | int
tm_mday | 일 값을 반환 | int
tm_hour | 시 값을 반환 | int
tm_min | 분 값을 반환 | int
tm_sec | 초 값을 반환 | int
tm_wday | 요일 값을 반환. 0이 월요일 | int
tm_yday | 연중 일수를 반환. 최댓값은 366 | int
tm_isdst | 서머타임 적용 여부. 0이면 서머타임이 아님 | int
tm_zone | 표준시간대 이름을 반환 | int
tm_gmtoff | 표준시간대의 UTC 오프셋 초를 반환 | int

### struct_time 샘플 코드

```python
>>> local = time.localtime() # 지역 시각 얻기
>>> utc = time.gmtime()   # UTC 시각 얻기
>>> local.tm_mday    # 9시간 차이 나는 것을 확인
9
>>> local.tm_hour
2
>>> local.tm_mday
9
>>> utc.tm_hour
17
```

## 스레드의 일시 정지 - sleep()
sleep() 메서드를 사용하면 현재 스레드를 지정한 시간 동안 일시 정지시킬 수 있습니다.

### sleep()

형식 | sleep(secs)
---|---
인수 | secs - 일시 정지할 초 수를 지정한다. 부동소수점 수도 지정 가능
반환값 | 없음

### sleep 샘플 코드

```python
>>> for i in range(5):
...     time.time()
...     time.sleep(0.5)
...
1507482433.221089
1507482433.723769
1507482434.226354
1507482434.731435
1507482435.236483
```

위 코드는 0.5초씩 정지하여 에포크로부터 경과한 초를 반환합니다. 0.5초씩 값이 증가하는 것을 확인 할 수 있습니다.
