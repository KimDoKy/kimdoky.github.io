---
layout: post
section-type: post
title: 파이썬을 이용한 데이터베이스 처리
category: python
tags: [ 'python' ]
---

커넥트 재단의 '파이썬을 이용한 데이터베이스 처리'의 일부 내용입니다.

```python
import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# Counts라는 테이블이 있으면 삭제합니다.
cur.execute('DROP TABLE IF EXISTS Counts')
# Counts 테이블을 생성하고, email, count 컬럼을 정의 합니다.
cur.execute('CREATE TABLE Counts (email TEXT, count INTEGER)')

fname = input('Enter file name: ')
# 아무것도 입력하지 않으면 기본 값으로 수행합니다.
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    # 'From: ' 으로 시작하지 않는것은 건너띄고 다음 loop를 돕니다.
    # startswith는 지정된 문자열로 시작하면 True를 반환합니다.
    # pass는 다음 코드로 넘기고, continue는 다음 loop로 넘어갑니다.
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    cur.execute('SELECT count FROM Counts WHERE email = ? ', (email,))
    # fetchone은 한 번의 호출에 하나의 row를 가져옵니다.
    row = cur.fetchone()
    if row is None:
        # row가 None이면 값을 새로 입력
        cur.execute('''INSERT INTO Counts (email, count)
                VALUES (?, 1)''', (email,))
    else:
        # row가 있으면 count에 1을 더합니다.
        cur.execute('UPDATE Counts SET count = count + 1 WHERE email = ?',
                    (email,))
    conn.commit()

sqlstr = 'SELECT email, count FROM Counts  ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
```
