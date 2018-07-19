---
layout: post
section-type: post
title: Introducing Python - chap10 - 연습문제
category: python
tags: [ 'python' ]
---

## 10.1 현재 날짜를 문자열로 작성하여 today.txt 파일에 저장하라

```Python
>>> import datetime
>>> print(datetime.datetime.today())
2018-07-19 12:46:38.275539
>>> with open('today.txt', 'wt') as today:
...     today_str = str(datetime.datetime.today())
...     today.write(today_str)

# 모범 답안
from datetime import date
>>> now = date.today()
>>> now_str = now.isoformat()
>>> with open('today.txt', 'rt') as output:
...     print(now_str, file=output)
```

## 10.2 today.txt 파일을 읽어 today_string 문자열에 저장하라.

```Python
>>> f = open('today.txt', 'rt')
>>> today_string = str(f.read())
>>> f.close()

# 모범 답안
>>> with oprn('today.txt', 'rt') as input:
...     today_string = input.read()
```

## 10.3 today_string 문자열을 날짜로 파싱하라.

```Python
>>> fmt = '%Y-%m-%d'
>>> datetime.datetime.strptime(today_string, fmt)
datetime.datetime(2018, 7, 19, 0, 0)
```

## 10.4 현재 디렉터리의 파일을 리스트로 출력하라.

```Python
>>> import os
>>> dir_list = os.listdir()
>>> dir_list
['.ipynb_checkpoints', 'today.txt', 'Untitled.ipynb']
```

## 10.5 상위(부모) 디렉터리의 파일을 리스트로 출력하라.

```Python
>>> os.chdir('../')
>>> os.listdir()
['.ipynb_checkpoints',
 '10_q',
 'dump.rdb',
 'jeepers.txt',
 'mp.py',
 'ohwell.txt',
 'poems',
 'terminate.py',
 'yikes.txt',
 '프로세스.ipynb']
```

## 10.6 multiprocessing을 사용하여 별도의 새 프로세스를 생성하라. 각 프로세스는 임의의 1~5초를 기다린 후, 현재 시간을 출력하고, 프로세스를 종료한다.

```Python
import multiprocessing
from time import sleep

def print_date():
    sleep(5)
    print(datetime.datetime.today())

for i in range(5):
    p = multiprocessing.Process(target=print_date())
    p.start()
    p.terminate()

# 모범 답안
import multiprocessing

def now(seconds):
  from datetime import datetime
  from time import sleep
  sleep(seconds)
  print('wait', seconds, 'seconds, time is', datetime.utcnow())

if __name__ == '__main__':
  import random
  for n in range(3):
    seconds = random.random()
    proc = multiprocessing.Process(target=now, args=(seconds,))
    proc.start()
```

## 10.7 본인의 태어난 날의 date 객체를 생성하라.

```Python
>>> from datetime import date
>>> born = date(1985, 11, 23)
```
## 10.8 무슨 요일에 태어났는가?

```Python
>>> born.weekday()
5
```

## 10.9 생일로부터 10,000일이 지났을 때의 날짜는?

```Python
>>> from datetime import timedelta
>>> plus_day = born + timedelta(days=10000)
>>> plus_day
datetime.date(2013, 4, 10)
```
